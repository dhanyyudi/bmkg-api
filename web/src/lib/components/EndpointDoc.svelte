<script lang="ts">
	import CodeBlock from './CodeBlock.svelte';
	import { PUBLIC_ORIGIN, request, type ApiResult } from '#lib/api';
	import { DEFAULT_PARAMS, cacheTime, type EndpointDef } from '#lib/endpoints';
	import { fill, href, useMessages } from '#lib/i18n';

	let { endpoint }: { endpoint: EndpointDef } = $props();
	const i18n = useMessages();

	let result = $state<ApiResult | null>(null);
	let loading = $state(false);
	let failed = $state(false);

	const examplePath = $derived(endpoint.path(DEFAULT_PARAMS));
	// Warning details need a real, currently active code, so that one runs in the explorer.
	const runnable = $derived(!examplePath.includes('%7B'));

	async function run() {
		loading = true;
		failed = false;
		try {
			result = await request(examplePath);
		} catch {
			failed = true;
		}
		loading = false;
	}

	const body = $derived.by(() => {
		if (!result) return '';
		const lines = JSON.stringify(result.body, null, 2).split('\n');
		return lines.length > 60
			? `${lines.slice(0, 60).join('\n')}\n${fill(i18n.m.docs.moreLines, { n: lines.length - 60 })}`
			: lines.join('\n');
	});
</script>

<article class="endpoint" id={endpoint.id}>
	<header>
		<span class="method">GET</span>
		<code class="path">{endpoint.template}</code>
		<span class="ttl mono">{fill(i18n.m.common.cached, { ttl: cacheTime(endpoint.ttl, i18n.m) })}</span>
	</header>
	<p>{i18n.m.endpoints[endpoint.id].detail}</p>

	{#if endpoint.reference.length}
		<div class="table-scroll">
			<table class="table">
				<tbody>
					{#each endpoint.reference as [name, need] (name)}
						<tr>
							<td><code>{name}</code></td>
							<td class="need">{i18n.m.common[need]}</td>
							<td>{i18n.m.reference[name]}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}

	<div class="actions">
		{#if runnable}
			<button type="button" class="btn small" onclick={run} disabled={loading}>
				{loading ? i18n.m.common.running : result ? i18n.m.common.runAgain : i18n.m.common.run}
			</button>
		{/if}
		<a class="btn small" href="{href(i18n.locale, '/')}?endpoint={endpoint.id}#explorer">{i18n.m.docs.openInExplorer}</a>
		<code class="example">{decodeURIComponent(examplePath)}</code>
	</div>

	<div aria-live="polite">
		{#if failed}
			<p class="problem">{i18n.m.docs.sendFailed}</p>
		{:else if result}
			<CodeBlock
				code={body}
				lang="json"
				title="{result.status} · {result.ms} ms · curl {PUBLIC_ORIGIN}{decodeURIComponent(result.path)}"
				maxHeight="340px"
			/>
		{/if}
	</div>
</article>

<style>
	.endpoint {
		padding: 14px 0 18px;
		border-top: 1px solid var(--hair);
		display: grid;
		gap: 10px;
		scroll-margin-top: 80px;
		min-width: 0;
	}

	header {
		display: flex;
		align-items: baseline;
		gap: 10px;
		flex-wrap: wrap;
	}

	.path {
		font-size: 1rem;
		font-weight: 500;
	}

	.ttl {
		margin-left: auto;
		font-size: 0.8125rem;
		color: var(--ink-2);
	}

	.need {
		font-size: 0.875rem;
		color: var(--ink-2);
		white-space: nowrap;
	}

	.actions {
		display: flex;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
	}

	.example {
		font-size: 0.8125rem;
		color: var(--ink-2);
		overflow-wrap: anywhere;
		min-width: 0;
	}

	.problem {
		color: var(--alert);
	}

	@media (max-width: 720px) {
		.actions .btn {
			min-height: 44px;
		}
	}
</style>
