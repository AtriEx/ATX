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

export const load = (async () => {
	const { data } = await adminSupabase
		.from('stock_info')
		.select('name, image, stock_price(stock_price), total_shares');

	if (!data) {
		console.error('No data');
		error(404, 'Not found');
	}

	const hottest = await hottestStocks();
	const losers = await biggestLosers();

	return { stocks: data, hottest, losers };
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
