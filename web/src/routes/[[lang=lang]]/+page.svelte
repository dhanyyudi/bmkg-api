<script lang="ts">
	import { onMount } from 'svelte';
	import HomeSheet from '#lib/components/HomeSheet.svelte';
	import Explorer from '#lib/components/Explorer.svelte';
	import CopyButton from '#lib/components/CopyButton.svelte';
	import CodeBlock from '#lib/components/CodeBlock.svelte';
	import Tabs from '#lib/components/Tabs.svelte';
	import { ENDPOINTS, GROUPS, cacheTime } from '#lib/endpoints';
	import { openInExplorer } from '#lib/explorer.svelte';
	import { MCP_CLIENTS, MCP_PROMPTS } from '#lib/snippets';
	import { PUBLIC_ORIGIN, REPO_URL } from '#lib/api';
	import { href, useMessages } from '#lib/i18n';

	const i18n = useMessages();
	const curl = `curl ${PUBLIC_ORIGIN}/v1/earthquake/latest`;

	const clients = $derived(
		MCP_CLIENTS.map((client) => ({
			...client,
			label: client.label || i18n.m.mcp.clientLabels[client.id as 'stdio' | 'local']
		}))
	);

	onMount(() => {
		// Links from the docs open a specific endpoint: /?endpoint=weather#explorer
		const wanted = new URLSearchParams(location.search).get('endpoint');
		if (wanted && ENDPOINTS.some((e) => e.id === wanted)) openInExplorer(wanted, {}, 'instant');
	});
</script>

<svelte:head>
	<title>{i18n.m.home.title}</title>
	<meta name="description" content={i18n.m.home.description} />
</svelte:head>

<div class="sheet">
	<section class="title">
		<h1>{i18n.m.home.h1}</h1>
		<div class="intro">
			<p>{i18n.m.home.lead}</p>
			<div class="curl">
				<code>{curl}</code>
				<CopyButton text={curl} />
			</div>
			<p class="actions">
				<a class="btn primary" href="#explorer">{i18n.m.home.openExplorer}</a>
				<a class="btn" href={href(i18n.locale, '/docs/')}>{i18n.m.home.readDocs}</a>
			</p>
		</div>
	</section>

	<section class="map" aria-label={i18n.m.map.plateTitle}>
		<HomeSheet onexplore={openInExplorer} />
	</section>

	<section class="block">
		<header>
			<h2>{i18n.m.home.indexTitle}</h2>
			<p>{i18n.m.home.indexNote}</p>
		</header>
		<div class="table-scroll">
			<!-- Roles are spelled out because the narrow layout lays rows out as
			     grids, which would otherwise drop the table semantics. -->
			<!-- svelte-ignore a11y_no_redundant_roles -->
			<table class="table index" role="table">
				<thead role="rowgroup">
					<tr role="row">
						<th role="columnheader">{i18n.m.home.colEndpoint}</th>
						<th role="columnheader">{i18n.m.home.colReturns}</th>
						<th role="columnheader">{i18n.m.home.colCache}</th>
						<th role="columnheader"><span class="sr-only">{i18n.m.common.tryIt}</span></th>
					</tr>
				</thead>
				{#each GROUPS as group (group)}
					<tbody role="rowgroup">
						<tr class="group" role="row"><th colspan="4" scope="rowgroup" role="rowheader">{i18n.m.groups[group]}</th></tr>
						{#each ENDPOINTS.filter((e) => e.group === group) as endpoint (endpoint.id)}
							<tr role="row">
								<td class="mono path" role="cell">{endpoint.template}</td>
								<td class="what" role="cell">{i18n.m.endpoints[endpoint.id].summary}</td>
								<td class="mono ttl" role="cell" data-label={i18n.m.home.colCache}>{cacheTime(endpoint.ttl, i18n.m)}</td>
								<td class="act" role="cell">
									<button type="button" class="btn small" onclick={() => openInExplorer(endpoint.id)}>
										{i18n.m.common.tryIt}<span class="sr-only"> {endpoint.template}</span>
									</button>
								</td>
							</tr>
						{/each}
					</tbody>
				{/each}
			</table>
		</div>
	</section>

	<section class="block" id="explorer">
		<header>
			<h2>{i18n.m.home.explorerTitle}</h2>
			<p>{i18n.m.home.explorerNote}</p>
		</header>
		<Explorer />
	</section>

	<section class="block" id="mcp">
		<header>
			<h2>{i18n.m.home.mcpTitle}</h2>
			<p>{i18n.m.home.mcpNote}</p>
			<p><a href={href(i18n.locale, '/mcp-setup/')}>{i18n.m.home.mcpMore}</a></p>
		</header>
		<div class="mcp">
			<Tabs items={clients} label={i18n.m.home.mcpClient}>
				{#snippet children(client)}
					<p class="note">{i18n.m.mcp.clients[client.id]}</p>
					<CodeBlock code={client.code} lang={client.lang} title={client.label} />
				{/snippet}
			</Tabs>
			<div class="prompts">
				<p>{i18n.m.home.mcpPrompts}</p>
				<ul>
					{#each MCP_PROMPTS as prompt (prompt)}
						<li lang="id">{prompt}</li>
					{/each}
				</ul>
			</div>
		</div>
	</section>

	<section class="block">
		<header>
			<h2>{i18n.m.home.sharedTitle}</h2>
		</header>
		<div class="shared">
			<p>{i18n.m.home.sharedNote}</p>
			<p class="actions">
				<a class="btn" href={href(i18n.locale, '/self-host/')}>{i18n.m.home.selfHostGuide}</a>
				<a class="btn" href={REPO_URL} rel="noopener">{i18n.m.home.sourceCode}</a>
			</p>
		</div>
	</section>
</div>

<style>
	/* The sheet title: name on the left, what it covers on the right. */
	.title {
		display: grid;
		grid-template-columns: minmax(0, 5fr) minmax(0, 6fr);
		gap: 20px 48px;
		align-items: end;
		padding: 40px 0 28px;
	}

	h1 {
		font-size: clamp(2.1rem, 4.8vw, 3.5rem);
		font-weight: 700;
		line-height: 1.04;
	}

	.intro {
		display: grid;
		gap: 14px;
	}

	.curl {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 10px;
		padding: 5px 5px 5px 12px;
		border: 1px solid var(--ink);
		background: var(--tint);
		min-width: 0;
	}

	.curl code {
		overflow-x: auto;
		white-space: nowrap;
	}

	.actions {
		display: flex;
		flex-wrap: wrap;
		gap: 10px;
	}

	.index .group th {
		padding-top: 18px;
		border-bottom: 1px solid var(--ink);
	}

	.index tbody:first-of-type .group th {
		padding-top: 8px;
	}

	.index td {
		vertical-align: middle;
	}

	.path {
		white-space: nowrap;
	}

	.ttl {
		white-space: nowrap;
		color: var(--ink-2);
	}

	.act {
		text-align: right;
	}

	.mcp {
		display: grid;
		gap: 24px;
		min-width: 0;
	}

	.note {
		font-size: 0.9375rem;
		color: var(--ink-2);
		margin-bottom: 10px;
	}

	.prompts {
		display: grid;
		gap: 6px;
	}

	.prompts ul {
		margin: 0;
		padding-left: 20px;
		display: grid;
		gap: 2px;
	}

	.shared {
		display: grid;
		gap: 16px;
		max-width: 680px;
	}

	@media (max-width: 860px) {
		.title {
			grid-template-columns: minmax(0, 1fr);
			padding-top: 28px;
		}

		.act .btn {
			min-height: 44px;
		}
	}

	/* Four columns do not fit a phone: each endpoint becomes a short entry,
	   with the path, what it returns and the cache time stacked beside the button. */
	@media (max-width: 720px) {
		.index thead {
			position: absolute;
			width: 1px;
			height: 1px;
			overflow: hidden;
			clip-path: inset(50%);
		}

		.index,
		.index tbody {
			display: block;
		}

		.index tr {
			display: grid;
			grid-template-columns: minmax(0, 1fr) auto;
			gap: 2px 12px;
			align-items: center;
			padding: 10px 0;
			border-bottom: 1px solid var(--hair);
		}

		.index tr.group {
			display: block;
			padding: 0;
			border-bottom: 0;
		}

		.index .group th {
			display: block;
			padding-inline: 0;
		}

		.index td {
			grid-column: 1;
			padding: 0;
			border: 0;
		}

		.index .path {
			white-space: normal;
			overflow-wrap: anywhere;
		}

		.index .ttl::before {
			content: attr(data-label) ' ';
			font-family: var(--font-sans);
		}

		.index .ttl {
			font-size: 0.8125rem;
		}

		.index .act {
			grid-column: 2;
			grid-row: 1 / span 3;
		}
	}
</style>
