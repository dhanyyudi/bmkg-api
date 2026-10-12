<script lang="ts">
	import type { Snippet } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { INDONESIA_PATH, MAP, NEIGHBOURS_PATH } from '#lib/geo/indonesia';
	import { project, type Box } from '#lib/geo/project';
	import { useMessages } from '#lib/i18n';

	interface Props {
		/** Area to show; the whole archipelago by default. */
		box?: Box;
		label: string;
		/** Marks drawn on the map. Receives map units per screen pixel, so marks can be sized in pixels. */
		children?: Snippet<[number]>;
	}

	const FULL: Box = { x: 0, y: 0, width: MAP.width, height: MAP.height };
	let { box = FULL, label, children }: Props = $props();

	const i18n = useMessages();
	const clip = $props.id();

	const view = new Tween(FULL, { duration: 600, easing: cubicOut });
	$effect(() => {
		const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
		view.set(box, still ? { duration: 0 } : undefined);
	});

	// The sheet margin holds the coordinate labels, as on a printed map.
	let width = $state(0);
	// Wide enough for the longest latitude label ("10° LS").
	const marginLeft = 48;
	const marginTop = 20;
	const marginRight = 1;
	const marginBottom = 1;

	// Map units per CSS pixel
	const unit = $derived(view.current.width / Math.max((width || 760) - marginLeft - marginRight, 120));
	const outer = $derived({
		x: view.current.x - marginLeft * unit,
		y: view.current.y - marginTop * unit,
		width: view.current.width + (marginLeft + marginRight) * unit,
		height: view.current.height + (marginTop + marginBottom) * unit
	});

	// Graticule: fewer, rounder lines the more of the country is shown.
	const span = $derived(view.current.width / MAP.k);
	const step = $derived(span > 30 ? 5 : span > 12 ? 2 : span > 5 ? 1 : 0.5);
	const west = $derived(MAP.lon0 + view.current.x / MAP.k);
	const northEdge = $derived(MAP.lat0 - view.current.y / MAP.k);

	function ticks(from: number, to: number, size: number): number[] {
		const out: number[] = [];
		for (let v = Math.ceil(from / size) * size; v <= to + 1e-9; v += size) out.push(Math.round(v * 10) / 10);
		return out;
	}

	const meridians = $derived(ticks(west, west + span, step));
	const parallels = $derived(ticks(northEdge - view.current.height / MAP.k, northEdge, step));

	const degrees = (value: number) =>
		Math.abs(value).toLocaleString(i18n.m.numberLocale, { maximumFractionDigits: 1 });
	const lonLabel = (lon: number) => `${degrees(lon)}° ${i18n.m.map.east}`;
	const latLabel = (lat: number) =>
		lat === 0 ? '0°' : `${degrees(lat)}° ${lat > 0 ? i18n.m.map.north : i18n.m.map.south}`;

	// Names follow the cartographic convention: water in blue serif italic,
	// land upright. Positions are [lat, lon].
	const SEAS: [keyof typeof i18n.m.map.seas, number, number][] = [
		['indian', -9.7, 103.6],
		['java', -5.3, 111.6],
		['banda', -5.9, 127.4],
		['flores', -7.55, 120.6],
		['celebes', 3.4, 122.2],
		['arafura', -9.4, 135.2],
		['natuna', 4.4, 107.4],
		['pacific', 4.6, 137.2]
	];
	const ISLANDS: [keyof typeof i18n.m.map.islands, number, number][] = [
		['sumatra', 0.2, 101.7],
		['kalimantan', 0.1, 114.2],
		['sulawesi', -2.2, 120.6],
		['java', -7.35, 110.3],
		['papua', -4.4, 138.2]
	];
	// Neighbouring countries are named in grey, so a land border reads as a
	// border and not as the edge of the data.
	const NEIGHBOURS: [keyof typeof i18n.m.map.neighbours, number, number][] = [
		['png', -6.4, 143.4],
		['malaysia', 2.7, 113.4],
		['malaysia', 4.3, 102.2],
		['timor', -8.85, 125.9],
		['philippines', 6.8, 125.0]
	];
	// Screen pixels per degree decide which names fit.
	const pxPerDegree = $derived(MAP.k / unit);
	// Every line gets a tick; a label only where it has room to be read.
	const lonEvery = $derived(Math.max(1, Math.ceil(52 / (step * pxPerDegree))));
	const latEvery = $derived(Math.max(1, Math.ceil(16 / (step * pxPerDegree))));
	const labelled = (value: number, every: number) => Math.round(value / step) % every === 0;

	const inView = (lat: number, lon: number) => {
		const [x, y] = project(lat, lon);
		const v = view.current;
		return x > v.x + 30 * unit && x < v.x + v.width - 30 * unit && y > v.y + 10 * unit && y < v.y + v.height - 10 * unit;
	};

	// Scale bar: a round length close to 90 px. One degree of longitude is
	// 111.32 km at the equator, which is where this projection is true.
	const KM_PER_DEGREE = 111.32;
	const scaleKm = $derived.by(() => {
		const target = ((90 * unit) / MAP.k) * KM_PER_DEGREE;
		return [1000, 500, 200, 100, 50, 20, 10, 5].find((km) => km <= target) ?? 5;
	});
	const scaleUnits = $derived((scaleKm / KM_PER_DEGREE) * MAP.k);
</script>

<div class="frame" bind:clientWidth={width}>
	<svg
		viewBox="{outer.x} {outer.y} {outer.width} {outer.height}"
		style:aspect-ratio="{outer.width} / {outer.height}"
		role="img"
		aria-label={label}
	>
		<defs>
			<clipPath id={clip}>
				<rect x={view.current.x} y={view.current.y} width={view.current.width} height={view.current.height} />
			</clipPath>
		</defs>

		<g clip-path="url(#{clip})">
			<rect x={view.current.x} y={view.current.y} width={view.current.width} height={view.current.height} class="sea" />

			{#each meridians as lon (lon)}
				{@const x = (lon - MAP.lon0) * MAP.k}
				<line x1={x} x2={x} y1={view.current.y} y2={view.current.y + view.current.height} class="grid" />
			{/each}
			{#each parallels as lat (lat)}
				{@const y = (MAP.lat0 - lat) * MAP.k}
				<line x1={view.current.x} x2={view.current.x + view.current.width} y1={y} y2={y} class="grid" class:equator={lat === 0} />
			{/each}

			<path d={NEIGHBOURS_PATH} class="foreign" />
			<path d={INDONESIA_PATH} class="land" />

			{#if pxPerDegree >= 5}
				{#each SEAS as [key, lat, lon] (key)}
					{#if inView(lat, lon) && (pxPerDegree >= 9 || key === 'java' || key === 'banda' || (key === 'indian' && pxPerDegree >= 7))}
						{@const [x, y] = project(lat, lon)}
						<text {x} {y} class="water-name" font-size={12.5 * unit} text-anchor="middle">{i18n.m.map.seas[key]}</text>
					{/if}
				{/each}
			{/if}
			{#if pxPerDegree >= 11}
				{#each NEIGHBOURS as [key, lat, lon] (`${key}${lon}`)}
					{#if inView(lat, lon)}
						{@const [x, y] = project(lat, lon)}
						<text {x} {y} class="foreign-name" font-size={9.5 * unit} letter-spacing={1.2 * unit} text-anchor="middle">
							{i18n.m.map.neighbours[key].toUpperCase()}
						</text>
					{/if}
				{/each}
				{#each ISLANDS as [key, lat, lon] (key)}
					{#if inView(lat, lon)}
						{@const [x, y] = project(lat, lon)}
						<text {x} {y} class="land-name" font-size={10 * unit} letter-spacing={1.6 * unit} text-anchor="middle">
							{i18n.m.map.islands[key].toUpperCase()}
						</text>
					{/if}
				{/each}
			{/if}

			{@render children?.(unit)}

			<g transform="translate({view.current.x + 14 * unit} {view.current.y + view.current.height - 16 * unit})">
				<rect x={-6 * unit} y={-16 * unit} width={scaleUnits + 46 * unit} height={26 * unit} class="scale-ground" />
				<rect x="0" y={-4 * unit} width={scaleUnits / 2} height={4 * unit} class="scale-dark" />
				<rect x={scaleUnits / 2} y={-4 * unit} width={scaleUnits / 2} height={4 * unit} class="scale-light" />
				<text x="0" y={-7 * unit} font-size={9.5 * unit} class="scale-text">0</text>
				<text x={scaleUnits} y={-7 * unit} font-size={9.5 * unit} class="scale-text" text-anchor="middle">
					{scaleKm.toLocaleString(i18n.m.numberLocale)} km
				</text>
			</g>
		</g>

		<rect x={view.current.x} y={view.current.y} width={view.current.width} height={view.current.height} class="neatline" />

		{#each meridians as lon (lon)}
			{@const x = (lon - MAP.lon0) * MAP.k}
			<line x1={x} x2={x} y1={view.current.y - 5 * unit} y2={view.current.y} class="tick" />
			<!-- A label at the right edge would be cut by the sheet. -->
			{#if labelled(lon, lonEvery) && x < view.current.x + view.current.width - 20 * unit}
				<text {x} y={view.current.y - 8 * unit} font-size={10 * unit} class="coord" text-anchor="middle">{lonLabel(lon)}</text>
			{/if}
		{/each}
		{#each parallels as lat (lat)}
			{@const y = (MAP.lat0 - lat) * MAP.k}
			<line x1={view.current.x - 5 * unit} x2={view.current.x} y1={y} y2={y} class="tick" />
			{#if labelled(lat, latEvery)}
				<text x={view.current.x - 8 * unit} y={y + 3.5 * unit} font-size={10 * unit} class="coord" text-anchor="end">{latLabel(lat)}</text>
			{/if}
		{/each}
	</svg>
</div>

<style>
	.frame {
		min-width: 0;
	}

	svg {
		display: block;
		width: 100%;
		height: auto;
		overflow: hidden;
	}

	.sea {
		fill: var(--water);
	}

	.grid {
		stroke: var(--water-ink);
		stroke-opacity: 0.22;
		stroke-width: 1;
		vector-effect: non-scaling-stroke;
	}

	.grid.equator {
		stroke-opacity: 0.5;
	}

	.foreign {
		fill: var(--foreign);
		stroke: var(--hair);
		stroke-width: 0.6;
		vector-effect: non-scaling-stroke;
	}

	.land {
		fill: var(--land);
		stroke: var(--land-edge);
		stroke-width: 0.8;
		vector-effect: non-scaling-stroke;
	}

	.water-name {
		font-family: var(--font-serif);
		font-style: italic;
		fill: var(--water-ink);
		pointer-events: none;
	}

	.land-name {
		font-family: var(--font-sans);
		font-weight: 600;
		fill: var(--ink);
		pointer-events: none;
	}

	.foreign-name {
		font-family: var(--font-sans);
		fill: var(--ink-2);
		pointer-events: none;
	}

	.neatline {
		fill: none;
		stroke: var(--ink);
		stroke-width: 1;
		vector-effect: non-scaling-stroke;
	}

	.tick {
		stroke: var(--ink);
		stroke-width: 1;
		vector-effect: non-scaling-stroke;
	}

	.coord {
		font-family: var(--font-mono);
		fill: var(--ink);
	}

	.scale-ground {
		fill: var(--paper);
		fill-opacity: 0.85;
	}

	.scale-dark {
		fill: var(--ink);
	}

	.scale-light {
		fill: var(--paper);
		stroke: var(--ink);
		stroke-width: 1;
		vector-effect: non-scaling-stroke;
	}

	.scale-text {
		font-family: var(--font-mono);
		fill: var(--ink);
	}
</style>
