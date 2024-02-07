import { createClient } from '@supabase/supabase-js';
import { PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY } from '$env/static/public';
import { loggedIn, user, profile } from './stores/userData';
import { loginDialog } from './stores/uiStates';
import { get } from 'svelte/store';
import type { Profile } from './types';

export const supabase = createClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY);

export async function login() {
	try {
		if (get(loggedIn)) {
			console.log(getUser());
			return;
		}
		const { data, error } = await supabase.auth.signInWithOAuth({
			provider: 'twitch'
		});
		if (error) throw error;
		console.log('data:', data);
	} catch (error) {
		console.error('Error logging in:', error);
	}
}

export async function logout() {
	try {
		const { error } = await supabase.auth.signOut();
		if (error) throw error;
	} catch (error) {
		console.error('Error logging out:', error);
	}
}

export async function getUser() {
	try {
		const tempUser = await supabase.auth.getUser();
		console.log('tempUser:', tempUser);
		user.set(tempUser.data.user);
		return tempUser;
	} catch (error) {
		console.error('Error getting user:', error);
	}
}

export async function getProfile() {
	try {
		if (get(user) === null) {
			return null;
		}
		console.log('getProfile', get(user));

		const { data: tempProfile } = (await supabase
			.from('profiles')
			.select('username, image, joined_at, networth, balance')
			.eq('userId', get(user)?.id)
			.single()
			.throwOnError()) as { data: Profile };
		console.log('tempProfile:', tempProfile);

		profile.set(tempProfile);
		return profile;
	} catch (error) {
		console.error('Error getting profile:', error);
	}
}

export async function onLogin() {
	console.log('onLogin');
	console.log(get(loggedIn));
	loginDialog.set(false);
	if (get(loggedIn)) {
		return;
	}
	const user = await getUser();
	if (user) {
		console.log('user in onlogin:', user);
		getProfile();
		loggedIn.set(true);
	}
}

export async function onLogout() {
	console.log('onLogout');
	if (!get(loggedIn)) {
		return;
	}
	const tempUser = await getUser();
	if (!tempUser) {
		loggedIn.set(false);
		user.set(null);
	}
}
