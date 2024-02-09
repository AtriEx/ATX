<script lang="ts">
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	export let order: 'asc' | 'desc' = 'asc';
	export let orderBy: Exclude<Query['orderBy'], undefined>;

	type Query = {
		query?: string;
		orderBy?: 'id' | 'name' | 'description' | 'image' | 'price' | 'totalShares';
		order?: 'asc' | 'desc';
	};

	function changeOrder() {
		const newOrder = order === 'asc' ? 'desc' : 'asc';
		const queryParams = new URLSearchParams($page.url.searchParams);
		queryParams.set('order', newOrder);
		queryParams.set('orderBy', orderBy);
		if (browser) goto('?' + queryParams.toString(), { replaceState: true });
	}
</script>

<th
	scope="col"
	class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider cursor-pointer"
	on:click={changeOrder}
>
	{orderBy}
	{#if $page.url.searchParams.get('orderBy') === orderBy}
		{order === 'asc' ? '▲' : '▼'}
	{/if}
</th>
