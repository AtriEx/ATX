import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { UserData } from '$lib/types';
import { createClient } from '@supabase/supabase-js';
import { PRIVATE_SUPABASE_SERVICE_ROLE_KEY } from '$env/static/private';
import { PUBLIC_SUPABASE_URL } from '$env/static/public';

// PersonalProfile represents the data of the currently logged in user
// UserProfile represents the data of the user whose profile is being viewed

const adminSupabase = createClient(PUBLIC_SUPABASE_URL, PRIVATE_SUPABASE_SERVICE_ROLE_KEY);

export const load = (async ({ parent, params }) => {
	//TODO - fetch user data from database
	const data = await parent();
	const username = params.username;
	if (username === '') throw error(404, 'User not found');

	const { data: profile } = await adminSupabase
		.from('profiles')
		.select('*')
		.eq('username', username)
		.single();
	console.log(profile);

	const userData: UserData = {
		...profile,
		joined_at: new Date(),
		badges: data.profile?.badges || [],
		stocks: data.profile?.stocks || []
	};

	console.log(userData);
	if (!userData) throw error(404, 'User not found');

	return {
		personalProfile: data.profile,
		userProfile: { ...userData, joined_at: new Date(), username } satisfies UserData
	};
}) satisfies PageServerLoad;
