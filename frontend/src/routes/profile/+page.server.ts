import { redirect, type ServerLoad } from '@sveltejs/kit';
import { get } from 'svelte/store';
import { profile } from '$lib/stores/userData';

export const load = (({ route }) => {
	// Don't need to check stuff if already on the profile page
	if (route.id === '/profile/[username]') return;

	const prof = get(profile);
	// Redirects to home if not logged in
	if (!prof) throw redirect(303, '/');
	throw redirect(303, `/profile/${prof.username}`);
}) satisfies ServerLoad;
