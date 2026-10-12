import type { Messages } from './id';

export const en: Messages = {
	locale: 'en',
	htmlLang: 'en',
	numberLocale: 'en-GB',
	apiLang: 'en',

	switchTo: { title: 'Beralih ke Bahasa Indonesia', locale: 'id' },

	nav: {
		skip: 'Skip to content',
		main: 'Main',
		explorer: 'Explorer',
		docs: 'Documentation',
		mcp: 'MCP',
		selfHost: 'Self-host',
		github: 'GitHub'
	},

	status: {
		checking: 'Checking the API',
		online: 'API {version} is up',
		offline: 'API unreachable',
		title: 'Result of the /health check'
	},

	common: {
		copy: 'Copy',
		copied: 'Copied',
		copyFailed: 'Copy failed',
		run: 'Run',
		running: 'Running',
		runAgain: 'Run again',
		tryIt: 'Try',
		justNow: 'just now',
		minutesAgo: '{n} min ago',
		hoursAgo: '{n} h ago',
		daysAgo: '{n} days ago',
		wib: 'WIB',
		cached: 'cached {ttl}',
		seconds: '{n} s',
		minutes: '{n} min',
		hours: '{n} h',
		required: 'required',
		optional: 'optional',
		inPath: 'in path',
		none: 'none'
	},

	footer: {
		source: 'Data source: BMKG (Badan Meteorologi, Klimatologi, dan Geofisika). This project is not affiliated with BMKG.',
		regions: 'Region data: Dukcapil Kemendagri 2024, via wilayah-id.',
		map: 'Map: Natural Earth 1:50m coastlines, equirectangular projection.',
		license: 'Source code under the MIT license. Made by dhanypedia.',
		nav: 'Links',
		openapi: 'OpenAPI reference'
	},

	home: {
		title: 'BMKG API: weather and earthquake data for Indonesia',
		description:
			'Free REST API and MCP server for Indonesian weather forecasts, earthquakes, severe weather warnings and region data, from BMKG open data.',
		h1: 'Weather and earthquake data for Indonesia',
		lead: 'A REST API and MCP server for BMKG open data: earthquakes, three-day forecasts for every village, severe weather warnings and region lookup. Every endpoint works without an API key. The source code is open under the MIT license.',
		openExplorer: 'Open the API explorer',
		readDocs: 'Read the documentation',
		indexTitle: 'Endpoints',
		indexNote: 'Every endpoint is a GET under /v1. Any row opens in the explorer.',
		colEndpoint: 'Endpoint',
		colReturns: 'Returns',
		colCache: 'Cached for',
		explorerTitle: 'API explorer',
		explorerNote:
			'Requests go to the real API. Each result is shown as a preview, as raw JSON, with its cache headers, and as code to copy.',
		mcpTitle: 'MCP server',
		mcpNote:
			'The same data is available as 13 read-only tools for Claude, Cursor, VS Code and other MCP clients. The server is hosted, so a client needs one URL.',
		mcpPrompts: 'Questions an assistant can then answer:',
		mcpMore: 'Tool list and response format',
		mcpClient: 'MCP client',
		sharedTitle: 'Shared instance',
		sharedNote:
			'This public instance is shared. The limit is 30 requests per minute per endpoint for each client, and responses are cached at the CDN. For production traffic there is a Docker image to run separately.',
		selfHostGuide: 'Self-hosting guide',
		sourceCode: 'Source code on GitHub'
	},

	map: {
		plateTitle: 'Recent earthquakes and active weather warnings',
		plateLabel: 'Map of recent earthquakes in Indonesia',
		updated: 'Updated {time}',
		loading: 'Loading data',
		unreachable: 'The API is unreachable. The map shows coastlines only.',
		legend: 'Legend',
		legendQuake: 'Earthquake epicentre, sized by magnitude',
		legendLatest: 'Latest earthquake',
		legendTrace: 'Seismogram trace: one burst per earthquake',
		scaleNote: 'Scale holds at the equator',
		latest: 'Latest earthquake',
		selected: 'Selected earthquake',
		depth: '{km} km deep',
		felt: 'Felt: {text}',
		noQuakes: 'Earthquake data is not available yet.',
		warnings: 'Active weather warnings',
		warningsCount: '{n} warnings',
		noWarnings: 'No province has an active warning.',
		warningsUnavailable: 'Warning data is not available yet.',
		openWarning: 'Open this warning in the explorer',
		drawnFrom: 'This map is drawn from four requests:',
		legendWarning: 'Area under a weather warning',
		warningLabel: 'Warning: {event}, {province}',
		validUntil: 'Valid until {time}',
		otherWarnings: 'Other provinces:',
		warningsMissing: '{n} warnings could not be read from BMKG.',
		traceCaption: '{n} earthquakes over the last {days} days',
		traceWaiting: 'Waiting for earthquake data',
		now: 'now',
		quakeLabel: 'Magnitude {m}, {region}',
		quakeLayer: 'Earthquakes on the map. Arrow keys move between earthquakes.',
		warningLayer: 'Warnings on the map. Arrow keys move between provinces.',
		east: 'E',
		south: 'S',
		north: 'N',
		seas: {
			java: 'Java Sea',
			indian: 'Indian Ocean',
			banda: 'Banda Sea',
			flores: 'Flores Sea',
			celebes: 'Celebes Sea',
			arafura: 'Arafura Sea',
			natuna: 'Natuna Sea',
			pacific: 'Pacific Ocean'
		},
		neighbours: {
			png: 'Papua New Guinea',
			malaysia: 'Malaysia',
			timor: 'Timor-Leste',
			philippines: 'Philippines'
		},
		islands: {
			sumatra: 'Sumatra',
			java: 'Java',
			kalimantan: 'Kalimantan',
			sulawesi: 'Sulawesi',
			papua: 'Papua'
		}
	},

	groups: {
		Earthquakes: 'Earthquakes',
		Weather: 'Weather',
		Warnings: 'Warnings',
		Regions: 'Regions'
	},

	endpoints: {
		'earthquake-latest': {
			summary: 'The latest earthquake',
			detail: 'The single latest earthquake: magnitude, depth, coordinates, region, tsunami potential, felt reports and a shakemap URL. Times are UTC.'
		},
		'earthquake-recent': {
			summary: 'Last 15 earthquakes of magnitude 5.0 or more',
			detail: 'The last 15 earthquakes of magnitude 5.0 or more, newest first.'
		},
		'earthquake-felt': {
			summary: 'Last 15 earthquakes that were felt',
			detail: 'The last 15 earthquakes reported as felt, small ones included, with where and how strongly each was felt.'
		},
		'earthquake-nearby': {
			summary: 'Recent earthquakes around a point',
			detail: "Earthquakes from the recent and felt lists within a radius of a point, nearest first, each with distance_km. An empty list means none among BMKG's latest records, not none ever."
		},
		weather: {
			summary: '3-day forecast for one village',
			detail: 'The forecast for one village over three days in 3-hour steps: temperature, humidity, weather in Indonesian and English, wind and cloud cover. visibility_m can be null.'
		},
		'weather-current': {
			summary: 'Current weather for one village',
			detail: "The forecast entry closest to now for one village. This is BMKG's forecast for the current 3-hour slot, not a station observation."
		},
		'nowcast-warnings': {
			summary: 'All active warnings with their areas',
			detail: 'Every active warning in full in one request, each with its affected areas as polygons. meta.missing lists the codes of warnings whose detail could not be read from BMKG, so a short list is not mistaken for a complete one.'
		},
		nowcast: {
			summary: 'Provinces with an active warning',
			detail: 'Provinces that currently have a severe weather warning, each with a code for the detail endpoint. An empty list means no warning is active.'
		},
		'nowcast-detail': {
			summary: 'One warning with its affected areas',
			detail: 'One warning in full: event, severity, validity period, description, an infographic URL and the affected areas as polygons. Only codes from the active list exist; any other code returns 404.'
		},
		'nowcast-check': {
			summary: 'Warnings that mention a place',
			detail: 'Active warnings whose text mentions a place name. has_warnings set to false means no active warning mentions it, which is not a forecast of good weather.'
		},
		'wilayah-search': {
			summary: 'Find regions by name',
			detail: 'Regions whose name contains the query, at every level, with code, level and full path.'
		},
		'wilayah-provinces': {
			summary: 'All provinces',
			detail: 'All provinces with their two-digit codes.'
		},
		'wilayah-districts': {
			summary: 'Regencies and cities of a province',
			detail: 'The regencies (kabupaten) and cities (kota) of one province.'
		},
		'wilayah-subdistricts': {
			summary: 'Districts of a regency or city',
			detail: 'The districts (kecamatan) of one regency or city.'
		},
		'wilayah-villages': {
			summary: 'Villages of a district',
			detail: 'The villages (desa and kelurahan) of one district. Their codes are the adm4 codes the weather endpoints take.'
		}
	},

	params: {
		lat: 'Latitude',
		lon: 'Longitude',
		radius_km: 'Radius (km)',
		adm4: 'Village',
		adm4Hint: 'Type a place name to find its code',
		adm4Placeholder: 'Place name or code, for example Tebet',
		noVillage: 'No village matches. Another spelling may work.',
		lang: 'Language',
		langId: 'Indonesian',
		langEn: 'English',
		alertCode: 'Active warning',
		alertsLoading: 'Loading active warnings',
		alertsNone: 'No warning is active right now',
		location: 'Place name',
		province: 'Province code',
		district: 'Regency or city code',
		subdistrict: 'District code',
		query: 'Name'
	},

	reference: {
		lat: 'Latitude, -90 to 90',
		lon: 'Longitude, -180 to 180',
		radius_km: 'Search radius in km, default 100',
		adm4_code: 'Village code as 2.2.2.4 digits, for example 31.74.04.1006',
		lang: 'id (default) or en',
		alert_code: 'A code from /v1/nowcast',
		location: 'Name of a district, city or regency as BMKG writes it',
		q: 'Part of a name, 2 to 100 characters',
		limit: '1 to 100, default 50',
		province: 'Two-digit province code, for example 31',
		district: 'Regency or city code, for example 31.74',
		subdistrict: 'District code, for example 31.74.04'
	},

	explorer: {
		endpoints: 'Endpoints',
		preview: 'Preview',
		json: 'JSON',
		headers: 'Headers',
		code: 'Code',
		fillIn: 'Fill in the parameter above, then run the request.',
		runToSee: 'Run the request to see the response.',
		networkError: 'The request was not sent. Check the connection, then run it again.',
		rejected: 'The request was rejected as invalid.',
		failed: 'The request failed.',
		previewFailed: 'This response cannot be previewed. The JSON tab shows exactly what the API returned.',
		responseBody: 'Response body',
		reproduce: 'Reproduce with curl',
		edge: 'CDN {status}',
		language: 'Programming language',
		headerNotes: {
			'cache-control': 'How long this response may be reused',
			'cf-cache-status': 'HIT means the CDN answered without reaching the server',
			age: 'Seconds since this copy entered a cache',
			'x-cache': "The server's own cache: HIT or MISS",
			'x-cache-ttl': 'Seconds until the server asks BMKG again',
			'x-ratelimit-limit': 'Requests allowed per minute',
			'x-ratelimit-remaining': 'Requests left in the current minute',
			'content-type': 'Format of the body'
		}
	},

	views: {
		noQuakes: "No earthquake matched. BMKG's latest records hold none in that area.",
		quakesLabel: 'Earthquake locations',
		fromPoint: '{km} km from the search point',
		shakemap: 'Open the BMKG shakemap',
		humidity: 'Humidity {v}%',
		wind: 'Wind {v} km/h {dir}',
		cloud: 'Cloud {v}%',
		slot: 'Forecast slot {time} local time',
		chartTitle: 'Temperature over the next {n} days',
		chartHint: 'Move the pointer across the chart',
		chartLabel: 'Temperature forecast from {lo} to {hi} degrees Celsius',
		localTime: '{time} local time',
		noWarning: 'No warning is active.',
		noMention: 'No active warning mentions "{place}". That is not a forecast of good weather.',
		areasLabel: 'Areas covered by the warning',
		areasCount: '{n} warning areas. Hover over one to see its name.',
		noPolygon: 'This warning has no polygon data.',
		infographic: 'BMKG infographic for this warning',
		effective: 'Effective',
		expires: 'Expires',
		urgency: 'Urgency',
		certainty: 'Certainty',
		noActive: 'No province has an active warning right now.',
		showMap: 'Show map',
		noRegion: 'No region matched.',
		code: 'Code',
		name: 'Name',
		next: 'Next step',
		toDistricts: 'Regencies and cities',
		toSubdistricts: 'Districts',
		toVillages: 'Villages',
		toForecast: 'Forecast'
	},

	docs: {
		title: 'Documentation · BMKG API',
		description: 'Reference for the BMKG API: endpoints, response format, errors, caching and rate limits, with examples that run.',
		h1: 'API reference',
		lead: 'Every example on this page runs against the real API.',
		onThisPage: 'On this page',
		basics: 'Basics',
		basicsItems: [
			'Base URL: {base}',
			'Every endpoint is a GET and works without an API key.',
			'CORS is open, so the API can be called from a browser.',
			'The data belongs to BMKG. The attribution value needs to be shown wherever the data is published.'
		],
		format: 'Response format',
		formatOk: 'A successful response always has data, meta and attribution.',
		formatFail: 'A failed response has error, message and status.',
		status: 'Status',
		meaning: 'Meaning',
		statuses: [
			['200', 'Success'],
			['400', 'An argument has the wrong format'],
			['404', 'No data for that code'],
			['422', 'A required parameter is missing or out of range'],
			['429', 'Rate limit exceeded. A retry works after one minute'],
			['503', 'BMKG is unreachable, or this server reached its request budget towards BMKG']
		],
		limits: 'Caching and rate limits',
		limitsIntro:
			'BMKG updates its data at fixed intervals. Every response is cached for as long as its data stays current, on this server and at the CDN in front of it. A request made more often than the cache time receives the same answer.',
		limitsItems: [
			'Cache-Control states how long a response stays fresh.',
			'X-Cache is HIT when this server answered from its cache.',
			'The limit is 30 requests per minute per endpoint for each client. X-RateLimit-Remaining shows what is left.'
		],
		limitsMore: 'For heavier use there is a guide to running a separate instance.',
		openInExplorer: 'Open in the explorer',
		sendFailed: 'The request was not sent.',
		moreLines: '… {n} more lines',
		polygons: 'Working with warning polygons',
		polygonsIntro: 'The warning detail endpoint returns each affected area as a polygon. Two things often go wrong:',
		polygonsItems: [
			'Points are written as [lat, lon]. Most map libraries expect [lon, lat].',
			"One area's list holds several rings joined without a separator."
		],
		polygonsCode: 'The maps on this site split them as follows:'
	},

	mcp: {
		title: 'MCP setup · BMKG API',
		description: 'Connecting Claude, Cursor, VS Code and other MCP clients to Indonesian weather and earthquake data from BMKG.',
		h1: 'MCP server',
		lead: 'Thirteen read-only tools for weather forecasts, earthquakes, severe weather warnings and region lookup. The server is hosted, so most clients need only a URL.',
		connect: 'Connecting a client',
		connectNote: 'The endpoint speaks Streamable HTTP and needs no API key:',
		ownInstance: 'Using a separate API instance',
		ownInstanceNote: 'The local server reads from this public instance by default. The following environment variable points it at another one:',
		clientConfig: 'MCP client config',
		tools: 'Tools',
		toolsNote:
			'Weather tools need a village-level adm4_code such as 31.74.04.1006. search_regions returns one, as does walking from provinces through regencies and districts to villages.',
		colTool: 'Tool',
		colArgs: 'Arguments',
		colReturns: 'Returns',
		prompts: 'The server also offers seven prompts: earthquake, weather, region lookup, emergency preparedness, travel, research and daily briefing.',
		response: 'Response format',
		responseNote: 'Every tool returns the same envelope. The status value is checked first.',
		toolResult: 'Tool result',
		errorsNote: 'On failure, status is "error", data is null and error.code holds one of these codes:',
		colCode: 'Code',
		errors: [
			['INVALID_ARGUMENT', 'The API rejected an argument'],
			['NOT_FOUND', 'No data for that input, for example a code without a forecast'],
			['RATE_LIMITED', 'Too many requests. A retry works after one minute'],
			['UPSTREAM_UNAVAILABLE', 'BMKG or the API is temporarily unreachable'],
			['INTERNAL_ERROR', 'Any other failure. meta.trace_id identifies it in a report']
		],
		schemaNote: "Arguments that do not match a tool's schema, such as a malformed code or a latitude out of range, are rejected by the protocol before the tool runs.",
		upgrading: 'Upgrading from 1.x',
		upgradingItems: [
			'Results are wrapped in the envelope above. What used to be the whole result is now under data.',
			'Failures used to be {"error": "<text>"}. They are now status "error" with a code.',
			'The debug_ping and get_cache_stats tools were removed.',
			'search_regions returns 20 results by default. The limit argument raises that.'
		],
		tools_returns: {
			get_latest_earthquake: 'The latest earthquake',
			get_recent_earthquakes: 'The last 15 earthquakes of magnitude 5.0 or more',
			get_felt_earthquakes: 'The last 15 earthquakes that were felt',
			get_nearby_earthquakes: 'Recent earthquakes around a point',
			get_weather_forecast: '3-day forecast in 3-hour steps',
			get_current_weather: 'Forecast for the current 3-hour slot',
			get_weather_warnings: 'Active severe weather warnings by province',
			check_location_warnings: 'Active warnings that mention a place',
			search_regions: 'Regions matching a name, with codes',
			get_provinces: 'Provinces with two-digit codes',
			get_districts: 'Regencies and cities of a province',
			get_subdistricts: 'Districts of a regency or city',
			get_villages: 'Villages, with adm4 codes'
		},
		clients: {
			'claude-code': 'One command. Also available as a plugin: claude plugin marketplace add dhanyyudi/bmkg-api, then claude plugin install bmkg@bmkg-api.',
			'claude-desktop': 'Settings, Connectors, Add custom connector, then paste this URL. The same works on claude.ai.',
			cursor: 'Goes into ~/.cursor/mcp.json.',
			vscode: 'Adds the server to the user profile.',
			stdio: 'For clients that only speak stdio: mcp-remote bridges to the hosted server.',
			local: 'Runs the server on the local machine with uv. Needs Python 3.12 or newer.'
		},
		clientLabels: { stdio: 'Other clients', local: 'Run locally' }
	},

	selfHost: {
		title: 'Self-hosting · BMKG API',
		description: 'Running a separate BMKG API instance with Docker: one image, no account, separate rate limits.',
		h1: 'Running a separate instance',
		lead: 'The public instance is shared and rate limited. A separate instance has limits of its own, and the whole API runs in one container.',
		docker: 'Docker',
		dockerNote: 'The image is built for amd64 and arm64 from the main branch, and includes this website.',
		runImage: 'Run the image',
		compose: 'Docker Compose with Redis',
		composeNote:
			"The repository's docker-compose.yml adds Redis so the cache survives a container restart. The stack joins an external network named private_network and opens no host port, which suits a reverse proxy or a tunnel. A ports entry gives direct access.",
		cloneStart: 'Clone and start',
		local: 'Local development',
		localNote: 'Python 3.12 or newer for the API, Node 22 or newer for the website.',
		fromSource: 'From source',
		config: 'Configuration',
		configNote: 'All settings are environment variables, read from .env when present.',
		colVariable: 'Variable',
		colDefault: 'Default',
		colPurpose: 'Purpose',
		empty: '(empty)',
		settings: {
			REDIS_URL: 'Cache backend. Without Redis the API uses an in-process cache.',
			RATE_LIMIT_ANONYMOUS: 'Requests allowed per client, per endpoint.',
			CLIENT_IP_HEADER: 'Header carrying the real client IP behind a proxy, for example CF-Connecting-IP. Left empty unless every request arrives through that proxy.',
			UPSTREAM_MAX_PER_MINUTE: 'Most requests per minute sent to each BMKG host. 0 removes the cap.',
			CACHE_TTL_EARTHQUAKE_LATEST: 'Seconds the latest earthquake is cached.',
			CACHE_TTL_EARTHQUAKE_LIST: 'Seconds earthquake lists are cached.',
			CACHE_TTL_NOWCAST: 'Seconds weather warnings are cached.',
			CACHE_TTL_WEATHER: 'Seconds a forecast is cached.',
			CACHE_TTL_WILAYAH: 'Cache lifetime sent for region data.'
		},
		public: 'Putting it on the internet',
		publicNote: 'A public instance gets flooded with requests sooner or later. Three things keep it up:',
		publicItems: [
			['Caching at a CDN.', "Every /v1 response carries Cache-Control matching its data's lifetime. With a CDN in front that honours the header, repeat requests never reach the server."],
			['Rate limiting by the real client.', 'Behind a proxy, CLIENT_IP_HEADER needs a value. Without it every visitor counts as the proxy.'],
			['A cap towards BMKG.', "UPSTREAM_MAX_PER_MINUTE keeps abuse of an instance from getting the server's IP blocked by BMKG."]
		],
		mcp: 'MCP server',
		mcpNote: 'The same image runs the MCP endpoint: a second container with the command python -m mcp_server.http_server, and BMKG_API_BASE_URL pointing at the API.',
		mcpLink: 'MCP setup guide',
		comments: { website: '# The website is a separate build, written to ./landing', dev: '# API on http://localhost:8099' }
	}
};
