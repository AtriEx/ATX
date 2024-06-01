import { writable, type Writable } from 'svelte/store';
import { type Profile } from '$lib/types';
import { type User } from '@supabase/supabase-js';

export const loggedIn = writable(false);
export const user: Writable<User | null> = writable(null);
export const profile: Writable<Profile | null> = writable(null);
