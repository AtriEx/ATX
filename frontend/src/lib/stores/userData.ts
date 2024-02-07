import { writable } from 'svelte/store';

export const isLoggedIn = writable(true);
export const username = writable("GlizzMeister");
export const userPfp = writable("https://static-cdn.jtvnw.net/jtv_user_pictures/6c45032c-a049-46c7-bfc9-f9ac2fc8c47e-profile_image-70x70.png");
export const currency = writable(1000);
export const netWorth = writable(2000);