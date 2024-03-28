import { createClient } from '@supabase/supabase-js';
import { PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY } from '$env/static/public';
import { loggedIn, user, profile } from './stores/userData';
import { loginDialog } from './stores/uiStates';
import { get } from 'svelte/store';

// Initialize Supabase client
export const supabase = createClient(PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY);

// Function to handle login
export async function login() {
	try {
		// Prevent login if already logged in
		if (get(loggedIn)) {
			console.log('User already logged in.');
			return;
		}

		const { data, error } = await supabase.auth.signInWithOAuth({ provider: 'twitch' });
		if (error) throw error;

		console.log('Login data:', data);
	} catch (error) {
		console.error('Error logging in:', error);
	}
}

// Function to handle logout
export async function logout() {
	try {
		const { error } = await supabase.auth.signOut();
		if (error) throw error;
	} catch (error) {
		console.error('Error logging out:', error);
	}
}

// Function to get the current user
export async function getUser() {
	try {
		const { data: userData } = await supabase.auth.getUser();
		console.log('Current user:', userData.user);
		user.set(userData.user);
		return userData;
	} catch (error) {
		console.error('Error getting user:', error);
	}
}

// Function to get the profile of the current user
export async function getProfile() {
	try {
		const currentUser = get(user);
		if (!currentUser) return null;

		const { data: userProfile } = await supabase
			.from('profiles')
			.select('username, image, joined_at, networth, balance')
			.eq('userId', currentUser.id)
			.single()
			.throwOnError();

		console.log('User profile:', userProfile);
		profile.set(userProfile);
		return profile;
	} catch (error) {
		console.error('Error getting profile:', error);
	}
}

// Function to handle actions post-login
export async function onLogin() {
	loginDialog.set(false);

	if (get(loggedIn)) return;
	loggedIn.set(true);

	const currentUser = await getUser();
	if (currentUser) {
		const currentProfile = await getProfile();

		if(!currentProfile) loggedIn.set(false);
	}
}

// Function to handle actions post-logout
export async function onLogout() {
	try {
		if (!get(loggedIn)) return;

		const tempUser = await getUser();
		if (!tempUser?.user) {
			// Clear state if logout is successful or if there's no user data
			loggedIn.set(false);
			user.set(null);
			profile.set(null);
		}
	} catch (error) {
		// Ensure state is cleared on error
		loggedIn.set(false);
		user.set(null);
		profile.set(null);
	}
}
