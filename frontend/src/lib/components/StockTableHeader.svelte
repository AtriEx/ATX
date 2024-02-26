<script lang="ts">
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	export let order: 'asc' | 'desc' = 'asc';
	export let orderBy: Exclude<Query['orderBy'], undefined>;
	export let mainTable = false;

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
		if (browser) goto('?' + queryParams.toString(), { replaceState: true });
	}
</script>

<th
	scope="col"
	class="px-6 py-3 text-left text-xs text-gray-500 dark:text-gray-300 uppercase cursor-pointer hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
	class:underline={orderBy === $page.url.searchParams.get('orderBy') && mainTable}
	on:click={changeOrder}
>
	{#if orderBy === 'total_shares'}
		Total Shares
	{:else}
		{orderBy}
	{/if}

	{#if $page.url.searchParams.get('orderBy') === orderBy && mainTable}
		{order === 'asc' ? '▲' : '▼'}
	{/if}
</th>
