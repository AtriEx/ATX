import type { Badge, OwnedStock, UserData } from '$lib/types';
import { createClient } from '@supabase/supabase-js';
import type { LayoutServerLoad } from './$types';
import { PUBLIC_SUPABASE_URL } from '$env/static/public';
import { PRIVATE_SUPABASE_SERVICE_ROLE_KEY } from '$env/static/private';

const adminSupabase = createClient(PUBLIC_SUPABASE_URL, PRIVATE_SUPABASE_SERVICE_ROLE_KEY);

export const load = (async () => {
	const {
		data: { session }
	} = await adminSupabase.auth.getSession();
	if (!session) return { profile: null, session: null };

	// TODO: Fetch user's profile from the database
	// const { data: profile, error } = await adminSupabase.from<UserData>('profiles').select('*').eq('id', session.user.id);
	const stocksOwned: OwnedStock[] = [
		{
			symbol: 'AAPL',
			name: 'Apple Inc.',
			price: 125.9,
			change: -0.2,
			quantity: 100
		},
		{
			symbol: 'GOOGL',
			name: 'Alphabet Inc.',
			price: 2_000,
			change: 0.5,
			quantity: 50
		},
		{
			symbol: 'AMZN',
			name: 'Amazon.com Inc.',
			price: 3_000,
			change: 0.3,
			quantity: 25
		}
	];

	const netWorth = stocksOwned.reduce((acc, stock) => acc + stock.price * stock.quantity, 0);

	const badges: Badge[] = [
		{
			name: 'First Purchase',
			dateObtained: new Date('2021-01-01')
		},
		{
			name: 'First Sale',
			dateObtained: new Date('2021-01-02')
		}
	];

	const profile: UserData = {
		userName: session.user.user_metadata.name,
		joinDate: new Date('2021-01-01'),
		netWorth,
		profileImage:
			'https://static-cdn.jtvnw.net/jtv_user_pictures/6c45032c-a049-46c7-bfc9-f9ac2fc8c47e-profile_image-70x70.png',
		stocks: stocksOwned,
		badges
	};
	return {
		profile: profile as UserData | null,
		session
	};
}) satisfies LayoutServerLoad;
