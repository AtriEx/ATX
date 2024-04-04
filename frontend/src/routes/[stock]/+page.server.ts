import { createClient } from '@supabase/supabase-js';
import { PRIVATE_SUPABASE_SERVICE_ROLE_KEY } from '$env/static/private';
import { PUBLIC_SUPABASE_URL } from '$env/static/public';
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { type Database } from '$lib/supabase.types';

const adminSupabase = createClient<Database>(
	PUBLIC_SUPABASE_URL,
	PRIVATE_SUPABASE_SERVICE_ROLE_KEY
);

export const load = (async ({ params, url }) => {
	const searchParams = url.searchParams;

	const period = searchParams.get('period') || 'daily';
	const stockName = params.stock;
	if (period === 'daily') {
		const { data, error: pgError } = await dailyInfo(stockName);
		if (!data || pgError) {
			console.error(pgError);
			error(404, 'Stock not found');
		}
		return { history: data, period: 'daily' as const, stock: stockName };
	}
	if (period === 'monthly') {
		const { data, error: pgError } = await monthlyInfo(stockName);
		if (!data || pgError) {
			console.error(pgError);
			error(404, 'Stock not found');
		}
		return { history: data, period: 'monthly' as const, stock: stockName };
	}
	if (period === 'weekly') {
		const { data, error: pgError } = await weeklyInfo(stockName);
		if (!data || pgError) {
			console.error(pgError);
			error(404, 'Stock not found');
		}
		return { history: data, period: 'weekly' as const, stock: stockName };
	}
	// Invalid period
	error(400, 'Invalid period');
}) satisfies PageServerLoad;

async function dailyInfo(stockName: string) {
	return await adminSupabase
		.from('stock_price_history_daily')
		.select('changed_at, price, id, stock_info!inner(name, image)')
		.eq('stock_info.name', stockName)
		.limit(7);
}

async function weeklyInfo(stockName: string) {
	return await adminSupabase
		.from('stock_price_history_weekly')
		.select('starting_hour, average_price, id, stock_info!inner(name, image)')
		.eq('stock_info.name', stockName)
		.limit(7);
}

async function monthlyInfo(stockName: string) {
	return await adminSupabase
		.from('stock_price_history_monthly')
		.select('starting_hour, average_price, id, stock_info!inner(name, image)')
		.eq('stock_info.name', stockName)
		.limit(7);
}
