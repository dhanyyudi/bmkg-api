<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import type { Snippet } from 'svelte';
	import { page } from '$app/state';
	import { PUBLIC_ORIGIN, REPO_URL } from '#lib/api';
	import { fill, href, switchPath, useMessages } from '#lib/i18n';

	let { children }: { children: Snippet } = $props();
	const i18n = useMessages();

	let status = $state<'checking' | 'online' | 'offline'>('checking');
	let version = $state('');

	const other = $derived(i18n.m.switchTo.locale === 'en' ? 'en' : 'id');
	const otherPath = $derived(switchPath(page.url.pathname, other));

	// The switch loads the other page afresh (data-sveltekit-reload): <html lang>
	// and the live data, which the API returns per language, both follow.
	// The choice is kept, so a later visit to an Indonesian URL opens in the
	// chosen language (see the script in app.html).
	function remember(locale: string) {
		try {
			localStorage.setItem('lang', locale);
		} catch {
			// Without storage the choice lasts for this visit only.
		}
	}

	onMount(async () => {
		try {
			const response = await fetch('/health');
			const health = await response.json();
			status = response.ok ? 'online' : 'offline';
			version = health.version ?? '';
		} catch {
			status = 'offline';
		}
	});
</script>

<svelte:head>
	<link rel="alternate" hreflang="id" href="{PUBLIC_ORIGIN}{switchPath(page.url.pathname, 'id')}" />
	<link rel="alternate" hreflang="en" href="{PUBLIC_ORIGIN}{switchPath(page.url.pathname, 'en')}" />
</svelte:head>

<a class="skip" href="#main">{i18n.m.nav.skip}</a>

<header class="top">
	<div class="sheet bar">
		<a class="brand" href={href(i18n.locale, '/')}>
			<img src="/logo.svg" alt="" width="32" height="32" />
			<span>BMKG <span class="api">API</span></span>
		</a>

		<nav aria-label={i18n.m.nav.main}>
			<a href="{href(i18n.locale, '/')}#explorer">{i18n.m.nav.explorer}</a>
			<a href={href(i18n.locale, '/docs/')}>{i18n.m.nav.docs}</a>
			<a href={href(i18n.locale, '/mcp-setup/')}>{i18n.m.nav.mcp}</a>
			<a href={href(i18n.locale, '/self-host/')}>{i18n.m.nav.selfHost}</a>
			<a href={REPO_URL} rel="noopener">{i18n.m.nav.github}</a>
		</nav>

		<div class="tools">
			<span class="status mono" class:offline={status === 'offline'} title={i18n.m.status.title}>
				{status === 'online'
					? fill(i18n.m.status.online, { version })
					: status === 'offline'
						? i18n.m.status.offline
						: i18n.m.status.checking}
			</span>
			<a
				class="lang"
				href={otherPath}
				hreflang={other}
				lang={other}
				aria-label={i18n.m.switchTo.title}
				title={i18n.m.switchTo.title}
				data-sveltekit-reload
				onclick={() => remember(other)}
			>
				<span class:on={i18n.locale === 'id'}>ID</span>
				<span class:on={i18n.locale === 'en'}>EN</span>
			</a>
		</div>
	</div>
</header>

<main id="main">
	{@render children()}
</main>

<footer class="foot">
	<div class="sheet foot-grid">
		<div class="notes">
			<p>{i18n.m.footer.source}</p>
			<p>{i18n.m.footer.regions}</p>
			<p>{i18n.m.footer.map}</p>
			<p>{i18n.m.footer.license}</p>
		</div>
		<nav aria-label={i18n.m.footer.nav}>
			<a href={href(i18n.locale, '/docs/')}>{i18n.m.nav.docs}</a>
			<a href="/redoc" rel="external">{i18n.m.footer.openapi}</a>
			<a href={href(i18n.locale, '/mcp-setup/')}>{i18n.m.nav.mcp}</a>
			<a href={href(i18n.locale, '/self-host/')}>{i18n.m.nav.selfHost}</a>
			<a href={REPO_URL} rel="noopener">{i18n.m.nav.github}</a>
		</nav>
	</div>
</footer>

<style>
	.skip {
		position: absolute;
		left: 12px;
		top: -60px;
		padding: 10px 14px;
		background: var(--ink);
		color: var(--paper);
		z-index: 20;
	}

	.skip:focus {
		top: 12px;
	}

	.top {
		position: sticky;
		top: 0;
		z-index: 10;
		background: var(--paper);
		border-bottom: 1px solid var(--ink);
	}

	.bar {
		display: flex;
		align-items: center;
		gap: 8px 28px;
		min-height: 60px;
	}

	.brand {
		display: inline-flex;
		align-items: center;
		gap: 10px;
		min-height: 44px;
		font-weight: 700;
		font-size: 1.0625rem;
		color: var(--ink);
		text-decoration: none;
	}

	.brand img {
		display: block;
	}

	/* As in the lockup: the place name upright and bold, the code in fixed width. */
	.brand .api {
		font-family: var(--font-mono);
		font-weight: 500;
		font-size: 0.94em;
	}

	nav {
		display: flex;
		gap: 4px 20px;
	}

	nav a {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		flex: none;
		min-width: 44px;
		min-height: 44px;
		color: var(--ink);
		text-decoration: none;
		white-space: nowrap;
	}

	nav a:hover {
		text-decoration: underline;
	}

	.tools {
		margin-left: auto;
		display: flex;
		align-items: center;
		gap: 16px;
	}

	.status {
		font-size: 0.75rem;
		color: var(--ink-2);
		white-space: nowrap;
	}

	.status.offline {
		color: var(--alert);
	}

	/* Both languages are shown; the one in use is printed in reverse. */
	.lang {
		display: inline-flex;
		border: 1px solid var(--ink);
		color: var(--ink);
		text-decoration: none;
		font-size: 0.875rem;
		font-weight: 600;
	}

	.lang span {
		display: grid;
		place-items: center;
		min-width: 44px;
		min-height: 44px;
	}

	.lang span.on {
		background: var(--ink);
		color: var(--paper);
	}

	.lang:hover span:not(.on) {
		background: var(--tint);
	}

	.foot {
		margin-top: 72px;
		padding: 20px 0 44px;
		border-top: 1px solid var(--ink);
	}

	.foot-grid {
		display: grid;
		grid-template-columns: minmax(0, 1fr) auto;
		gap: 20px 48px;
		font-size: 0.875rem;
	}

	.notes {
		display: grid;
		gap: 4px;
		color: var(--ink-2);
		max-width: 720px;
	}

	.foot nav {
		display: grid;
		gap: 0;
		align-content: start;
	}

	.foot nav a {
		min-height: 32px;
		color: var(--water-ink);
		text-decoration: underline;
		text-decoration-thickness: 1px;
	}

	@media (max-width: 900px) {
		/* The wrapped header is too tall to keep pinned on a small screen. */
		.top {
			position: static;
		}

		.bar {
			flex-wrap: wrap;
			padding: 6px 0;
		}

		/* Wraps instead of scrolling sideways: no page link is hidden. */
		nav {
			order: 3;
			width: 100%;
			flex-wrap: wrap;
			gap: 0 16px;
			border-top: 1px solid var(--hair);
		}

		.status {
			display: none;
		}

		.foot-grid {
			grid-template-columns: minmax(0, 1fr);
		}

		.foot nav a {
			min-height: 44px;
		}
	}
</style>
