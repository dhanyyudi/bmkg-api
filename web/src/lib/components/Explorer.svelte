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
		type ActiveWarning,
		type ActiveWarningFull,
		type ApiResult,
		type Envelope
	} from '#lib/api';
	import { parseTime, timeAgo } from '#lib/format';
	import { fill, useMessages } from '#lib/i18n';
	import { CODE_LANGUAGES, codeFor } from '#lib/snippets';

	type Tab = 'preview' | 'json' | 'headers' | 'code';
	const TABS: Tab[] = ['preview', 'json', 'headers', 'code'];

	const i18n = useMessages();

	let result = $state<ApiResult | null>(null);
	let resultEndpoint = $state('');
	let loading = $state(false);
	let networkError = $state(false);
	let tab = $state<Tab>('preview');
	let alerts = $state<ActiveWarning[] | null>(null);
	let codeLanguage = $state('curl');

	const endpoint = $derived(endpointById(explorer.endpoint));
	const path = $derived(endpoint.path(explorer.params));
	const incomplete = $derived(path.includes('%7B') || path.includes('{'));
	const data = $derived(result?.ok ? (result.body as Envelope<any>).data : null);

	const shownHeaders = $derived(
		result
			? (Object.keys(i18n.m.explorer.headerNotes) as (keyof typeof i18n.m.explorer.headerNotes)[]).filter(
					(name) => name in result!.headers
				)
			: []
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
		networkError = false;
		try {
			const response = await request(target);
			if (ticket !== latestRun) return;
			result = response;
			resultEndpoint = requested.id;
			if (tab !== 'code') tab = 'preview';
		} catch {
			if (ticket !== latestRun) return;
			result = null;
			networkError = true;
		}
		loading = false;
	}

	function select(id: string) {
		explorer.endpoint = id;
		latestRun++; // a response still on its way belongs to the previous endpoint
		loading = false;
		result = null;
		networkError = false;
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
		// Warning text follows the page language unless it is changed here.
		explorer.params.lang = i18n.m.apiLang;
		run();
	});
</script>

<div class="explorer">
	<div class="main">
		<form
			class="request"
			onsubmit={(event) => {
				event.preventDefault();
				run();
			}}
		>
			<div class="params">
				<label for="p-endpoint" class="pick">
					<span>{i18n.m.explorer.endpoints}</span>
					<select id="p-endpoint" value={endpoint.id} onchange={(event) => select(event.currentTarget.value)}>
						{#each GROUPS as group (group)}
							<optgroup label={i18n.m.groups[group]}>
								{#each ENDPOINTS.filter((e) => e.group === group) as item (item.id)}
									<option value={item.id}>{item.template} · {i18n.m.endpoints[item.id].summary}</option>
								{/each}
							</optgroup>
						{/each}
					</select>
				</label>
				{#each endpoint.params as param (param.name)}
						<label for="p-{param.name}" class:wide={param.kind === 'region'}>
							<span>{i18n.m.params[param.name]}</span>
							{#if param.kind === 'region'}
								<RegionPicker id="p-{param.name}" bind:value={explorer.params[param.name]} />
								<small>{i18n.m.params.adm4Hint}</small>
							{:else if param.kind === 'language'}
								<select id="p-{param.name}" bind:value={explorer.params[param.name]}>
									<option value="id">{i18n.m.params.langId}</option>
									<option value="en">{i18n.m.params.langEn}</option>
								</select>
							{:else if param.kind === 'alert'}
								<select id="p-{param.name}" bind:value={explorer.params[param.name]} disabled={!alerts?.length}>
									{#if alerts === null}
										<option value="">{i18n.m.params.alertsLoading}</option>
									{:else if alerts.length === 0}
										<option value="">{i18n.m.params.alertsNone}</option>
									{:else}
										{#each alerts as alert (alert.code)}
											<option value={alert.code}>
												{alert.province}, {timeAgo(parseTime(alert.published_at), i18n.m)}
											</option>
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
						</label>
					{/each}
			</div>

			<div class="line">
				<span class="method">GET</span>
				<code class="url">{decodeURIComponent(path)}</code>
				<button type="submit" class="btn primary small" disabled={loading || incomplete}>
					{loading ? i18n.m.common.running : i18n.m.common.run}
				</button>
			</div>
		</form>

		<div class="response" aria-live="polite" aria-busy={loading}>
			{#if networkError}
				<p class="problem">{i18n.m.explorer.networkError}</p>
			{:else if !result}
				<p class="hint">
					{loading ? i18n.m.common.running : incomplete ? i18n.m.explorer.fillIn : i18n.m.explorer.runToSee}
				</p>
			{:else}
				<div class="bar">
					<div class="tabs" role="tablist">
						{#each TABS as name (name)}
							<button type="button" role="tab" aria-selected={tab === name} class:on={tab === name} onclick={() => (tab = name)}>
								{i18n.m.explorer[name]}
							</button>
						{/each}
					</div>
					<p class="stat mono">
						<span class:bad={!result.ok}>{result.status}</span> · {result.ms} ms
						{#if result.headers['cf-cache-status']}
							· {fill(i18n.m.explorer.edge, { status: result.headers['cf-cache-status'] })}
						{/if}
					</p>
				</div>

				{#if tab === 'json'}
					<CodeBlock code={JSON.stringify(result.body, null, 2)} lang="json" title={i18n.m.explorer.responseBody} maxHeight="480px" />
				{:else if tab === 'headers'}
					<div class="table-scroll">
						<table class="table">
							<tbody>
								{#each shownHeaders as name (name)}
									<tr>
										<td class="mono">{name}</td>
										<td class="mono">{result.headers[name]}</td>
										<td>{i18n.m.explorer.headerNotes[name]}</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
					<CodeBlock code={`curl -i "${PUBLIC_ORIGIN}${result.path}"`} lang="bash" title={i18n.m.explorer.reproduce} />
				{:else if tab === 'code'}
					<label class="language" for="code-language">
						<span>{i18n.m.explorer.language}</span>
						<select id="code-language" bind:value={codeLanguage}>
							{#each CODE_LANGUAGES as language (language.id)}
								<option value={language.id}>{language.label}</option>
							{/each}
						</select>
					</label>
					<CodeBlock
						code={codeFor(codeLanguage, `${PUBLIC_ORIGIN}${result.path}`)}
						lang={codeLanguage === 'curl' ? 'bash' : 'text'}
						title={CODE_LANGUAGES.find((l) => l.id === codeLanguage)?.label}
					/>
				{:else}
					<svelte:boundary>
						{#if !result.ok}
							{@const body = result.body as { message?: string; detail?: unknown } | null}
							<p class="problem">
								<strong class="mono">{result.status}</strong>
								{body?.message ?? (body?.detail ? i18n.m.explorer.rejected : i18n.m.explorer.failed)}
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
								<p class="hint">{i18n.m.views.noActive}</p>
							{:else}
								<ul class="alerts">
									{#each data as alert (alert.code)}
										<li>
											<div>
												<strong>{alert.province}</strong>
												<span class="when">{timeAgo(parseTime(alert.published_at), i18n.m)}</span>
												<p>{alert.description}</p>
											</div>
											<button type="button" class="btn small" onclick={() => openInExplorer('nowcast-detail', { alertCode: alert.code })}>
												{i18n.m.views.showMap}
											</button>
										</li>
									{/each}
								</ul>
							{/if}
						{:else if resultEndpoint === 'nowcast-warnings'}
							<WarningView
								warnings={data.map((entry: ActiveWarningFull) => entry.warning)}
								emptyText={i18n.m.views.noActive}
							/>
						{:else if resultEndpoint === 'nowcast-detail'}
							<WarningView warnings={data.warnings} />
						{:else if resultEndpoint === 'nowcast-check'}
							<WarningView warnings={data.warnings} emptyText={fill(i18n.m.views.noMention, { place: data.location })} />
						{:else}
							<RegionView regions={data} onopen={openInExplorer} />
						{/if}
						{#snippet failed()}
							<p class="problem">{i18n.m.explorer.previewFailed}</p>
						{/snippet}
					</svelte:boundary>
				{/if}
			{/if}
		</div>
	</div>
</div>

<style>
	/* The endpoint list lives in the table above; here one select picks the
	   request, so the response gets the full width of the sheet. */
	.explorer {
		border: 1px solid var(--ink);
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
		grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
		gap: 12px;
	}

	/* The endpoint and the village search hold long text and get two columns. */
	.pick,
	.wide {
		grid-column: span 2;
	}

	label {
		display: grid;
		gap: 4px;
		align-content: start;
		font-size: 0.875rem;
	}

	label :global(input),
	select {
		min-height: 44px;
		padding: 0 10px;
		border: 1px solid var(--ink);
		background: var(--paper);
		color: var(--ink);
		font-size: 1rem;
		width: 100%;
	}

	small {
		font-size: 0.8125rem;
		color: var(--ink-2);
	}

	.line {
		display: flex;
		align-items: center;
		gap: 10px;
		padding: 4px 4px 4px 12px;
		border: 1px solid var(--ink);
		background: var(--tint);
		min-width: 0;
	}

	.url {
		flex: 1;
		overflow-x: auto;
		white-space: nowrap;
	}

	.line .btn {
		min-height: 44px;
		font-weight: 600;
	}

	.response {
		min-height: 240px;
		display: grid;
		gap: 12px;
		align-content: start;
		min-width: 0;
	}

	.bar {
		display: flex;
		align-items: flex-end;
		justify-content: space-between;
		gap: 4px 12px;
		flex-wrap: wrap;
		border-bottom: 1px solid var(--ink);
	}

	.tabs {
		display: flex;
		flex-wrap: wrap;
	}

	.tabs button {
		min-height: 44px;
		padding: 0 14px;
		border: 1px solid transparent;
		border-bottom: 0;
		background: none;
		color: var(--ink-2);
		margin-bottom: -1px;
	}

	.tabs button.on {
		border-color: var(--ink);
		background: var(--paper);
		color: var(--ink);
		font-weight: 600;
	}

	.stat {
		font-size: 0.8125rem;
		color: var(--ink-2);
		padding-bottom: 8px;
	}

	.stat .bad {
		color: var(--alert);
	}

	.hint {
		color: var(--ink-2);
	}

	.problem {
		padding: 10px 12px;
		border: 1px solid var(--alert);
		color: var(--alert);
	}

	.language {
		max-width: 260px;
	}

	.alerts {
		list-style: none;
		margin: 0;
		padding: 0;
		max-height: 460px;
		overflow: auto;
	}

	.alerts li {
		display: flex;
		align-items: start;
		justify-content: space-between;
		gap: 12px;
		padding: 10px 0;
		border-bottom: 1px solid var(--hair);
		font-size: 0.9375rem;
	}

	.alerts p {
		color: var(--ink-2);
		margin-top: 2px;
	}

	.when {
		font-size: 0.8125rem;
		color: var(--ink-2);
		margin-left: 6px;
	}

	@media (max-width: 560px) {
		.pick,
		.wide {
			grid-column: auto;
		}

		/* Keeps the four tabs on one line. */
		.tabs button {
			padding: 0 10px;
		}
	}
</style>
