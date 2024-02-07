import { writable, type Writable } from 'svelte/store';
import { type Profile } from '$lib/types';
import { type User } from '@supabase/gotrue-js/src/lib/types';

export const loggedIn = writable(false);
export const user: Writable<User | null> = writable(null);
export const profile: Writable<Profile | null> = writable(null);

export const username = writable('GlizzMeister');
export const userPfp = writable(
	'https://static-cdn.jtvnw.net/jtv_user_pictures/6c45032c-a049-46c7-bfc9-f9ac2fc8c47e-profile_image-70x70.png'
);
export const currency = writable(1000);
export const netWorth = writable(2000);
