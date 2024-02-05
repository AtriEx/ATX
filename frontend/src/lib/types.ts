export type Stock = {
	symbol: string;
	name: string;
	price: number;
	change: number;
};

export type OwnedStock = Stock & {
	quantity: number;
};

export type Badge = {
	name: string;
	iconImage?: string;
	dateObtained: Date;
};

export type UserData = {
	joined_at: Date;
	username: string;
	balance: number;
	networth: number;
	userId: string;
	image: string;
	stocks: OwnedStock[];
	badges: Badge[];
};
