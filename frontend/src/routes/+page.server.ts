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

	if (orderBy !== 'price') {
		builder = builder.order(orderBy, { ascending: order === 'asc' });
	}

	let { data } = await builder;
	if (!data) {
		console.error('No data');
		error(404, 'Not found');
	}

	const hottest = await hottestStocks();
	const losers = await biggestLosers();

	if (orderBy === 'price')
		data = data.sort((a, b) =>
			order === 'asc'
				? a.stock_price!.stock_price - b.stock_price!.stock_price
				: b.stock_price!.stock_price - a.stock_price!.stock_price
		);

	return { stockInfo: data, hottest, losers };
}) satisfies PageServerLoad;

async function biggestLosers() {
	const { data, error: pgError } = await adminSupabase
		.from('stock_info')
		.select('name, image, stock_price(stock_price), total_shares');
	if (pgError || !data) {
		console.error(pgError);
		return [];
	}

	const sorted = data.sort((a, b) => {
		const aPrice = a.stock_price?.stock_price || 0;
		const bPrice = b.stock_price?.stock_price || 0;
		return aPrice - bPrice;
	});

	return sorted.slice(0, 5);
}

async function hottestStocks() {
	const { data, error: pgError } = await adminSupabase
		.from('stock_info')
		.select('name, image, stock_price(stock_price), total_shares')
		.order('stock_price', {
			ascending: false,
			referencedTable: 'stock_price'
		});
	if (pgError || !data) {
		console.error(pgError);
		return [];
	}

	const sorted = data.sort((a, b) => {
		const aPrice = a.stock_price?.stock_price || 0;
		const bPrice = b.stock_price?.stock_price || 0;
		return bPrice - aPrice;
	});

	return sorted.slice(0, 5);
}
