<script lang="ts">
	import type { Earthquake } from '#lib/api';
	import { fill, useMessages } from '#lib/i18n';
	import { fractionOf, REPLAY_DELAY_MS, REPLAY_MS, type Timeline } from '#lib/timeline';

	let { quakes, timeline }: { quakes: Earthquake[]; timeline: Timeline } = $props();

	const i18n = useMessages();

	const W = 1200;
	const H = 56;
	const MID = H / 2;
	const STEP = 2;

	// Each earthquake adds a burst that starts at its moment and rings down.
	const trace = $derived.by(() => {
		const bursts = quakes.map((quake) => ({
			x: fractionOf(quake, timeline) * W,
			amplitude: Math.min(24, 4 + Math.max(0, quake.magnitude - 2.5) * 5.2)
		}));

		let d = '';
		for (let x = 0; x <= W; x += STEP) {
			// Background tremor, so the line reads as a recording between events
			let y = Math.sin(x * 0.11) * 0.7 + Math.sin(x * 0.37 + 1.3) * 0.45;
			for (const burst of bursts) {
				const dx = x - burst.x;
				if (dx >= 0 && dx < 90) y += burst.amplitude * Math.exp(-dx / 16) * Math.sin(dx * 0.9);
			}
			d += `${x === 0 ? 'M' : 'L'}${x},${(MID - y).toFixed(1)}`;
		}
		return d;
	});

	const days = $derived(Math.max(1, Math.round(timeline.span / 86_400_000)));
</script>

<figure class="seismogram" class:ready={quakes.length > 0} style:--replay="{REPLAY_MS}ms" style:--wait="{REPLAY_DELAY_MS}ms">
	<svg viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true">
		<line x1="0" x2={W} y1={MID} y2={MID} class="base" />
		{#key trace}
			<path d={trace} pathLength="1" class="trace" />
		{/key}
	</svg>
	<figcaption>
		<span>
			{quakes.length
				? fill(i18n.m.map.traceCaption, { n: quakes.length, days })
				: i18n.m.map.traceWaiting}
		</span>
		<span>{i18n.m.map.now}</span>
	</figcaption>
</figure>

<style>
	.seismogram {
		margin: 0;
		padding: 8px 10px 6px;
		border-top: 1px solid var(--ink);
	}

	svg {
		display: block;
		width: 100%;
		height: 56px;
	}

	.base {
		stroke: var(--hair);
		stroke-width: 1;
		vector-effect: non-scaling-stroke;
	}

	/* Brown is the relief colour: the trace is ground motion. */
	.trace {
		fill: none;
		stroke: var(--relief);
		stroke-width: 1.25;
		stroke-linejoin: round;
		vector-effect: non-scaling-stroke;
		stroke-dasharray: 1;
		stroke-dashoffset: 1;
	}

	/* Drawn once from past to present, at the pace the marks appear on the map. */
	.ready .trace {
		animation: draw var(--replay) linear var(--wait) forwards;
	}

	@keyframes draw {
		to {
			stroke-dashoffset: 0;
		}
	}

	figcaption {
		display: flex;
		justify-content: space-between;
		gap: 12px;
		font-family: var(--font-mono);
		font-size: 0.75rem;
		color: var(--ink-2);
	}

	@media (prefers-reduced-motion: reduce) {
		.ready .trace {
			animation: none;
			stroke-dashoffset: 0;
		}
	}
</style>
