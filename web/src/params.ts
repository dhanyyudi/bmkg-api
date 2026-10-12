import { defineParams } from '@sveltejs/kit/params';

export const params = defineParams({
	// Only English has a prefix; Indonesian pages have none.
	lang: (param) => (param === 'en' ? 'en' : undefined)
});
