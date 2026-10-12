import { DEFAULT_PARAMS } from './endpoints';

/** Explorer state, shared so other parts of the page can load a request into it. */
export const explorer = $state({
	endpoint: 'earthquake-latest',
	params: { ...DEFAULT_PARAMS } as Record<string, string>,
	/** Incremented to ask the explorer to run the current request. */
	runRequest: 0
});

/**
 * Select an endpoint, fill in parameters, run it and bring the explorer into view.
 * A click glides there; a link that opens the page on the explorer jumps.
 */
export function openInExplorer(
	endpoint: string,
	params: Record<string, string> = {},
	behavior: ScrollBehavior = 'smooth'
) {
	explorer.endpoint = endpoint;
	Object.assign(explorer.params, params);
	explorer.runRequest += 1;
	document.getElementById('explorer')?.scrollIntoView({ behavior, block: 'start' });
}
