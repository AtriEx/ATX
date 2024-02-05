import type { Badge, OwnedStock, UserData } from '$lib/types';
import type { LayoutServerLoad } from './$types';

export const load = (async () => {
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
		userName: 'GHEwing',
		joinDate: new Date('2021-01-01'),
		netWorth,
		profileImage:
			'https://static-cdn.jtvnw.net/jtv_user_pictures/6c45032c-a049-46c7-bfc9-f9ac2fc8c47e-profile_image-70x70.png',
		stocks: stocksOwned,
		badges
	};
	return {
		profile: profile as UserData | null
	};
}) satisfies LayoutServerLoad;
