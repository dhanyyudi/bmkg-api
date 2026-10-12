<script lang="ts">
	import { getData, type Region } from '#lib/api';
	import { useMessages } from '#lib/i18n';

	interface Props {
		/** The chosen adm4 code. */
		value: string;
		id: string;
	}

	let { value = $bindable(), id }: Props = $props();
	const i18n = useMessages();

	let text = $state(value);
	let matches = $state<Region[]>([]);
	let open = $state(false);
	let active = $state(0);
	let timer: ReturnType<typeof setTimeout> | undefined;
	let controller: AbortController | undefined;

	const isCode = (s: string) => /^\d{2}\.\d{2}\.\d{2}\.\d{4}$/.test(s.trim());

	// Another part of the page can set the code (for example a region table).
	// Only that change is copied into the field: comparing against the text
	// itself would undo every keystroke of a place name.
	let seen = value;
	$effect(() => {
		if (value === seen) return;
		seen = value;
		if (isCode(value)) text = value;
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

	// "Province > District > Subdistrict > Village", read from the nearest level
	// outwards: the subdistrict is what tells two villages of one name apart.
	const whereabouts = (region: Region) => (region.full_path ?? '').split(' > ').slice(0, -1).reverse().join(', ');

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
		placeholder={i18n.m.params.adm4Placeholder}
		autocomplete="off"
		role="combobox"
		aria-expanded={open}
		aria-controls="{id}-list"
		aria-autocomplete="list"
		aria-activedescendant={open && matches.length ? `${id}-option-${active}` : undefined}
	/>
	{#if open}
		<ul id="{id}-list" role="listbox">
			{#each matches as region, i (region.code)}
				<li role="option" id="{id}-option-{i}" aria-selected={i === active}>
					<button type="button" class:on={i === active} tabindex="-1" onmousedown={() => choose(region)}>
						<span>{region.name}</span>
						<span class="path">{whereabouts(region)}</span>
						<span class="mono code">{region.code}</span>
					</button>
				</li>
			{:else}
				<li class="none">{i18n.m.params.noVillage}</li>
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
		top: 100%;
		left: 0;
		right: 0;
		list-style: none;
		margin: -1px 0 0;
		padding: 0;
		background: var(--paper);
		border: 1px solid var(--ink);
		max-height: 300px;
		overflow: auto;
	}

	button {
		display: grid;
		grid-template-columns: minmax(0, 1fr) auto;
		gap: 0 10px;
		width: 100%;
		min-height: 44px;
		padding: 6px 10px;
		border: 0;
		border-bottom: 1px solid var(--hair);
		background: none;
		text-align: left;
		font-size: 0.9375rem;
	}

	button.on,
	button:hover {
		background: var(--tint);
	}

	.path {
		grid-column: 1;
		font-size: 0.8125rem;
		color: var(--ink-2);
	}

	.code {
		grid-column: 2;
		grid-row: 1 / span 2;
		align-self: center;
		color: var(--ink-2);
	}

	.none {
		padding: 10px;
		font-size: 0.9375rem;
		color: var(--ink-2);
	}
</style>
