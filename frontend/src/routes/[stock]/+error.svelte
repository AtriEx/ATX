<script lang="ts">
	import { page } from '$app/stores';
</script>

<div class="flex flex-col justify-center items-center space-y-4">
	{#if $page.error}
		<h1 class="text-3xl font-bold text-center text-red-500">
			Error:
			<span class="text-black dark:text-white">{$page.error.message}</span>
		</h1>
	{/if}
	<a href="/" class="block text-center text-blue-500">Go back to home</a>
</div>
