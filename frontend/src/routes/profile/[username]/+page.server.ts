import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { UserData } from '$lib/types';

// PersonalProfile represents the data of the currently logged in user
// UserProfile represents the data of the user whose profile is being viewed

// const adminSupabase = createClient(PUBLIC_SUPABASE_URL, PRIVATE_SUPABASE_SERVICE_ROLE_KEY);

export const load = (async ({ parent, params }) => {
	//TODO - fetch user data from database
	const data = await parent();
	const username = params.username;
	if (username === '') throw error(404, 'User not found');

	// const { data: profile, error } = await adminSupabase.from<UserData>('profiles').select('*').eq('userName', username);

	const userData: UserData | null = data.profile;

	if (!userData) throw error(404, 'User not found');

	return {
		personalProfile: data.profile,
		userProfile: { ...userData, joinDate: new Date(), userName: username } satisfies UserData
	};
}) satisfies PageServerLoad;
