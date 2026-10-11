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
				if (word) return `<span class="n">${word}</span>`;
				if (num) return `<span class="n">${num}</span>`;
				return match;
			}
		);
	}

	function highlightBash(text: string): string {
		return escape(text)
			.replace(/^(#.*)$/gm, '<span class="c">$1</span>')
			.replace(/(https?:\/\/[^\s'"]+)/g, '<span class="s">$1</span>');
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
	<pre style:max-height={maxHeight}><code>{@html html}</code></pre>
</figure>

<style>
	.code {
		margin: 0;
		border-radius: var(--radius);
		background: var(--code-bg);
		color: var(--code-ink);
		overflow: hidden;
		min-width: 0;
	}

	figcaption {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 12px;
		padding: 8px 10px 8px 14px;
		border-bottom: 1px solid rgb(255 255 255 / 8%);
		font-family: var(--font-mono);
		font-size: 0.75rem;
		color: var(--code-muted);
	}

	pre {
		margin: 0;
		padding: 14px;
		overflow: auto;
		font-size: 0.8125rem;
		line-height: 1.6;
		tab-size: 2;
	}

	pre :global(.k) {
		color: var(--code-key);
	}

	pre :global(.s) {
		color: var(--code-str);
	}

	pre :global(.n) {
		color: var(--code-num);
	}

	pre :global(.c) {
		color: var(--code-muted);
	}
</style>
