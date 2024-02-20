<script lang="ts">
	import StockSearch from './../lib/components/StockSearch.svelte';
	import type { PageData } from './$types';
	import StockTable from '$lib/components/StockTable.svelte';

	export let data: PageData;
</script>

<main class="bg-white dark:bg-gray-900 p-4 md:p-8">
	<h1 class="text-3xl md:text-4xl font-bold text-center text-gray-900 dark:text-gray-100 mb-6">
		Markets
	</h1>
	<StockSearch />
	<div class="overflow-x-auto rounded-lg">
		<StockTable stockInfo={data.stockInfo} />
	</div>
	<div class="md:flex justify-evenly p-2 pt-5">
		<div class="md:mr-4 md:w-1/2">
			<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6 text-center">
				Hottest Stocks
			</h2>
			<StockTable stockInfo={data.hottest} />
		</div>
		<div class="md:mr-4 md:w-1/2">
			<h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-6 text-center">
				Biggest Losers
			</h2>
			<StockTable stockInfo={data.losers} />
		</div>
	</div>
</main>
