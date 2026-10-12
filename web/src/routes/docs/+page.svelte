<script lang="ts">
	import CodeBlock from '#lib/components/CodeBlock.svelte';
	import EndpointDoc from '#lib/components/EndpointDoc.svelte';
	import { ENDPOINTS, GROUPS } from '#lib/endpoints';
	import { PUBLIC_ORIGIN } from '#lib/api';

	type Row = [string, string, string];
	const lang: Row = ['lang', 'optional', 'id (default) or en'];

	const REFERENCE: Record<string, { detail: string; params: Row[]; ttl: string }> = {
		'earthquake-latest': {
			detail: 'The single most recent earthquake: magnitude, depth, coordinates, region, tsunami potential, felt reports and a shakemap URL. Times are UTC.',
			params: [],
			ttl: '60 s'
		},
		'earthquake-recent': {
			detail: 'The 15 most recent earthquakes of magnitude 5.0 or higher, newest first.',
			params: [],
			ttl: '5 min'
		},
		'earthquake-felt': {
			detail: 'The 15 most recent earthquakes that people reported feeling, including small ones, with where and how strongly each was felt.',
			params: [],
			ttl: '5 min'
		},
		'earthquake-nearby': {
			detail: "Earthquakes from the recent and felt lists within a radius of a point, nearest first, each with distance_km. An empty list means none among BMKG's latest records, not none ever.",
			params: [
				['lat', 'required', 'Latitude, -90 to 90'],
				['lon', 'required', 'Longitude, -180 to 180'],
				['radius_km', 'optional', 'Search radius in km, default 100']
			],
			ttl: '5 min'
		},
		weather: {
			detail: 'Forecast for one village (kelurahan or desa) for three days in 3-hour steps: temperature, humidity, weather in Indonesian and English, wind and cloud cover. visibility_m can be null.',
			params: [['adm4_code', 'in path', 'Village code as 2.2.2.4 digits, e.g. 31.74.04.1006']],
			ttl: '15 min'
		},
		'weather-current': {
			detail: "The forecast entry closest to now for one village. This is BMKG's forecast for the current 3-hour slot, not a live station reading.",
			params: [['adm4_code', 'in path', 'Village code as 2.2.2.4 digits']],
			ttl: '15 min'
		},
		nowcast: {
			detail: 'Provinces that currently have an active severe weather warning, each with a code for the detail endpoint. An empty list means no active warning.',
			params: [lang],
			ttl: '2 min'
		},
		'nowcast-detail': {
			detail: 'One warning in full: event, severity, urgency, validity period, description, an infographic URL and the affected areas as polygons. Only codes from the active list exist; anything else is a 404.',
			params: [['alert_code', 'in path', 'A code from /v1/nowcast'], lang],
			ttl: '2 min'
		},
		'nowcast-check': {
			detail: 'Active warnings whose text mentions a place name. has_warnings false means no active warning mentions it, which is not a forecast of good weather.',
			params: [['location', 'required', 'Kecamatan, city or regency name as BMKG writes it'], lang],
			ttl: '2 min'
		},
		'wilayah-search': {
			detail: 'Regions whose name contains the query, at every level, with code, level and full path.',
			params: [
				['q', 'required', 'Part of a name, 2 to 100 characters'],
				['limit', 'optional', '1 to 100, default 50']
			],
			ttl: '24 h'
		},
		'wilayah-provinces': {
			detail: 'All 38 provinces with their 2-digit codes.',
			params: [],
			ttl: '24 h'
		},
		'wilayah-districts': {
			detail: 'Kabupaten and kota of one province.',
			params: [['province', 'required', '2-digit province code, e.g. 31']],
			ttl: '24 h'
		},
		'wilayah-subdistricts': {
			detail: 'Kecamatan of one district.',
			params: [['district', 'required', 'District code, e.g. 31.74']],
			ttl: '24 h'
		},
		'wilayah-villages': {
			detail: 'Kelurahan and desa of one subdistrict. Their codes are the adm4 codes the weather endpoints take.',
			params: [['subdistrict', 'required', 'Subdistrict code, e.g. 31.74.04']],
			ttl: '24 h'
		}
	};

	const success = `{
  "data": { "magnitude": 5.4, "region": "18 km TimurLaut Pekalongan" },
  "meta": { "fetched_at": "2026-02-16T08:30:00Z", "cache_ttl": 60 },
  "attribution": "BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)"
}`;

	const failure = `{
  "error": "not_found",
  "message": "Weather data not available for ADM4 code '99.99.99.9999'.",
  "status": 404
}`;

	const rings = `// Each area's polygon is one flat list of [lat, lon] points holding several
// closed rings back to back. A ring ends when a point returns to the ring's
// start, or when the next point is more than 10 km away.
function splitRings(coords) {
  const rings = [];
  let start = coords[0];
  let ring = [coords[0]];

  for (let i = 1; i < coords.length; i++) {
    const point = coords[i];

    if (ring.length >= 4 && distanceKm(ring.at(-1), point) > 10) {
      rings.push([...ring, ring[0]]);
      start = point;
      ring = [point];
      continue;
    }

    ring.push(point);
    if (samePoint(point, start) && ring.length >= 4) {
      rings.push(ring);
      ring = [];
      if (i + 1 < coords.length) {
        start = coords[i + 1];
        ring = [start];
        i++;
      }
    }
  }

  if (ring.length >= 4) rings.push([...ring, ring[0]]);
  return rings;
}

// Drop strip artifacts: real boundaries have short edges, a ring with an
// edge over 20 km joins two distant clusters.
const drawable = splitRings(area.polygon).filter((ring) =>
  ring.every((point, i) => i === 0 || distanceKm(ring[i - 1], point) <= 20)
);`;

	const STATUS: [string, string][] = [
		['200', 'Success'],
		['400', 'An argument has the wrong format'],
		['404', 'No data for that code'],
		['422', 'A required parameter is missing or out of range'],
		['429', 'Rate limit exceeded; wait a minute'],
		['503', 'BMKG is unreachable, or this server reached its request budget towards BMKG; try again shortly']
	];
</script>

<svelte:head>
	<title>Documentation · BMKG API</title>
	<meta name="description" content="Reference for the BMKG API: endpoints, response format, errors, caching and rate limits, with live examples." />
</svelte:head>

<div class="wrap layout">
	<aside aria-label="On this page">
		<nav>
			<a href="#basics">Basics</a>
			<a href="#format">Response format</a>
			<a href="#limits">Caching and limits</a>
			{#each GROUPS as group (group)}
				<a href="#{group.toLowerCase()}">{group}</a>
			{/each}
			<a href="#polygons">Warning polygons</a>
			<a href="/redoc" rel="external">OpenAPI reference ↗</a>
		</nav>
	</aside>

	<div class="content">
		<header class="page-head">
			<p class="eyebrow">Documentation</p>
			<h1>API reference</h1>
			<p>Every endpoint on this page can be run live against the real API.</p>
		</header>

		<div class="prose">
			<h2 id="basics">Basics</h2>
			<ul>
				<li>Base URL: <code>{PUBLIC_ORIGIN}/v1</code></li>
				<li>All endpoints are <code>GET</code> and need no API key.</li>
				<li>CORS is open, so the API can be called from a browser.</li>
				<li>Data belongs to BMKG. Show the <code>attribution</code> value when you publish it.</li>
			</ul>

			<h2 id="format">Response format</h2>
			<p>A successful response always has <code>data</code>, <code>meta</code> and <code>attribution</code>.</p>
			<CodeBlock code={success} lang="json" title="200" />
			<p>A failed one has <code>error</code>, <code>message</code> and <code>status</code>.</p>
			<CodeBlock code={failure} lang="json" title="404" />
			<div class="table-scroll">
				<table class="table">
					<thead><tr><th>Status</th><th>Meaning</th></tr></thead>
					<tbody>
						{#each STATUS as [code, meaning] (code)}
							<tr><td class="mono">{code}</td><td>{meaning}</td></tr>
						{/each}
					</tbody>
				</table>
			</div>

			<h2 id="limits">Caching and rate limits</h2>
			<p>
				BMKG updates its data at fixed intervals, so every response is cached for as long as it
				stays current, here and at the CDN in front. Asking more often than the cache time returns
				the same answer.
			</p>
			<ul>
				<li><code>Cache-Control</code> tells you how long a response stays fresh.</li>
				<li><code>X-Cache</code> is <code>HIT</code> when this server answered from its cache.</li>
				<li>The limit is 30 requests per minute per endpoint, per client. <code>X-RateLimit-Remaining</code> counts down.</li>
			</ul>
			<p>Need more than that? <a href="/self-host/">Run your own instance.</a></p>
		</div>

		{#each GROUPS as group (group)}
			<section class="group">
				<h2 id={group.toLowerCase()}>{group}</h2>
				{#each ENDPOINTS.filter((e) => e.group === group) as endpoint (endpoint.id)}
					<EndpointDoc {endpoint} {...REFERENCE[endpoint.id]} />
				{/each}
			</section>
		{/each}

		<div class="prose">
			<h2 id="polygons">Working with warning polygons</h2>
			<p>
				<code>/v1/nowcast/&#123;alert_code&#125;</code> returns each affected area as a polygon. Two
				things trip people up:
			</p>
			<ul>
				<li>Points are <code>[lat, lon]</code>. Most map libraries want <code>[lon, lat]</code>.</li>
				<li>One area's list holds several rings back to back, with no separator.</li>
			</ul>
			<p>This is how the maps on this site split them:</p>
			<CodeBlock code={rings} lang="text" title="JavaScript" />
		</div>
	</div>
</div>

<style>
	.layout {
		display: grid;
		grid-template-columns: 190px minmax(0, 1fr);
		gap: 48px;
		padding-bottom: 56px;
	}

	aside nav {
		position: sticky;
		top: 84px;
		display: grid;
		gap: 2px;
		padding-top: 56px;
	}

	aside a {
		padding: 5px 10px;
		border-radius: 6px;
		color: var(--muted);
		text-decoration: none;
		font-size: 0.9375rem;
	}

	aside a:hover {
		color: var(--ink);
		background: var(--surface-2);
	}

	.content {
		display: grid;
		gap: 8px;
		min-width: 0;
	}

	.group {
		display: grid;
		gap: 12px;
		margin-top: 36px;
	}

	.group h2 {
		font-size: 1.5rem;
		scroll-margin-top: 80px;
	}

	@media (max-width: 860px) {
		.layout {
			grid-template-columns: minmax(0, 1fr);
			gap: 0;
		}

		aside nav {
			position: static;
			display: flex;
			flex-wrap: wrap;
			padding-top: 20px;
		}
	}
</style>
