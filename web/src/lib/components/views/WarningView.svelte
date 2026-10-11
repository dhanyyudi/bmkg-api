<script lang="ts">
	import IndonesiaMap from '../IndonesiaMap.svelte';
	import { frame, ringPath, warningRings, type LatLon } from '#lib/geo/project';
	import { formatWib, parseTime, type Warning } from '#lib/api';

	let { warnings, emptyText }: { warnings: Warning[]; emptyText?: string } = $props();

	let picked = $state(0);
	$effect(() => {
		void warnings;
		picked = 0;
	});

	const warning = $derived(warnings[picked]);
	const rings = $derived(
		warning ? warning.areas.flatMap((area) => warningRings(area.polygon).map((ring) => ({ area: area.name, ring }))) : []
	);
	const box = $derived(frame(rings.flatMap((r) => r.ring as LatLon[]), 2.5));
	let hoveredArea = $state<string | null>(null);
</script>

{#if !warning}
	<p class="empty">{emptyText ?? 'No active warning.'}</p>
{:else}
	{#if warnings.length > 1}
		<div class="tabs" role="tablist">
			{#each warnings as item, i (item.identifier)}
				<button type="button" role="tab" aria-selected={i === picked} class:on={i === picked} onclick={() => (picked = i)}>
					{item.areas[0]?.name ?? item.event}
				</button>
			{/each}
		</div>
	{/if}

	<div class="layout">
		<div class="text">
			<p class="head">
				<strong>{warning.event}</strong>
				<span class="badge">{warning.severity}</span>
			</p>
			<p class="headline">{warning.headline}</p>
			<p class="desc">{warning.description}</p>
			<dl>
				<div><dt>Effective</dt><dd>{formatWib(parseTime(warning.effective))}</dd></div>
				<div><dt>Expires</dt><dd>{formatWib(parseTime(warning.expires))}</dd></div>
				<div><dt>Urgency</dt><dd>{warning.urgency}</dd></div>
				<div><dt>Certainty</dt><dd>{warning.certainty}</dd></div>
			</dl>
		</div>

		<div class="visual">
			{#if rings.length}
				<IndonesiaMap {box} label="Areas covered by the warning">
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
				</IndonesiaMap>
				<p class="caption">
					{hoveredArea ?? `${rings.length} warning ${rings.length === 1 ? 'area' : 'areas'} · hover for the name`}
				</p>
			{:else}
				<p class="empty">This warning has no polygon data.</p>
			{/if}
			{#if warning.infographic_url}
				<a class="info" href={warning.infographic_url} target="_blank" rel="noopener">
					<img src={warning.infographic_url} alt="BMKG infographic for this warning" loading="lazy" />
				</a>
			{/if}
		</div>
	</div>
{/if}

<style>
	.tabs {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
		margin-bottom: 12px;
	}

	.tabs button {
		padding: 4px 10px;
		border-radius: 999px;
		border: 1px solid var(--line);
		background: none;
		font-size: 0.8125rem;
	}

	.tabs button.on {
		background: var(--warn-soft);
		border-color: var(--warn);
		color: var(--warn);
	}

	.layout {
		display: grid;
		grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
		gap: 18px;
		align-items: start;
	}

	.text {
		display: grid;
		gap: 8px;
		font-size: 0.9375rem;
	}

	.head {
		display: flex;
		align-items: center;
		gap: 10px;
		font-size: 1.0625rem;
	}

	.badge {
		font-size: 0.75rem;
		padding: 2px 8px;
		border-radius: 999px;
		background: var(--warn-soft);
		color: var(--warn);
	}

	.headline {
		color: var(--muted);
	}

	.desc {
		font-size: 0.875rem;
	}

	dl {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 8px 16px;
		margin: 4px 0 0;
		padding-top: 10px;
		border-top: 1px solid var(--line);
	}

	dt {
		font-size: 0.75rem;
		color: var(--muted);
	}

	dd {
		margin: 0;
		font-size: 0.875rem;
	}

	.visual {
		display: grid;
		gap: 8px;
	}

	.zone {
		fill: var(--warn);
		fill-opacity: 0.4;
		stroke: var(--warn);
		stroke-width: 1.5;
		vector-effect: non-scaling-stroke;
	}

	.zone.on {
		fill-opacity: 0.75;
	}

	.caption {
		font-size: 0.8125rem;
		color: var(--muted);
		min-height: 1.4em;
	}

	.info img {
		display: block;
		width: 100%;
		border-radius: 8px;
		border: 1px solid var(--line);
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
