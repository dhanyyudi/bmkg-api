<script lang="ts">
	import MapSheet from '../MapSheet.svelte';
	import { frame, project, type LatLon } from '#lib/geo/project';
	import type { Earthquake } from '#lib/api';
	import { formatWib, magnitude, parseTime, quakeRadius, timeAgo } from '#lib/format';
	import { fill, useMessages } from '#lib/i18n';

	let { quakes, center }: { quakes: Earthquake[]; center?: LatLon } = $props();
	const i18n = useMessages();

	let picked = $state(0);
	$effect(() => {
		// A new result starts on its first row.
		void quakes;
		picked = 0;
	});

	const current = $derived(quakes[picked]);
	// Taller than the country strip, so the map fills the response panel.
	const box = $derived(
		frame([...quakes.map((q) => [q.lat, q.lon] as LatLon), ...(center ? [center] : [])], 16, 1.7)
	);
</script>

{#if quakes.length === 0}
	<p class="empty">{i18n.m.views.noQuakes}</p>
{:else}
	<div class="map">
		<MapSheet {box} label={i18n.m.views.quakesLabel}>
			{#snippet children(unit)}
				{#if center}
					{@const [cx, cy] = project(center[0], center[1])}
					<path d="M{cx - 8 * unit},{cy}H{cx + 8 * unit}M{cx},{cy - 8 * unit}V{cy + 8 * unit}" class="cross" />
				{/if}
				<!-- A pointer shortcut only: the rows below select the same earthquakes
				     from the keyboard. -->
				{#each quakes as quake, i (i)}
					{@const [x, y] = project(quake.lat, quake.lon)}
					<!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_static_element_interactions -->
					<circle
						cx={x}
						cy={y}
						r={quakeRadius(quake.magnitude) * unit}
						class="mark"
						class:on={i === picked}
						onclick={() => (picked = i)}
					>
						<title>{fill(i18n.m.map.quakeLabel, { m: magnitude(quake.magnitude, i18n.m), region: quake.region })}</title>
					</circle>
				{/each}
			{/snippet}
		</MapSheet>
	</div>

	<div class="below" class:single={quakes.length === 1}>
		<div class="detail">
			<p class="big">
				<span class="mono mag">M {magnitude(current.magnitude, i18n.m)}</span>
				<span class="mono depth">{fill(i18n.m.map.depth, { km: current.depth_km })}</span>
			</p>
			<p>{current.region}</p>
			<p class="fine">
				{formatWib(parseTime(current.datetime), i18n.m)}, {timeAgo(parseTime(current.datetime), i18n.m)}
			</p>
			<p class="fine mono">{current.lat_text}, {current.lon_text}</p>
			{#if current.distance_km !== undefined}
				<p class="fine">{fill(i18n.m.views.fromPoint, { km: current.distance_km.toFixed(0) })}</p>
			{/if}
			{#if current.tsunami_potential}<p class="fine">{current.tsunami_potential}</p>{/if}
			{#if current.felt_report}<p class="fine">{fill(i18n.m.map.felt, { text: current.felt_report })}</p>{/if}
			{#if current.shakemap_url}
				<p><a href={current.shakemap_url} target="_blank" rel="noopener">{i18n.m.views.shakemap}</a></p>
			{/if}
		</div>

		{#if quakes.length > 1}
			<ol class="rows">
				{#each quakes as quake, i (i)}
					<li>
						<button type="button" class:on={i === picked} onclick={() => (picked = i)}>
							<span class="mono">M {magnitude(quake.magnitude, i18n.m)}</span>
							<span class="where">{quake.region}</span>
							<span class="when">{timeAgo(parseTime(quake.datetime), i18n.m)}</span>
						</button>
					</li>
				{/each}
			</ol>
		{/if}
	</div>
{/if}

<style>
	.map {
		border: 1px solid var(--ink);
		padding: 6px 8px 8px 0;
	}

	.below {
		display: grid;
		grid-template-columns: minmax(0, 2fr) minmax(0, 3fr);
		gap: 16px 28px;
		margin-top: 14px;
		align-items: start;
	}

	.below.single {
		grid-template-columns: minmax(0, 1fr);
	}

	.detail {
		display: grid;
		gap: 4px;
	}

	.big {
		display: flex;
		gap: 12px;
		align-items: baseline;
		flex-wrap: wrap;
	}

	.mag {
		font-size: 1.5rem;
		font-weight: 500;
		color: var(--alert);
	}

	.depth {
		color: var(--relief);
	}

	.fine {
		font-size: 0.875rem;
		color: var(--ink-2);
	}

	.mark {
		fill: var(--alert);
		fill-opacity: 0.4;
		stroke: var(--alert);
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
		margin: 0;
		padding: 0;
		border-top: 1px solid var(--ink);
		max-height: 264px;
		overflow: auto;
	}

	.rows button {
		display: grid;
		grid-template-columns: 62px minmax(0, 1fr) auto;
		gap: 10px;
		align-items: baseline;
		width: 100%;
		min-height: 44px;
		padding: 6px 8px;
		border: 0;
		border-bottom: 1px solid var(--hair);
		background: none;
		text-align: left;
		font-size: 0.9375rem;
	}

	.rows button:hover {
		background: var(--tint);
	}

	/* The chosen row is printed in reverse, like a highlighted table line. */
	.rows button.on {
		background: var(--ink);
		color: var(--paper);
	}

	.when {
		font-size: 0.8125rem;
	}

	.where {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.empty {
		color: var(--ink-2);
	}

	@media (max-width: 720px) {
		.below {
			grid-template-columns: minmax(0, 1fr);
		}
	}
</style>
