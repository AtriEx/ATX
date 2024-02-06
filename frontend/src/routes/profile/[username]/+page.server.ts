import type { PageServerLoad } from './$types';
import { createClient } from '@supabase/supabase-js';
import { PRIVATE_SUPABASE_SERVICE_ROLE_KEY } from '$env/static/private';
import { PUBLIC_SUPABASE_URL } from '$env/static/public';
import { type Database } from '$lib/supabase.types';
import { error } from '@sveltejs/kit';

interface StockInfo {
	name: string;
	image: string;
	description: string;
	quantity: number;
	price: number;
}

interface Portfolio {
	stockId: string;
	quantity: number;
	stockInfo: StockInfo;
}

interface ProfileData {
	networth: number;
	balance: number;
	username: string;
	image: string;
	joined_at: Date;
	portfolio: Portfolio[];
	flags: any[]; // Define this more precisely based on your actual flags structure
}

// Initialize the Supabase client
const adminSupabase = createClient<Database>(
	PUBLIC_SUPABASE_URL,
	PRIVATE_SUPABASE_SERVICE_ROLE_KEY
);

export const load: PageServerLoad = async ({ params }) => {
	// Check if the username is empty
	if (!params.username || params.username === '') error(404, 'Profile not found');

	// Perform a combined query to fetch profile, portfolio, and flags
	const { data, error: fetchError } = (await adminSupabase
		.from('profiles')
		.select(
			`
        networth,
        balance,
        username,
        image,
        joined_at,
        portfolio(stockId, quantity, stockInfo:stockId(name, image, description, price)),
        flags(id, name, image, description, type)
    `
		)
		.eq('username', params.username)
		.single()
		.throwOnError()) as { data: ProfileData | null; error: any };

	console.log('data', data);

	// Handle potential errors from the fetch operation
	if (fetchError) error(404, 'Profile not found');
	if (!data) error(404, 'Profile not found');

	// Structure the data to include in the load response
	const profile = {
		...data,
		badges: data.flags?.filter((flag) => flag.type === 'badge') || [],
		achievements: data.flags?.filter((flag) => flag.type === 'achievement') || [],
		stocks:
			data.portfolio?.map((item) => ({
				name: item.stockInfo.name,
				image: item.stockInfo.image,
				description: item.stockInfo.description,
				price: item.stockInfo.price,
				quantity: item.quantity
			})) || []
	};

	// Return the structured profile data
	return { profile };
};
