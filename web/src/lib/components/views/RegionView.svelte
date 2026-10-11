<script lang="ts">
	import type { Region } from '#lib/api';

	interface Props {
		regions: Region[];
		/** Load another request into the explorer. */
		onopen: (endpoint: string, params: Record<string, string>) => void;
	}

	let { regions, onopen }: Props = $props();

	const depth = (code: string) => code.split('.').length;

	// What you can do next with a code depends on its level.
	function next(code: string): { label: string; endpoint: string; params: Record<string, string> } {
		switch (depth(code)) {
			case 1:
				return { label: 'Districts', endpoint: 'wilayah-districts', params: { province: code } };
			case 2:
				return { label: 'Subdistricts', endpoint: 'wilayah-subdistricts', params: { district: code } };
			case 3:
				return { label: 'Villages', endpoint: 'wilayah-villages', params: { subdistrict: code } };
			default:
				return { label: 'Forecast', endpoint: 'weather', params: { adm4: code } };
		}
	}
</script>

{#if regions.length === 0}
	<p class="empty">No region matched.</p>
{:else}
	<table>
		<thead>
			<tr><th>Code</th><th>Name</th><th><span class="sr-only">Next step</span></th></tr>
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
					<td class="act">
						<button type="button" class="btn small" onclick={() => onopen(step.endpoint, step.params)}>
							{step.label} →
						</button>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>
{/if}

<style>
	table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.875rem;
	}

	th {
		text-align: left;
		font-weight: 500;
		font-size: 0.75rem;
		color: var(--muted);
		padding: 0 8px 6px;
	}

	td {
		padding: 6px 8px;
		border-top: 1px solid var(--line);
		vertical-align: middle;
	}

	.path {
		display: block;
		font-size: 0.75rem;
		color: var(--muted);
	}

	.act {
		text-align: right;
		white-space: nowrap;
	}

	.empty {
		color: var(--muted);
	}
</style>
