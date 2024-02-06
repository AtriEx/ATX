<script lang="ts">
	export let name: string;
	export let totalShares: number;
	export let image: string | null = null;
</script>

<div
	class="bg-light-background dark:bg-dark-background rounded-lg shadow-md p-4 sm:p-5 my-4 flex flex-col md:flex-row items-center space-y-4 md:space-y-0"
>
	<div class="flex flex-col items-start space-y-3 w-full">
		<a
			href="/{name}"
			class="text-xl font-semibold text-light-primary dark:text-dark-primary hover:underline transition ease-in-out duration-200 active:scale-95"
			>{name}</a
		>
		<img
			src={image}
			alt="{name} Icon"
			class="w-12 h-12 rounded-full bg-gray-200 border-light-accent dark:border-dark-accent border-2 p-2"
		/>
		<div class="flex flex-col sm:flex-row sm:items-center sm:space-x-4">
			<p class="text-md font-medium text-light-text dark:text-dark-text">
				Shares: <span class="text-light-text/80 dark:text-dark-text/80">{totalShares}</span>
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
