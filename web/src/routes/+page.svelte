<script lang="ts">
	import { onMount } from 'svelte';
	import LiveBoard from '#lib/components/LiveBoard.svelte';
	import Seismogram from '#lib/components/Seismogram.svelte';
	import Explorer from '#lib/components/Explorer.svelte';
	import CopyButton from '#lib/components/CopyButton.svelte';
	import CodeBlock from '#lib/components/CodeBlock.svelte';
	import Tabs from '#lib/components/Tabs.svelte';
	import { ENDPOINTS, GROUPS } from '#lib/endpoints';
	import { openInExplorer } from '#lib/explorer.svelte';
	import { CODE_SAMPLES, MCP_CLIENTS } from '#lib/snippets';
	import { PUBLIC_ORIGIN, REPO_URL, type Earthquake } from '#lib/api';

	let quakes = $state<Earthquake[]>([]);

	const curl = `curl ${PUBLIC_ORIGIN}/v1/earthquake/latest`;

	const GROUP_NOTES: Record<(typeof GROUPS)[number], string> = {
		Earthquakes: "From BMKG's seismic network. Refreshed every minute.",
		Weather: '3-day forecasts in 3-hour steps for every village in Indonesia.',
		Warnings: 'Severe weather warnings with the affected areas as polygons.',
		Regions: 'Provinces down to villages, with the codes the forecasts need.'
	};

	const PROMPTS = [
		'Gempa terbaru di Indonesia?',
		'Cuaca 3 hari ke depan di Jakarta Selatan?',
		'Ada peringatan cuaca di Yogyakarta?'
	];

	onMount(() => {
		// Links from the docs open a specific endpoint: /?endpoint=weather#explorer
		const wanted = new URLSearchParams(location.search).get('endpoint');
		if (wanted && ENDPOINTS.some((e) => e.id === wanted)) openInExplorer(wanted);
	});
</script>

<svelte:head>
	<title>BMKG API · Indonesian weather and earthquake data</title>
	<meta
		name="description"
		content="Free REST API and MCP server for Indonesian weather forecasts, earthquakes, severe weather warnings and region lookup, from BMKG open data."
	/>
</svelte:head>

<section class="hero">
	<div class="wrap hero-grid">
		<div class="pitch">
			<p class="eyebrow">Free · No API key · Open source</p>
			<h1>Indonesia's weather and earthquake data, as clean JSON.</h1>
			<p class="lead">
				A REST API and MCP server over BMKG open data: earthquakes, 3-day forecasts for every
				village, severe weather warnings and region lookup.
			</p>

			<div class="curl">
				<code>{curl}</code>
				<CopyButton text={curl} />
			</div>

			<div class="actions">
				<a class="btn primary" href="#explorer">Try it in the explorer</a>
				<a class="btn" href="/docs/">Read the docs</a>
			</div>
		</div>

		<div class="board">
			<LiveBoard onexplore={openInExplorer} bind:quakes />
		</div>
	</div>
	<div class="wrap trace">
		<Seismogram {quakes} />
	</div>
</section>

<section class="section tight" aria-label="What the API covers">
	<div class="wrap groups">
		{#each GROUPS as group (group)}
			<article class="card group">
				<h3>{group}</h3>
				<p>{GROUP_NOTES[group]}</p>
				<ul>
					{#each ENDPOINTS.filter((e) => e.group === group) as endpoint (endpoint.id)}
						<li>
							<button type="button" onclick={() => openInExplorer(endpoint.id)} title="Open in the explorer">
								<span class="mono">{endpoint.template.replace('/v1', '')}</span>
							</button>
						</li>
					{/each}
				</ul>
			</article>
		{/each}
	</div>
</section>

<section class="section" id="explorer">
	<div class="wrap">
		<div class="section-head">
			<p class="eyebrow">API explorer</p>
			<h2>Run real requests, see what comes back.</h2>
			<p>Every endpoint, with a readable preview, the raw JSON and the caching headers.</p>
		</div>
		<Explorer />
	</div>
</section>

<section class="section" id="code">
	<div class="wrap split">
		<div class="section-head">
			<p class="eyebrow">Quick start</p>
			<h2>One GET request. No key, no SDK.</h2>
			<p>
				Responses share one shape: <code>data</code>, <code>meta</code> and
				<code>attribution</code>. Errors are JSON too, with a stable <code>error</code> code.
			</p>
			<p><a href="/docs/">Response format and errors →</a></p>
		</div>
		<Tabs items={CODE_SAMPLES} label="Language">
			{#snippet children(sample)}
				<CodeBlock code={sample.code} lang={sample.id === 'curl' ? 'bash' : 'text'} title={sample.label} />
			{/snippet}
		</Tabs>
	</div>
</section>

<section class="section" id="mcp">
	<div class="wrap split">
		<div class="section-head">
			<p class="eyebrow">For AI assistants</p>
			<h2>Ask in plain language through MCP.</h2>
			<p>
				The same data as 13 read-only tools for Claude, Cursor, VS Code and any other MCP client.
				Hosted, so there is nothing to install.
			</p>
			<ul class="prompts">
				{#each PROMPTS as prompt (prompt)}
					<li>“{prompt}”</li>
				{/each}
			</ul>
			<p><a href="/mcp-setup/">Tools, response format and every client →</a></p>
		</div>
		<Tabs items={MCP_CLIENTS} label="MCP client">
			{#snippet children(client)}
				<p class="client-note">{client.note}</p>
				<CodeBlock code={client.code} lang={client.lang} title={client.label} />
			{/snippet}
		</Tabs>
	</div>
</section>

<section class="section">
	<div class="wrap">
		<div class="card notice">
			<div>
				<h2>This is a shared demo instance.</h2>
				<p>
					It is rate limited to 30 requests per minute per endpoint and cached at the edge so it
					stays up for everyone. For production traffic, run your own: one Docker image, no
					account needed.
				</p>
			</div>
			<div class="actions">
				<a class="btn primary" href="/self-host/">Self-host guide</a>
				<a class="btn" href={REPO_URL} rel="noopener">Source on GitHub</a>
			</div>
		</div>
	</div>
</section>

<style>
	.hero {
		padding: 56px 0 24px;
	}

	.hero-grid {
		display: grid;
		grid-template-columns: minmax(0, 5fr) minmax(0, 6fr);
		gap: 48px;
		align-items: center;
	}

	.pitch {
		display: grid;
		gap: 20px;
	}

	/* The banner assembles itself: text first, then the live board. */
	.pitch > :global(*),
	.board,
	.trace {
		animation: rise 0.7s cubic-bezier(0.2, 0.7, 0.2, 1) both;
	}

	.pitch > :global(:nth-child(2)) {
		animation-delay: 70ms;
	}

	.pitch > :global(:nth-child(3)) {
		animation-delay: 140ms;
	}

	.pitch > :global(:nth-child(4)) {
		animation-delay: 210ms;
	}

	.pitch > :global(:nth-child(5)) {
		animation-delay: 280ms;
	}

	.board {
		animation-delay: 180ms;
		min-width: 0;
	}

	.trace {
		animation-delay: 420ms;
		margin-top: 36px;
	}

	@keyframes rise {
		from {
			opacity: 0;
			transform: translateY(14px);
		}
	}

	h1 {
		font-size: clamp(2.1rem, 4.6vw, 3.4rem);
		letter-spacing: -0.03em;
	}

	.lead {
		font-size: 1.125rem;
		color: var(--muted);
		max-width: 34em;
	}

	.curl {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 12px;
		padding: 10px 10px 10px 16px;
		border-radius: var(--radius);
		background: var(--code-bg);
		color: var(--code-ink);
		min-width: 0;
	}

	.curl code {
		overflow-x: auto;
		white-space: nowrap;
		font-size: 0.8125rem;
	}

	.actions {
		display: flex;
		flex-wrap: wrap;
		gap: 10px;
	}

	.tight {
		padding: 24px 0 8px;
	}

	.groups {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr));
		gap: 14px;
	}

	.group {
		padding: 18px;
		display: grid;
		gap: 8px;
		align-content: start;
	}

	.group h3 {
		font-size: 1.0625rem;
	}

	.group p {
		color: var(--muted);
		font-size: 0.875rem;
	}

	.group ul {
		list-style: none;
		margin: 6px 0 0;
		padding: 0;
		display: grid;
		gap: 2px;
	}

	.group button {
		width: 100%;
		padding: 4px 6px;
		margin-left: -6px;
		border: 0;
		border-radius: 6px;
		background: none;
		text-align: left;
		color: var(--accent);
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.group button:hover {
		background: var(--accent-soft);
	}

	.split {
		display: grid;
		grid-template-columns: minmax(0, 4fr) minmax(0, 6fr);
		gap: 48px;
		align-items: start;
	}

	.split .section-head {
		margin: 0;
	}

	.prompts {
		list-style: none;
		margin: 4px 0;
		padding: 0;
		display: grid;
		gap: 6px;
	}

	.prompts li {
		padding: 8px 12px;
		border-left: 2px solid var(--accent);
		background: var(--surface);
		font-size: 0.9375rem;
		border-radius: 0 6px 6px 0;
	}

	.client-note {
		font-size: 0.875rem;
		color: var(--muted);
		margin-bottom: 10px;
	}

	.notice {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 24px 40px;
		flex-wrap: wrap;
		padding: 28px;
	}

	.notice > div:first-child {
		display: grid;
		gap: 8px;
		max-width: 620px;
	}

	.notice h2 {
		font-size: 1.375rem;
	}

	.notice p {
		color: var(--muted);
	}

	@media (max-width: 900px) {
		.hero {
			padding-top: 32px;
		}

		.hero-grid,
		.split {
			grid-template-columns: minmax(0, 1fr);
			gap: 28px;
		}

		.groups {
			grid-template-columns: repeat(2, minmax(0, 1fr));
		}
	}

	@media (max-width: 520px) {
		.groups {
			grid-template-columns: minmax(0, 1fr);
		}
	}
</style>
