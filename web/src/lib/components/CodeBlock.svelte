<script lang="ts">
	import CopyButton from './CopyButton.svelte';

	interface Props {
		code: string;
		lang?: 'json' | 'bash' | 'text';
		title?: string;
		maxHeight?: string;
	}

	let { code, lang = 'text', title, maxHeight }: Props = $props();

	const escape = (text: string) =>
		text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

	// The input is escaped first, so the markup added here is the only HTML.
	function highlightJson(text: string): string {
		return escape(text).replace(
			/("(?:\\.|[^"\\])*")(\s*:)?|\b(true|false|null)\b|(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)/g,
			(match, str, colon, word, num) => {
				if (str) return colon ? `<span class="k">${str}</span>${colon}` : `<span class="s">${str}</span>`;
				if (word || num) return `<span class="n">${word ?? num}</span>`;
				return match;
			}
		);
	}

	function highlightBash(text: string): string {
		return escape(text).replace(/^(#.*)$/gm, '<span class="c">$1</span>');
	}

	const html = $derived(
		lang === 'json' ? highlightJson(code) : lang === 'bash' ? highlightBash(code) : escape(code)
	);
</script>

<figure class="code">
	<figcaption>
		<span>{title ?? lang}</span>
		<CopyButton text={code} />
	</figcaption>
	<!-- eslint-disable-next-line svelte/no-at-html-tags -->
	<!-- A scrolling code block has to be reachable to be scrolled by keyboard. -->
	<!-- svelte-ignore a11y_no_noninteractive_tabindex -->
	<pre style:max-height={maxHeight} tabindex="0"><code>{@html html}</code></pre>
</figure>

<style>
	/* Code sits on the unprinted margin tint, like a note beside the map. */
	.code {
		margin: 0;
		border: 1px solid var(--ink);
		background: var(--tint);
		min-width: 0;
	}

	figcaption {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 12px;
		padding: 6px 6px 6px 12px;
		border-bottom: 1px solid var(--hair);
		background: var(--paper);
		font-family: var(--font-mono);
		font-size: 0.75rem;
		color: var(--ink-2);
		overflow-wrap: anywhere;
	}

	pre {
		margin: 0;
		padding: 12px;
		overflow: auto;
		font-size: 0.8125rem;
		line-height: 1.55;
		tab-size: 2;
	}

	/* Keys in water blue, strings in relief brown; numbers stay ink. */
	pre :global(.k) {
		color: var(--water-ink);
	}

	pre :global(.s) {
		color: var(--relief);
	}

	pre :global(.n) {
		font-weight: 500;
	}

	pre :global(.c) {
		color: var(--ink-2);
	}
</style>
