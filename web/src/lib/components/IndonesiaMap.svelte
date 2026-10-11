<script lang="ts">
	import type { Snippet } from 'svelte';
	import { Tween } from 'svelte/motion';
	import { cubicOut } from 'svelte/easing';
	import { INDONESIA_PATH, MAP, NEIGHBOURS_PATH } from '#lib/geo/indonesia';
	import type { Box } from '#lib/geo/project';

	interface Props {
		/** Area to show; the whole archipelago by default. */
		box?: Box;
		label: string;
		/** Overlay content. Receives the map units per screen pixel, so marks can be sized in pixels. */
		children?: Snippet<[number]>;
	}

	const FULL: Box = { x: 0, y: 0, width: MAP.width, height: MAP.height };
	let { box = FULL, label, children }: Props = $props();

	const view = new Tween(FULL, { duration: 600, easing: cubicOut });
	$effect(() => {
		const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
		view.set(box, still ? { duration: 0 } : undefined);
	});

	let width = $state(0);
	// Map units per CSS pixel at the current zoom and rendered size
	// Below 420 px the map is treated as 420 px wide, so marks shrink with it
	// instead of crowding a small map.
	const unit = $derived(view.current.width / Math.max(width || MAP.width, 420));
</script>

<div class="frame" bind:clientWidth={width}>
<svg
	viewBox="{view.current.x} {view.current.y} {view.current.width} {view.current.height}"
	role="img"
	aria-label={label}
	preserveAspectRatio="xMidYMid meet"
>
	<rect x={-2000} y={-2000} width={6000} height={6000} class="sea" />
	<path d={NEIGHBOURS_PATH} class="neighbours" />
	<path d={INDONESIA_PATH} class="indonesia" />
	{@render children?.(unit)}
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
		aspect-ratio: 940 / 380;
		border-radius: 8px;
		background: var(--sea);
	}

	.sea {
		fill: var(--sea);
	}

	.neighbours {
		fill: var(--land);
	}

	.indonesia {
		fill: var(--land-id);
		stroke: var(--sea);
		stroke-width: 0.6;
		vector-effect: non-scaling-stroke;
	}
</style>
