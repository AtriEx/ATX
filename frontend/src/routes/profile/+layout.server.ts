import { createClient } from '@supabase/supabase-js';
import type { LayoutServerLoad } from './$types';
import { PUBLIC_SUPABASE_URL } from '$env/static/public';
import { PRIVATE_SUPABASE_SERVICE_ROLE_KEY } from '$env/static/private';
import { error, redirect } from '@sveltejs/kit';
import type { Database } from '$lib/supabase.types';

const adminSupabase = createClient<Database>(
	PUBLIC_SUPABASE_URL,
	PRIVATE_SUPABASE_SERVICE_ROLE_KEY
);

export const load = (async ({ route }) => {
	// Don't need to check stuff if already on the profile page
	if (route.id === '/profile/[username]') return;
	const {
		data: { session }
	} = await adminSupabase.auth.getSession();

	// Redirects to home if not logged in
	if (!session) throw redirect(303, '/');

	const { data: profile } = await adminSupabase
		.from('profiles')
		.select('username')
		.eq('username', 'example')
		.single();

	if (!profile) error(404, 'Profile not found');
	throw redirect(303, `/profile/${profile.username}`);
}) satisfies LayoutServerLoad;
