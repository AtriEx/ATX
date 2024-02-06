<script lang="ts">
	import type { PageData } from './$types';
	import { formatDate, formatNumber } from '$lib/format';
	import type { Database } from '$lib/supabase.types';
	import AchievementComponent from '$lib/components/AchievementComponent.svelte';
	import ProfileBadge from '$lib/components/ProfileBadge.svelte';
	import ShareProfile from '$lib/components/ShareProfile.svelte';
	import StockCard from '$lib/components/StockCard.svelte';

	export let data: PageData;
	$: profile = data.profile;

	console.log(data);
</script>

<svelte:head>
	<title>{profile.username}'s Profile</title>
	<meta name="description" content="{profile.username}'s profile page" />
</svelte:head>

<div class="dark:bg-dark-background bg-light-background flex-1">
	<div class="mx-5 my-3 p-4 bg-dark-primary/5 dark:bg-dark-primary/10 rounded-lg shadow-md flex">
		<div class="flex items-center space-x-4 w-full">
			<img
				src={profile.image}
				alt="{profile.username} Image"
				class="w-10 h-10 md:w-16 md:h-16 rounded-full bg-gray-200 dark:bg-gray-600 border-light-accent dark:border-dark-accent/90 border-2 shadow"
			/>
			<div class="flex flex-col grow">
				<div class="flex-grow flex md:flex-row flex-col md:items-center md:gap-2">
					<h1 class="text-2xl md:text-3xl font-bold text-light-primary dark:text-dark-primary">
						{profile.username}
					</h1>
					<div class="flex space-x-2 mt-2">
						{#each profile.badges as badge}
							<ProfileBadge {...badge} />
						{/each}
					</div>
				</div>
				<div class="flex flex-row items-center w-full justify-between grow">
					<div class="flex flex-row grow gap-2 uppercase font-bold">
						<p class="text-sm md:text-base text-gray-600 dark:text-gray-300 mt-2">
							Joined:
							<span class="text-light-primary">
								{formatDate(profile.joined_at)}
							</span>
						</p>
						<p class="text-sm md:text-base text-gray-600 dark:text-gray-300 mt-2 font-bold">
							NETWORTH:
							<span class="text-light-primary">
								{formatNumber(profile.networth)} Coins
							</span>
						</p>
						<p class="text-sm md:text-base text-gray-600 dark:text-gray-300 mt-2 uppercase">
							Balance:
							<span class="text-light-primary font-bold">
								{formatNumber(profile.balance)} Coins
							</span>
						</p>
					</div>
					<ShareProfile userName={profile.username} />
				</div>
			</div>
		</div>
	</div>

	<div class="flex m-5 gap-5">
		<div class="w-full md:w-3/5 bg-dark-primary/5 dark:bg-dark-primary/10 rounded-xl p-5 shadow-md">
			<h2 class="text-xl md:text-2xl font-bold text-light-text dark:text-dark-text">
				Stocks Owned
			</h2>
			<div class="h-80 md:h-96 overflow-y-auto transparent-scrollbar mt-3 rounded p-2">
				{#if profile?.stocks.length === 0}
					<p class="text-center text-light-text dark:text-dark-text">No stocks owned</p>
				{:else}
					{#each profile?.stocks as stock}
						<StockCard {stock} />
					{/each}
				{/if}
			</div>
		</div>

		<div class="w-full md:w-2/5 bg-dark-primary/5 dark:bg-dark-primary/10 rounded-xl p-5 shadow-md">
			<h2 class="text-xl md:text-2xl font-bold text-light-text dark:text-dark-text">
				Achievements
			</h2>
			<div class="h-80 md:h-96 overflow-y-auto mt-3 p-2">
				{#each profile.achievements as achievement}
					<AchievementComponent {achievement} />
				{/each}
			</div>
		</div>
	</div>
</div>
