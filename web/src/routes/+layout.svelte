<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import type { Snippet } from 'svelte';
	import { REPO_URL } from '#lib/api';

	let { children }: { children: Snippet } = $props();

	let status = $state<'checking' | 'online' | 'offline'>('checking');
	let version = $state('');
	let dark = $state(false);

	function toggleTheme() {
		dark = !dark;
		document.documentElement.dataset.theme = dark ? 'dark' : 'light';
		try {
			localStorage.setItem('theme', dark ? 'dark' : 'light');
		} catch {
			// Storage can be unavailable; the choice then lasts for this page only.
		}
	}

	onMount(async () => {
		dark = document.documentElement.dataset.theme === 'dark';
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

<a class="skip" href="#main">Skip to content</a>

<header class="top">
	<div class="wrap bar">
		<a class="brand" href="/">
			<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">
				<path d="M2 12h4l2.5-7 4 14 3-9 1.5 2H22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
			</svg>
			BMKG API
		</a>

		<nav aria-label="Main">
			<a href="/#explorer">Explorer</a>
			<a href="/docs/">Docs</a>
			<a href="/mcp-setup/">MCP</a>
			<a href="/self-host/">Self-host</a>
			<a href={REPO_URL} rel="noopener">GitHub</a>
		</nav>

		<div class="tools">
			<span class="status {status}" title="Result of /health">
				<span class="dot"></span>
				{status === 'online' ? `API ${version}` : status === 'offline' ? 'API offline' : 'Checking'}
			</span>
			<button type="button" class="theme" onclick={toggleTheme} aria-label="Switch to {dark ? 'light' : 'dark'} theme">
				{#if dark}
					<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><circle cx="12" cy="12" r="4.5" fill="none" stroke="currentColor" stroke-width="2" /><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8" stroke="currentColor" stroke-width="2" stroke-linecap="round" /></svg>
				{:else}
					<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" /></svg>
				{/if}
			</button>
		</div>
	</div>
</header>

<main id="main">
	{@render children()}
</main>

<footer class="foot">
	<div class="wrap foot-grid">
		<div>
			<p class="brand small">BMKG API</p>
			<p class="muted">
				All data belongs to
				<a href="https://www.bmkg.go.id" rel="noopener">BMKG</a>
				(Badan Meteorologi, Klimatologi, dan Geofisika). This project is not affiliated with BMKG.
			</p>
		</div>
		<nav aria-label="Footer">
			<a href="/docs/">Documentation</a>
			<a href="/redoc" rel="external">OpenAPI reference</a>
			<a href="/mcp-setup/">MCP setup</a>
			<a href="/self-host/">Self-hosting</a>
			<a href={REPO_URL} rel="noopener">GitHub</a>
		</nav>
		<p class="muted fine">
			Made by <a href="https://github.com/dhanyyudi" rel="noopener">dhanypedia</a> · MIT License
		</p>
	</div>
</footer>

<style>
	.skip {
		position: absolute;
		left: 12px;
		top: -48px;
		padding: 8px 12px;
		background: var(--accent);
		color: var(--accent-ink);
		border-radius: 6px;
		z-index: 20;
	}

	.skip:focus {
		top: 12px;
	}

	.top {
		position: sticky;
		top: 0;
		z-index: 10;
		background: color-mix(in srgb, var(--bg) 88%, transparent);
		backdrop-filter: blur(10px);
		border-bottom: 1px solid var(--line);
	}

	.bar {
		display: flex;
		align-items: center;
		gap: 24px;
		min-height: 60px;
	}

	.brand {
		display: inline-flex;
		align-items: center;
		gap: 8px;
		font-weight: 600;
		font-size: 1.05rem;
		letter-spacing: -0.01em;
		color: var(--ink);
		text-decoration: none;
	}

	.brand svg {
		color: var(--accent);
	}

	nav {
		display: flex;
		gap: 4px;
		margin-left: auto;
	}

	nav a {
		padding: 6px 10px;
		border-radius: 6px;
		color: var(--muted);
		text-decoration: none;
		font-size: 0.9375rem;
		white-space: nowrap;
	}

	nav a:hover {
		color: var(--ink);
		background: var(--surface-2);
	}

	.tools {
		display: flex;
		align-items: center;
		gap: 10px;
	}

	.status {
		display: inline-flex;
		align-items: center;
		gap: 7px;
		font-family: var(--font-mono);
		font-size: 0.75rem;
		color: var(--muted);
		white-space: nowrap;
	}

	.status .dot {
		width: 7px;
		height: 7px;
		border-radius: 50%;
		background: var(--muted);
	}

	.status.online .dot {
		background: var(--ok);
	}

	.status.offline .dot {
		background: var(--quake);
	}

	.theme {
		display: grid;
		place-items: center;
		width: 36px;
		height: 36px;
		border: 1px solid var(--line);
		border-radius: 8px;
		background: var(--surface);
	}

	.foot {
		border-top: 1px solid var(--line);
		padding: 40px 0 48px;
		margin-top: 40px;
	}

	.foot-grid {
		display: grid;
		grid-template-columns: 1.4fr 1fr;
		gap: 24px 48px;
	}

	.foot nav {
		margin: 0;
		flex-wrap: wrap;
		align-content: start;
	}

	.brand.small {
		font-size: 1rem;
		margin-bottom: 6px;
	}

	.muted {
		color: var(--muted);
		font-size: 0.9375rem;
	}

	.fine {
		grid-column: 1 / -1;
		font-size: 0.8125rem;
	}

	@media (max-width: 760px) {
		.bar {
			flex-wrap: wrap;
			gap: 4px 12px;
			padding: 8px 0;
		}

		.tools {
			margin-left: auto;
		}

		nav {
			order: 3;
			width: 100%;
			margin-left: -10px;
			overflow-x: auto;
		}

		.foot-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
