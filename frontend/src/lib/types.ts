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

export type Profile = {
	username: string;
	image: string;
	joined_at: Date;
	networth: number;
	balance: number;
};

export type Flags = {
	name: string;
	image: string;
	description: string;
	type: string;
};
