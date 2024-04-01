<script lang="ts">
	import {
		getCoreRowModel,
		type ColumnDef,
		type OnChangeFn,
		type SortingState,
		type TableOptions,
		getSortedRowModel,
		createSvelteTable,
		flexRender,
		type FilterFn,
		getFilteredRowModel
	} from '@tanstack/svelte-table';
	import type { Table } from '$lib/stores/tableState';
	import { writable } from 'svelte/store';
	import { rankItem } from '@tanstack/match-sorter-utils';
	import { goto } from '$app/navigation';

	export let stockInfo: Table[];
	export let mainTable = false;

	const defaultColumns: ColumnDef<Table>[] = [
		{ accessorKey: 'name', enableSorting: mainTable, header: 'Name', id: 'name' },
		{
			accessorFn: (row) => row.stock_price?.stock_price || 0,
			enableSorting: mainTable,
			id: 'stockPrice',
			header: 'Stock Price'
		},
		{ accessorKey: 'total_shares', enableSorting: mainTable, header: 'Total Shares' }
	];

	let sorting: SortingState = [];

	const fuzzyFilter: FilterFn<any> = (row, columnId, value, addMeta) => {
		const itemRank = rankItem(row.getValue(columnId), value);

		addMeta({ itemRank });

		return itemRank.passed;
	};

	const setSorting: OnChangeFn<SortingState> = (updater) => {
		if (updater instanceof Function) {
			sorting = updater(sorting);
		} else {
			sorting = updater;
		}
		options.update((old) => ({
			...old,
			state: {
				...old.state,
				sorting
			}
		}));
	};

	const handleKeyUp = (e: any) => {
		$table.setGlobalFilter(String(e?.target?.value));
	};
	const options = writable<TableOptions<Table>>({
		data: stockInfo,
		columns: defaultColumns,
		state: {
			sorting
		},
		filterFns: {
			fuzzy: fuzzyFilter
		},
		onSortingChange: setSorting,
		getCoreRowModel: getCoreRowModel(),
		getSortedRowModel: getSortedRowModel(),
		getFilteredRowModel: getFilteredRowModel()
	});

	const table = createSvelteTable(options);

	function onClick(name: string) {
		goto(`/stock/${name}`);
	}
</script>

<div class="relative w-full mb-4">
	{#if mainTable}
		<input
			type="text"
			on:keyup={handleKeyUp}
			class="w-full p-3 pl-10 rounded-lg shadow-sm text-light-text dark:text-dark-text dark:bg-dark-secondary bg-light-secondary focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-colors duration-200 ease-in-out"
			placeholder="Search for a stock"
		/>
		<div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="h-5 w-5 text-gray-500"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
				stroke-width="2"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
				/>
			</svg>
		</div>
	{/if}
</div>
<table class="min-w-full leading-normal shadow-lg rounded-lg overflow-hidden">
	<thead>
		<tr
			class="text-left text-sm font-semibold bg-light-background dark:bg-dark-background bg-gradient-to-r from-light-primary to-light-accent dark:from-dark-primary dark:to-dark-accent"
		>
			{#each $table.getHeaderGroups() as headerGroup}
				{#each headerGroup.headers as header}
					<th
						colSpan={header.colSpan}
						class="border-light-background dark:border-dark-background border-2 first:rounded-tl-lg last:rounded-tr-lg first:w-1/3 w-1/6"
					>
						{#if !header.isPlaceholder}
							<button
								class="flex items-center space-x-2 cursor-pointer select-none text-light-text dark:text-dark-text px-6 py-3 w-full"
								on:click={header.column.getToggleSortingHandler()}
								class:cursor-default={!mainTable}
							>
								<svelte:component
									this={flexRender(header.column.columnDef.header, header.getContext())}
								/>
								{#if header.column.getIsSorted().toString() === 'asc'}
									<svg
										class="w-4 h-4"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
										xmlns="http://www.w3.org/2000/svg"
										><path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M5 15l7-7 7 7"
										></path></svg
									>
								{:else if header.column.getIsSorted().toString() === 'desc'}
									<svg
										class="w-4 h-4"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
										xmlns="http://www.w3.org/2000/svg"
										><path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M19 9l-7 7-7-7"
										></path></svg
									>
								{/if}
							</button>
						{/if}
					</th>
				{/each}
			{/each}
		</tr>
	</thead>
	<tbody class="text-light-text dark:text-dark-text">
		{#each $table.getRowModel().rows as row}
			<tr
				class="{mainTable
					? 'bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800'
					: 'bg-gray-50 dark:bg-gray-800 hover:bg-white dark:hover:bg-gray-900'} transition duration-150 ease-in-out border-b border-gray-200 dark:border-gray-700 cursor-pointer"
				on:click={() => onClick(row.original.name)}
			>
				{#each row.getVisibleCells() as cell}
					<td class="px-6 py-4 whitespace-no-wrap text-sm leading-5">
						{#if cell.column.columnDef.id === 'name'}
							<div class="flex items-center space-x-2">
								<img
									src={cell.row.original.image}
									alt={cell.row.original.name}
									class="w-8 h-8 rounded-full mr-5 border-light-accent dark:border-dark-accent border-2"
								/>
								<svelte:component
									this={flexRender(cell.column.columnDef.cell, cell.getContext())}
								/>
							</div>
						{:else}
							<svelte:component this={flexRender(cell.column.columnDef.cell, cell.getContext())} />
						{/if}
					</td>
				{/each}
			</tr>
		{/each}
	</tbody>
</table>
