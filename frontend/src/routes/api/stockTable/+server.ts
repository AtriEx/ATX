import { PRIVATE_SUPABASE_SERVICE_ROLE_KEY } from '$env/static/private';
import { PUBLIC_SUPABASE_URL } from '$env/static/public';
import { type Database } from '$lib/supabase.types';
import { createClient } from '@supabase/supabase-js';
import { json, type RequestHandler } from '@sveltejs/kit';

const supabaseAdmin = createClient<Database>(
	PUBLIC_SUPABASE_URL,
	PRIVATE_SUPABASE_SERVICE_ROLE_KEY
);

type OrderBy = 'name' | 'price' | 'total_shares' | null;

const GET: RequestHandler = async ({ url }) => {
	const query = url.searchParams.get('query') || undefined;
	const orderBy = (url.searchParams.get('orderBy') as OrderBy) || 'name';
	const order = (url.searchParams.get('order') as 'asc' | 'desc') || 'asc';

	const data = await updateMainTable(query, orderBy, order);

	return json(data);
};

export { GET };

async function updateMainTable(
	query: string | undefined,
	orderBy: 'name' | 'price' | 'total_shares' = 'name',
	order: 'asc' | 'desc'
) {
	let builder = supabaseAdmin
		.from('stock_info')
		.select('name, image, stock_price(stock_price), total_shares');

	if (query) builder = builder.ilike('name', `%${query}%`);

	if (orderBy !== 'price') {
		builder = builder.order(orderBy, { ascending: order === 'asc' });
	}

	let { data } = await builder;
	if (!data) {
		console.error('No data');
		return [];
	}

	if (orderBy === 'price')
		data = data.sort((a, b) => {
			const aPrice = a.stock_price?.stock_price || 0;
			const bPrice = b.stock_price?.stock_price || 0;

			return order === 'asc' ? aPrice - bPrice : bPrice - aPrice;
		});

	return data;
}
