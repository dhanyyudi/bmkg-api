import { page } from '$app/state';
import { id, type Messages } from './id';
import { en } from './en';

export type Locale = 'id' | 'en';
export type { Messages };

const MESSAGES: Record<Locale, Messages> = { id, en };

/** Indonesian lives at /, English under /en. */
export function localeOf(lang: string | undefined): Locale {
	return lang === 'en' ? 'en' : 'id';
}

export function messagesFor(locale: Locale): Messages {
	return MESSAGES[locale];
}

/** The messages for the page being shown. Call inside a component. */
export function useMessages(): { readonly m: Messages; readonly locale: Locale } {
	return {
		get locale() {
			return localeOf(page.params.lang);
		},
		get m() {
			return MESSAGES[localeOf(page.params.lang)];
		}
	};
}

/** Fill {placeholders} in a message. */
export function fill(text: string, values: Record<string, string | number>): string {
	return text.replace(/\{(\w+)\}/g, (match, key) => (key in values ? String(values[key]) : match));
}

/** Path of a site page in a locale: href('en', '/docs/') is '/en/docs/'. */
export function href(locale: Locale, path: string): string {
	return locale === 'en' ? `/en${path}` : path;
}

/** The same page in the other locale. */
export function switchPath(pathname: string, to: Locale): string {
	const bare = pathname.replace(/^\/en(?=\/|$)/, '') || '/';
	return href(to, bare);
}
