<script lang="ts">
	import ProfileBadge from '$lib/components/ProfileBadge.svelte';
	import RewardButton from '$lib/components/RewardButton.svelte';
	import ShareProfile from '$lib/components/ShareProfile.svelte';
	import StockCard from '$lib/components/StockCard.svelte';
	import type { PageData } from './$types';
	import * as Dialog from '$lib/components/ui/dialog';

	export let data: PageData;
	$: profile = data.userProfile;

	function formatDate(date: Date) {
		return date.toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		});
	}

	function formatNumber(num: number) {
		return num.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
	}

	let modal = true;
	$: () => console.log(modal);
</script>

<svelte:head>
	<title>{profile.username}'s Profile</title>
	<meta name="description" content="{profile.username}'s profile page" />
</svelte:head>

{#if profile}
	<header class="m-5 p-5 bg-white rounded-lg shadow-lg flex">
		<div class="flex items-center space-x-5 w-full">
			{#if profile.image}
				<img
					src={profile.image}
					alt="{profile.username} Image"
					class="w-8 h-8 md:w-16 md:h-16 rounded-full bg-gray-300 border-violet-300 border-2"
				/>
			{:else}
				<div class="w-8 h-8 md:w-16 md:h-16 rounded-full bg-gray-300 border-violet-300 border-2" />
			{/if}
			<div class="flex-grow">
				<h1 class="text-xl md:text-3xl font-bold text-violet-700">{profile.username}</h1>
				<p class="text-slate-500 mt-1 text-xs md:text-base">
					Joined {formatDate(profile.joined_at)}
				</p>
			</div>
		</div>
	</header>
	<main class="m-5 p-5 bg-white rounded-lg shadow-lg">
		<div class="flex justify-between">
			<p class="text-sm md:text-lg font-bold text-slate-700 inline-block">
				Current net worth:
				<span class="font-bold text-green-500">{formatNumber(profile.networth)}</span>
			</p>
			<ShareProfile userName={profile.username} />
		</div>
		<div class="flex flex-col md:flex-row">
			<div class="mt-5 w-full md:w-3/5">
				<h2 class="text-lg md:text-2xl font-bold text-black">Stocks Owned</h2>
				<div class="h-96 overflow-y-scroll">
					{#each profile.stocks as stock}
						<StockCard {...stock} />
					{/each}
				</div>
			</div>
			<div class="mt-5 w-full md:w-2/5">
				<h2 class="text-lg md:text-2xl font-bold text-black">Badges</h2>
				<div class="h-96 overflow-y-scroll">
					{#each profile.badges as badge}
						<ProfileBadge {...badge} />
					{/each}
				</div>
			</div>
		</div>
	</main>
{:else}
	<header class="mx-5 my-3 p-4 bg-white rounded-lg shadow-md flex">
		<div class="flex items-center space-x-4 w-full">
			<div class="w-10 h-10 md:w-16 md:h-16 rounded-full bg-gray-300 border-violet-400 border-2" />
			<div class="flex-grow">
				<h1 class="text-2xl md:text-3xl font-bold text-violet-800">Your Name</h1>
				<p class="text-gray-600 text-sm md:text-base mt-1">
					Joined {formatDate(new Date())}
				</p>
			</div>
			<div class="flex-shrink-0">
				<Dialog.Root open>
					<Dialog.Trigger>
						<button
							class="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded transition duration-200 ease-in-out"
						>
							Register/Login
						</button>
					</Dialog.Trigger>
					<Dialog.Content class="bg-white rounded-lg p-6 shadow-lg sm:max-w-lg mx-auto">
						<Dialog.Header class="border-b border-gray-200 pb-4 mb-4">
							<Dialog.Title class="text-xl font-semibold text-gray-800"
								>Register to create and view your own profile</Dialog.Title
							>
							<Dialog.Description class="text-sm text-gray-600 mt-2">
								You need to register to create and view your own profile. If you already have an
								account, please log in.
							</Dialog.Description>
						</Dialog.Header>
						<div class="	text-center">
							<p class="text-md text-gray-700">Click the button below to register/login</p>
							<a href="/register" class="text-blue-500 hover:underline">Register/Login</a>
						</div>
					</Dialog.Content>
				</Dialog.Root>
			</div>
		</div>
	</header>

	<main class="mx-5 my-3 p-4 bg-white rounded-lg shadow-md">
		<div class="flex justify-between">
			<p class="text-md md:text-lg text-gray-800 font-semibold">
				Your current net worth: <span class="text-green-600 font-bold">{formatNumber(0)}</span>
			</p>
		</div>
		<div class="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4 mt-5">
			<div class="w-full md:w-3/5">
				<h2 class="text-xl md:text-2xl font-bold text-gray-800">Your Stocks</h2>
				<div class="h-80 md:h-96 overflow-y-auto mt-3 bg-gray-100 rounded p-2"></div>
			</div>
			<div class="w-full md:w-2/5">
				<h2 class="text-xl md:text-2xl font-bold text-gray-800">Badges</h2>
				<div class="h-80 md:h-96 overflow-y-auto mt-3 bg-gray-100 rounded p-2"></div>
			</div>
		</div>
	</main>
{/if}
