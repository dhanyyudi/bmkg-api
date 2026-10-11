<script lang="ts">
	import CodeBlock from '#lib/components/CodeBlock.svelte';
	import Tabs from '#lib/components/Tabs.svelte';
	import { MCP_CLIENTS, MCP_TOOLS } from '#lib/snippets';
	import { MCP_URL } from '#lib/api';

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

	const ERRORS = [
		['INVALID_ARGUMENT', 'The API rejected an argument'],
		['NOT_FOUND', 'No data for that input, for example a code BMKG has no forecast for'],
		['RATE_LIMITED', 'Too many requests; wait a minute'],
		['UPSTREAM_UNAVAILABLE', 'BMKG or the API is temporarily unreachable'],
		['INTERNAL_ERROR', 'Anything else; quote meta.trace_id when reporting it']
	];
</script>

<svelte:head>
	<title>MCP setup · BMKG API</title>
	<meta name="description" content="Connect Claude, Cursor, VS Code and other MCP clients to live Indonesian weather and earthquake data from BMKG." />
</svelte:head>

<div class="wrap">
	<header class="page-head">
		<p class="eyebrow">Model Context Protocol</p>
		<h1>Connect an AI assistant to BMKG data.</h1>
		<p>
			Thirteen read-only tools for weather forecasts, earthquakes, severe weather warnings and
			region lookup. The server is hosted, so most clients need only a URL.
		</p>
	</header>

	<div class="page-body prose">
		<h2 id="connect">Connect</h2>
		<p>The hosted endpoint speaks Streamable HTTP and needs no API key: <code>{MCP_URL}</code></p>
		<Tabs items={MCP_CLIENTS} label="MCP client">
			{#snippet children(client)}
				<p class="note">{client.note}</p>
				<CodeBlock code={client.code} lang={client.lang} title={client.label} />
			{/snippet}
		</Tabs>

		<h3>Using your own API instance</h3>
		<p>
			The local server reads from this public demo by default. Point it at a
			<a href="/self-host/">self-hosted</a> instance with an environment variable:
		</p>
		<CodeBlock code={ownInstance} lang="json" title="MCP client config" />

		<h2 id="tools">Tools</h2>
		<p>
			Weather tools need a village-level <code>adm4_code</code> such as <code>31.74.04.1006</code>.
			Get one from <code>search_regions</code>, or walk provinces → districts → subdistricts →
			villages.
		</p>
		<div class="table-scroll">
			<table class="table">
				<thead><tr><th>Tool</th><th>Arguments</th><th>Returns</th></tr></thead>
				<tbody>
					{#each MCP_TOOLS as tool (tool.name)}
						<tr>
							<td><code>{tool.name}</code></td>
							<td class="mono">{tool.args || '—'}</td>
							<td>{tool.returns}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
		<p>
			The server also offers seven prompts: earthquake, weather, region lookup, emergency
			preparedness, travel, research and daily briefing.
		</p>

		<h2 id="response">Response format</h2>
		<p>Every tool returns the same envelope. Check <code>status</code> first.</p>
		<CodeBlock code={envelope} lang="json" title="Tool result" />
		<p>
			On failure, <code>status</code> is <code>"error"</code>, <code>data</code> is
			<code>null</code> and <code>error.code</code> is one of:
		</p>
		<div class="table-scroll">
			<table class="table">
				<thead><tr><th>Code</th><th>Meaning</th></tr></thead>
				<tbody>
					{#each ERRORS as [code, meaning] (code)}
						<tr><td><code>{code}</code></td><td>{meaning}</td></tr>
					{/each}
				</tbody>
			</table>
		</div>
		<p>
			Arguments that do not match a tool's schema, such as a malformed code or a latitude out of
			range, are rejected by the protocol before the tool runs.
		</p>

		<h2 id="upgrading">Upgrading from 1.x</h2>
		<ul>
			<li>Results are wrapped in the envelope above. What used to be the whole result is now under <code>data</code>.</li>
			<li>Failures used to be <code>{'{"error": "<text>"}'}</code>. They are now <code>status: "error"</code> with a code.</li>
			<li>The <code>debug_ping</code> and <code>get_cache_stats</code> tools were removed.</li>
			<li><code>search_regions</code> returns 20 results by default; pass <code>limit</code> for more.</li>
		</ul>
	</div>
</div>

<style>
	.note {
		font-size: 0.9375rem;
		color: var(--muted);
		margin-bottom: 10px;
	}
</style>
