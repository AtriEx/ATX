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
	userName: string;
	joinDate: Date;
	profileImage?: string;
	netWorth: number;
	stocks: OwnedStock[];
	badges: Badge[];
};
