<script lang="ts">
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import IndonesiaMap from './IndonesiaMap.svelte';
	import { project } from '#lib/geo/project';
	import {
		formatWib,
		getData,
		parseTime,
		timeAgo,
		type ActiveWarning,
		type Earthquake
	} from '#lib/api';

	interface Props {
		/** Open an endpoint in the explorer. */
		onexplore?: (endpoint: string, params?: Record<string, string>) => void;
		/** The loaded earthquakes, newest first, for other parts of the page. */
		quakes?: Earthquake[];
	}

	let { onexplore, quakes = $bindable([]) }: Props = $props();

	let warnings = $state<ActiveWarning[] | null>(null);
	let selected = $state<Earthquake | null>(null);
	let loaded = $state(false);
	let failed = $state(false);
	let now = $state(new Date());

	const latest = $derived(quakes[0] ?? null);
	const shown = $derived(selected ?? latest);

	// The latest magnitude counts up when it first arrives.
	const magnitude = new Tween(0, { duration: 900, easing: cubicOut });
	$effect(() => {
		if (!latest) return;
		const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
		magnitude.set(latest.magnitude, still ? { duration: 0 } : undefined);
	});

	const key = (q: Earthquake) => `${q.datetime}|${q.lat}|${q.lon}`;
	/** Marker radius in screen pixels. */
	const radius = (magnitude: number) => 3 + Math.max(0, magnitude - 2) * 1.5;

	async function load() {
		const [latestQuake, recent, felt, active] = await Promise.all([
			getData<Earthquake>('/v1/earthquake/latest'),
			getData<Earthquake[]>('/v1/earthquake/recent'),
			getData<Earthquake[]>('/v1/earthquake/felt'),
			getData<ActiveWarning[]>('/v1/nowcast')
		]);

		const seen = new Map<string, Earthquake>();
		for (const quake of [latestQuake, ...(felt ?? []), ...(recent ?? [])]) {
			if (quake && !seen.has(key(quake))) seen.set(key(quake), quake);
		}
		const merged = [...seen.values()].sort(
			(a, b) => parseTime(b.datetime).getTime() - parseTime(a.datetime).getTime()
		);

		failed = merged.length === 0 && active === null;
		if (merged.length) quakes = merged;
		if (active !== null) warnings = active;
		if (selected && !seen.has(key(selected))) selected = null;
		loaded = true;
		now = new Date();
	}

	onMount(() => {
		load();
		// The API caches the newest earthquake for a minute; ask no more often.
		const refresh = setInterval(() => {
			if (!document.hidden) load();
		}, 60_000);
		const clock = setInterval(() => (now = new Date()), 15_000);
		return () => {
			clearInterval(refresh);
			clearInterval(clock);
		};
	});
</script>

<section class="board card" aria-label="Live data from the API">
	<header>
		<span class="live" class:off={failed}>
			<span class="dot"></span>
			{failed ? 'API unreachable' : loaded ? 'Live from the API' : 'Loading live data'}
		</span>
		<span class="eyebrow">Indonesia right now</span>
	</header>

	<IndonesiaMap label="Map of recent earthquakes in Indonesia">
		{#snippet children(unit)}
			{#each [...quakes].reverse() as quake, i (key(quake))}
				{@const [x, y] = project(quake.lat, quake.lon)}
				{@const isLatest = quake === latest}
				{@const isShown = quake === shown}
				<g
					class="quake"
					class:latest={isLatest}
					class:shown={isShown}
					role="button"
					tabindex="0"
					aria-label="Magnitude {quake.magnitude}, {quake.region}"
					style:--delay="{400 + i * 70}ms"
					onclick={() => (selected = quake)}
					onkeydown={(e) => (e.key === 'Enter' || e.key === ' ') && (selected = quake)}
					onmouseenter={() => (selected = quake)}
				>
					{#if isLatest}
						<circle cx={x} cy={y} r={radius(quake.magnitude) * unit} class="pulse" />
					{/if}
					<circle cx={x} cy={y} r={radius(quake.magnitude) * unit} class="mark" />
					<circle cx={x} cy={y} r={14 * unit} class="hit" />
				</g>
			{/each}
		{/snippet}
	</IndonesiaMap>

	<div class="readout">
		<div class="quake-info">
			<p class="eyebrow">{shown === latest ? 'Latest earthquake' : 'Selected earthquake'}</p>
			{#if shown}
				<p class="magnitude">
					<span class="mono">M {(shown === latest ? magnitude.current : shown.magnitude).toFixed(1)}</span>
					<span class="depth">{shown.depth_km} km deep</span>
				</p>
				<p class="region">{shown.region}</p>
				<p class="when">
					{formatWib(parseTime(shown.datetime))} · {timeAgo(parseTime(shown.datetime), now)}
				</p>
				{#if shown.felt_report}
					<p class="felt">Felt: {shown.felt_report}</p>
				{/if}
			{:else if loaded}
				<p class="region">No earthquake data available right now.</p>
			{:else}
				<p class="skeleton" style:width="60%"></p>
				<p class="skeleton" style:width="85%"></p>
			{/if}
		</div>

		<div class="warnings">
			<p class="eyebrow">Active weather warnings</p>
			{#if warnings === null}
				{#if loaded}
					<p class="region">Warnings are unavailable right now.</p>
				{:else}
					<p class="skeleton" style:width="40%"></p>
				{/if}
			{:else if warnings.length === 0}
				<p class="count mono">0</p>
				<p class="region">No province has an active warning.</p>
			{:else}
				<p class="count">
					<span class="mono">{warnings.length}</span>
					<span class="depth">{warnings.length === 1 ? 'province' : 'provinces'}</span>
				</p>
				<ul>
					{#each warnings as warning (warning.code)}
						<li>
							<button
								type="button"
								title="Open this warning in the explorer"
								onclick={() => onexplore?.('nowcast-detail', { alertCode: warning.code })}
							>
								{warning.province}
							</button>
						</li>
					{/each}
				</ul>
			{/if}
		</div>
	</div>
</section>

<style>
	.board {
		padding: 14px;
		box-shadow: var(--shadow);
		display: grid;
		gap: 14px;
		min-width: 0;
	}

	header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 12px;
	}

	.live {
		display: inline-flex;
		align-items: center;
		gap: 8px;
		font-size: 0.8125rem;
		font-weight: 500;
		color: var(--ok);
	}

	.live.off {
		color: var(--quake);
	}

	.dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: currentColor;
		animation: blink 2s ease-in-out infinite;
	}

	@keyframes blink {
		50% {
			opacity: 0.35;
		}
	}

	.quake {
		cursor: pointer;
		outline: none;
	}

	.mark {
		fill: var(--quake);
		fill-opacity: 0.55;
		stroke: var(--surface);
		stroke-width: 1;
		vector-effect: non-scaling-stroke;
		transition: fill-opacity 0.15s;
		/* Marks appear oldest first, so the map fills in as time passes. */
		transform-box: fill-box;
		transform-origin: center;
		animation: pop 0.55s cubic-bezier(0.2, 1.5, 0.4, 1) var(--delay, 0ms) both;
	}

	@keyframes pop {
		from {
			transform: scale(0);
			opacity: 0;
		}
	}

	.quake.latest .mark,
	.quake.shown .mark {
		fill-opacity: 1;
	}

	.quake.shown .mark,
	.quake:focus-visible .mark {
		stroke: var(--ink);
		stroke-width: 2;
	}

	.hit {
		fill: transparent;
	}

	.pulse {
		fill: none;
		stroke: var(--quake);
		stroke-width: 2;
		vector-effect: non-scaling-stroke;
		transform-box: fill-box;
		transform-origin: center;
		opacity: 0;
		animation: pulse 2.2s ease-out var(--delay, 0ms) infinite;
	}

	@keyframes pulse {
		from {
			transform: scale(1);
			opacity: 0.9;
		}
		to {
			transform: scale(4.5);
			opacity: 0;
		}
	}

	.readout {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 16px;
		padding: 2px 4px 4px;
	}

	.readout > div {
		display: grid;
		gap: 4px;
		align-content: start;
		min-width: 0;
	}

	.magnitude,
	.count {
		display: flex;
		align-items: baseline;
		gap: 10px;
		font-size: 1.75rem;
		font-weight: 500;
		line-height: 1.1;
	}

	.magnitude .mono {
		color: var(--quake);
		font-size: 1em;
	}

	.count .mono,
	.count.mono {
		color: var(--warn);
		font-size: 1em;
	}

	.depth {
		font-size: 0.875rem;
		font-weight: 400;
		color: var(--muted);
	}

	.region {
		font-size: 0.9375rem;
	}

	.when,
	.felt {
		font-size: 0.8125rem;
		color: var(--muted);
	}

	ul {
		list-style: none;
		margin: 4px 0 0;
		padding: 0;
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
		max-height: 92px;
		overflow: auto;
	}

	li button {
		font-size: 0.8125rem;
		padding: 3px 9px;
		border-radius: 999px;
		border: 1px solid transparent;
		background: var(--warn-soft);
		color: var(--warn);
	}

	li button:hover {
		border-color: var(--warn);
	}

	.skeleton {
		height: 14px;
		border-radius: 4px;
		background: var(--surface-2);
		animation: blink 1.4s ease-in-out infinite;
	}

	@media (max-width: 520px) {
		.readout {
			grid-template-columns: 1fr;
		}
	}
</style>
