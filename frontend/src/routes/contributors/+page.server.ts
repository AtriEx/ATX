// import type { PageServerLoad } from './$types';
import { createClient } from '@supabase/supabase-js';
import { PRIVATE_SUPABASE_SERVICE_ROLE_KEY } from '$env/static/private';
import { PUBLIC_SUPABASE_URL } from '$env/static/public';
import { error } from '@sveltejs/kit';

// Initialize the Supabase client
const adminSupabase = createClient(
	PUBLIC_SUPABASE_URL,
	PRIVATE_SUPABASE_SERVICE_ROLE_KEY
);

export const load = async() => {
    // Fetch contributors
    const { data, error: fetchError } = (await adminSupabase
        .from('contributors')
        .select(
        `
        name,
        description,
        image,
        role,
        twitterUsername,
        discordUserID,
        githubUsername
        `
        ))

    console.log('data: ', data);

    // Handle potential errors from the fetch operation
    if (fetchError) error(404, 'Unable to retrieve contributors');
    if (!data) error(404, 'Unable to retrieve contributors');

    // Return the structured profile data
    return { data };
};
