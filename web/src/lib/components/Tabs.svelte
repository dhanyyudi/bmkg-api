<script lang="ts" generics="T extends { id: string; label: string }">
	import type { Snippet } from 'svelte';

	interface Props {
		items: T[];
		label: string;
		children: Snippet<[T]>;
	}

	let { items, label, children }: Props = $props();
	let current = $state(0);
	const uid = $props.id();

	function onKey(event: KeyboardEvent) {
		if (event.key !== 'ArrowRight' && event.key !== 'ArrowLeft') return;
		event.preventDefault();
		current = (current + (event.key === 'ArrowRight' ? 1 : -1) + items.length) % items.length;
		const tabs = (event.currentTarget as HTMLElement).querySelectorAll<HTMLElement>('[role="tab"]');
		tabs[current]?.focus();
	}
</script>

<div class="tabs">
	<!-- Focus sits on the selected tab; the list only listens for arrow keys. -->
	<!-- svelte-ignore a11y_interactive_supports_focus -->
	<div class="list" role="tablist" aria-label={label} onkeydown={onKey}>
		{#each items as item, i (item.id)}
			<button
				type="button"
				role="tab"
				id="{uid}-tab-{i}"
				aria-selected={i === current}
				aria-controls="{uid}-panel"
				tabindex={i === current ? 0 : -1}
				class:on={i === current}
				onclick={() => (current = i)}
			>
				{item.label}
			</button>
		{/each}
	</div>
	<div role="tabpanel" id="{uid}-panel" aria-labelledby="{uid}-tab-{current}">
		{@render children(items[current])}
	</div>
</div>

<style>
	.tabs {
		display: grid;
		/* Without a zero minimum, one long code line widens the whole page. */
		grid-template-columns: minmax(0, 1fr);
		gap: 12px;
		min-width: 0;
	}

	.list {
		display: flex;
		flex-wrap: wrap;
		border-bottom: 1px solid var(--ink);
	}

	button {
		min-height: 44px;
		padding: 0 14px;
		border: 1px solid transparent;
		border-bottom: 0;
		background: none;
		color: var(--ink-2);
		margin-bottom: -1px;
	}

	button:hover {
		color: var(--ink);
	}

	/* The chosen tab joins the panel below it, like a folder tab. */
	button.on {
		border-color: var(--ink);
		background: var(--paper);
		color: var(--ink);
		font-weight: 600;
	}
</style>
