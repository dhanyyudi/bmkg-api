<script lang="ts" generics="T extends { id: string; label: string }">
	import type { Snippet } from 'svelte';

	interface Props {
		items: T[];
		label: string;
		children: Snippet<[T]>;
	}

	let { items, label, children }: Props = $props();
	let current = $state(0);

	function onKey(event: KeyboardEvent) {
		if (event.key !== 'ArrowRight' && event.key !== 'ArrowLeft') return;
		current = (current + (event.key === 'ArrowRight' ? 1 : -1) + items.length) % items.length;
		const tabs = (event.currentTarget as HTMLElement).querySelectorAll<HTMLElement>('[role="tab"]');
		tabs[current]?.focus();
	}
</script>

<div class="tabs">
	<div class="list" role="tablist" aria-label={label} onkeydown={onKey} tabindex="-1">
		{#each items as item, i (item.id)}
			<button
				type="button"
				role="tab"
				aria-selected={i === current}
				tabindex={i === current ? 0 : -1}
				class:on={i === current}
				onclick={() => (current = i)}
			>
				{item.label}
			</button>
		{/each}
	</div>
	<div role="tabpanel">
		{@render children(items[current])}
	</div>
</div>

<style>
	.tabs {
		display: grid;
		gap: 12px;
		min-width: 0;
	}

	.list {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
	}

	button {
		padding: 6px 12px;
		border-radius: 999px;
		border: 1px solid var(--line);
		background: var(--surface);
		font-size: 0.875rem;
		color: var(--muted);
	}

	button:hover {
		color: var(--ink);
	}

	button.on {
		background: var(--ink);
		border-color: var(--ink);
		color: var(--bg);
	}
</style>
