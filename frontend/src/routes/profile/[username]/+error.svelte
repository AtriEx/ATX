<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
</script>

<svelte:head>
	<title>Error</title>
</svelte:head>

<div class="dark:bg-dark-background bg-light-background flex flex-col flex-1">
	<div
		class="mx-4 sm:mx-5 my-4 sm:my-3 p-4 sm:p-6 bg-dark-primary/5 dark:bg-dark-primary/10 rounded-lg shadow-lg flex flex-col md:flex-row"
	>
		<div class="flex flex-col grow mt-4 md:mt-0 md:ml-4">
			<div class="flex-grow flex flex-col md:flex-row items-center md:space-x-4">
				<h1
					class="text-2xl sm:text-3xl md:text-4xl font-bold text-light-primary dark:text-dark-primary text-center md:text-left"
				>
					{#if $page.status === 404}
						Not Found
					{:else}
						Error
					{/if}
				</h1>
			</div>
			<div
				class="flex flex-col md:flex-row items-center justify-between text-center md:text-left mt-4"
			>
				<div
					class="flex flex-col md:flex-row gap-4 uppercase font-bold text-gray-600 dark:text-gray-300 w-full"
				>
					<p class="text-base sm:text-lg">{$page.error?.message}</p>
				</div>
			</div>
			<div class="w-full flex justify-center">
				<button
					class="bg-light-primary dark:bg-dark-primary p-2 rounded-lg text-light-text dark:text-dark-text"
					on:click={() => goto('/')}>Home</button
				>
			</div>
		</div>
	</div>
</div>
