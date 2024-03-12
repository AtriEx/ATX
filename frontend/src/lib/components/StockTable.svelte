<script lang="ts">
	import StockTableHeader from './StockTableHeader.svelte';
	import StockTableRow from './StockTableRow.svelte';
	import { page } from '$app/stores';
	import type { PageData } from '../../routes/$types';

	export let stockInfo: PageData['stockInfo'];
	export let mainTable = false;

	const headers = ['name', 'price', 'total_shares'] as const;
</script>

<table class="w-full min-w-full divide-y divide-gray-200 dark:divide-gray-700">
	<thead class="bg-gray-100 dark:bg-gray-700">
		<tr>
			<th
				class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
			/>
			{#each headers as header}
				<StockTableHeader orderBy={header} {mainTable} />
			{/each}
		</tr>
	</thead>
	<tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
		{#each stockInfo as stock}
			<StockTableRow {stock} />
		{/each}
	</tbody>
</table>
