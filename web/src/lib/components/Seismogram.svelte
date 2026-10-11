<script lang="ts">
	import { parseTime, type Earthquake } from '#lib/api';

	let { quakes }: { quakes: Earthquake[] } = $props();

	const W = 1200;
	const H = 72;
	const MID = H / 2;
	const STEP = 2;

	// The trace covers the period the loaded earthquakes span, ending now. Each
	// earthquake adds a burst that starts at its moment and rings down.
	const trace = $derived.by(() => {
		const now = Date.now();
		const times = quakes.map((q) => parseTime(q.datetime).getTime());
		const start = times.length ? Math.min(...times) : now - 86_400_000;
		const span = Math.max(now - start, 3_600_000) * 1.04;
		const origin = now - span;

		const bursts = quakes.map((quake, i) => ({
			x: ((times[i] - origin) / span) * W,
			amplitude: Math.min(30, 5 + Math.max(0, quake.magnitude - 2.5) * 6.5)
		}));

		let d = '';
		for (let x = 0; x <= W; x += STEP) {
			// Background tremor, so the line is alive between events
			let y = Math.sin(x * 0.11) * 0.9 + Math.sin(x * 0.37 + 1.3) * 0.6;
			for (const burst of bursts) {
				const dx = x - burst.x;
				if (dx >= 0 && dx < 90) y += burst.amplitude * Math.exp(-dx / 16) * Math.sin(dx * 0.9);
			}
			d += `${x === 0 ? 'M' : 'L'}${x},${(MID - y).toFixed(1)}`;
		}

		const days = Math.max(1, Math.round(span / 86_400_000));
		return { d, days };
	});
</script>

<figure class="seismogram" class:ready={quakes.length > 0}>
	<svg viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true">
		<line x1="0" x2={W} y1={MID} y2={MID} class="base" />
		{#key trace.d}
			<path d={trace.d} pathLength="1" class="trace" />
		{/key}
	</svg>
	<figcaption>
		<span>
			{#if quakes.length}
				{quakes.length} earthquakes over the last {trace.days} {trace.days === 1 ? 'day' : 'days'},
				drawn from live data
			{:else}
				Waiting for earthquake data
			{/if}
		</span>
		<span>now</span>
	</figcaption>
</figure>

<style>
	.seismogram {
		margin: 0;
		display: grid;
		gap: 4px;
	}

	svg {
		display: block;
		width: 100%;
		height: 72px;
	}

	.base {
		stroke: var(--line);
		stroke-width: 1;
		vector-effect: non-scaling-stroke;
	}

	.trace {
		fill: none;
		stroke: var(--quake);
		stroke-width: 1.5;
		stroke-linejoin: round;
		vector-effect: non-scaling-stroke;
		stroke-dasharray: 1;
		stroke-dashoffset: 1;
	}

	/* Draw from past to present once the data is in. */
	.ready .trace {
		animation: draw 2.6s cubic-bezier(0.3, 0, 0.2, 1) 0.2s forwards;
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
		font-size: 0.6875rem;
		letter-spacing: 0.04em;
		color: var(--muted);
	}

	@media (prefers-reduced-motion: reduce) {
		.ready .trace {
			animation: none;
			stroke-dashoffset: 0;
		}
	}
</style>
