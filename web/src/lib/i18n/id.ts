// Teks situs dalam bahasa Indonesia. Berkas ini menjadi acuan bentuk kamus:
// en.ts harus punya kunci yang sama.

export const id = {
	locale: 'id',
	htmlLang: 'id',
	numberLocale: 'id-ID',
	/** Bahasa teks peringatan yang diminta dari API. */
	apiLang: 'id',

	/** Tertulis dalam bahasa tujuan, supaya terbaca oleh orang yang mencarinya. */
	switchTo: { title: 'Switch to English', locale: 'en' },

	nav: {
		skip: 'Lompat ke isi',
		main: 'Utama',
		explorer: 'Explorer',
		docs: 'Dokumentasi',
		mcp: 'MCP',
		selfHost: 'Self-host',
		github: 'GitHub'
	},

	status: {
		checking: 'Memeriksa API',
		online: 'API {version} aktif',
		offline: 'API tidak terjangkau',
		title: 'Hasil pemeriksaan /health'
	},

	common: {
		copy: 'Salin',
		copied: 'Tersalin',
		copyFailed: 'Gagal menyalin',
		run: 'Jalankan',
		running: 'Menjalankan',
		runAgain: 'Jalankan lagi',
		tryIt: 'Coba',
		justNow: 'baru saja',
		minutesAgo: '{n} menit lalu',
		hoursAgo: '{n} jam lalu',
		daysAgo: '{n} hari lalu',
		wib: 'WIB',
		cached: 'cache {ttl}',
		seconds: '{n} detik',
		minutes: '{n} menit',
		hours: '{n} jam',
		required: 'wajib',
		optional: 'opsional',
		inPath: 'di path',
		none: 'tidak ada'
	},

	footer: {
		source: 'Sumber data: BMKG (Badan Meteorologi, Klimatologi, dan Geofisika). Proyek ini tidak berafiliasi dengan BMKG.',
		regions: 'Data wilayah: Dukcapil Kemendagri 2024, melalui wilayah-id.',
		map: 'Peta: garis pantai Natural Earth 1:50m, proyeksi ekuirektangular.',
		license: 'Open source berlisensi MIT. Dibuat oleh dhanypedia.',
		nav: 'Tautan',
		openapi: 'Referensi OpenAPI'
	},

	home: {
		title: 'BMKG API: data cuaca dan gempa bumi Indonesia',
		description:
			'REST API dan server MCP gratis untuk prakiraan cuaca, gempa bumi, peringatan dini cuaca, dan data wilayah Indonesia dari data terbuka BMKG.',
		h1: 'Data cuaca dan gempa bumi Indonesia',
		lead: 'REST API dan server MCP untuk data terbuka BMKG: gempa bumi, prakiraan cuaca tiga hari per desa, peringatan dini cuaca, dan pencarian wilayah. Semua endpoint dapat dipanggil tanpa API key. Open source dengan lisensi MIT.',
		openExplorer: 'Buka API Explorer',
		readDocs: 'Baca dokumentasi',
		indexTitle: 'Daftar endpoint',
		indexNote: 'Semua endpoint memakai GET di bawah /v1. Baris mana pun dapat dibuka di Explorer.',
		colEndpoint: 'Endpoint',
		colReturns: 'Isi',
		colCache: 'Masa cache',
		explorerTitle: 'API Explorer',
		explorerNote:
			'Request dijalankan ke API yang sebenarnya. Hasilnya tampil sebagai preview, raw JSON, header cache, dan kode siap salin.',
		mcpTitle: 'Server MCP',
		mcpNote:
			'Data yang sama tersedia sebagai 13 tool read-only untuk Claude, Cursor, VS Code, dan client MCP lain. Servernya di-hosting, jadi client cukup diberi satu URL.',
		mcpPrompts: 'Contoh pertanyaan untuk asisten:',
		mcpMore: 'Daftar tool dan format response',
		mcpClient: 'Client MCP',
		sharedTitle: 'Instance bersama',
		sharedNote:
			'Instance publik ini dipakai bersama. Rate limit-nya 30 request per menit per endpoint untuk tiap client, dan response di-cache di CDN. Untuk beban production tersedia image Docker yang dapat dijalankan sendiri.',
		selfHostGuide: 'Panduan self-host',
		sourceCode: 'Source code di GitHub'
	},

	map: {
		plateTitle: 'Gempa bumi terkini dan peringatan dini cuaca',
		plateLabel: 'Peta gempa bumi terkini di Indonesia',
		updated: 'Diperbarui {time}',
		loading: 'Memuat data',
		unreachable: 'API tidak terjangkau. Peta menampilkan garis pantai saja.',
		legend: 'Keterangan',
		legendQuake: 'Episentrum gempa, ukuran menurut magnitudo',
		legendLatest: 'Gempa terbaru',
		legendTrace: 'Jejak seismogram: tiap lonjakan satu gempa',
		scaleNote: 'Skala berlaku di khatulistiwa',
		latest: 'Gempa terbaru',
		selected: 'Gempa terpilih',
		depth: 'kedalaman {km} km',
		felt: 'Dirasakan: {text}',
		noQuakes: 'Data gempa belum tersedia.',
		warnings: 'Peringatan dini cuaca aktif',
		warningsCount: '{n} peringatan',
		noWarnings: 'Tidak ada provinsi dengan peringatan aktif.',
		warningsUnavailable: 'Data peringatan belum tersedia.',
		openWarning: 'Buka peringatan ini di Explorer',
		drawnFrom: 'Peta ini digambar dari empat request:',
		legendWarning: 'Wilayah dengan peringatan dini cuaca',
		warningLabel: 'Peringatan {event}, {province}',
		validUntil: 'Berlaku sampai {time}',
		otherWarnings: 'Provinsi lain:',
		warningsMissing: '{n} peringatan tidak terbaca dari BMKG.',
		traceCaption: '{n} gempa dalam {days} hari terakhir',
		traceWaiting: 'Menunggu data gempa',
		now: 'sekarang',
		quakeLabel: 'Magnitudo {m}, {region}',
		quakeLayer: 'Gempa pada peta. Tombol panah berpindah antargempa.',
		warningLayer: 'Peringatan pada peta. Tombol panah berpindah antarprovinsi.',
		east: 'BT',
		south: 'LS',
		north: 'LU',
		seas: {
			java: 'Laut Jawa',
			indian: 'Samudra Hindia',
			banda: 'Laut Banda',
			flores: 'Laut Flores',
			celebes: 'Laut Sulawesi',
			arafura: 'Laut Arafura',
			natuna: 'Laut Natuna',
			pacific: 'Samudra Pasifik'
		},
		neighbours: {
			png: 'Papua Nugini',
			malaysia: 'Malaysia',
			timor: 'Timor-Leste',
			philippines: 'Filipina'
		},
		islands: {
			sumatra: 'Sumatera',
			java: 'Jawa',
			kalimantan: 'Kalimantan',
			sulawesi: 'Sulawesi',
			papua: 'Papua'
		}
	},

	groups: {
		Earthquakes: 'Gempa bumi',
		Weather: 'Cuaca',
		Warnings: 'Peringatan dini',
		Regions: 'Wilayah'
	},

	endpoints: {
		'earthquake-latest': {
			summary: 'Gempa terbaru',
			detail: 'Satu gempa terbaru: magnitudo, kedalaman, koordinat, wilayah, potensi tsunami, laporan dirasakan, dan URL shakemap. Waktu dalam UTC.'
		},
		'earthquake-recent': {
			summary: '15 gempa terakhir bermagnitudo 5,0 ke atas',
			detail: '15 gempa terakhir bermagnitudo 5,0 ke atas, dari yang terbaru.'
		},
		'earthquake-felt': {
			summary: '15 gempa terakhir yang dirasakan',
			detail: '15 gempa terakhir yang dilaporkan dirasakan, termasuk gempa kecil, beserta tempat dan intensitasnya.'
		},
		'earthquake-nearby': {
			summary: 'Gempa terkini di sekitar satu titik',
			detail: 'Gempa dari daftar terkini dan dirasakan dalam radius tertentu dari satu titik, dari yang terdekat, dengan distance_km. Daftar kosong berarti tidak ada di antara catatan terbaru BMKG, bukan tidak pernah ada.'
		},
		weather: {
			summary: 'Prakiraan 3 hari untuk satu desa',
			detail: 'Prakiraan satu desa atau kelurahan untuk tiga hari, tiap 3 jam: suhu, kelembapan, cuaca dalam bahasa Indonesia dan Inggris, angin, dan tutupan awan. visibility_m dapat bernilai null.'
		},
		'weather-current': {
			summary: 'Cuaca saat ini untuk satu desa',
			detail: 'Entri prakiraan yang paling dekat dengan waktu sekarang untuk satu desa. Ini prakiraan BMKG untuk slot 3 jam berjalan, bukan pengamatan stasiun.'
		},
		'nowcast-warnings': {
			summary: 'Semua peringatan aktif beserta wilayahnya',
			detail: 'Semua peringatan aktif secara lengkap dalam satu request, masing-masing dengan wilayah terdampak sebagai poligon. meta.missing memuat kode peringatan yang rinciannya tidak terbaca dari BMKG, supaya daftar yang pendek tidak dikira lengkap.'
		},
		nowcast: {
			summary: 'Provinsi dengan peringatan aktif',
			detail: 'Provinsi yang sedang punya peringatan dini cuaca, masing-masing dengan kode untuk endpoint rinciannya. Daftar kosong berarti tidak ada peringatan aktif.'
		},
		'nowcast-detail': {
			summary: 'Satu peringatan beserta wilayah terdampak',
			detail: 'Satu peringatan secara lengkap: kejadian, tingkat keparahan, masa berlaku, uraian, URL infografik, dan wilayah terdampak sebagai poligon. Hanya kode dari daftar aktif yang tersedia; kode lain menghasilkan 404.'
		},
		'nowcast-check': {
			summary: 'Peringatan yang menyebut satu tempat',
			detail: 'Peringatan aktif yang teksnya menyebut nama tempat. has_warnings bernilai false berarti tidak ada peringatan aktif yang menyebutnya, bukan prakiraan cuaca baik.'
		},
		'wilayah-search': {
			summary: 'Cari wilayah menurut nama',
			detail: 'Wilayah yang namanya memuat kata pencarian, di semua tingkat, dengan kode, tingkat, dan path lengkapnya.'
		},
		'wilayah-provinces': {
			summary: 'Semua provinsi',
			detail: 'Semua provinsi dengan kode dua digit.'
		},
		'wilayah-districts': {
			summary: 'Kabupaten dan kota dalam satu provinsi',
			detail: 'Kabupaten dan kota dalam satu provinsi.'
		},
		'wilayah-subdistricts': {
			summary: 'Kecamatan dalam satu kabupaten atau kota',
			detail: 'Kecamatan dalam satu kabupaten atau kota.'
		},
		'wilayah-villages': {
			summary: 'Desa dan kelurahan dalam satu kecamatan',
			detail: 'Desa dan kelurahan dalam satu kecamatan. Kodenya adalah kode adm4 yang dipakai endpoint cuaca.'
		}
	},

	params: {
		lat: 'Lintang',
		lon: 'Bujur',
		radius_km: 'Radius (km)',
		adm4: 'Desa',
		adm4Hint: 'Ketik nama tempat untuk mencari kodenya',
		adm4Placeholder: 'Nama tempat atau kode, misalnya Tebet',
		noVillage: 'Tidak ada desa yang cocok. Coba ejaan lain.',
		lang: 'Bahasa',
		langId: 'Indonesia',
		langEn: 'Inggris',
		alertCode: 'Peringatan aktif',
		alertsLoading: 'Memuat peringatan aktif',
		alertsNone: 'Tidak ada peringatan aktif saat ini',
		location: 'Nama tempat',
		province: 'Kode provinsi',
		district: 'Kode kabupaten atau kota',
		subdistrict: 'Kode kecamatan',
		query: 'Nama'
	},

	reference: {
		lat: 'Lintang, -90 sampai 90',
		lon: 'Bujur, -180 sampai 180',
		radius_km: 'Radius pencarian dalam km, default 100',
		adm4_code: 'Kode desa dengan pola 2.2.2.4 digit, misalnya 31.74.04.1006',
		lang: 'id (default) atau en',
		alert_code: 'Kode dari /v1/nowcast',
		location: 'Nama kecamatan, kota, atau kabupaten seperti ditulis BMKG',
		q: 'Bagian dari nama, 2 sampai 100 karakter',
		limit: '1 sampai 100, default 50',
		province: 'Kode provinsi dua digit, misalnya 31',
		district: 'Kode kabupaten atau kota, misalnya 31.74',
		subdistrict: 'Kode kecamatan, misalnya 31.74.04'
	},

	explorer: {
		endpoints: 'Endpoint',
		preview: 'Preview',
		json: 'JSON',
		headers: 'Header',
		code: 'Kode',
		fillIn: 'Isi parameter di atas, lalu jalankan request.',
		runToSee: 'Jalankan request untuk melihat response.',
		networkError: 'Request tidak terkirim. Periksa koneksi, lalu coba lagi.',
		rejected: 'Request ditolak karena tidak valid.',
		failed: 'Request gagal.',
		previewFailed: 'Preview tidak tersedia untuk response ini. Tab JSON menampilkan isi persis dari API.',
		responseBody: 'Isi response',
		reproduce: 'Ulangi dengan curl',
		edge: 'CDN {status}',
		language: 'Bahasa pemrograman',
		headerNotes: {
			'cache-control': 'Berapa lama response ini boleh dipakai ulang',
			'cf-cache-status': 'HIT berarti CDN menjawab tanpa menghubungi server',
			age: 'Detik sejak salinan ini masuk cache',
			'x-cache': 'Cache milik server: HIT atau MISS',
			'x-cache-ttl': 'Detik sampai server bertanya lagi ke BMKG',
			'x-ratelimit-limit': 'Request yang diizinkan per menit',
			'x-ratelimit-remaining': 'Sisa request dalam menit ini',
			'content-type': 'Format isi response'
		}
	},

	views: {
		noQuakes: 'Tidak ada gempa yang cocok. Di antara catatan terbaru BMKG tidak ada gempa di area itu.',
		quakesLabel: 'Lokasi gempa',
		fromPoint: '{km} km dari titik pencarian',
		shakemap: 'Buka shakemap BMKG',
		humidity: 'Kelembapan {v}%',
		wind: 'Angin {v} km/jam {dir}',
		cloud: 'Awan {v}%',
		slot: 'Slot prakiraan {time} waktu setempat',
		chartTitle: 'Suhu selama {n} hari ke depan',
		chartHint: 'Geser kursor di atas grafik',
		chartLabel: 'Prakiraan suhu dari {lo} sampai {hi} derajat Celsius',
		localTime: '{time} waktu setempat',
		noWarning: 'Tidak ada peringatan aktif.',
		noMention: 'Tidak ada peringatan aktif yang menyebut "{place}". Itu bukan prakiraan cuaca baik.',
		areasLabel: 'Wilayah yang dicakup peringatan',
		areasCount: '{n} wilayah peringatan. Arahkan kursor untuk melihat namanya.',
		noPolygon: 'Peringatan ini tidak punya data poligon.',
		infographic: 'Infografik BMKG untuk peringatan ini',
		effective: 'Berlaku',
		expires: 'Berakhir',
		urgency: 'Urgensi',
		certainty: 'Kepastian',
		noActive: 'Tidak ada provinsi dengan peringatan aktif saat ini.',
		showMap: 'Lihat peta',
		noRegion: 'Tidak ada wilayah yang cocok.',
		code: 'Kode',
		name: 'Nama',
		next: 'Langkah berikutnya',
		toDistricts: 'Kabupaten dan kota',
		toSubdistricts: 'Kecamatan',
		toVillages: 'Desa',
		toForecast: 'Prakiraan'
	},

	docs: {
		title: 'Dokumentasi · BMKG API',
		description: 'Referensi BMKG API: endpoint, format response, error, cache, dan rate limit, dengan contoh yang dapat dijalankan.',
		h1: 'Referensi API',
		lead: 'Setiap contoh di halaman ini dapat dijalankan langsung ke API.',
		onThisPage: 'Di halaman ini',
		basics: 'Dasar',
		basicsItems: [
			'URL dasar: {base}',
			'Semua endpoint memakai GET dan dapat dipanggil tanpa API key.',
			'CORS terbuka, sehingga API dapat dipanggil dari browser.',
			'Data milik BMKG. Nilai attribution perlu ditampilkan saat data dipublikasikan.'
		],
		format: 'Format response',
		formatOk: 'Response berhasil selalu memuat data, meta, dan attribution.',
		formatFail: 'Response gagal memuat error, message, dan status.',
		status: 'Status',
		meaning: 'Arti',
		statuses: [
			['200', 'Berhasil'],
			['400', 'Format argumen salah'],
			['404', 'Tidak ada data untuk kode itu'],
			['422', 'Parameter wajib tidak ada atau di luar rentang'],
			['429', 'Rate limit terlampaui. Coba lagi setelah satu menit'],
			['503', 'BMKG tidak terjangkau, atau server ini mencapai batas request-nya ke BMKG']
		],
		limits: 'Cache dan rate limit',
		limitsIntro:
			'BMKG memperbarui datanya pada selang tetap. Setiap response di-cache selama datanya masih berlaku, di server ini dan di CDN di depannya. Request yang lebih sering dari masa cache menerima jawaban yang sama.',
		limitsItems: [
			'Cache-Control menyatakan berapa lama response tetap fresh.',
			'X-Cache bernilai HIT saat server ini menjawab dari cache.',
			'Rate limit-nya 30 request per menit per endpoint untuk tiap client. X-RateLimit-Remaining menunjukkan sisa jatah.'
		],
		limitsMore: 'Untuk kebutuhan yang lebih besar tersedia panduan menjalankan instance sendiri.',
		openInExplorer: 'Buka di Explorer',
		sendFailed: 'Request tidak terkirim.',
		moreLines: '… {n} baris lagi',
		polygons: 'Mengolah poligon peringatan',
		polygonsIntro: 'Endpoint rincian peringatan mengembalikan tiap wilayah terdampak sebagai poligon. Ada dua hal yang sering keliru:',
		polygonsItems: [
			'Titik ditulis sebagai [lintang, bujur]. Sebagian besar library peta meminta [bujur, lintang].',
			'Daftar satu wilayah memuat beberapa ring yang disambung tanpa pemisah.'
		],
		polygonsCode: 'Peta di situs ini memisahkannya dengan cara berikut:'
	},

	mcp: {
		title: 'Setup MCP · BMKG API',
		description: 'Menghubungkan Claude, Cursor, VS Code, dan client MCP lain ke data cuaca dan gempa bumi Indonesia dari BMKG.',
		h1: 'Server MCP',
		lead: 'Tiga belas tool read-only untuk prakiraan cuaca, gempa bumi, peringatan dini cuaca, dan pencarian wilayah. Servernya di-hosting, jadi sebagian besar client hanya butuh satu URL.',
		connect: 'Menghubungkan client',
		connectNote: 'Endpoint memakai Streamable HTTP dan tidak butuh API key:',
		ownInstance: 'Memakai instance API sendiri',
		ownInstanceNote: 'Server lokal membaca dari instance publik ini secara default. Environment variable berikut mengarahkannya ke instance lain:',
		clientConfig: 'Konfigurasi client MCP',
		tools: 'Tool',
		toolsNote:
			'Tool cuaca membutuhkan adm4_code tingkat desa, misalnya 31.74.04.1006. Kode itu didapat dari search_regions, atau dengan menelusuri provinsi, kabupaten, kecamatan, lalu desa.',
		colTool: 'Tool',
		colArgs: 'Argumen',
		colReturns: 'Hasil',
		prompts: 'Server juga menyediakan tujuh prompt: gempa bumi, cuaca, pencarian wilayah, kesiapsiagaan darurat, perjalanan, riset, dan ringkasan harian.',
		response: 'Format response',
		responseNote: 'Semua tool mengembalikan envelope yang sama. Nilai status diperiksa lebih dulu.',
		toolResult: 'Hasil tool',
		errorsNote: 'Saat gagal, status bernilai "error", data bernilai null, dan error.code berisi salah satu kode berikut:',
		colCode: 'Kode',
		errors: [
			['INVALID_ARGUMENT', 'API menolak salah satu argumen'],
			['NOT_FOUND', 'Tidak ada data untuk input itu, misalnya kode yang tidak punya prakiraan'],
			['RATE_LIMITED', 'Terlalu banyak request. Tunggu satu menit'],
			['UPSTREAM_UNAVAILABLE', 'BMKG atau API sedang tidak terjangkau'],
			['INTERNAL_ERROR', 'Kegagalan lain. Sertakan meta.trace_id saat melaporkannya']
		],
		schemaNote: 'Argumen yang tidak sesuai schema tool, seperti kode yang salah bentuk atau lintang di luar rentang, ditolak oleh protokol sebelum tool berjalan.',
		upgrading: 'Pindah dari versi 1.x',
		upgradingItems: [
			'Hasil dibungkus envelope di atas. Yang dulu menjadi seluruh hasil kini berada di data.',
			'Kegagalan dulu berbentuk {"error": "<teks>"}. Kini berbentuk status "error" dengan kode.',
			'Tool debug_ping dan get_cache_stats dihapus.',
			'search_regions mengembalikan 20 hasil secara default. Argumen limit menambahnya.'
		],
		tools_returns: {
			get_latest_earthquake: 'Gempa terbaru',
			get_recent_earthquakes: '15 gempa terakhir bermagnitudo 5,0 ke atas',
			get_felt_earthquakes: '15 gempa terakhir yang dirasakan',
			get_nearby_earthquakes: 'Gempa terkini di sekitar satu titik',
			get_weather_forecast: 'Prakiraan 3 hari tiap 3 jam',
			get_current_weather: 'Prakiraan untuk slot 3 jam berjalan',
			get_weather_warnings: 'Peringatan dini cuaca aktif per provinsi',
			check_location_warnings: 'Peringatan aktif yang menyebut satu tempat',
			search_regions: 'Wilayah yang cocok dengan nama, beserta kodenya',
			get_provinces: 'Provinsi dengan kode dua digit',
			get_districts: 'Kabupaten dan kota dalam satu provinsi',
			get_subdistricts: 'Kecamatan dalam satu kabupaten atau kota',
			get_villages: 'Desa dan kelurahan, dengan kode adm4'
		},
		clients: {
			'claude-code': 'Satu perintah. Tersedia juga sebagai plugin: claude plugin marketplace add dhanyyudi/bmkg-api, lalu claude plugin install bmkg@bmkg-api.',
			'claude-desktop': 'Settings, Connectors, Add custom connector, lalu tempel URL ini. Berlaku juga di claude.ai.',
			cursor: 'Ditambahkan ke ~/.cursor/mcp.json.',
			vscode: 'Menambahkan server ke profil pengguna.',
			stdio: 'Untuk client yang hanya mendukung stdio: mcp-remote menjembatani ke server yang di-hosting.',
			local: 'Menjalankan server di mesin sendiri dengan uv. Butuh Python 3.12 atau lebih baru.'
		},
		clientLabels: { stdio: 'Client lain', local: 'Jalankan lokal' }
	},

	selfHost: {
		title: 'Self-host · BMKG API',
		description: 'Menjalankan instance BMKG API sendiri dengan Docker: satu image, tanpa akun, dengan rate limit sendiri.',
		h1: 'Menjalankan instance sendiri',
		lead: 'Instance publik dipakai bersama dan dibatasi. Instance sendiri punya batasnya sendiri, dan seluruh API berjalan dalam satu container.',
		docker: 'Docker',
		dockerNote: 'Image dibangun untuk amd64 dan arm64 dari branch utama, dan sudah memuat situs ini.',
		runImage: 'Menjalankan image',
		compose: 'Docker Compose dengan Redis',
		composeNote:
			'Berkas docker-compose.yml di repository menambahkan Redis supaya cache bertahan saat container dimulai ulang. Stack itu bergabung ke network eksternal bernama private_network dan tidak membuka port host, cocok untuk reverse proxy atau tunnel. Untuk akses langsung, tambahkan entri ports.',
		cloneStart: 'Clone lalu jalankan',
		local: 'Development lokal',
		localNote: 'Python 3.12 atau lebih baru untuk API, Node 22 atau lebih baru untuk situs.',
		fromSource: 'Dari source code',
		config: 'Konfigurasi',
		configNote: 'Semua pengaturan berupa environment variable, dibaca dari .env bila ada.',
		colVariable: 'Variabel',
		colDefault: 'Default',
		colPurpose: 'Kegunaan',
		empty: '(kosong)',
		settings: {
			REDIS_URL: 'Backend cache. Tanpa Redis, API memakai cache di dalam proses.',
			RATE_LIMIT_ANONYMOUS: 'Request yang diizinkan per client, per endpoint.',
			CLIENT_IP_HEADER: 'Header pembawa IP client yang sebenarnya di belakang proxy, misalnya CF-Connecting-IP. Dibiarkan kosong kecuali semua request datang lewat proxy itu.',
			UPSTREAM_MAX_PER_MINUTE: 'Jumlah request terbanyak per menit ke tiap host BMKG. Nilai 0 menghapus batas.',
			CACHE_TTL_EARTHQUAKE_LATEST: 'Detik gempa terbaru di-cache.',
			CACHE_TTL_EARTHQUAKE_LIST: 'Detik daftar gempa di-cache.',
			CACHE_TTL_NOWCAST: 'Detik peringatan dini di-cache.',
			CACHE_TTL_WEATHER: 'Detik satu prakiraan di-cache.',
			CACHE_TTL_WILAYAH: 'Masa cache yang dikirim untuk data wilayah.'
		},
		public: 'Membukanya ke internet',
		publicNote: 'Instance publik cepat atau lambat akan dibanjiri request. Tiga hal menjaganya tetap hidup:',
		publicItems: [
			['Cache di CDN.', 'Setiap response /v1 membawa Cache-Control sesuai umur datanya. Dengan CDN di depan yang mematuhi header itu, request berulang tidak sampai ke server.'],
			['Rate limit per client yang sebenarnya.', 'Di belakang proxy, CLIENT_IP_HEADER perlu diisi. Tanpa itu semua pengunjung terhitung sebagai proxy.'],
			['Batas ke BMKG.', 'UPSTREAM_MAX_PER_MINUTE mencegah penyalahgunaan instance berujung pada pemblokiran IP server oleh BMKG.']
		],
		mcp: 'Server MCP',
		mcpNote: 'Image yang sama menjalankan endpoint MCP: container kedua dengan perintah python -m mcp_server.http_server, dan BMKG_API_BASE_URL diarahkan ke API.',
		mcpLink: 'Panduan setup MCP',
		comments: { website: '# Situs dibangun terpisah, hasilnya ditulis ke ./landing', dev: '# API di http://localhost:8099' }
	}
};

export type Messages = typeof id;
