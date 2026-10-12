import { fill, type Messages } from './i18n';

/** Earthquake times are UTC without an offset; other timestamps carry one. */
export function parseTime(value: string): Date {
	return new Date(/[zZ]|[+-]\d{2}:?\d{2}$/.test(value) ? value : `${value}Z`);
}

export function timeAgo(date: Date, m: Messages, now: Date = new Date()): string {
	const seconds = Math.max(0, Math.round((now.getTime() - date.getTime()) / 1000));
	if (seconds < 60) return m.common.justNow;
	const minutes = Math.round(seconds / 60);
	if (minutes < 60) return fill(m.common.minutesAgo, { n: minutes });
	const hours = Math.round(minutes / 60);
	if (hours < 48) return fill(m.common.hoursAgo, { n: hours });
	return fill(m.common.daysAgo, { n: Math.round(hours / 24) });
}

/** Date and time in Western Indonesia Time, the reference most readers expect. */
export function formatWib(date: Date, m: Messages): string {
	const text = new Intl.DateTimeFormat(m.numberLocale, {
		day: 'numeric',
		month: 'short',
		hour: '2-digit',
		minute: '2-digit',
		hour12: false,
		timeZone: 'Asia/Jakarta'
	}).format(date);
	return `${text} ${m.common.wib}`;
}

export function clockWib(date: Date, m: Messages): string {
	const text = new Intl.DateTimeFormat(m.numberLocale, {
		hour: '2-digit',
		minute: '2-digit',
		hour12: false,
		timeZone: 'Asia/Jakarta'
	}).format(date);
	return `${text} ${m.common.wib}`;
}

export function magnitude(value: number, m: Messages): string {
	return value.toLocaleString(m.numberLocale, { minimumFractionDigits: 1, maximumFractionDigits: 1 });
}

/** Radius of an earthquake mark in screen pixels. */
export function quakeRadius(value: number): number {
	return 3 + Math.max(0, value - 2) * 1.6;
}
