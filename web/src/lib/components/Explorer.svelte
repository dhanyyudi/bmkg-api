<script lang="ts">
	import { onMount } from 'svelte';
	import CodeBlock from './CodeBlock.svelte';
	import RegionPicker from './RegionPicker.svelte';
	import QuakeView from './views/QuakeView.svelte';
	import ForecastView from './views/ForecastView.svelte';
	import WarningView from './views/WarningView.svelte';
	import RegionView from './views/RegionView.svelte';
	import { ENDPOINTS, GROUPS, endpointById } from '#lib/endpoints';
	import { explorer, openInExplorer } from '#lib/explorer.svelte';
	import {
		PUBLIC_ORIGIN,
		getData,
		request,
		timeAgo,
		parseTime,
		type ActiveWarning,
		type ApiResult,
		type Envelope
	} from '#lib/api';

	type Tab = 'preview' | 'json' | 'headers';

	let result = $state<ApiResult | null>(null);
	let resultEndpoint = $state('');
	let loading = $state(false);
	let networkError = $state('');
	let tab = $state<Tab>('preview');
	let alerts = $state<ActiveWarning[] | null>(null);

	const endpoint = $derived(endpointById(explorer.endpoint));
	const path = $derived(endpoint.path(explorer.params));
	const incomplete = $derived(path.includes('%7B') || path.includes('{'));
	const data = $derived(result?.ok ? (result.body as Envelope<any>).data : null);

	const HEADER_NOTES: Record<string, string> = {
		'cache-control': 'How long this response may be reused',
		'cf-cache-status': 'HIT means Cloudflare answered without reaching the server',
		age: 'Seconds this copy has spent in a cache',
		'x-cache': "The server's own cache: HIT or MISS",
		'x-cache-ttl': "Seconds until the server asks BMKG again",
		'x-ratelimit-limit': 'Requests allowed per minute',
		'x-ratelimit-remaining': 'Requests left in the current minute',
		'content-type': 'Format of the body'
	};
	const shownHeaders = $derived(
		result ? Object.keys(HEADER_NOTES).filter((name) => name in result!.headers) : []
	);

	async function loadAlerts() {
		alerts = (await getData<ActiveWarning[]>('/v1/nowcast')) ?? [];
		if (!explorer.params.alertCode && alerts.length) explorer.params.alertCode = alerts[0].code;
	}

	let latestRun = 0;

	async function run() {
		// Requests can overlap (the first one on load, then a link from elsewhere
		// on the page). Only the newest may write its result, and a result is
		// always shown with the endpoint that produced it.
		const ticket = ++latestRun;
		const requested = endpoint;

		if (requested.params.some((p) => p.kind === 'alert') && alerts === null) await loadAlerts();
		const target = requested.path(explorer.params);
		if (target.includes('{') || target.includes('%7B')) return;

		loading = true;
		networkError = '';
		try {
			const response = await request(target);
			if (ticket !== latestRun) return;
			result = response;
			resultEndpoint = requested.id;
			tab = 'preview';
		} catch {
			if (ticket !== latestRun) return;
			result = null;
			networkError = 'The request could not be sent. Check your connection and try again.';
		}
		loading = false;
	}

	function select(id: string) {
		explorer.endpoint = id;
		latestRun++; // a response still on its way belongs to the previous endpoint
		loading = false;
		result = null;
		networkError = '';
		if (endpointById(id).params.some((p) => p.kind === 'alert') && alerts === null) loadAlerts();
	}

	let seenRun = 0;
	$effect(() => {
		// Other parts of the page ask for a run by bumping the counter.
		if (explorer.runRequest !== seenRun) {
			seenRun = explorer.runRequest;
			run();
		}
	});

	onMount(() => {
		run();
	});
</script>

<div class="explorer card">
	<div class="side">
		{#each GROUPS as group (group)}
			<div class="group">
				<p class="eyebrow">{group}</p>
				{#each ENDPOINTS.filter((e) => e.group === group) as item (item.id)}
					<button type="button" class="endpoint" class:on={item.id === endpoint.id} onclick={() => select(item.id)}>
						<span class="mono path">{item.template.replace('/v1', '')}</span>
						<span class="summary">{item.summary}</span>
					</button>
				{/each}
			</div>
		{/each}
	</div>

	<div class="main">
		<form
			class="request"
			onsubmit={(event) => {
				event.preventDefault();
				run();
			}}
		>
			{#if endpoint.params.length}
				<div class="params">
					{#each endpoint.params as param (param.name)}
						<label for="p-{param.name}">
							<span>{param.label}</span>
							{#if param.kind === 'region'}
								<RegionPicker id="p-{param.name}" bind:value={explorer.params[param.name]} />
							{:else if param.kind === 'language'}
								<select id="p-{param.name}" bind:value={explorer.params[param.name]}>
									<option value="id">Indonesian</option>
									<option value="en">English</option>
								</select>
							{:else if param.kind === 'alert'}
								<select id="p-{param.name}" bind:value={explorer.params[param.name]} disabled={!alerts?.length}>
									{#if alerts === null}
										<option value="">Loading active warnings…</option>
									{:else if alerts.length === 0}
										<option value="">No active warning right now</option>
									{:else}
										{#each alerts as alert (alert.code)}
											<option value={alert.code}>{alert.province} · {timeAgo(parseTime(alert.published_at))}</option>
										{/each}
									{/if}
								</select>
							{:else}
								<input
									id="p-{param.name}"
									type="text"
									inputmode={param.kind === 'number' ? 'decimal' : 'text'}
									placeholder={param.placeholder}
									bind:value={explorer.params[param.name]}
								/>
							{/if}
							{#if param.hint}<small>{param.hint}</small>{/if}
						</label>
					{/each}
				</div>
			{/if}

			<div class="line">
				<span class="method">GET</span>
				<code class="url">{decodeURIComponent(path)}</code>
				<button type="submit" class="btn primary small" disabled={loading || incomplete}>
					{loading ? 'Running…' : 'Run'}
				</button>
			</div>
		</form>

		<div class="response" aria-live="polite" aria-busy={loading}>
			{#if networkError}
				<p class="problem">{networkError}</p>
			{:else if !result}
				<p class="hint">{incomplete ? 'Fill in the parameter above, then run the request.' : 'Run the request to see the response.'}</p>
			{:else}
				<div class="bar">
					<div class="tabs" role="tablist">
						{#each ['preview', 'json', 'headers'] as const as name (name)}
							<button type="button" role="tab" aria-selected={tab === name} class:on={tab === name} onclick={() => (tab = name)}>
								{name === 'json' ? 'JSON' : name[0].toUpperCase() + name.slice(1)}
							</button>
						{/each}
					</div>
					<p class="stat mono">
						<span class="code" class:bad={!result.ok}>{result.status}</span>
						{result.ms} ms
						{#if result.headers['cf-cache-status']}· edge {result.headers['cf-cache-status']}{/if}
					</p>
				</div>

				{#if tab === 'json'}
					<CodeBlock code={JSON.stringify(result.body, null, 2)} lang="json" title="Response body" maxHeight="460px" />
				{:else if tab === 'headers'}
					<table class="headers">
						<tbody>
							{#each shownHeaders as name (name)}
								<tr>
									<th class="mono">{name}</th>
									<td class="mono">{result.headers[name]}</td>
									<td class="note">{HEADER_NOTES[name]}</td>
								</tr>
							{/each}
						</tbody>
					</table>
					<CodeBlock code={`curl -i "${PUBLIC_ORIGIN}${result.path}"`} lang="bash" title="Reproduce with curl" />
				{:else}
				<svelte:boundary>
				{#if !result.ok}
					{@const body = result.body as { message?: string; detail?: unknown } | null}
					<p class="problem">
						<strong>{result.status}</strong>
						{body?.message ?? (body?.detail ? 'The request was rejected as invalid.' : 'The request failed.')}
					</p>
				{:else if resultEndpoint === 'earthquake-latest'}
					<QuakeView quakes={[data]} />
				{:else if resultEndpoint.startsWith('earthquake')}
					<QuakeView
						quakes={data}
						center={resultEndpoint === 'earthquake-nearby'
							? [Number(explorer.params.lat), Number(explorer.params.lon)]
							: undefined}
					/>
				{:else if resultEndpoint === 'weather'}
					<ForecastView location={data.location} days={data.forecast} />
				{:else if resultEndpoint === 'weather-current'}
					<ForecastView location={data.location} current={data.current} />
				{:else if resultEndpoint === 'nowcast'}
					{#if data.length === 0}
						<p class="hint">No province has an active warning right now.</p>
					{:else}
						<ul class="alerts">
							{#each data as alert (alert.code)}
								<li>
									<div>
										<strong>{alert.province}</strong>
										<span class="when">{timeAgo(parseTime(alert.published_at))}</span>
										<p>{alert.description}</p>
									</div>
									<button type="button" class="btn small" onclick={() => openInExplorer('nowcast-detail', { alertCode: alert.code })}>
										Map →
									</button>
								</li>
							{/each}
						</ul>
					{/if}
				{:else if resultEndpoint === 'nowcast-detail'}
					<WarningView warnings={data.warnings} />
				{:else if resultEndpoint === 'nowcast-check'}
					<WarningView
						warnings={data.warnings}
						emptyText={`No active warning mentions "${data.location}". That is not a forecast of good weather.`}
					/>
				{:else}
					<RegionView regions={data} onopen={openInExplorer} />
				{/if}
				{#snippet failed()}
					<p class="problem">
						This response could not be previewed. The JSON tab shows exactly what the API returned.
					</p>
				{/snippet}
				</svelte:boundary>
				{/if}
			{/if}
		</div>
	</div>
</div>

<style>
	.explorer {
		display: grid;
		grid-template-columns: 270px minmax(0, 1fr);
		overflow: hidden;
		box-shadow: var(--shadow);
	}

	.side {
		padding: 16px 10px;
		border-right: 1px solid var(--line);
		background: var(--surface-2);
		display: grid;
		gap: 16px;
		align-content: start;
	}

	.group {
		display: grid;
		gap: 2px;
	}

	.group .eyebrow {
		padding: 0 8px 4px;
	}

	.endpoint {
		display: grid;
		gap: 1px;
		padding: 6px 8px;
		border: 0;
		border-radius: 6px;
		background: none;
		text-align: left;
	}

	.endpoint:hover {
		background: color-mix(in srgb, var(--surface) 70%, transparent);
	}

	.endpoint.on {
		background: var(--surface);
		box-shadow: inset 2px 0 0 var(--accent);
	}

	.path {
		font-size: 0.8125rem;
	}

	.summary {
		font-size: 0.75rem;
		color: var(--muted);
	}

	.main {
		padding: 16px;
		display: grid;
		gap: 16px;
		align-content: start;
		min-width: 0;
	}

	.request {
		display: grid;
		gap: 12px;
	}

	.params {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
		gap: 12px;
	}

	label {
		display: grid;
		gap: 4px;
		font-size: 0.8125rem;
		color: var(--muted);
	}

	label :global(input),
	select {
		min-height: 38px;
		padding: 0 10px;
		border: 1px solid var(--line);
		border-radius: 8px;
		background: var(--surface);
		color: var(--ink);
		font-size: 0.9375rem;
		width: 100%;
	}

	small {
		font-size: 0.75rem;
	}

	.line {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 8px 8px 8px 12px;
		border-radius: 8px;
		background: var(--code-bg);
		color: var(--code-ink);
		min-width: 0;
	}

	.url {
		flex: 1;
		overflow-x: auto;
		white-space: nowrap;
	}

	.line .btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.response {
		min-height: 260px;
		display: grid;
		gap: 12px;
		align-content: start;
		min-width: 0;
	}

	.bar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 12px;
		flex-wrap: wrap;
		border-bottom: 1px solid var(--line);
	}

	.tabs {
		display: flex;
		gap: 2px;
	}

	.tabs button {
		padding: 8px 12px;
		border: 0;
		border-bottom: 2px solid transparent;
		background: none;
		color: var(--muted);
		font-size: 0.875rem;
		margin-bottom: -1px;
	}

	.tabs button.on {
		color: var(--ink);
		border-color: var(--accent);
	}

	.stat {
		font-size: 0.75rem;
		color: var(--muted);
	}

	.code {
		padding: 1px 6px;
		border-radius: 4px;
		background: var(--accent-soft);
		color: var(--accent);
		margin-right: 4px;
	}

	.code.bad {
		background: color-mix(in srgb, var(--quake) 15%, transparent);
		color: var(--quake);
	}

	.hint {
		color: var(--muted);
	}

	.problem {
		padding: 12px 14px;
		border-radius: 8px;
		background: color-mix(in srgb, var(--quake) 10%, transparent);
		color: var(--ink);
	}

	.headers {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.8125rem;
	}

	.headers th,
	.headers td {
		text-align: left;
		padding: 6px 8px;
		border-bottom: 1px solid var(--line);
		font-weight: 400;
		vertical-align: top;
	}

	.headers th {
		color: var(--accent);
		white-space: nowrap;
	}

	.note {
		color: var(--muted);
	}

	.alerts {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		max-height: 440px;
		overflow: auto;
	}

	.alerts li {
		display: flex;
		align-items: start;
		justify-content: space-between;
		gap: 12px;
		padding: 10px 2px;
		border-bottom: 1px solid var(--line);
		font-size: 0.875rem;
	}

	.alerts p {
		color: var(--muted);
		margin-top: 2px;
	}

	.when {
		font-size: 0.75rem;
		color: var(--muted);
		margin-left: 6px;
	}

	@media (max-width: 860px) {
		.explorer {
			grid-template-columns: minmax(0, 1fr);
		}

		.side {
			border-right: 0;
			border-bottom: 1px solid var(--line);
			grid-auto-flow: column;
			grid-auto-columns: 220px;
			overflow-x: auto;
		}
	}
</style>
