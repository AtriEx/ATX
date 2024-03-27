<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { tableState } from '$lib/stores/tableState';

	export let orderBy: Exclude<Query['orderBy'], undefined>;
	export let mainTable = false;

	$: order = $tableState.order;

	type Query = {
		query?: string;
		orderBy?: 'id' | 'name' | 'description' | 'image' | 'price' | 'total_shares';
		order?: 'asc' | 'desc';
	};

	function changeOrder() {
		if (!mainTable) return;
		const newOrder = order === 'asc' ? 'desc' : 'asc';
		const queryParams = new URLSearchParams($page.url.searchParams);
		queryParams.set('order', newOrder);
		queryParams.set('orderBy', orderBy);
		goto('/?' + queryParams.toString(), { replaceState: false, noScroll: true });
		if ($tableState.order !== newOrder) tableState.changeOrder();
		if ($tableState.orderBy !== orderBy) tableState.changeOrderBy(orderBy);
	}
</script>

<th
	scope="col"
	class="px-6 py-3 text-left text-xs uppercase cursor-pointer transition-colors
		   text-light-secondary dark:text-dark-accent
		   hover:text-light-primary dark:hover:text-dark-primary
		   select-none
		   {orderBy === $tableState.orderBy && mainTable ? 'underline' : ''}"
	on:click={changeOrder}
>
	{#if orderBy === 'total_shares'}
		Total Shares
	{:else}
		{orderBy}
	{/if}

	{#if $tableState.orderBy === orderBy && mainTable}
		<span
			class={order === 'asc'
				? 'text-light-accent dark:text-dark-primary'
				: 'text-light-primary dark:text-dark-accent'}
		>
			{order === 'asc' ? '▲' : '▼'}
		</span>
	{/if}
</th>
