import { createClient } from '@supabase/supabase-js';
import type { PageServerLoad } from './$types';
import { PUBLIC_SUPABASE_URL } from '$env/static/public';
import { PRIVATE_SUPABASE_SERVICE_ROLE_KEY } from '$env/static/private';
import { type Database } from '$lib/supabase.types';
import { error } from '@sveltejs/kit';

const adminClient = createClient<Database>(PUBLIC_SUPABASE_URL, PRIVATE_SUPABASE_SERVICE_ROLE_KEY);

export const load = (async () => {
	const { data, error: pgError } = await adminClient
		.from('profiles')
		.select('username, networth, userId, image')
		.order('networth', { ascending: false })
		.limit(10);

	if (pgError) {
		console.log(pgError);
		error(500, pgError.message);
	}

	return {
		users: data
	};
}) satisfies PageServerLoad;
