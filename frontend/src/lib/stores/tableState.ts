import { writable } from 'svelte/store';

type Table = {
	name: string;
	image: string | null;
	stock_price: {
		stock_price: number;
	} | null;
	total_shares: number;
};

type TableStates = {
	mainTable: Table[];
	biggestLosers: Table[];
	hottestStocks: Table[];
	orderBy?: 'name' | 'price' | 'total_shares' | 'description' | 'image' | 'id';
	order?: 'asc' | 'desc';
	query?: string;
};

function useTableState() {
	const { subscribe, set, update } = writable<TableStates>({
		mainTable: [],
		biggestLosers: [],
		hottestStocks: [],
		orderBy: 'name',
		order: 'asc'
	});

	async function fetchAndUpdateMainTable(
		query?: string,
		orderBy: Exclude<TableStates['orderBy'], undefined> = 'name',
		order: 'asc' | 'desc' = 'asc'
	) {
		const queryParams = new URLSearchParams({ query: query || '', orderBy, order });
		const res = await fetch(`/api/stockTable?${queryParams}`);
		const data = await res.json();
		update((state) => ({ ...state, mainTable: data }));
	}

	function changeOrder() {
		update((state) => {
			const newOrder = state.order === 'asc' ? 'desc' : 'asc';
			fetchAndUpdateMainTable(state.query, state.orderBy, newOrder);
			return { ...state, order: newOrder };
		});
	}

	function changeOrderBy(orderBy: Exclude<TableStates['orderBy'], undefined>) {
		update((state) => {
			fetchAndUpdateMainTable(state.query, orderBy, state.order);
			return { ...state, orderBy };
		});
	}

	function changeQuery(query?: string) {
		update((state) => {
			fetchAndUpdateMainTable(query, state.orderBy, state.order);
			return { ...state, query };
		});
	}

	return {
		init: ({ tables }: { tables: TableStates }) => set(tables),
		changeOrder,
		changeOrderBy,
		subscribe,
		changeQuery
	};
}

export const tableState = useTableState();
