<script lang="ts">
	import { transformAmount } from '$lib';
	type User = {
		username: string;
		networth: number;
		image: string | null;
		userId: string;
	};

	export let users: User[];
</script>

<div class="flex w-full h-96 items-end justify-center gap-4 md:gap-8 pb-3 text-center">
	<a
		href="/profile/{users[1].username}"
		class="w-1/3 md:w-1/5 bg-light-accent dark:bg-dark-accent/60 rounded-t-3xl shadow-2xl flex flex-col items-center justify-center md:p-6 h-[75%] transform transition duration-500 hover:-translate-y-2"
	>
		<img
			src={users[1].image}
			alt={users[1].username}
			class="w-20 h-20 rounded-full mb-3 border-4 border-slate-300 dark:border-slate-600 shadow-lg bg-slate-500"
		/>
		<h2 class="text-lg md:text-2xl font-bold text-light-text dark:text-dark-text">
			{users[1].username}
		</h2>
		<p class="text-light-text dark:text-dark-text">
			<strong>{transformAmount(users[1].networth)}</strong> coins
		</p>
		<div
			class="bg-slate-300 dark:bg-slate-600 text-light-text dark:text-dark-text mt-3 px-3 py-1 rounded-full shadow"
		>
			2nd
		</div>
	</a>
	<a
		href="/profile/{users[0].username}"
		class="w-1/3 md:w-1/5 bg-light-primary dark:bg-dark-primary rounded-t-3xl shadow-2xl flex flex-col items-center justify-center p-6 h-full transform transition duration-500 hover:scale-110"
	>
		<img
			src={users[0].image}
			alt={users[0].username}
			class="w-24 h-24 rounded-full mb-3 border-4 border-yellow-500 dark:border-yellow-400 shadow-lg bg-slate-500"
		/>
		<h1 class="text-xl md:text-3xl font-bold text-light-text dark:text-dark-text">
			{users[0].username}
		</h1>
		<p class="text-light-text dark:text-dark-text">
			<strong>{transformAmount(users[0].networth)}</strong> coins
		</p>
		<div
			class="bg-yellow-400 text-light-text dark:text-dark-text mt-3 px-3 py-1 rounded-full shadow"
		>
			1st
		</div>
	</a>
	<a
		href="/profile/{users[2].username}"
		class="w-1/3 md:w-1/5 bg-light-accent dark:bg-dark-accent/50 rounded-t-3xl shadow-lg flex flex-col items-center justify-center p-6 h-[60%] transform transition duration-500 hover:-translate-y-2"
	>
		<img
			src={users[2].image}
			alt={users[2].username}
			class="w-20 h-20 rounded-full mb-3 border-4 border-amber-600 dark:border-amber-800 shadow-lg bg-slate-500"
		/>
		<h2 class="text-lg md:text-2xl font-bold text-light-text dark:text-dark-text">
			{users[2].username}
		</h2>
		<p class="text-light-text dark:text-dark-text">
			<strong>{transformAmount(users[2].networth)}</strong> coins
		</p>
		<div
			class="bg-amber-600 dark:bg-amber-800 text-light-text dark:text-dark-text mt-3 px-3 py-1 rounded-full shadow"
		>
			3rd
		</div>
	</a>
</div>
