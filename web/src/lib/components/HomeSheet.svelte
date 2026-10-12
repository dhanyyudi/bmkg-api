<script lang="ts">
	import { onMount } from 'svelte';
	import MapSheet from './MapSheet.svelte';
	import Seismogram from './Seismogram.svelte';
	import { project, ringPath, warningRings } from '#lib/geo/project';
	import { getData, request, type ActiveWarningFull, type Earthquake, type Envelope } from '#lib/api';
	import { clockWib, formatWib, magnitude, parseTime, quakeRadius, timeAgo } from '#lib/format';
	import { fill, useMessages } from '#lib/i18n';
	import { fractionOf, REPLAY_DELAY_MS, REPLAY_MS, timelineOf } from '#lib/timeline';

	interface Props {
		/** Open an endpoint in the explorer. */
		onexplore: (endpoint: string, params?: Record<string, string>) => void;
	}

	let { onexplore }: Props = $props();
	const i18n = useMessages();

	let quakes = $state<Earthquake[]>([]);
	let warnings = $state<ActiveWarningFull[] | null>(null);
	/** Active warnings whose detail BMKG did not return. */
	let missing = $state(0);
	let selected = $state<Earthquake | null>(null);
	let pickedWarning = $state<string | null>(null);
	let loaded = $state(false);
	let failed = $state(false);
	let now = $state(new Date());

	const latest = $derived(quakes[0] ?? null);
	const shown = $derived(selected ?? latest);

	// Warning areas as drawable rings, and the warning the readout describes.
	const zones = $derived(
		(warnings ?? []).map((entry) => {
			const rings = entry.warning.areas.flatMap((area) => warningRings(area.polygon));
			// At country scale a warning area is a few pixels wide, so each one
			// also gets a point symbol at its centre.
			const points = rings.flat();
			const centre = points.length
				? project(
						points.reduce((sum, p) => sum + p[0], 0) / points.length,
						points.reduce((sum, p) => sum + p[1], 0) / points.length
					)
				: null;
			return { entry, rings, centre };
		})
	);
	const shownWarning = $derived(
		warnings?.find((entry) => entry.code === pickedWarning) ?? warnings?.[0] ?? null
	);
	const hatch = $props.id();
	const timeline = $derived(timelineOf(quakes, now.getTime()));

	const key = (q: Earthquake) => `${q.datetime}|${q.lat}|${q.lon}`;
	// A mark appears when the seismogram trace reaches its moment.
	const delay = (q: Earthquake) => Math.round(REPLAY_DELAY_MS + fractionOf(q, timeline) * REPLAY_MS);

	// Each layer of marks is one Tab stop; the arrow keys walk its marks in
	// drawing order, so a keyboard does not have to Tab through every mark.
	function walk(event: KeyboardEvent, select: () => void) {
		const mark = event.currentTarget as SVGGElement;
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			select();
			return;
		}
		const step =
			event.key === 'ArrowRight' || event.key === 'ArrowDown'
				? 1
				: event.key === 'ArrowLeft' || event.key === 'ArrowUp'
					? -1
					: 0;
		if (!step) return;
		event.preventDefault();
		const marks = [...(mark.parentElement?.children ?? [])].filter(
			(el): el is SVGGElement => el instanceof SVGGElement && el.classList.contains('stop')
		);
		const next = marks[(marks.indexOf(mark) + step + marks.length) % marks.length];
		// Focusing a mark selects it (see onfocus), which moves the Tab stop along.
		next?.focus();
	}

	const REQUESTS = [
		['earthquake-latest', '/v1/earthquake/latest'],
		['earthquake-felt', '/v1/earthquake/felt'],
		['earthquake-recent', '/v1/earthquake/recent'],
		['nowcast-warnings', '/v1/nowcast/warnings']
	] as const;

	async function loadWarnings(): Promise<void> {
		const lang = i18n.m.apiLang === 'en' ? '?lang=en' : '';
		try {
			const result = await request(`/v1/nowcast/warnings${lang}`);
			if (!result.ok) return;
			const body = result.body as Envelope<ActiveWarningFull[]>;
			warnings = body.data;
			missing = Array.isArray(body.meta.missing) ? body.meta.missing.length : 0;
			if (!warnings.some((entry) => entry.code === pickedWarning)) pickedWarning = null;
		} catch {
			// Keep what is on screen; the next refresh tries again.
		}
	}

	async function load() {
		const [latestQuake, recent, felt] = await Promise.all([
			getData<Earthquake>('/v1/earthquake/latest'),
			getData<Earthquake[]>('/v1/earthquake/recent'),
			getData<Earthquake[]>('/v1/earthquake/felt'),
			loadWarnings()
		]);

		const seen = new Map<string, Earthquake>();
		for (const quake of [latestQuake, ...(felt ?? []), ...(recent ?? [])]) {
			if (quake && !seen.has(key(quake))) seen.set(key(quake), quake);
		}
		const merged = [...seen.values()].sort(
			(a, b) => parseTime(b.datetime).getTime() - parseTime(a.datetime).getTime()
		);

		failed = merged.length === 0 && warnings === null;
		now = new Date();
		if (merged.length) quakes = merged;
		if (selected && !seen.has(key(selected))) selected = null;
		loaded = true;
	}

	onMount(() => {
		load();
		// The API caches the newest earthquake for a minute; ask no more often.
		const refresh = setInterval(() => {
			if (!document.hidden) load();
		}, 60_000);
		return () => clearInterval(refresh);
	});
</script>

<figure class="plate">
	<figcaption class="head">
		<strong>{i18n.m.map.plateTitle}</strong>
		<span class="mono" class:alert={failed} aria-live="polite">
			{failed
				? i18n.m.map.unreachable
				: loaded
					? fill(i18n.m.map.updated, { time: clockWib(now, i18n.m) })
					: i18n.m.map.loading}
		</span>
	</figcaption>

	<MapSheet label={i18n.m.map.plateLabel}>
		{#snippet children(unit)}
			<defs>
				<pattern id={hatch} patternUnits="userSpaceOnUse" width={5 * unit} height={5 * unit} patternTransform="rotate(45)">
					<line x1="0" y1="0" x2="0" y2={5 * unit} class="hatch-line" stroke-width={2.2 * unit} />
				</pattern>
			</defs>
			<g role="group" aria-label={i18n.m.map.warningLayer}>
				{#each zones as zone (zone.entry.code)}
					<g
						class="zone stop"
						class:shown={zone.entry === shownWarning}
						role="button"
						tabindex={zone.entry === shownWarning ? 0 : -1}
						aria-label={fill(i18n.m.map.warningLabel, { event: zone.entry.warning.event, province: zone.entry.province })}
						onclick={() => (pickedWarning = zone.entry.code)}
						onfocus={() => (pickedWarning = zone.entry.code)}
						onkeydown={(e) => walk(e, () => (pickedWarning = zone.entry.code))}
						onmouseenter={() => (pickedWarning = zone.entry.code)}
					>
						{#each zone.rings as ring, i (i)}
							<path d={ringPath(ring)} fill="url(#{hatch})" class="area" />
						{/each}
						{#if zone.centre}
							{@const [x, y] = zone.centre}
							<path
								d="M{x},{y - 8 * unit}L{x + 7.5 * unit},{y + 5 * unit}H{x - 7.5 * unit}Z"
								class="sign"
							/>
							<circle cx={x} cy={y} r={14 * unit} class="hit" />
						{/if}
					</g>
				{/each}
			</g>
			<g role="group" aria-label={i18n.m.map.quakeLayer}>
				{#each [...quakes].reverse() as quake (key(quake))}
					{@const [x, y] = project(quake.lat, quake.lon)}
					{@const r = quakeRadius(quake.magnitude) * unit}
					{@const isLatest = quake === latest}
					<g
						class="quake stop"
						class:latest={isLatest}
						class:shown={quake === shown}
						role="button"
						tabindex={quake === shown ? 0 : -1}
						aria-label={fill(i18n.m.map.quakeLabel, { m: magnitude(quake.magnitude, i18n.m), region: quake.region })}
						style:--delay="{delay(quake)}ms"
						onclick={() => (selected = quake)}
						onfocus={() => (selected = quake)}
						onkeydown={(e) => walk(e, () => (selected = quake))}
						onmouseenter={() => (selected = quake)}
					>
						{#if isLatest}
							<circle cx={x} cy={y} {r} class="ripple" />
							<path
								d="M{x - r - 7 * unit},{y}H{x - r - 2 * unit}M{x + r + 2 * unit},{y}H{x + r + 7 * unit}M{x},{y - r - 7 * unit}V{y - r - 2 * unit}M{x},{y + r + 2 * unit}V{y + r + 7 * unit}"
								class="cross"
							/>
						{/if}
						<circle cx={x} cy={y} {r} class="mark" />
						<circle cx={x} cy={y} r={Math.max(r, 12 * unit)} class="hit" />
					</g>
				{/each}
			</g>
		{/snippet}
	</MapSheet>

	<Seismogram {quakes} {timeline} />
</figure>

<div class="margin">
	<section>
		<h2>{i18n.m.map.legend}</h2>
		<ul class="legend">
			<li>
				<svg viewBox="0 0 64 26" width="64" height="26" aria-hidden="true">
					<circle cx="6" cy="13" r={quakeRadius(3)} class="lg-mark" />
					<circle cx="24" cy="13" r={quakeRadius(5)} class="lg-mark" />
					<circle cx="50" cy="13" r={quakeRadius(7)} class="lg-mark" />
				</svg>
				<span>{i18n.m.map.legendQuake} <span class="mono">(M 3, 5, 7)</span></span>
			</li>
			<li>
				<svg viewBox="0 0 64 26" width="64" height="26" aria-hidden="true">
					<path d="M12,13H18M30,13H36M24,1V7M24,19V25" class="lg-cross" />
					<circle cx="24" cy="13" r="5" class="lg-latest" />
				</svg>
				<span>{i18n.m.map.legendLatest}</span>
			</li>
			<li>
				<svg viewBox="0 0 64 26" width="64" height="26" aria-hidden="true">
					<defs>
						<pattern id="{hatch}-legend" patternUnits="userSpaceOnUse" width="5" height="5" patternTransform="rotate(45)">
							<line x1="0" y1="0" x2="0" y2="5" class="hatch-line" stroke-width="2.2" />
						</pattern>
					</defs>
					<rect x="2" y="4" width="26" height="18" fill="url(#{hatch}-legend)" class="lg-zone" />
					<path d="M48,5L56,19H40Z" class="lg-sign" />
				</svg>
				<span>{i18n.m.map.legendWarning}</span>
			</li>
			<li>
				<svg viewBox="0 0 64 26" width="64" height="26" aria-hidden="true">
					<path d="M0,13H18L21,3L25,23L29,7L33,18L36,11L39,14H64" class="lg-trace" />
				</svg>
				<span>{i18n.m.map.legendTrace}</span>
			</li>
		</ul>
		<p class="fine">{i18n.m.map.scaleNote}</p>
	</section>

	<section aria-live="polite">
		<h2>{shown && shown !== latest ? i18n.m.map.selected : i18n.m.map.latest}</h2>
		{#if shown}
			<p class="reading">
				<span class="mono mag">M {magnitude(shown.magnitude, i18n.m)}</span>
				<span class="depth mono">{fill(i18n.m.map.depth, { km: shown.depth_km })}</span>
			</p>
			<p>{shown.region}</p>
			<p class="fine">
				{formatWib(parseTime(shown.datetime), i18n.m)}, {timeAgo(parseTime(shown.datetime), i18n.m, now)}
			</p>
			{#if shown.felt_report}
				<p class="fine">{fill(i18n.m.map.felt, { text: shown.felt_report })}</p>
			{/if}
		{:else if loaded}
			<p>{i18n.m.map.noQuakes}</p>
		{:else}
			<p class="fine">{i18n.m.map.loading}</p>
		{/if}
	</section>

	<section aria-live="polite">
		<h2>{i18n.m.map.warnings}</h2>
		{#if warnings === null}
			<p class="fine">{loaded ? i18n.m.map.warningsUnavailable : i18n.m.map.loading}</p>
		{:else if !shownWarning}
			<p>{i18n.m.map.noWarnings}</p>
		{:else}
			<p class="reading">
				<span class="mono warn">{fill(i18n.m.map.warningsCount, { n: warnings.length })}</span>
			</p>
			<p><strong>{shownWarning.province}</strong>: {shownWarning.warning.event}</p>
			<p class="fine">
				{fill(i18n.m.map.validUntil, { time: formatWib(parseTime(shownWarning.warning.expires), i18n.m) })}
			</p>
			<p>
				<button type="button" class="link" onclick={() => onexplore('nowcast-detail', { alertCode: shownWarning.code })}>
					{i18n.m.map.openWarning}
				</button>
			</p>
			{#if warnings.length > 1}
				<p class="fine others">
					{i18n.m.map.otherWarnings}
					{#each warnings.filter((entry) => entry !== shownWarning) as entry (entry.code)}
						<button type="button" class="link" onclick={() => (pickedWarning = entry.code)}>{entry.province}</button>
					{/each}
				</p>
			{/if}
			{#if missing > 0}
				<p class="fine">{fill(i18n.m.map.warningsMissing, { n: missing })}</p>
			{/if}
		{/if}
	</section>
</div>

<p class="requests">
	{i18n.m.map.drawnFrom}
	{#each REQUESTS as [endpoint, path] (endpoint)}
		<button type="button" class="mono" onclick={() => onexplore(endpoint)}>GET {path}</button>
	{/each}
</p>

<style>
	.plate {
		margin: 0;
		border: 1px solid var(--ink);
	}

	.head {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
		gap: 8px 16px;
		flex-wrap: wrap;
		padding: 8px 10px;
		border-bottom: 1px solid var(--ink);
		font-size: 0.9375rem;
	}

	.head .mono {
		font-size: 0.75rem;
		color: var(--ink-2);
	}

	.head .alert {
		color: var(--alert);
	}

	.plate :global(.frame) {
		padding: 6px 8px 8px 0;
	}

	.quake,
	.zone {
		cursor: pointer;
		outline: none;
	}

	/* Warning areas share the alert red with epicentres, as areas instead of
	   points: hatching leaves the coastline readable underneath. */
	.zone .area {
		stroke: var(--alert);
		stroke-width: 1;
		vector-effect: non-scaling-stroke;
		animation: appear-flat 0.5s ease-out both;
	}

	/* The warning sign: a triangle, as on a road sign. */
	.sign {
		fill: var(--paper);
		stroke: var(--alert);
		stroke-width: 2;
		stroke-linejoin: round;
		vector-effect: non-scaling-stroke;
		animation: appear-flat 0.5s ease-out both;
	}

	.zone.shown .sign,
	.zone:focus-visible .sign {
		fill: var(--alert);
		stroke: var(--ink);
	}

	:global(.hatch-line) {
		stroke: var(--alert);
	}

	.lg-zone {
		stroke: var(--alert);
	}

	.lg-sign {
		fill: var(--paper);
		stroke: var(--alert);
		stroke-width: 2;
		stroke-linejoin: round;
	}

	/* Red is reserved for what matters: here, epicentres. */
	.mark {
		fill: var(--alert);
		fill-opacity: 0.4;
		stroke: var(--alert);
		stroke-width: 1;
		vector-effect: non-scaling-stroke;
		/* Marks appear in the order the earthquakes happened. */
		transform-box: fill-box;
		transform-origin: center;
		animation: appear 0.4s ease-out var(--delay, 0ms) both;
	}

	@keyframes appear {
		from {
			transform: scale(0);
			opacity: 0;
		}
	}

	.quake.latest .mark {
		fill-opacity: 1;
	}

	.quake.shown .mark,
	.quake:focus-visible .mark {
		fill-opacity: 1;
		stroke: var(--ink);
		stroke-width: 2;
	}

	.cross {
		stroke: var(--ink);
		stroke-width: 1.25;
		vector-effect: non-scaling-stroke;
		animation: appear-flat 0.3s ease-out var(--delay, 0ms) both;
	}

	@keyframes appear-flat {
		from {
			opacity: 0;
		}
	}

	/* One outward ring when the newest earthquake lands, then stillness. */
	.ripple {
		fill: none;
		stroke: var(--alert);
		stroke-width: 1.5;
		vector-effect: non-scaling-stroke;
		transform-box: fill-box;
		transform-origin: center;
		opacity: 0;
		animation: ripple 1.4s ease-out var(--delay, 0ms) 2;
	}

	@keyframes ripple {
		from {
			transform: scale(1);
			opacity: 0.9;
		}
		to {
			transform: scale(4.5);
			opacity: 0;
		}
	}

	.hit {
		fill: transparent;
	}

	/* Keyboard focus gets its own ring, so it reads apart from the selection. */
	.stop:focus-visible .hit {
		stroke: var(--ink);
		stroke-width: 2;
		stroke-dasharray: 3 2;
		vector-effect: non-scaling-stroke;
	}

	.margin {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 20px 32px;
		margin-top: 18px;
	}

	.margin section {
		display: grid;
		gap: 6px;
		align-content: start;
		min-width: 0;
	}

	.margin h2 {
		font-size: 0.9375rem;
		padding-bottom: 5px;
		border-bottom: 1px solid var(--ink);
	}

	.legend {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		gap: 4px;
		font-size: 0.875rem;
	}

	.legend li {
		display: grid;
		grid-template-columns: 64px minmax(0, 1fr);
		gap: 10px;
		align-items: center;
	}

	.lg-mark {
		fill: var(--alert);
		fill-opacity: 0.4;
		stroke: var(--alert);
	}

	.lg-latest {
		fill: var(--alert);
		stroke: var(--alert);
	}

	.lg-cross {
		stroke: var(--ink);
		stroke-width: 1.25;
	}

	.lg-trace {
		fill: none;
		stroke: var(--relief);
		stroke-width: 1.25;
		stroke-linejoin: round;
	}

	.reading {
		display: flex;
		align-items: baseline;
		gap: 12px;
		flex-wrap: wrap;
		line-height: 1.15;
	}

	.mag {
		font-size: 1.75rem;
		font-weight: 500;
		color: var(--alert);
	}

	.warn {
		font-size: 1.25rem;
		font-weight: 500;
		color: var(--alert);
	}

	/* Brown marks relief, and depth is how far below the surface. */
	.depth {
		color: var(--relief);
	}

	.fine {
		font-size: 0.8125rem;
		color: var(--ink-2);
	}

	.others {
		display: flex;
		flex-wrap: wrap;
		gap: 0 12px;
		align-items: baseline;
	}

	.link,
	.requests button {
		padding: 6px 0;
		border: 0;
		background: none;
		color: var(--water-ink);
		text-decoration: underline;
		text-decoration-thickness: 1px;
		text-underline-offset: 3px;
	}

	.link:hover,
	.requests button:hover {
		text-decoration-thickness: 2px;
	}

	.requests {
		margin-top: 18px;
		padding-top: 10px;
		border-top: 1px solid var(--hair);
		font-size: 0.875rem;
		color: var(--ink-2);
		display: flex;
		flex-wrap: wrap;
		gap: 0 16px;
		align-items: baseline;
	}

	@media (max-width: 760px) {
		.margin {
			grid-template-columns: minmax(0, 1fr);
		}

		.link,
		.requests button {
			min-width: 44px;
			min-height: 44px;
		}
	}
</style>
