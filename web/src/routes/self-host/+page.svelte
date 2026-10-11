<script lang="ts">
	import CodeBlock from '#lib/components/CodeBlock.svelte';
	import { REPO_URL } from '#lib/api';

	const docker = `docker run -d --name bmkg-api -p 8099:8099 ghcr.io/dhanyyudi/bmkg-api:latest

curl http://localhost:8099/health`;

	const compose = `git clone ${REPO_URL}.git
cd bmkg-api
cp .env.example .env
docker compose up -d`;

	const local = `git clone ${REPO_URL}.git
cd bmkg-api
make setup
source venv/bin/activate
make dev        # API on http://localhost:8099

# The website is a separate build, written to ./landing
cd web && npm install && npm run build`;

	const SETTINGS = [
		['REDIS_URL', 'redis://localhost:6379', 'Cache backend. Without Redis the API falls back to an in-process cache.'],
		['RATE_LIMIT_ANONYMOUS', '30/minute', 'Requests allowed per client, per endpoint.'],
		['CLIENT_IP_HEADER', '(empty)', 'Header carrying the real client IP behind a proxy, e.g. CF-Connecting-IP. Leave empty unless every request arrives through that proxy.'],
		['UPSTREAM_MAX_PER_MINUTE', '50', 'Most requests per minute sent to each BMKG host. 0 removes the cap.'],
		['CACHE_TTL_EARTHQUAKE_LATEST', '60', 'Seconds the latest earthquake is cached.'],
		['CACHE_TTL_EARTHQUAKE_LIST', '300', 'Seconds earthquake lists are cached.'],
		['CACHE_TTL_NOWCAST', '120', 'Seconds weather warnings are cached.'],
		['CACHE_TTL_WEATHER', '900', 'Seconds a forecast is cached.'],
		['CACHE_TTL_WILAYAH', '86400', 'Cache lifetime sent for region data.']
	];
</script>

<svelte:head>
	<title>Self-hosting · BMKG API</title>
	<meta name="description" content="Run your own BMKG API instance with Docker: one image, no account, your own rate limits." />
</svelte:head>

<div class="wrap">
	<header class="page-head">
		<p class="eyebrow">Self-hosting</p>
		<h1>Run your own instance.</h1>
		<p>
			The public demo is shared and rate limited. Your own instance has your own limits, and the
			whole API is one container.
		</p>
	</header>

	<div class="page-body prose">
		<h2 id="docker">Docker</h2>
		<p>The image is built for amd64 and arm64 from the main branch, and includes this website.</p>
		<CodeBlock code={docker} lang="bash" title="Run the image" />

		<h2 id="compose">Docker Compose, with Redis</h2>
		<p>
			The repository's <code>docker-compose.yml</code> adds Redis for a cache that survives
			restarts. It attaches to an external network named <code>private_network</code> and exposes
			no host port, which suits a reverse proxy or a tunnel; add a <code>ports</code> entry to
			reach it directly.
		</p>
		<CodeBlock code={compose} lang="bash" title="Clone and start" />

		<h2 id="local">Local development</h2>
		<p>Python 3.12 or newer for the API, Node 22 or newer for the website.</p>
		<CodeBlock code={local} lang="bash" title="From source" />

		<h2 id="configuration">Configuration</h2>
		<p>All settings are environment variables, read from <code>.env</code> when present.</p>
		<div class="table-scroll">
			<table class="table">
				<thead><tr><th>Variable</th><th>Default</th><th>What it does</th></tr></thead>
				<tbody>
					{#each SETTINGS as [name, fallback, note] (name)}
						<tr>
							<td><code>{name}</code></td>
							<td class="mono">{fallback}</td>
							<td>{note}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>

		<h2 id="public">Putting it on the internet</h2>
		<p>A public instance will be hammered sooner or later. Three things keep it standing:</p>
		<ul>
			<li>
				<strong>Cache at the edge.</strong> Every <code>/v1</code> response carries
				<code>Cache-Control</code> matching its data's lifetime. Put a CDN in front and tell it to
				honour that header, and repeat requests never reach your server.
			</li>
			<li>
				<strong>Rate limit by the real client.</strong> Behind a proxy, set
				<code>CLIENT_IP_HEADER</code>, or every visitor is counted as the proxy.
			</li>
			<li>
				<strong>Keep the upstream cap.</strong> <code>UPSTREAM_MAX_PER_MINUTE</code> stops abuse
				of your instance from getting your server's IP blocked by BMKG.
			</li>
		</ul>

		<h2 id="mcp">The MCP server</h2>
		<p>
			The same image runs the MCP endpoint: start a second container with the command
			<code>python -m mcp_server.http_server</code> and set <code>BMKG_API_BASE_URL</code> to your
			API. See the <a href="/mcp-setup/">MCP setup guide</a>.
		</p>
	</div>
</div>
