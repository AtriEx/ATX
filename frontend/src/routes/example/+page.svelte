<script lang="ts">
	import { supabase } from '$lib/supabase';
	import { onMount } from 'svelte';

	interface StockInfo {
		id: number;
		name: string;
	}

	// Data coming from load function in the +page.server.ts file
	export let data;

	let directExampleData: Array<StockInfo> = [];
	let pageLoadExampleData: Array<StockInfo> = data.stockInfo;
	let apiEndpointExampleData: Array<StockInfo> = [];

	// Data coming straight from the supabase API
	// Slower than using the API endpoint
	async function exampleLoad() {
		try {
			const { data: fetchedData } = await supabase.from('stockInfo').select('*').throwOnError();
			directExampleData = fetchedData as StockInfo[];
		} catch (error) {
			console.error(error);
		}
	}

	// Data coming from the API endpoint
	// Faster than using the supabase API, and has admin access be careful when using
	async function exampleApiGet() {
		try {
			const response = await fetch('/api/exampleEndpoint');
			if (response.ok) {
				const result = await response.json();
				apiEndpointExampleData = result;
				console.log(result, result);
			} else {
				throw new Error('Failed to fetch data');
			}
		} catch (error) {
			console.error(error);
		}
	}

	exampleLoad();
	onMount(() => {
		exampleApiGet();
	});
</script>

<h1>Page</h1>

<p>Direct Example Data</p>
<ul>
	{#each directExampleData as stock}
		<li>{stock.name}</li>
	{/each}
</ul>

<p>Page Load Example Data</p>
<ul>
	{#each pageLoadExampleData as stock}
		<li>{stock.name}</li>
	{/each}
</ul>

<p>API Endpoint Example Data</p>
<ul>
	{#each apiEndpointExampleData as stock}
		<li>{stock.name}</li>
	{/each}
</ul>
