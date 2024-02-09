<script lang="ts">
	import type { PageData } from './$types';
	import { page } from '$app/stores';
	import StockTableHeader from '$lib/components/StockTableHeader.svelte';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';

	export let data: PageData;

	$: order = ($page.url.searchParams.get('order') || 'asc') as 'asc' | 'desc';

	let timer: NodeJS.Timeout;
	let value = $page.url.searchParams.get('query');

	$: {
		clearTimeout(timer);
		timer = setTimeout(() => {
			const queryParams = new URLSearchParams($page.url.searchParams);
			if (!value) queryParams.delete('query');
			else queryParams.set('query', value);
			if (browser) goto('?' + queryParams.toString(), { replaceState: true });
		}, 500);
	}

	const headers = ['name', 'price', 'totalShares'] as const;
</script>

<main class="bg-white dark:bg-gray-900 p-4 md:p-8">
	<h1 class="text-3xl md:text-4xl font-bold text-center text-gray-900 dark:text-gray-100 mb-6">
		Markets
	</h1>
	<input
		type="text"
		class="w-full p-3 mb-4 rounded-lg border border-gray-300 dark:border-gray-700 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
		bind:value
		autofocus
		placeholder="Search by name"
	/>
	<div class="overflow-x-auto rounded-lg">
		<table class="w-full min-w-full divide-y divide-gray-200 dark:divide-gray-700">
			<thead class="bg-gray-100 dark:bg-gray-700">
				<tr>
					<th
						class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
					/>
					{#each headers as header}
						<StockTableHeader {order} orderBy={header} />
					{/each}
				</tr>
			</thead>
			<tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
				{#each data.stockInfo as stock}
					<tr class="hover:bg-gray-50 dark:hover:bg-gray-700">
						<td class="px-6 py-4 whitespace-nowrap">
							<div class="flex items-center">
								<div class="flex-shrink-0 h-10 w-10">
									<img class="h-10 w-10 rounded-full" src={stock.image} alt={stock.name} />
								</div>
							</div>
						</td>
						<td
							class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white"
						>
							{stock.name}
						</td>
						<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
							{stock.price} coin(s)
						</td>
						<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
							{stock.totalShares}
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</main>
