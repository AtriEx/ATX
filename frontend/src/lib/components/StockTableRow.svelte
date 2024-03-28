<script lang="ts">
	import type { PageData } from '../../routes/stocks/$types';

	type Stock = PageData['stockInfo'][number];

	export let stock: Stock;
</script>

<tr class="hover:bg-gray-50 dark:hover:bg-gray-700">
	<td class="px-6 py-4 whitespace-nowrap">
		<div class="flex items-center">
			<div class="flex-shrink-0 h-10 w-10">
				<img class="h-10 w-10 rounded-full" src={stock.image} alt={stock.name} />
			</div>
		</div>
	</td>
	<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
		<a href="/{stock.name}" class="hover:text-blue-500 dark:hover:text-blue-300">
			{stock.name}
		</a>
	</td>
	<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
		{stock.stock_price?.stock_price || 0} coin(s)
	</td>
	<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
		{stock.total_shares}
	</td>
</tr>
