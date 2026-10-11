// Typed access to the BMKG API. Pages are served by the API itself, so
// requests are same-origin and need no base URL.

export const PUBLIC_ORIGIN = 'https://bmkg-api.dhanypedia.com';
export const MCP_URL = 'https://mcp-bmkg.dhanypedia.com/mcp';
export const REPO_URL = 'https://github.com/dhanyyudi/bmkg-api';

export interface Earthquake {
	datetime: string;
	magnitude: number;
	depth_km: number;
	lat: number;
	lon: number;
	lat_text: string;
	lon_text: string;
	region: string;
	tsunami_potential: string | null;
	felt_report: string | null;
	shakemap_url: string | null;
	distance_km?: number;
}

export interface ActiveWarning {
	code: string;
	province: string;
	description: string;
	published_at: string;
	detail_url: string;
}

export interface WarningArea {
	name: string;
	polygon: [number, number][] | null;
}

export interface Warning {
	identifier: string;
	event: string;
	severity: string;
	urgency: string;
	certainty: string;
	effective: string;
	expires: string;
	headline: string;
	description: string;
	sender: string;
	infographic_url: string | null;
	areas: WarningArea[];
	is_expired: boolean;
}

export interface ForecastEntry {
	local_datetime: string;
	utc_datetime: string;
	temperature_c: number;
	humidity_pct: number;
	weather: string;
	weather_en: string;
	weather_code: number;
	wind_speed_kmh: number;
	wind_direction: string;
	wind_direction_deg: number;
	cloud_cover_pct: number;
	visibility_m: number | null;
	visibility_text: string | null;
	icon_url: string;
}

export interface WeatherLocation {
	code: string;
	province: string;
	district: string;
	subdistrict: string;
	village: string;
	lat: number;
	lon: number;
	timezone: string;
}

export interface Region {
	code: string;
	name: string;
	level?: string;
	full_path?: string;
	parent_code?: string;
}

export interface Envelope<T> {
	data: T;
	meta: Record<string, unknown>;
	attribution: string;
}

export interface ApiResult {
	ok: boolean;
	status: number;
	/** Parsed JSON body, or null when the response was not JSON. */
	body: unknown;
	headers: Record<string, string>;
	ms: number;
	path: string;
}

/** Run a GET request and keep everything worth showing about the response. */
export async function request(path: string, signal?: AbortSignal): Promise<ApiResult> {
	const started = performance.now();
	const response = await fetch(path, { signal, headers: { Accept: 'application/json' } });
	const ms = Math.round(performance.now() - started);
	const headers: Record<string, string> = {};
	response.headers.forEach((value, name) => (headers[name] = value));
	let body: unknown = null;
	try {
		body = await response.json();
	} catch {
		body = null;
	}
	return { ok: response.ok, status: response.status, body, headers, ms, path };
}

/** Fetch an endpoint's data, or null if it is unavailable. */
export async function getData<T>(path: string, signal?: AbortSignal): Promise<T | null> {
	try {
		const result = await request(path, signal);
		return result.ok ? (result.body as Envelope<T>).data : null;
	} catch {
		return null;
	}
}

/** Earthquake times are UTC without an offset; other timestamps carry one. */
export function parseTime(value: string): Date {
	return new Date(/[zZ]|[+-]\d{2}:?\d{2}$/.test(value) ? value : `${value}Z`);
}

export function timeAgo(date: Date, now: Date = new Date()): string {
	const seconds = Math.max(0, Math.round((now.getTime() - date.getTime()) / 1000));
	if (seconds < 60) return 'just now';
	const minutes = Math.round(seconds / 60);
	if (minutes < 60) return `${minutes} min ago`;
	const hours = Math.round(minutes / 60);
	if (hours < 48) return `${hours} h ago`;
	return `${Math.round(hours / 24)} days ago`;
}

const dateTime = new Intl.DateTimeFormat('en-GB', {
	day: 'numeric',
	month: 'short',
	hour: '2-digit',
	minute: '2-digit',
	timeZone: 'Asia/Jakarta'
});

/** Format in Western Indonesia Time, the reference most readers expect. */
export function formatWib(date: Date): string {
	return `${dateTime.format(date)} WIB`;
}
