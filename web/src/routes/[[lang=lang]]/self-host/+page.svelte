<script lang="ts">
	import CodeBlock from '#lib/components/CodeBlock.svelte';
	import { REPO_URL } from '#lib/api';
	import { href, useMessages, type Messages } from '#lib/i18n';

	const i18n = useMessages();

	const docker = `docker run -d --name bmkg-api -p 8099:8099 ghcr.io/dhanyyudi/bmkg-api:latest

curl http://localhost:8099/health`;

	const compose = `git clone ${REPO_URL}.git
cd bmkg-api
cp .env.example .env
docker compose up -d`;

	const local = $derived(`git clone ${REPO_URL}.git
cd bmkg-api
make setup
source venv/bin/activate
make dev        ${i18n.m.selfHost.comments.dev}

${i18n.m.selfHost.comments.website}
make web`);

	const DEFAULTS: [keyof Messages['selfHost']['settings'], string][] = [
		['REDIS_URL', 'redis://localhost:6379'],
		['RATE_LIMIT_ANONYMOUS', '30/minute'],
		['CLIENT_IP_HEADER', ''],
		['UPSTREAM_MAX_PER_MINUTE', '50'],
		['CACHE_TTL_EARTHQUAKE_LATEST', '60'],
		['CACHE_TTL_EARTHQUAKE_LIST', '300'],
		['CACHE_TTL_NOWCAST', '120'],
		['CACHE_TTL_WEATHER', '900'],
		['CACHE_TTL_WILAYAH', '86400']
	];
</script>

<svelte:head>
	<title>{i18n.m.selfHost.title}</title>
	<meta name="description" content={i18n.m.selfHost.description} />
</svelte:head>

<div class="sheet">
	<header class="page-head">
		<h1>{i18n.m.selfHost.h1}</h1>
		<p>{i18n.m.selfHost.lead}</p>
	</header>

	<div class="page-body prose">
		<h2 id="docker">{i18n.m.selfHost.docker}</h2>
		<p>{i18n.m.selfHost.dockerNote}</p>
		<CodeBlock code={docker} lang="bash" title={i18n.m.selfHost.runImage} />

		<h2 id="compose">{i18n.m.selfHost.compose}</h2>
		<p>{i18n.m.selfHost.composeNote}</p>
		<CodeBlock code={compose} lang="bash" title={i18n.m.selfHost.cloneStart} />

		<h2 id="local">{i18n.m.selfHost.local}</h2>
		<p>{i18n.m.selfHost.localNote}</p>
		<CodeBlock code={local} lang="bash" title={i18n.m.selfHost.fromSource} />

		<h2 id="configuration">{i18n.m.selfHost.config}</h2>
		<p>{i18n.m.selfHost.configNote}</p>
		<div class="table-scroll">
			<table class="table">
				<thead>
					<tr>
						<th>{i18n.m.selfHost.colVariable}</th>
						<th>{i18n.m.selfHost.colDefault}</th>
						<th>{i18n.m.selfHost.colPurpose}</th>
					</tr>
				</thead>
				<tbody>
					{#each DEFAULTS as [name, fallback] (name)}
						<tr>
							<td><code>{name}</code></td>
							<td class="mono">{fallback || i18n.m.selfHost.empty}</td>
							<td>{i18n.m.selfHost.settings[name]}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>

		<h2 id="public">{i18n.m.selfHost.public}</h2>
		<p>{i18n.m.selfHost.publicNote}</p>
		<ul>
			{#each i18n.m.selfHost.publicItems as [lead, rest] (lead)}
				<li><strong>{lead}</strong> {rest}</li>
			{/each}
		</ul>

		<h2 id="mcp">{i18n.m.selfHost.mcp}</h2>
		<p>{i18n.m.selfHost.mcpNote}</p>
		<p><a href={href(i18n.locale, '/mcp-setup/')}>{i18n.m.selfHost.mcpLink}</a></p>
	</div>
</div>
