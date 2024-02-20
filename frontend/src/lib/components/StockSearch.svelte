<script lang="ts">
	import { page } from '$app/stores';
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';

	let timer: NodeJS.Timeout;
	let value = $page.url.searchParams.get('query');

	$: {
		clearTimeout(timer);
		timer = setTimeout(() => {
			const queryParams = new URLSearchParams($page.url.searchParams);
			if (!value) queryParams.delete('query');
			else queryParams.set('query', value);
			if (browser) goto('?' + queryParams.toString(), { replaceState: true, noScroll: true });
		}, 500);
	}
</script>

<input
	type="text"
	class="w-full p-3 mb-4 rounded-lg border border-gray-300 dark:border-gray-700 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
	bind:value
	placeholder="Search by name"
/>
