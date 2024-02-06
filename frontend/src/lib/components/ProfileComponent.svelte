<script lang="ts">
	import { formatDate, formatNumber } from '$lib/format';
	import type { Database } from '$lib/supabase.types';
	import AchievementComponent from './AchievementComponent.svelte';
	import ProfileBadge from './ProfileBadge.svelte';
	import ShareProfile from './ShareProfile.svelte';
	import StockCard from './StockCard.svelte';

	export let image: string | null = null;
	export let username: string;
	export let joined_at: string;
	export let networth: number;
	export let stocks: Array<Database['public']['Tables']['stockInfo']['Row']>;
	export let badges: Array<Database['public']['Tables']['flags']['Row']>;
	export let achievements: Array<Database['public']['Tables']['flags']['Row']>;
	export let balance: number;
</script>

<header class="mx-5 my-3 p-4 bg-light-background dark:bg-dark-background rounded-lg shadow-md flex">
	<div class="flex items-center space-x-4 w-full">
		<img
			src={image}
			alt="{username} Image"
			class="w-10 h-10 md:w-16 md:h-16 rounded-full bg-gray-200 dark:bg-gray-600 border-light-accent dark:border-dark-accent/90 border-2 shadow"
		/>

		<div class="flex-grow">
			<h1 class="text-2xl md:text-3xl font-bold text-light-primary dark:text-dark-primary">
				{username}
			</h1>
			<p class="text-sm md:text-base text-gray-600 dark:text-gray-300 mt-2">
				Joined {formatDate(joined_at)}
			</p>
			<div class="flex space-x-2 mt-2">
				{#each badges as badge}
					<ProfileBadge {...badge} />
				{/each}
			</div>
		</div>
	</div>
</header>

<main class="mx-5 my-3 p-4 bg-light-background dark:bg-dark-background rounded-lg shadow-md">
	<div class="flex justify-between items-center">
		<div class="flex">
			<p class="text-md md:text-lg text-light-text dark:text-dark-text font-semibold">
				Current net worth:
				<span class="text-green-600">{formatNumber(networth)}</span>
			</p>
			<p class="text-md md:text-lg text-light-text dark:text-dark-text font-semibold ml-4">
				Current balance:
				<span class="text-green-600">{formatNumber(balance)}</span>
			</p>
		</div>
		<ShareProfile userName={username} />
	</div>
	<div class="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4 mt-5">
		<div class="w-full md:w-3/5">
			<h2 class="text-xl md:text-2xl font-bold text-light-text dark:text-dark-text">
				Stocks Owned
			</h2>
			<div
				class="h-80 md:h-96 overflow-y-auto mt-3 bg-light-background dark:bg-dark-background rounded p-2"
			>
				{#each stocks as stock}
					<StockCard {...stock} />
				{/each}
			</div>
		</div>
		<div class="w-full md:w-2/5">
			<h2 class="text-xl md:text-2xl font-bold text-light-text dark:text-dark-text">
				Achievements
			</h2>
			<div
				class="h-80 md:h-96 overflow-y-auto mt-3 bg-light-background dark:bg-dark-background rounded p-2"
			>
				{#each achievements as achievement}
					<AchievementComponent {achievement} />
				{/each}
			</div>
		</div>
	</div>
</main>
