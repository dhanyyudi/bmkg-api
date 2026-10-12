<script lang="ts">
	import type { ForecastEntry, WeatherLocation } from '#lib/api';
	import { fill, useMessages } from '#lib/i18n';

	interface Day {
		date: string;
		entries: ForecastEntry[];
	}

	let { location, days, current }: { location: WeatherLocation; days?: Day[]; current?: ForecastEntry } =
		$props();
	const i18n = useMessages();

	const entries = $derived(days ? days.flatMap((d) => d.entries) : []);
	let hovered = $state<number | null>(null);

	// BMKG gives each condition in both languages.
	const condition = (e: ForecastEntry) => (i18n.locale === 'en' ? e.weather_en : e.weather);

	// Chart geometry
	const W = 640;
	const H = 150;
	const PAD = { left: 32, right: 12, top: 14, bottom: 22 };
	const temps = $derived(entries.map((e) => e.temperature_c));
	const lo = $derived(Math.floor(Math.min(...temps) - 1));
	const hi = $derived(Math.ceil(Math.max(...temps) + 1));
	const xAt = (i: number) => PAD.left + (i * (W - PAD.left - PAD.right)) / Math.max(1, entries.length - 1);
	const yAt = (t: number) => PAD.top + ((hi - t) * (H - PAD.top - PAD.bottom)) / Math.max(1, hi - lo);
	const line = $derived(
		entries.map((e, i) => `${i ? 'L' : 'M'}${xAt(i).toFixed(1)},${yAt(e.temperature_c).toFixed(1)}`).join('')
	);
	const focus = $derived(hovered !== null ? entries[hovered] : null);

	// One date label where each day begins, skipping any that would collide.
	const dayStarts = $derived.by(() => {
		const starts: { index: number; label: string }[] = [];
		entries.forEach((entry, index) => {
			const day = entry.local_datetime.slice(0, 10);
			const isStart = index === 0 || entries[index - 1].local_datetime.slice(0, 10) !== day;
			const last = starts[starts.length - 1];
			if (isStart && (!last || xAt(index) - xAt(last.index) > 60)) {
				starts.push({ index, label: `${day.slice(8, 10)}/${day.slice(5, 7)}` });
			}
		});
		return starts;
	});

	const hour = (e: ForecastEntry) => e.local_datetime.slice(11, 16);
	const dayLabel = (date: string) =>
		new Date(`${date}T00:00:00Z`).toLocaleDateString(i18n.m.numberLocale, {
			weekday: 'long',
			day: 'numeric',
			month: 'long',
			timeZone: 'UTC'
		});

	// Icons are hosted by BMKG; keep the layout if one fails to load.
	function hide(event: Event) {
		(event.currentTarget as HTMLImageElement).style.visibility = 'hidden';
	}

	function track(event: PointerEvent) {
		const svg = event.currentTarget as SVGSVGElement;
		const rect = svg.getBoundingClientRect();
		const x = ((event.clientX - rect.left) / rect.width) * W;
		const step = (W - PAD.left - PAD.right) / Math.max(1, entries.length - 1);
		hovered = Math.min(entries.length - 1, Math.max(0, Math.round((x - PAD.left) / step)));
	}
</script>

<p class="place">
	<strong>{location.village}</strong>, {location.subdistrict}, {location.district}, {location.province}
	<span class="mono">{location.code}</span>
</p>

{#if current}
	<div class="now">
		<img src={current.icon_url} alt="" width="56" height="56" onerror={hide} />
		<p class="temp mono">{current.temperature_c}°C</p>
		<div>
			<p>{condition(current)}</p>
			<p class="fine">
				{fill(i18n.m.views.humidity, { v: current.humidity_pct })} ·
				{fill(i18n.m.views.wind, { v: current.wind_speed_kmh, dir: current.wind_direction })} ·
				{fill(i18n.m.views.cloud, { v: current.cloud_cover_pct })}
			</p>
			<p class="fine">{fill(i18n.m.views.slot, { time: current.local_datetime })}</p>
		</div>
	</div>
{/if}

{#if entries.length > 1}
	<figure class="chart">
		<figcaption>
			{#if focus}
				<span>
					<strong class="mono">{focus.temperature_c}°C</strong> · {condition(focus)} ·
					{fill(i18n.m.views.humidity, { v: focus.humidity_pct })}
				</span>
				<span class="fine">{fill(i18n.m.views.localTime, { time: focus.local_datetime })}</span>
			{:else}
				<span>{fill(i18n.m.views.chartTitle, { n: days?.length ?? 0 })}</span>
				<span class="fine">{i18n.m.views.chartHint}</span>
			{/if}
		</figcaption>
		<svg
			viewBox="0 0 {W} {H}"
			role="img"
			aria-label={fill(i18n.m.views.chartLabel, { lo, hi })}
			onpointermove={track}
			onpointerdown={track}
			onpointerleave={() => (hovered = null)}
		>
			{#each [lo, Math.round((lo + hi) / 2), hi] as tick (tick)}
				<line x1={PAD.left} x2={W - PAD.right} y1={yAt(tick)} y2={yAt(tick)} class="grid" />
				<text x={PAD.left - 6} y={yAt(tick) + 4} text-anchor="end" class="axis">{tick}°</text>
			{/each}
			<path d={line} class="line" />
			{#each dayStarts as start (start.index)}
				<text x={xAt(start.index)} y={H - 6} text-anchor={start.index === 0 ? 'start' : 'middle'} class="axis">
					{start.label}
				</text>
			{/each}
			{#if hovered !== null && focus}
				<line x1={xAt(hovered)} x2={xAt(hovered)} y1={PAD.top} y2={H - PAD.bottom} class="cursor" />
				<circle cx={xAt(hovered)} cy={yAt(focus.temperature_c)} r="4.5" class="point" />
			{/if}
		</svg>
	</figure>

	<div class="days">
		{#each days ?? [] as day (day.date)}
			<section>
				<h4>{dayLabel(day.date)}</h4>
				<ul>
					{#each day.entries as entry (entry.utc_datetime)}
						<li>
							<span class="mono">{hour(entry)}</span>
							<img src={entry.icon_url} alt="" width="24" height="24" loading="lazy" onerror={hide} />
							<span class="mono">{entry.temperature_c}°</span>
							<span class="what">{condition(entry)}</span>
						</li>
					{/each}
				</ul>
			</section>
		{/each}
	</div>
{/if}

<style>
	.place {
		margin-bottom: 12px;
	}

	.place .mono {
		margin-left: 6px;
		color: var(--ink-2);
	}

	.now {
		display: flex;
		align-items: center;
		gap: 14px;
		flex-wrap: wrap;
	}

	.temp {
		font-size: 2.25rem;
		font-weight: 500;
		line-height: 1;
	}

	.fine {
		color: var(--ink-2);
		font-size: 0.875rem;
	}

	.chart {
		margin: 0;
		border: 1px solid var(--ink);
		padding: 8px 10px 4px;
	}

	figcaption {
		display: flex;
		justify-content: space-between;
		gap: 12px;
		flex-wrap: wrap;
		font-size: 0.9375rem;
		min-height: 1.6em;
	}

	svg {
		display: block;
		width: 100%;
		height: auto;
		touch-action: pan-y;
		cursor: crosshair;
	}

	.grid {
		stroke: var(--hair);
	}

	.axis {
		fill: var(--ink-2);
		font-family: var(--font-mono);
		font-size: 10px;
	}

	.line {
		fill: none;
		stroke: var(--ink);
		stroke-width: 1.75;
		stroke-linejoin: round;
	}

	.cursor {
		stroke: var(--ink-2);
		stroke-dasharray: 3 3;
	}

	.point {
		fill: var(--ink);
		stroke: var(--paper);
		stroke-width: 2;
	}

	.days {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
		gap: 16px 24px;
		margin-top: 14px;
	}

	h4 {
		font-size: 0.9375rem;
		padding-bottom: 5px;
		margin-bottom: 4px;
		border-bottom: 1px solid var(--ink);
	}

	ul {
		list-style: none;
		margin: 0;
		padding: 0;
	}

	li {
		display: grid;
		grid-template-columns: 46px 24px 34px minmax(0, 1fr);
		align-items: center;
		gap: 6px;
		padding: 3px 0;
		font-size: 0.875rem;
		border-bottom: 1px solid var(--hair);
	}

	.what {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
</style>
