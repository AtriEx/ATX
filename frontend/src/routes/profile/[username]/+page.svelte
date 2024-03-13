<script lang="ts">
	import type { PageData } from './$types';
	import { formatDate, formatNumber } from '$lib/format';
	import AchievementComponent from '$lib/components/AchievementComponent.svelte';
	import ProfileBadge from '$lib/components/ProfileBadge.svelte';
	import ShareProfile from '$lib/components/ShareProfile.svelte';
	import StockCard from '$lib/components/StockCard.svelte';

	export let data: PageData;
	$: profile = data.profile;
</script>

<svelte:head>
	<title>{profile.username}'s Profile</title>
	<meta
		name="description"
		content="{profile.username}'s profile page \n Networth: {profile.networth} \n Balance: {profile.balance}"
	/>
</svelte:head>

<div class="dark:bg-dark-background bg-light-background flex flex-col flex-1">
	<div class="mx-5 my-3 p-6 bg-dark-primary/5 dark:bg-dark-primary/10 rounded-lg shadow-lg flex">
		<div class="flex items-center space-x-4 w-full">
			<img
				src={profile.image}
				alt="{profile.username} Image"
				class="w-16 h-16 lg:w-20 lg:h-20 rounded-full bg-gray-200 dark:bg-gray-700 border-light-accent dark:border-dark-accent border-4 shadow-lg"
			/>
			<div class="flex flex-col grow">
				<div class="flex-grow flex md:flex-row flex-col md:items-center md:space-x-4">
					<h1 class="text-3xl lg:text-4xl font-bold text-light-primary dark:text-dark-primary">
						{profile.username}
					</h1>
					<div class="flex space-x-2 mt-2 md:mt-0">
						{#each profile.badges as badge}
							<ProfileBadge {...badge} />
						{/each}
					</div>
				</div>
				<div class="flex flex-row items-center w-full justify-between mt-4">
					<div
						class="flex flex-col lg:flex-row gap-4 uppercase font-bold text-gray-600 dark:text-gray-300"
					>
						<p class="text-base lg:text-lg">
							Joined: <span class="text-light-primary dark:text-dark-accent"
								>{formatDate(profile.joined_at)}</span
							>
						</p>
						<p class="text-base lg:text-lg">
							NETWORTH: <span class="text-light-primary dark:text-dark-accent"
								>{formatNumber(profile.networth)} Coins</span
							>
						</p>
						<p class="text-base lg:text-lg">
							Balance: <span class="text-light-primary dark:text-dark-accent font-bold"
								>{formatNumber(profile.balance)} Coins</span
							>
						</p>
					</div>
					<ShareProfile userName={profile.username} />
				</div>
			</div>
		</div>
	</div>

	<div class="md:flex flex-wrap m-5 gap-5">
		<div
			class="flex-1 min-w-[40%] bg-dark-primary/5 dark:bg-dark-primary/10 rounded-xl p-6 shadow-lg"
		>
			<h2 class="text-2xl font-bold text-light-text dark:text-dark-text">Stocks Owned</h2>
			<div
				class="h-80 overflow-y-auto scrollbar-thin scrollbar-thumb-light-accent dark:scrollbar-thumb-dark-accent mt-3 rounded p-4"
			>
				{#if profile?.stocks.length === 0}
					<p class="text-center text-light-text dark:text-dark-text mt-24 font-bold text-lg">
						{profile?.username} doesn't own any stocks yet.
					</p>
				{:else}
					{#each profile?.stocks as stock}
						<StockCard {stock} />
					{/each}
				{/if}
			</div>
		</div>

		<div
			class="flex-1 min-w-[40%] bg-dark-primary/5 dark:bg-dark-primary/10 rounded-xl p-6 shadow-lg"
		>
			<h2 class="text-2xl font-bold text-light-text dark:text-dark-text">Achievements</h2>
			<div
				class="h-80 overflow-y-auto scrollbar-thin scrollbar-thumb-light-accent dark:scrollbar-thumb-dark-accent mt-3 rounded p-4"
			>
				{#each profile.achievements as achievement}
					<AchievementComponent {achievement} />
				{/each}
			</div>
		</div>
	</div>
</div>
