import type { PageServerLoad } from './$types';
import { createClient } from '@supabase/supabase-js';
import { PRIVATE_SUPABASE_SERVICE_ROLE_KEY } from '$env/static/private';
import { PUBLIC_SUPABASE_URL } from '$env/static/public';
import { type Database } from '$lib/supabase.types';
import { error } from '@sveltejs/kit';

const adminSupabase = createClient<Database>(
	PUBLIC_SUPABASE_URL,
	PRIVATE_SUPABASE_SERVICE_ROLE_KEY
);

export const load = (async ({ params }) => {
	// Check if the username is empty
	if (!params.username || params.username === '') error(404, 'Profile not found');
	const { data: profile } = await adminSupabase
		.from('profiles')
		.select()
		.eq('username', params.username)
		.single();

	if (!profile) error(404, 'Profile not found');

	// Get the badges, achievements, and stocks
	const { data: flags } = await adminSupabase.from('flags').select();
	const { data: stocks } = await adminSupabase.from('stockInfo').select();

	const badges = flags?.filter((flag) => flag.type === 'badge') || [];
	const achievements = flags?.filter((flag) => flag.type === 'achievement') || [];

	return {
		profile: {
			...profile,
			badges,
			achievements,
			stocks: stocks || []
		}
	};
}) satisfies PageServerLoad;
