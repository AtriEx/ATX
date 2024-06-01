<script lang="ts">
	import type { PageData } from './$types';
	import StockTable from '$lib/components/StockTable.svelte';

	export let data: PageData;
</script>

<main
	class="bg-light-background dark:bg-dark-background p-4 md:p-8 text-light-text dark:text-dark-text"
>
	<h1
		class="text-3xl md:text-4xl font-bold text-center text-light-primary dark:text-dark-accent mb-6"
	>
		Markets
	</h1>
	<div class="overflow-x-auto rounded-lg shadow-lg">
		<StockTable stockInfo={data.stocks} mainTable />
	</div>
	<div class="md:flex justify-evenly p-2 pt-5 space-y-6 md:space-y-0 md:space-x-6">
		<div class="p-4 md:w-1/2">
			<h2 class="text-2xl font-bold text-center text-light-primary dark:text-dark-accent mb-6">
				Hottest Stocks
			</h2>
			<StockTable stockInfo={data.hottest} />
		</div>
		<div class="p-4 md:w-1/2">
			<h2 class="text-2xl font-bold text-center text-light-primary dark:text-dark-accent mb-6">
				Biggest Losers
			</h2>
			<StockTable stockInfo={data.losers} />
		</div>
	</div>
</main>
