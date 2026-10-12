<script lang="ts">
	import CodeBlock from '#lib/components/CodeBlock.svelte';
	import Tabs from '#lib/components/Tabs.svelte';
	import { MCP_CLIENTS, MCP_TOOLS } from '#lib/snippets';
	import { MCP_URL } from '#lib/api';
	import { useMessages } from '#lib/i18n';

	const i18n = useMessages();

	const clients = $derived(
		MCP_CLIENTS.map((client) => ({
			...client,
			label: client.label || i18n.m.mcp.clientLabels[client.id as 'stdio' | 'local']
		}))
	);

	const envelope = `{
  "status": "success",
  "data": { "magnitude": 5.4, "region": "18 km TimurLaut Pekalongan" },
  "error": null,
  "meta": {
    "tool_version": "2.0.0",
    "operation": "get_latest_earthquake",
    "trace_id": "4b1f0c7e9d2a4f6c8e3b5a7d9c1e2f30",
    "latency_ms": 84.2,
    "source": "BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)",
    "fetched_at": "2026-02-16T08:30:00Z",
    "cache_ttl_seconds": 60,
    "served_from_cache": false,
    "details": {},
    "warnings": []
  }
}`;

	const ownInstance = `{
  "mcpServers": {
    "bmkg": {
      "command": "uvx",
      "args": ["bmkg-api-mcp"],
      "env": { "BMKG_API_BASE_URL": "http://localhost:8099/v1" }
    }
  }
}`;
</script>

<svelte:head>
	<title>{i18n.m.mcp.title}</title>
	<meta name="description" content={i18n.m.mcp.description} />
</svelte:head>

<div class="sheet">
	<header class="page-head">
		<h1>{i18n.m.mcp.h1}</h1>
		<p>{i18n.m.mcp.lead}</p>
	</header>

	<div class="page-body prose">
		<h2 id="connect">{i18n.m.mcp.connect}</h2>
		<p>{i18n.m.mcp.connectNote} <code>{MCP_URL}</code></p>
		<Tabs items={clients} label={i18n.m.home.mcpClient}>
			{#snippet children(client)}
				<p class="note">{i18n.m.mcp.clients[client.id]}</p>
				<CodeBlock code={client.code} lang={client.lang} title={client.label} />
			{/snippet}
		</Tabs>

		<h3>{i18n.m.mcp.ownInstance}</h3>
		<p>{i18n.m.mcp.ownInstanceNote}</p>
		<CodeBlock code={ownInstance} lang="json" title={i18n.m.mcp.clientConfig} />

		<h2 id="tools">{i18n.m.mcp.tools}</h2>
		<p>{i18n.m.mcp.toolsNote}</p>
		<div class="table-scroll">
			<table class="table">
				<thead>
					<tr><th>{i18n.m.mcp.colTool}</th><th>{i18n.m.mcp.colArgs}</th><th>{i18n.m.mcp.colReturns}</th></tr>
				</thead>
				<tbody>
					{#each MCP_TOOLS as tool (tool.name)}
						<tr>
							<td><code>{tool.name}</code></td>
							<td class="mono">{tool.args || i18n.m.common.none}</td>
							<td>{i18n.m.mcp.tools_returns[tool.name as keyof typeof i18n.m.mcp.tools_returns]}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
		<p>{i18n.m.mcp.prompts}</p>

		<h2 id="response">{i18n.m.mcp.response}</h2>
		<p>{i18n.m.mcp.responseNote}</p>
		<CodeBlock code={envelope} lang="json" title={i18n.m.mcp.toolResult} />
		<p>{i18n.m.mcp.errorsNote}</p>
		<div class="table-scroll">
			<table class="table">
				<thead><tr><th>{i18n.m.mcp.colCode}</th><th>{i18n.m.docs.meaning}</th></tr></thead>
				<tbody>
					{#each i18n.m.mcp.errors as [code, meaning] (code)}
						<tr><td><code>{code}</code></td><td>{meaning}</td></tr>
					{/each}
				</tbody>
			</table>
		</div>
		<p>{i18n.m.mcp.schemaNote}</p>

		<h2 id="upgrading">{i18n.m.mcp.upgrading}</h2>
		<ul>
			{#each i18n.m.mcp.upgradingItems as item (item)}
				<li>{item}</li>
			{/each}
		</ul>
	</div>
</div>

<style>
	.note {
		font-size: 0.9375rem;
		color: var(--ink-2);
		margin-bottom: 10px;
	}
</style>
