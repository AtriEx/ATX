<script lang="ts">
	import Badge from './ui/badge/badge.svelte';
	import * as HoverCard from './ui/hover-card';

	export let name: string;
	export let image: string | null = null;
	export let description: string | null = null;
</script>

<HoverCard.Root>
	<HoverCard.Trigger>
		<Badge class="">
			{name}
		</Badge>
	</HoverCard.Trigger>
	<HoverCard.Content
		class="p-6 bg-light-primary dark:bg-dark-background/80 rounded-lg shadow-lg w-full max-w-lg"
	>
		<div class="flex items-center space-x-4">
			<img
				src={image}
				alt="{name} Badge"
				class="w-10 h-10 md:w-16 md:h-16 rounded-full bg-gray-200 dark:bg-gray-600 border-light-accent dark:border-dark-accent border-2 shadow"
			/>
			<div class="flex-grow text-light-text dark:text-dark-text">
				<h1 class="text-2xl md:text-3xl font-bold">
					{name}
				</h1>
				<p class="text-md md:text-lg mt-2">
					{description}
				</p>
			</div>
		</div>
	</HoverCard.Content>
</HoverCard.Root>
