<script lang="ts">
	interface StockCardProps {
		name: string | undefined;
		image: string | undefined;
		description: string | undefined;
		quantity: number | undefined;
		price: number | undefined;
	}

	export let stock: StockCardProps;
</script>

<div
	class="bg-light-background dark:bg-dark-secondary rounded-xl shadow-xl p-5 my-5 flex flex-col md:flex-row items-center justify-between transition duration-300 ease-in-out hover:shadow-2xl"
>
	<div class="flex flex-col md:flex-row md:items-center gap-4 w-full">
		<img
			src={stock.image}
			alt="{stock.name} Icon"
			class="md:w-20 md:h-20 w-24 h-24 rounded-full object-cover bg-gray-200 dark:bg-gray-800 border-light-accent dark:border-dark-accent border-4 shadow-lg transition-transform duration-300 ease-in-out hover:scale-105"
		/>

		<div class="flex-1">
			<a
				href="/{stock.name}"
				class="text-2xl md:text-3xl font-bold text-light-primary dark:text-dark-primary hover:underline transition ease-in-out duration-200 active:scale-95"
			>
				{stock.name}
			</a>
			<p class="text-sm md:text-md text-light-text dark:text-dark-text mt-2">
				<span class="font-medium text-light-accent dark:text-dark-accent">
					{stock.quantity} stock(s) at {stock.price} coins each
				</span>
			</p>
			<p class="mt-2 text-light-text dark:text-dark-text">
				{stock.description}
			</p>
		</div>
	</div>
</div>
