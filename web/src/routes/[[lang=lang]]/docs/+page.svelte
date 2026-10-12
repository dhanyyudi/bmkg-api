<script lang="ts">
	import CodeBlock from '#lib/components/CodeBlock.svelte';
	import EndpointDoc from '#lib/components/EndpointDoc.svelte';
	import { ENDPOINTS, GROUPS } from '#lib/endpoints';
	import { PUBLIC_ORIGIN } from '#lib/api';
	import { fill, href, useMessages } from '#lib/i18n';

	const i18n = useMessages();

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

	const rings = `// One area's polygon is a flat list of [lat, lon] points holding several
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

// Real boundaries have short edges. A ring with an edge over 20 km joins
// two distant clusters and is dropped.
const drawable = splitRings(area.polygon).filter((ring) =>
  ring.every((point, i) => i === 0 || distanceKm(ring[i - 1], point) <= 20)
);`;
</script>

<svelte:head>
	<title>{i18n.m.docs.title}</title>
	<meta name="description" content={i18n.m.docs.description} />
</svelte:head>

<div class="sheet layout">
	<aside>
		<nav aria-label={i18n.m.docs.onThisPage}>
			<a href="#basics">{i18n.m.docs.basics}</a>
			<a href="#format">{i18n.m.docs.format}</a>
			<a href="#limits">{i18n.m.docs.limits}</a>
			{#each GROUPS as group (group)}
				<a href="#{group.toLowerCase()}">{i18n.m.groups[group]}</a>
			{/each}
			<a href="#polygons">{i18n.m.docs.polygons}</a>
			<a href="/redoc" rel="external">{i18n.m.footer.openapi}</a>
		</nav>
	</aside>

	<div class="content">
		<header class="page-head">
			<h1>{i18n.m.docs.h1}</h1>
			<p>{i18n.m.docs.lead}</p>
		</header>

		<div class="prose">
			<h2 id="basics">{i18n.m.docs.basics}</h2>
			<ul>
				{#each i18n.m.docs.basicsItems as item (item)}
					<li>{fill(item, { base: `${PUBLIC_ORIGIN}/v1` })}</li>
				{/each}
			</ul>

			<h2 id="format">{i18n.m.docs.format}</h2>
			<p>{i18n.m.docs.formatOk}</p>
			<CodeBlock code={success} lang="json" title="200" />
			<p>{i18n.m.docs.formatFail}</p>
			<CodeBlock code={failure} lang="json" title="404" />
			<div class="table-scroll">
				<table class="table">
					<thead><tr><th>{i18n.m.docs.status}</th><th>{i18n.m.docs.meaning}</th></tr></thead>
					<tbody>
						{#each i18n.m.docs.statuses as [code, meaning] (code)}
							<tr><td class="mono">{code}</td><td>{meaning}</td></tr>
						{/each}
					</tbody>
				</table>
			</div>

			<h2 id="limits">{i18n.m.docs.limits}</h2>
			<p>{i18n.m.docs.limitsIntro}</p>
			<ul>
				{#each i18n.m.docs.limitsItems as item (item)}
					<li>{item}</li>
				{/each}
			</ul>
			<p><a href={href(i18n.locale, '/self-host/')}>{i18n.m.docs.limitsMore}</a></p>
		</div>

		{#each GROUPS as group (group)}
			<section class="group">
				<h2 id={group.toLowerCase()}>{i18n.m.groups[group]}</h2>
				{#each ENDPOINTS.filter((e) => e.group === group) as endpoint (endpoint.id)}
					<EndpointDoc {endpoint} />
				{/each}
			</section>
		{/each}

		<div class="prose">
			<h2 id="polygons">{i18n.m.docs.polygons}</h2>
			<p>{i18n.m.docs.polygonsIntro}</p>
			<ul>
				{#each i18n.m.docs.polygonsItems as item (item)}
					<li>{item}</li>
				{/each}
			</ul>
			<p>{i18n.m.docs.polygonsCode}</p>
			<CodeBlock code={rings} lang="text" title="JavaScript" />
		</div>
	</div>
</div>

<style>
	.layout {
		display: grid;
		grid-template-columns: 200px minmax(0, 1fr);
		gap: 40px;
		padding-bottom: 24px;
	}

	aside nav {
		position: sticky;
		top: 84px;
		display: grid;
		padding-top: 52px;
	}

	aside a {
		display: flex;
		align-items: center;
		min-height: 36px;
		color: var(--ink);
		text-decoration: none;
		font-size: 0.9375rem;
		border-bottom: 1px solid var(--hair);
	}

	aside a:hover {
		text-decoration: underline;
	}

	.content {
		display: grid;
		gap: 8px;
		min-width: 0;
	}

	.group {
		margin-top: 36px;
		max-width: 860px;
	}

	.group h2 {
		font-size: 1.375rem;
		padding: 14px 0;
		border-top: 1px solid var(--ink);
		scroll-margin-top: 80px;
	}

	@media (max-width: 860px) {
		.layout {
			grid-template-columns: minmax(0, 1fr);
			gap: 0;
		}

		aside nav {
			position: static;
			padding-top: 16px;
		}

		aside a {
			min-height: 44px;
		}
	}
</style>
