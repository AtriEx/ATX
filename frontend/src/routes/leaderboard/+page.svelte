<script lang="ts">
	import Podium from '$lib/components/PodiumComponent.svelte';
	import type { PageData } from './$types';

	export let data: PageData;

	$: top3 = data.users.slice(0, 3);
	$: rest = data.users.slice(3);
</script>

<main class="p-6 md:p-12 lg:p-16">
	<h1
		class="text-5xl lg:text-6xl font-bold text-light-primary dark:text-dark-primary mb-8 md:mb-12"
	>
		Leaderboard
	</h1>
	<Podium users={top3} />
	<div class="overflow-x-auto rounded-lg shadow-lg">
		<table class="w-full text-md md:text-lg lg:text-xl">
			<thead
				class="text-light-text dark:text-dark-text bg-light-secondary dark:bg-dark-secondary rounded-t-lg"
			>
				<tr>
					<th class="px-6 py-4 text-left font-semibold">Rank</th>
					<th class="px-6 py-4 text-left font-semibold">
						<div class="w-8 h-2rounded-full inline-block mr-2 bg-transparent" />
						Name</th
					>
					<th class="px-6 py-4 text-left font-semibold">Net Worth</th>
				</tr>
			</thead>
			<tbody class="divide-y divide-light-primary dark:divide-dark-primary/20">
				{#each rest as player, i (player.userId)}
					<tr
						class="hover:bg-light-accent/10 dark:hover:bg-dark-accent/10 transition duration-150 ease-in-out"
					>
						<td class="px-6 py-4 text-light-text dark:text-dark-text">{i + 4}</td>
						<td class="px-6 py-4 font-medium text-light-primary dark:text-dark-accent">
							<img
								src={player.image}
								alt={player.username}
								class="w-8 h-8 rounded-full inline-block mr-2 bg-slate-500"
							/>
							<a href="/user/{player.userId}">
								{player.username}
							</a>
						</td>
						<td class="px-6 py-4 text-light-text dark:text-dark-text">{player.networth} coins</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</main>
