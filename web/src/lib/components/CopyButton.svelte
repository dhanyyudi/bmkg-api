<script lang="ts">
	import { useMessages } from '#lib/i18n';

	let { text }: { text: string } = $props();
	const i18n = useMessages();

	let state = $state<'idle' | 'copied' | 'failed'>('idle');
	let timer: ReturnType<typeof setTimeout> | undefined;

	// Embedded browsers often refuse the clipboard API; a selected, hidden
	// field still copies there.
	function copyWithSelection(): boolean {
		const field = document.createElement('textarea');
		field.value = text;
		field.setAttribute('readonly', '');
		field.style.position = 'fixed';
		field.style.opacity = '0';
		document.body.appendChild(field);
		field.select();
		let done = false;
		try {
			done = document.execCommand('copy');
		} catch {
			done = false;
		}
		field.remove();
		return done;
	}

	async function copy() {
		let done = false;
		try {
			await navigator.clipboard.writeText(text);
			done = true;
		} catch {
			done = copyWithSelection();
		}
		// Say so when nothing was copied: a button that stays silent looks broken.
		state = done ? 'copied' : 'failed';
		clearTimeout(timer);
		timer = setTimeout(() => (state = 'idle'), 1800);
	}
</script>

<button type="button" class="copy" onclick={copy} aria-live="polite">
	{state === 'copied' ? i18n.m.common.copied : state === 'failed' ? i18n.m.common.copyFailed : i18n.m.common.copy}
</button>

<style>
	.copy {
		min-height: 30px;
		padding: 0 10px;
		border: 1px solid var(--ink);
		background: var(--paper);
		font-size: 0.8125rem;
		white-space: nowrap;
	}

	.copy:hover {
		background: var(--tint);
	}

	@media (pointer: coarse), (max-width: 900px) {
		.copy {
			min-height: 44px;
			min-width: 44px;
		}
	}
</style>
