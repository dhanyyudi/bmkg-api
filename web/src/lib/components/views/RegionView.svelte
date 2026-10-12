<script lang="ts">
	import type { Region } from '#lib/api';
	import { useMessages } from '#lib/i18n';

	interface Props {
		regions: Region[];
		/** Load another request into the explorer. */
		onopen: (endpoint: string, params: Record<string, string>) => void;
	}

	let { regions, onopen }: Props = $props();
	const i18n = useMessages();

	// What comes next depends on the level of the code.
	function next(code: string): { label: string; endpoint: string; params: Record<string, string> } {
		switch (code.split('.').length) {
			case 1:
				return { label: i18n.m.views.toDistricts, endpoint: 'wilayah-districts', params: { province: code } };
			case 2:
				return { label: i18n.m.views.toSubdistricts, endpoint: 'wilayah-subdistricts', params: { district: code } };
			case 3:
				return { label: i18n.m.views.toVillages, endpoint: 'wilayah-villages', params: { subdistrict: code } };
			default:
				return { label: i18n.m.views.toForecast, endpoint: 'weather', params: { adm4: code } };
		}
	}
</script>

{#if regions.length === 0}
	<p class="empty">{i18n.m.views.noRegion}</p>
{:else}
	<div class="table-scroll">
		<table class="table">
			<thead>
				<tr>
					<th>{i18n.m.views.code}</th>
					<th>{i18n.m.views.name}</th>
					<th>{i18n.m.views.next}</th>
				</tr>
			</thead>
			<tbody>
				{#each regions as region (region.code)}
					{@const step = next(region.code)}
					<tr>
						<td class="mono">{region.code}</td>
						<td>
							{region.name}
							{#if region.full_path}<span class="path">{region.full_path}</span>{/if}
						</td>
						<td>
							<button type="button" class="btn small" onclick={() => onopen(step.endpoint, step.params)}>
								{step.label}
							</button>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}

<style>
	td {
		vertical-align: middle;
	}

	.path {
		display: block;
		font-size: 0.8125rem;
		color: var(--ink-2);
	}

	.empty {
		color: var(--ink-2);
	}
</style>
