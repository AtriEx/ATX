import type { LayoutServerLoad } from './$types';

export const load = (async ({ locals: { getSession } }) => {
	return {
		session: await getSession()
	};
}) satisfies LayoutServerLoad;
