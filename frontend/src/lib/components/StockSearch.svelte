<script lang="ts">
	import { page } from '$app/stores';
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { tableState } from '$lib/stores/tableState';

	let timer: NodeJS.Timeout;
	let value = $page.url.searchParams.get('query');

	$: {
		clearTimeout(timer);
		timer = setTimeout(() => {
			const queryParams = new URLSearchParams($page.url.searchParams);
			if (!value) queryParams.delete('query');
			else queryParams.set('query', value);
			if (!browser) return;
			tableState.changeQuery(value || undefined);
			goto('/?' + queryParams.toString(), { replaceState: false, noScroll: true });
		}, 500);
	}
</script>

<input
	type="text"
	class="w-full p-3 mb-4 rounded-lg border border-light-secondary dark:border-dark-secondary shadow-sm focus:border-light-primary focus:ring-light-accent dark:focus:border-dark-accent dark:focus:ring-dark-primary dark:bg-dark-background dark:text-dark-text transition-colors duration-300 ease-in-out"
	bind:value
	placeholder="Search by name"
/>
