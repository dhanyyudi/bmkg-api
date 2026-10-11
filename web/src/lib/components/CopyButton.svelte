<script lang="ts">
	interface Props {
		text: string;
		label?: string;
	}

	let { text, label = 'Copy' }: Props = $props();
	let copied = $state(false);
	let timer: ReturnType<typeof setTimeout> | undefined;

	async function copy() {
		try {
			await navigator.clipboard.writeText(text);
			copied = true;
			clearTimeout(timer);
			timer = setTimeout(() => (copied = false), 1600);
		} catch {
			// Clipboard access can be denied; the text stays selectable.
		}
	}
</script>

<button type="button" class="copy" class:copied onclick={copy} aria-live="polite">
	{copied ? 'Copied' : label}
</button>

<style>
	.copy {
		font-family: var(--font-mono);
		font-size: 0.75rem;
		padding: 4px 10px;
		border-radius: 6px;
		border: 1px solid rgb(255 255 255 / 18%);
		background: rgb(255 255 255 / 8%);
		color: var(--code-ink);
		transition: background 0.15s;
	}

	.copy:hover {
		background: rgb(255 255 255 / 16%);
	}

	.copied {
		color: var(--code-key);
		border-color: var(--code-key);
	}
</style>
