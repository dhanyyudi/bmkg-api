<script lang="ts">
	import CodeBlock from './CodeBlock.svelte';
	import { PUBLIC_ORIGIN, request, type ApiResult } from '#lib/api';
	import { DEFAULT_PARAMS, type EndpointDef } from '#lib/endpoints';

	interface Props {
		endpoint: EndpointDef;
		detail: string;
		/** Query or path parameters: name, whether required, and what it means. */
		params: [string, string, string][];
		ttl: string;
	}

	let { endpoint, detail, params, ttl }: Props = $props();

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
		const text = JSON.stringify(result.body, null, 2);
		const lines = text.split('\n');
		return lines.length > 60 ? `${lines.slice(0, 60).join('\n')}\n  … ${lines.length - 60} more lines` : text;
	});
</script>

<article class="endpoint card" id={endpoint.id}>
	<header>
		<span class="method">GET</span>
		<code class="path">{endpoint.template}</code>
		<span class="ttl" title="How long a response is cached">cached {ttl}</span>
	</header>
	<p>{detail}</p>

	{#if params.length}
		<table class="table">
			<tbody>
				{#each params as [name, need, meaning] (name)}
					<tr>
						<td><code>{name}</code></td>
						<td class="need">{need}</td>
						<td>{meaning}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	{/if}

	<div class="actions">
		{#if runnable}
			<button type="button" class="btn small" onclick={run} disabled={loading}>
				{loading ? 'Running…' : result ? 'Run again' : 'Run live'}
			</button>
		{/if}
		<a class="btn small" href="/?endpoint={endpoint.id}#explorer">Open in explorer</a>
		<code class="example">{decodeURIComponent(examplePath)}</code>
	</div>

	{#if failed}
		<p class="problem">The request could not be sent.</p>
	{:else if result}
		<CodeBlock
			code={body}
			lang="json"
			title="{result.status} · {result.ms} ms · curl {PUBLIC_ORIGIN}{decodeURIComponent(result.path)}"
			maxHeight="340px"
		/>
	{/if}
</article>

<style>
	.endpoint {
		padding: 16px;
		display: grid;
		gap: 10px;
		scroll-margin-top: 80px;
		min-width: 0;
	}

	header {
		display: flex;
		align-items: center;
		gap: 10px;
		flex-wrap: wrap;
	}

	.path {
		font-size: 0.9375rem;
		font-weight: 500;
	}

	.ttl {
		margin-left: auto;
		font-family: var(--font-mono);
		font-size: 0.75rem;
		color: var(--muted);
	}

	.need {
		font-size: 0.8125rem;
		color: var(--muted);
		white-space: nowrap;
	}

	.actions {
		display: flex;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
	}

	.example {
		font-size: 0.75rem;
		color: var(--muted);
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		min-width: 0;
	}

	.problem {
		color: var(--quake);
	}
</style>
