import { createClient } from '@supabase/supabase-js';
import type { PageServerLoad } from './$types';
import { PUBLIC_SUPABASE_URL } from '$env/static/public';
import { PRIVATE_SUPABASE_SERVICE_ROLE_KEY } from '$env/static/private';
import { type Database } from '$lib/supabase.types';
import { error } from '@sveltejs/kit';

const adminSupabase = createClient<Database>(
	PUBLIC_SUPABASE_URL,
	PRIVATE_SUPABASE_SERVICE_ROLE_KEY
);

export type Query = {
	query?: string;
	orderBy?: 'name' | 'description' | 'image' | 'price' | 'totalShares';
	order?: 'asc' | 'desc';
};

export const load = (async ({ url }) => {
	const query = url.searchParams.get('query');
	const orderBy = (url.searchParams.get('orderBy') as Query['orderBy']) || 'name';
	const order = (url.searchParams.get('order') as Query['order']) || 'asc';

	let builder = adminSupabase.from('stockInfo').select('name, image, price, totalShares');

	if (query) builder = builder.ilike('name', `*${query}*`);
	builder = builder.order(orderBy, { ascending: order === 'asc' });

	const { data, error: pgError } = await builder;
	if (pgError || !data) {
		console.error(pgError);
		error(404, 'Not found');
	}
	return { stockInfo: data };
}) satisfies PageServerLoad;
