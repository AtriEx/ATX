<script lang="ts">
	export let symbol: string;
	export let name: string;
	export let price: number;
	export let quantity: number;
	export let change: number;
</script>

<div
	class="bg-white rounded-lg shadow-md p-4 sm:p-5 my-4 flex flex-col md:flex-row items-center space-y-4 md:space-y-0"
>
	<div class="flex flex-col items-start space-y-3 w-full">
		<a
			href="/{symbol}"
			class="text-xl font-semibold text-sky-600 hover:text-sky-700 hover:underline transition ease-in-out duration-200 active:scale-95"
			>{symbol}</a
		>
		<h3 class="text-lg font-medium text-gray-800">{name}</h3>
		<div class="flex flex-col sm:flex-row sm:items-center sm:space-x-4">
			<p class="text-md font-medium text-gray-800">
				Price: <span class="text-green-600"
					>${price.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span
				>
			</p>
			<p class="text-md font-medium text-gray-800">
				Shares: <span class="text-gray-600">{quantity}</span>
			</p>
			<p class="text-md font-medium text-gray-800 animate-pulse" class:animate-pulse={change !== 0}>
				Change:
				<span class:text-green-600={change > 0} class:text-red-600={change < 0}>
					{change}
					{#if change > 0}
						▲
					{:else if change < 0}
						▼
					{/if}
				</span>
			</p>
		</div>
		<div class="flex items-center space-x-3">
			<button
				class="bg-green-500 hover:bg-green-600 text-white font-medium px-4 py-2 rounded transition duration-200 ease-in-out active:scale-95 active:shadow-inner active:bg-green-700"
				>Buy</button
			>
			<button
				class="bg-red-500 hover:bg-red-600 text-white font-medium px-4 py-2 rounded transition duration-200 ease-in-out active:scale-95 active:shadow-inner active:bg-red-700"
				>Sell</button
			>
		</div>
	</div>
</div>
