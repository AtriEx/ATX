import type { PageServerLoad } from './$types';
import { createClient } from '@supabase/supabase-js';
import { PRIVATE_SUPABASE_SERVICE_ROLE_KEY } from '$env/static/private';
import { PUBLIC_SUPABASE_URL } from '$env/static/public';
import { type Database } from '$lib/supabase.types';
import { error } from '@sveltejs/kit';

const adminSupabase = createClient<Database>(
	PUBLIC_SUPABASE_URL,
	PRIVATE_SUPABASE_SERVICE_ROLE_KEY
);

export const load: PageServerLoad = async ({ params }) => {
	// Check if the username is empty
	if (!params.username || params.username === '') error(404, { message: 'Profile not found' });

	// Perform a combined query to fetch profile, portfolio, and flags
	const { data, error: fetchError } = await adminSupabase
		.from('profiles')
		.select(
			`
        networth,
        balance,
        username,
        image,
        joined_at,
        portfolio(stockId, quantity, stock_info(name, image, description, stock_price(stock_price))),
        flags(id, name, image, description, type)
    `
		)
		.eq('username', params.username)
		.single();

	if (fetchError) error(404, { message: 'Profile not found' });
	if (!data) error(404, { message: 'Profile not found' });

	const profile = {
		...data,
		badges: data.flags?.filter((flag) => flag.type === 'badge') || [],
		achievements: data.flags?.filter((flag) => flag.type === 'achievement') || [],
		stocks:
			data.portfolio?.map((item) => ({
				name: item.stock_info?.name || '',
				image: item.stock_info?.image || '',
				description: item.stock_info?.description || '',
				price: item.stock_info?.stock_price?.stock_price || 0,
				quantity: item.quantity
			})) || []
	};

	// Return the structured profile data
	return { profile };
};
