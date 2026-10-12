import type { Handle } from '@sveltejs/kit/hooks';

// Pages are prerendered once per language; set <html lang> to match.
export const handle: Handle = ({ event, resolve }) =>
	resolve(event, {
		transformPageChunk: ({ html }) => html.replace('%lang%', event.params.lang === 'en' ? 'en' : 'id')
	});
