export type Table = {
	name: string;
	image: string | null;
	stock_price: {
		stock_price: number;
	} | null;
	total_shares: number;
};
