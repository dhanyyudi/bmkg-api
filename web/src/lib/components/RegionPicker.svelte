<script lang="ts">
	import { getData, type Region } from '#lib/api';

	interface Props {
		/** The chosen adm4 code. */
		value: string;
		id: string;
	}

	let { value = $bindable(), id }: Props = $props();

	let text = $state(value);
	let matches = $state<Region[]>([]);
	let open = $state(false);
	let active = $state(0);
	let timer: ReturnType<typeof setTimeout> | undefined;
	let controller: AbortController | undefined;

	const isCode = (s: string) => /^\d{2}\.\d{2}\.\d{2}\.\d{4}$/.test(s.trim());

	$effect(() => {
		// Another part of the page can set the code (for example a region table).
		if (isCode(value) && value !== text && !open) text = value;
	});

	function onInput() {
		clearTimeout(timer);
		controller?.abort();
		const query = text.trim();
		if (isCode(query)) {
			value = query;
			open = false;
			return;
		}
		if (query.length < 3) {
			matches = [];
			open = false;
			return;
		}
		// Wait for a pause in typing: every search is a request to the API.
		timer = setTimeout(async () => {
			controller = new AbortController();
			const found = await getData<Region[]>(
				`/v1/wilayah/search?q=${encodeURIComponent(query)}&limit=30`,
				controller.signal
			);
			matches = (found ?? []).filter((r) => r.level === 'village').slice(0, 8);
			active = 0;
			open = true;
		}, 350);
	}

	function choose(region: Region) {
		value = region.code;
		text = region.code;
		open = false;
	}

	function onKey(event: KeyboardEvent) {
		if (!open || !matches.length) return;
		if (event.key === 'ArrowDown') active = (active + 1) % matches.length;
		else if (event.key === 'ArrowUp') active = (active - 1 + matches.length) % matches.length;
		else if (event.key === 'Enter') choose(matches[active]);
		else if (event.key === 'Escape') open = false;
		else return;
		event.preventDefault();
	}
</script>

<div class="picker">
	<input
		{id}
		type="text"
		bind:value={text}
		oninput={onInput}
		onkeydown={onKey}
		onblur={() => setTimeout(() => (open = false), 150)}
		placeholder="Place name or code, e.g. Tebet"
		autocomplete="off"
		role="combobox"
		aria-expanded={open}
		aria-controls="{id}-list"
		aria-autocomplete="list"
	/>
	{#if open}
		<ul id="{id}-list" role="listbox">
			{#each matches as region, i (region.code)}
				<li role="option" aria-selected={i === active}>
					<button type="button" class:on={i === active} onmousedown={() => choose(region)}>
						<span>{region.name}</span>
						<span class="path">{region.full_path}</span>
						<span class="mono code">{region.code}</span>
					</button>
				</li>
			{:else}
				<li class="none">No village matches. Try another spelling.</li>
			{/each}
		</ul>
	{/if}
</div>

<style>
	.picker {
		position: relative;
	}

	input {
		width: 100%;
	}

	ul {
		position: absolute;
		z-index: 5;
		top: calc(100% + 4px);
		left: 0;
		right: 0;
		list-style: none;
		margin: 0;
		padding: 4px;
		background: var(--surface);
		border: 1px solid var(--line);
		border-radius: 8px;
		box-shadow: var(--shadow);
		max-height: 280px;
		overflow: auto;
	}

	button {
		display: grid;
		grid-template-columns: minmax(0, 1fr) auto;
		gap: 0 10px;
		width: 100%;
		padding: 6px 8px;
		border: 0;
		border-radius: 6px;
		background: none;
		text-align: left;
		font-size: 0.875rem;
	}

	button.on,
	button:hover {
		background: var(--surface-2);
	}

	.path {
		grid-column: 1;
		font-size: 0.75rem;
		color: var(--muted);
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.code {
		grid-column: 2;
		grid-row: 1 / span 2;
		align-self: center;
		color: var(--muted);
	}

	.none {
		padding: 8px;
		font-size: 0.875rem;
		color: var(--muted);
	}
</style>
