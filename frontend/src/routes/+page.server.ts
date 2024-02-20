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
	orderBy?: 'name' | 'description' | 'image' | 'price' | 'total_shares';
	order?: 'asc' | 'desc';
};

export const load = (async ({ url }) => {
	const query = url.searchParams.get('query');
	const orderBy = (url.searchParams.get('orderBy') as Query['orderBy']) || 'name';
	const order = (url.searchParams.get('order') as Query['order']) || 'asc';

	let builder = adminSupabase
		.from('stock_info')
		.select('name, image, stock_price(stock_price), total_shares');

	if (query) builder = builder.ilike('name', `*${query}*`);

	if (orderBy === 'price') {
		builder = builder.order('stock_price', {
			ascending: order === 'asc',
			referencedTable: 'stock_price'
		});
	} else {
		builder = builder.order(orderBy, { ascending: order === 'asc' });
	}

	const { data, error: pgError } = await builder;
	if (pgError || !data) {
		console.error(pgError);
		error(404, 'Not found');
	}

	const hottest = await hottestStocks();
	const losers = await biggestLosers();

	return { stockInfo: data, hottest, losers };
}) satisfies PageServerLoad;

async function hottestStocks() {
	const { data, error: pgError } = await adminSupabase
		.from('stock_info')
		.select('name, image, stock_price(stock_price), total_shares')
		.order('stock_price', {
			ascending: false,
			referencedTable: 'stock_price'
		})
		.limit(3);
	if (pgError || !data) {
		console.error(pgError);
		error(404, 'Not found');
	}
	return data;
}

async function biggestLosers() {
	const { data, error: pgError } = await adminSupabase
		.from('stock_info')
		.select('name, image, stock_price(stock_price), total_shares')
		.order('stock_price', {
			ascending: false,
			referencedTable: 'stock_price'
		})
		.limit(3);
	if (pgError || !data) {
		console.error(pgError);
		error(404, 'Not found');
	}
	return data;
}
