import adapter from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

// In development the pages run on Vite's port, so forward API calls to a local
// API instance (make dev) or to whatever BMKG_API_ORIGIN points at.
const api = process.env.BMKG_API_ORIGIN ?? 'http://127.0.0.1:8099';

export default defineConfig({
	plugins: [
		sveltekit({
			// Plain static files, written to ../landing where the API serves them from.
			adapter: adapter({ pages: '../landing', assets: '../landing', fallback: '404.html', strict: true }),
			// One script and one stylesheet: the site is small, and fewer requests
			// keep a first visit well under the API's rate limit.
			output: { bundleStrategy: 'single' }
		})
	],
	server: {
		proxy: {
			'/v1': { target: api, changeOrigin: true },
			'/health': { target: api, changeOrigin: true },
			'/openapi.json': { target: api, changeOrigin: true }
		}
	}
});
