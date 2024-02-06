<script lang="ts">
	interface StockCardProps {
		name: string | undefined;
		image: string | undefined;
		description: string | undefined;
		quantity: number | undefined;
		price: number | undefined;
	}

	export let stock: StockCardProps;

	console.log(stock);
</script>

<div
	class="bg-light-background dark:bg-dark-secondary rounded-lg shadow-md p-2 sm:p-5 my-4 flex flex-col md:flex-row items-center md:space-y-0"
>
	<div class="flex flex-col w-full gap-3">
		<div class="flex flex-row items-center gap-3">
			<a
				href="/{stock.name}"
				class="text-2xl font-bold text-light-primary dark:text-dark-primary hover:underline transition ease-in-out duration-200 active:scale-95"
			>
				{stock.name}
			</a>
			<div class="flex flex-col sm:flex-row sm:items-center sm:space-x-4">
				<p class="text-md font-medium text-light-text dark:text-dark-text">
					<span class="text-light-text/80 dark:text-dark-text/80">
						{stock.quantity} stock(s) at {stock.price} coins each
					</span>
				</p>
			</div>
		</div>
		<div class="">
			<p class="text-light-text dark:text-dark-text">{stock.description}</p>
		</div>
	</div>

	<img
		src={stock.image}
		alt="{stock.name} Icon"
		class="w-24 h-24 rounded-3xl m-4 bg-gray-200 border-light-accent dark:border-dark-accent border-2 p-2"
	/>
</div>
