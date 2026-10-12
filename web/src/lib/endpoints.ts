import { fill, type Messages } from './i18n';

export type ParamKind = 'text' | 'number' | 'region' | 'alert' | 'language';
export type ParamName = 'lat' | 'lon' | 'radius_km' | 'adm4' | 'lang' | 'alertCode' | 'location' | 'province' | 'district' | 'subdistrict' | 'query';
export type EndpointId = keyof Messages['endpoints'];
export type Group = keyof Messages['groups'];

export interface ParamDef {
	name: ParamName;
	kind: ParamKind;
	placeholder?: string;
}

/** A parameter as the reference documents it: its real name, and whether it is needed. */
export type ReferenceParam = [name: keyof Messages['reference'], need: 'required' | 'optional' | 'inPath'];

export interface EndpointDef {
	id: EndpointId;
	group: Group;
	/** Path with {placeholders}, as shown in the docs. */
	template: string;
	/** Seconds a response is cached. */
	ttl: number;
	params: ParamDef[];
	reference: ReferenceParam[];
	/** Build the request path from the current parameter values. */
	path: (p: Record<string, string>) => string;
}

const q = (pairs: Record<string, string | undefined>) => {
	const search = new URLSearchParams();
	for (const [name, value] of Object.entries(pairs)) if (value) search.set(name, value);
	const text = search.toString();
	return text ? `?${text}` : '';
};

const language: ParamDef = { name: 'lang', kind: 'language' };
const english = (p: Record<string, string>) => (p.lang === 'en' ? 'en' : undefined);

export const DEFAULT_PARAMS: Record<string, string> = {
	adm4: '31.74.04.1006',
	lat: '-6.2',
	lon: '106.8',
	radius_km: '300',
	lang: 'id',
	alertCode: '',
	location: 'Jakarta',
	province: '31',
	district: '31.74',
	subdistrict: '31.74.04',
	query: 'tebet'
};

export const ENDPOINTS: EndpointDef[] = [
	{ id: 'earthquake-latest', group: 'Earthquakes', template: '/v1/earthquake/latest', ttl: 60, params: [], reference: [], path: () => '/v1/earthquake/latest' },
	{ id: 'earthquake-recent', group: 'Earthquakes', template: '/v1/earthquake/recent', ttl: 300, params: [], reference: [], path: () => '/v1/earthquake/recent' },
	{ id: 'earthquake-felt', group: 'Earthquakes', template: '/v1/earthquake/felt', ttl: 300, params: [], reference: [], path: () => '/v1/earthquake/felt' },
	{
		id: 'earthquake-nearby',
		group: 'Earthquakes',
		template: '/v1/earthquake/nearby',
		ttl: 300,
		params: [
			{ name: 'lat', kind: 'number', placeholder: '-6.2' },
			{ name: 'lon', kind: 'number', placeholder: '106.8' },
			{ name: 'radius_km', kind: 'number', placeholder: '300' }
		],
		reference: [['lat', 'required'], ['lon', 'required'], ['radius_km', 'optional']],
		path: (p) => `/v1/earthquake/nearby${q({ lat: p.lat, lon: p.lon, radius_km: p.radius_km })}`
	},
	{
		id: 'weather',
		group: 'Weather',
		template: '/v1/weather/{adm4_code}',
		ttl: 900,
		params: [{ name: 'adm4', kind: 'region' }],
		reference: [['adm4_code', 'inPath']],
		path: (p) => `/v1/weather/${encodeURIComponent(p.adm4 || '{adm4_code}')}`
	},
	{
		id: 'weather-current',
		group: 'Weather',
		template: '/v1/weather/{adm4_code}/current',
		ttl: 900,
		params: [{ name: 'adm4', kind: 'region' }],
		reference: [['adm4_code', 'inPath']],
		path: (p) => `/v1/weather/${encodeURIComponent(p.adm4 || '{adm4_code}')}/current`
	},
	{
		id: 'nowcast',
		group: 'Warnings',
		template: '/v1/nowcast',
		ttl: 120,
		params: [language],
		reference: [['lang', 'optional']],
		path: (p) => `/v1/nowcast${q({ lang: english(p) })}`
	},
	{
		id: 'nowcast-warnings',
		group: 'Warnings',
		template: '/v1/nowcast/warnings',
		ttl: 120,
		params: [language],
		reference: [['lang', 'optional']],
		path: (p) => `/v1/nowcast/warnings${q({ lang: english(p) })}`
	},
	{
		id: 'nowcast-detail',
		group: 'Warnings',
		template: '/v1/nowcast/{alert_code}',
		ttl: 120,
		params: [{ name: 'alertCode', kind: 'alert' }, language],
		reference: [['alert_code', 'inPath'], ['lang', 'optional']],
		path: (p) => `/v1/nowcast/${encodeURIComponent(p.alertCode || '{alert_code}')}${q({ lang: english(p) })}`
	},
	{
		id: 'nowcast-check',
		group: 'Warnings',
		template: '/v1/nowcast/check',
		ttl: 120,
		params: [{ name: 'location', kind: 'text', placeholder: 'Jakarta' }, language],
		reference: [['location', 'required'], ['lang', 'optional']],
		path: (p) => `/v1/nowcast/check${q({ location: p.location, lang: english(p) })}`
	},
	{
		id: 'wilayah-search',
		group: 'Regions',
		template: '/v1/wilayah/search',
		ttl: 86400,
		params: [{ name: 'query', kind: 'text', placeholder: 'tebet' }],
		reference: [['q', 'required'], ['limit', 'optional']],
		path: (p) => `/v1/wilayah/search${q({ q: p.query, limit: '20' })}`
	},
	{ id: 'wilayah-provinces', group: 'Regions', template: '/v1/wilayah/provinces', ttl: 86400, params: [], reference: [], path: () => '/v1/wilayah/provinces' },
	{
		id: 'wilayah-districts',
		group: 'Regions',
		template: '/v1/wilayah/districts',
		ttl: 86400,
		params: [{ name: 'province', kind: 'text', placeholder: '31' }],
		reference: [['province', 'required']],
		path: (p) => `/v1/wilayah/districts${q({ province: p.province })}`
	},
	{
		id: 'wilayah-subdistricts',
		group: 'Regions',
		template: '/v1/wilayah/subdistricts',
		ttl: 86400,
		params: [{ name: 'district', kind: 'text', placeholder: '31.74' }],
		reference: [['district', 'required']],
		path: (p) => `/v1/wilayah/subdistricts${q({ district: p.district })}`
	},
	{
		id: 'wilayah-villages',
		group: 'Regions',
		template: '/v1/wilayah/villages',
		ttl: 86400,
		params: [{ name: 'subdistrict', kind: 'text', placeholder: '31.74.04' }],
		reference: [['subdistrict', 'required']],
		path: (p) => `/v1/wilayah/villages${q({ subdistrict: p.subdistrict })}`
	}
];

export const GROUPS: Group[] = ['Earthquakes', 'Weather', 'Warnings', 'Regions'];

export const endpointById = (id: string) => ENDPOINTS.find((e) => e.id === id) ?? ENDPOINTS[0];

/** A cache lifetime in the largest whole unit: 60 s, 5 min, 24 h. */
export function cacheTime(seconds: number, m: Messages): string {
	if (seconds >= 3600) return fill(m.common.hours, { n: seconds / 3600 });
	if (seconds > 60) return fill(m.common.minutes, { n: seconds / 60 });
	return fill(m.common.seconds, { n: seconds });
}
