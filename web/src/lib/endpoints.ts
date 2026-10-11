export type ParamKind = 'text' | 'number' | 'region' | 'alert' | 'language';

export interface ParamDef {
	name: string;
	label: string;
	kind: ParamKind;
	placeholder?: string;
	hint?: string;
}

export interface EndpointDef {
	id: string;
	group: 'Earthquakes' | 'Weather' | 'Warnings' | 'Regions';
	/** Path with {placeholders}, as shown in the docs. */
	template: string;
	summary: string;
	params: ParamDef[];
	/** Build the request path from the current parameter values. */
	path: (p: Record<string, string>) => string;
}

const q = (pairs: Record<string, string | undefined>) => {
	const search = new URLSearchParams();
	for (const [name, value] of Object.entries(pairs)) if (value) search.set(name, value);
	const text = search.toString();
	return text ? `?${text}` : '';
};

const language: ParamDef = { name: 'lang', label: 'Language', kind: 'language' };

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
	{
		id: 'earthquake-latest',
		group: 'Earthquakes',
		template: '/v1/earthquake/latest',
		summary: 'The most recent earthquake',
		params: [],
		path: () => '/v1/earthquake/latest'
	},
	{
		id: 'earthquake-recent',
		group: 'Earthquakes',
		template: '/v1/earthquake/recent',
		summary: 'Last 15 earthquakes of M 5.0+',
		params: [],
		path: () => '/v1/earthquake/recent'
	},
	{
		id: 'earthquake-felt',
		group: 'Earthquakes',
		template: '/v1/earthquake/felt',
		summary: 'Last 15 earthquakes people felt',
		params: [],
		path: () => '/v1/earthquake/felt'
	},
	{
		id: 'earthquake-nearby',
		group: 'Earthquakes',
		template: '/v1/earthquake/nearby',
		summary: 'Recent earthquakes around a point',
		params: [
			{ name: 'lat', label: 'Latitude', kind: 'number', placeholder: '-6.2' },
			{ name: 'lon', label: 'Longitude', kind: 'number', placeholder: '106.8' },
			{ name: 'radius_km', label: 'Radius (km)', kind: 'number', placeholder: '300' }
		],
		path: (p) => `/v1/earthquake/nearby${q({ lat: p.lat, lon: p.lon, radius_km: p.radius_km })}`
	},
	{
		id: 'weather',
		group: 'Weather',
		template: '/v1/weather/{adm4_code}',
		summary: '3-day forecast for a village',
		params: [{ name: 'adm4', label: 'Village', kind: 'region', hint: 'Type a place name to find its code' }],
		path: (p) => `/v1/weather/${encodeURIComponent(p.adm4 || '{adm4_code}')}`
	},
	{
		id: 'weather-current',
		group: 'Weather',
		template: '/v1/weather/{adm4_code}/current',
		summary: 'Weather right now for a village',
		params: [{ name: 'adm4', label: 'Village', kind: 'region', hint: 'Type a place name to find its code' }],
		path: (p) => `/v1/weather/${encodeURIComponent(p.adm4 || '{adm4_code}')}/current`
	},
	{
		id: 'nowcast',
		group: 'Warnings',
		template: '/v1/nowcast',
		summary: 'Provinces with an active warning',
		params: [language],
		path: (p) => `/v1/nowcast${q({ lang: p.lang === 'en' ? 'en' : undefined })}`
	},
	{
		id: 'nowcast-detail',
		group: 'Warnings',
		template: '/v1/nowcast/{alert_code}',
		summary: 'One warning, with affected areas',
		params: [{ name: 'alertCode', label: 'Active warning', kind: 'alert' }, language],
		path: (p) =>
			`/v1/nowcast/${encodeURIComponent(p.alertCode || '{alert_code}')}${q({ lang: p.lang === 'en' ? 'en' : undefined })}`
	},
	{
		id: 'nowcast-check',
		group: 'Warnings',
		template: '/v1/nowcast/check',
		summary: 'Warnings that mention a place',
		params: [{ name: 'location', label: 'Place name', kind: 'text', placeholder: 'Jakarta' }, language],
		path: (p) => `/v1/nowcast/check${q({ location: p.location, lang: p.lang === 'en' ? 'en' : undefined })}`
	},
	{
		id: 'wilayah-search',
		group: 'Regions',
		template: '/v1/wilayah/search',
		summary: 'Find regions by name',
		params: [{ name: 'query', label: 'Name', kind: 'text', placeholder: 'tebet' }],
		path: (p) => `/v1/wilayah/search${q({ q: p.query, limit: '20' })}`
	},
	{
		id: 'wilayah-provinces',
		group: 'Regions',
		template: '/v1/wilayah/provinces',
		summary: 'All provinces',
		params: [],
		path: () => '/v1/wilayah/provinces'
	},
	{
		id: 'wilayah-districts',
		group: 'Regions',
		template: '/v1/wilayah/districts',
		summary: 'Districts of a province',
		params: [{ name: 'province', label: 'Province code', kind: 'text', placeholder: '31' }],
		path: (p) => `/v1/wilayah/districts${q({ province: p.province })}`
	},
	{
		id: 'wilayah-subdistricts',
		group: 'Regions',
		template: '/v1/wilayah/subdistricts',
		summary: 'Subdistricts of a district',
		params: [{ name: 'district', label: 'District code', kind: 'text', placeholder: '31.74' }],
		path: (p) => `/v1/wilayah/subdistricts${q({ district: p.district })}`
	},
	{
		id: 'wilayah-villages',
		group: 'Regions',
		template: '/v1/wilayah/villages',
		summary: 'Villages of a subdistrict',
		params: [{ name: 'subdistrict', label: 'Subdistrict code', kind: 'text', placeholder: '31.74.04' }],
		path: (p) => `/v1/wilayah/villages${q({ subdistrict: p.subdistrict })}`
	}
];

export const GROUPS = ['Earthquakes', 'Weather', 'Warnings', 'Regions'] as const;

export const endpointById = (id: string) => ENDPOINTS.find((e) => e.id === id) ?? ENDPOINTS[0];
