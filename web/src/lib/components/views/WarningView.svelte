<script lang="ts">
	import MapSheet from '../MapSheet.svelte';
	import { frame, ringPath, warningRings, type LatLon } from '#lib/geo/project';
	import type { Warning } from '#lib/api';
	import { formatWib, parseTime } from '#lib/format';
	import { fill, useMessages } from '#lib/i18n';

	let { warnings, emptyText }: { warnings: Warning[]; emptyText?: string } = $props();
	const i18n = useMessages();

	let picked = $state(0);
	$effect(() => {
		void warnings;
		picked = 0;
	});

	const warning = $derived(warnings[picked]);
	const rings = $derived(
		warning ? warning.areas.flatMap((area) => warningRings(area.polygon).map((ring) => ({ area: area.name, ring }))) : []
	);
	const box = $derived(frame(rings.flatMap((r) => r.ring as LatLon[]), 3, 1.7));
	let hoveredArea = $state<string | null>(null);
</script>

{#if !warning}
	<p class="empty">{emptyText ?? i18n.m.views.noWarning}</p>
{:else}
	{#if warnings.length > 1}
		<div class="pick">
			{#each warnings as item, i (item.identifier)}
				<button type="button" aria-pressed={i === picked} class:on={i === picked} onclick={() => (picked = i)}>
					{item.areas[0]?.name ?? item.event}
				</button>
			{/each}
		</div>
	{/if}

	<p class="head">
		<strong>{warning.event}</strong>
		<span class="severity mono">{warning.severity}</span>
	</p>
	<p class="headline">{warning.headline}</p>

	{#if rings.length}
		<div class="map">
			<MapSheet {box} label={i18n.m.views.areasLabel}>
				{#snippet children()}
					{#each rings as item, i (i)}
						<path
							d={ringPath(item.ring)}
							class="zone"
							class:on={hoveredArea === item.area}
							role="img"
							aria-label={item.area}
							onpointerenter={() => (hoveredArea = item.area)}
							onpointerleave={() => (hoveredArea = null)}
						/>
					{/each}
				{/snippet}
			</MapSheet>
		</div>
		<p class="caption" aria-live="polite">
			{hoveredArea ?? fill(i18n.m.views.areasCount, { n: rings.length })}
		</p>
	{:else}
		<p class="empty">{i18n.m.views.noPolygon}</p>
	{/if}

	<div class="below">
		<div class="text">
			<p>{warning.description}</p>
			<dl>
				<div><dt>{i18n.m.views.effective}</dt><dd>{formatWib(parseTime(warning.effective), i18n.m)}</dd></div>
				<div><dt>{i18n.m.views.expires}</dt><dd>{formatWib(parseTime(warning.expires), i18n.m)}</dd></div>
				<div><dt>{i18n.m.views.urgency}</dt><dd>{warning.urgency}</dd></div>
				<div><dt>{i18n.m.views.certainty}</dt><dd>{warning.certainty}</dd></div>
			</dl>
		</div>
		{#if warning.infographic_url}
			<a class="info" href={warning.infographic_url} target="_blank" rel="noopener">
				<img src={warning.infographic_url} alt={i18n.m.views.infographic} loading="lazy" />
			</a>
		{/if}
	</div>
{/if}

<style>
	.pick {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
		margin-bottom: 12px;
	}

	.pick button {
		min-height: 36px;
		padding: 0 12px;
		border: 1px solid var(--ink);
		background: var(--paper);
		font-size: 0.9375rem;
	}

	.pick button.on {
		background: var(--ink);
		color: var(--paper);
	}

	.head {
		display: flex;
		align-items: baseline;
		gap: 12px;
		flex-wrap: wrap;
		font-size: 1.125rem;
	}

	/* Severity is the warning's own classification, so it carries the alert red. */
	.severity {
		color: var(--alert);
		font-size: 0.875rem;
	}

	.headline {
		color: var(--ink-2);
		margin-bottom: 10px;
	}

	.map {
		border: 1px solid var(--ink);
		padding: 6px 8px 8px 0;
	}

	.zone {
		fill: var(--alert);
		fill-opacity: 0.28;
		stroke: var(--alert);
		stroke-width: 1.25;
		vector-effect: non-scaling-stroke;
	}

	.zone.on {
		fill-opacity: 0.6;
	}

	.caption {
		font-size: 0.875rem;
		color: var(--ink-2);
		min-height: 1.5em;
		margin-top: 6px;
	}

	.below {
		display: grid;
		grid-template-columns: minmax(0, 3fr) minmax(0, 2fr);
		gap: 16px 28px;
		margin-top: 10px;
		align-items: start;
	}

	.text {
		display: grid;
		gap: 10px;
		font-size: 0.9375rem;
	}

	dl {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 8px 16px;
		margin: 0;
		padding-top: 10px;
		border-top: 1px solid var(--ink);
	}

	dt {
		font-size: 0.8125rem;
		color: var(--ink-2);
	}

	dd {
		margin: 0;
	}

	.info img {
		display: block;
		width: 100%;
		border: 1px solid var(--ink);
	}

	.empty {
		color: var(--ink-2);
	}

	@media (max-width: 720px) {
		.below {
			grid-template-columns: minmax(0, 1fr);
		}

		.pick button {
			min-height: 44px;
		}
	}
</style>
