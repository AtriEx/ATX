<script lang="ts">
	import { goto } from '$app/navigation';
	import DailyChart from '$lib/components/DailyChart.svelte';
	import WeeklyMonthly from '$lib/components/WeeklyMonthlyChart.svelte';
	import type { PageData } from './$types';

	export let data: PageData;
	type Option = (typeof options)[number];

	function selectTimePeriod() {
		goto(`/${data.stock}?period=${selected}`, { replaceState: true, noScroll: true });
	}

	const options = ['daily', 'weekly', 'monthly'] as const;

	let selected = data.period as Option;
</script>

<main class="py-8 px-4 sm:px-6 lg:px-8">
	<h1 class="text-3xl font-semibold dark:text-dark-text text-light-text text-center mb-6">
		{data.stock}
	</h1>
	<div class="flex justify-center items-center mb-8">
		<select
			class="form-select appearance-none block w-1/2 max-w-xs mx-auto bg-white dark:bg-dark-secondary text-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-600 rounded-md py-2 px-4 leading-tight focus:outline-none focus:bg-white focus:border-light-primary dark:focus:border-dark-primary transition duration-150 ease-in-out"
			bind:value={selected}
			on:change={selectTimePeriod}
		>
			{#each options as option}
				<option value={option}>{option.charAt(0).toUpperCase() + option.slice(1)}</option>
			{/each}
		</select>
	</div>
	{#if data.history.length === 0}
		<p class="text-center text-lg dark:text-dark-text text-light-text">No data available</p>
	{:else if data.period === 'daily'}
		<DailyChart data={data.history} />
	{:else if data.period === 'weekly'}
		<WeeklyMonthly data={data.history} />
	{:else}
		<WeeklyMonthly data={data.history} />
	{/if}
</main>
