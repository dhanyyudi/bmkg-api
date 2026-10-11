<script lang="ts">
	import IndonesiaMap from '../IndonesiaMap.svelte';
	import { frame, project, type LatLon } from '#lib/geo/project';
	import { formatWib, parseTime, timeAgo, type Earthquake } from '#lib/api';

	let { quakes, center }: { quakes: Earthquake[]; center?: LatLon } = $props();

	let picked = $state(0);
	$effect(() => {
		// A new result starts on its first row.
		void quakes;
		picked = 0;
	});

	const current = $derived(quakes[picked]);
	/** Marker radius in screen pixels. */
	const radius = (magnitude: number) => 4 + Math.max(0, magnitude - 2) * 1.6;
	const box = $derived(
		quakes.length === 1
			? frame([[quakes[0].lat, quakes[0].lon]], 14)
			: frame([...quakes.map((q) => [q.lat, q.lon] as LatLon), ...(center ? [center] : [])], 14)
	);
</script>

{#if quakes.length === 0}
	<p class="empty">No earthquakes matched. Among BMKG's latest records there is none in that area.</p>
{:else}
	<div class="layout">
		<div class="map">
			<IndonesiaMap {box} label="Earthquake locations">
				{#snippet children(unit)}
					{#if center}
						{@const [cx, cy] = project(center[0], center[1])}
						<path d="M{cx - 7 * unit},{cy}H{cx + 7 * unit}M{cx},{cy - 7 * unit}V{cy + 7 * unit}" class="cross" />
					{/if}
					{#each quakes as quake, i (i)}
						{@const [x, y] = project(quake.lat, quake.lon)}
						<circle
							cx={x}
							cy={y}
							r={radius(quake.magnitude) * unit}
							class="mark"
							class:on={i === picked}
							role="button"
							tabindex="0"
							aria-label="Magnitude {quake.magnitude}, {quake.region}"
							onclick={() => (picked = i)}
							onkeydown={(e) => e.key === 'Enter' && (picked = i)}
						/>
					{/each}
				{/snippet}
			</IndonesiaMap>
		</div>

		<div class="detail">
			<p class="big"><span class="mono">M {current.magnitude.toFixed(1)}</span> · {current.depth_km} km deep</p>
			<p>{current.region}</p>
			<p class="muted">
				{formatWib(parseTime(current.datetime))} · {timeAgo(parseTime(current.datetime))} ·
				{current.lat_text}, {current.lon_text}
			</p>
			{#if current.distance_km !== undefined}
				<p class="muted">{current.distance_km.toFixed(0)} km from the search point</p>
			{/if}
			{#if current.tsunami_potential}<p class="note">{current.tsunami_potential}</p>{/if}
			{#if current.felt_report}<p class="muted">Felt: {current.felt_report}</p>{/if}
			{#if current.shakemap_url}
				<a href={current.shakemap_url} target="_blank" rel="noopener">Open BMKG shakemap</a>
			{/if}
		</div>
	</div>

	{#if quakes.length > 1}
		<ol class="rows">
			{#each quakes as quake, i (i)}
				<li>
					<button type="button" class:on={i === picked} onclick={() => (picked = i)}>
						<span class="mono mag">M {quake.magnitude.toFixed(1)}</span>
						<span class="where">{quake.region}</span>
						<span class="muted">{timeAgo(parseTime(quake.datetime))}</span>
					</button>
				</li>
			{/each}
		</ol>
	{/if}
{/if}

<style>
	.layout {
		display: grid;
		grid-template-columns: minmax(0, 3fr) minmax(0, 2fr);
		gap: 16px;
		align-items: start;
	}

	.detail {
		display: grid;
		gap: 6px;
		font-size: 0.9375rem;
	}

	.big {
		font-size: 1.25rem;
		font-weight: 500;
	}

	.big .mono {
		color: var(--quake);
		font-size: 1em;
	}

	.muted {
		color: var(--muted);
		font-size: 0.8125rem;
	}

	.note {
		font-size: 0.8125rem;
		padding: 6px 10px;
		border-radius: 6px;
		background: var(--surface-2);
	}

	.mark {
		fill: var(--quake);
		fill-opacity: 0.5;
		stroke: var(--surface);
		stroke-width: 1;
		vector-effect: non-scaling-stroke;
		cursor: pointer;
	}

	.mark.on {
		fill-opacity: 1;
		stroke: var(--ink);
		stroke-width: 2;
	}

	.cross {
		stroke: var(--ink);
		stroke-width: 1.5;
		vector-effect: non-scaling-stroke;
	}

	.rows {
		list-style: none;
		margin: 14px 0 0;
		padding: 0;
		border-top: 1px solid var(--line);
		max-height: 220px;
		overflow: auto;
	}

	.rows button {
		display: grid;
		grid-template-columns: 64px minmax(0, 1fr) auto;
		gap: 10px;
		width: 100%;
		padding: 7px 8px;
		border: 0;
		border-bottom: 1px solid var(--line);
		background: none;
		text-align: left;
		font-size: 0.875rem;
	}

	.rows button:hover,
	.rows button.on {
		background: var(--surface-2);
	}

	.mag {
		color: var(--quake);
	}

	.where {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.empty {
		color: var(--muted);
	}

	@media (max-width: 720px) {
		.layout {
			grid-template-columns: minmax(0, 1fr);
		}
	}
</style>
