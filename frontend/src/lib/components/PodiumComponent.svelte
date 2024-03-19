<script lang="ts">
	type User = {
		username: string;
		networth: number;
		image: string | null;
		userId: string;
	};

	export let users: User[];
</script>

<div class="flex w-full h-96 items-end justify-center gap-8 p-3">
	<div
		class="w-1/5 bg-light-accent dark:bg-dark-accent/60 rounded-t-3xl shadow-2xl flex flex-col items-center justify-center p-6 h-[75%] transform transition duration-500 hover:-translate-y-2"
	>
		<img
			src={users[1].image}
			alt={users[1].username}
			class="w-20 h-20 rounded-full mb-3 border-4 border-slate-50 dark:border-slate-600 shadow-lg bg-slate-500"
		/>
		<h2 class="text-2xl font-bold text-light-text dark:text-dark-text">
			{users[1].username}
		</h2>
		<p class="text-light-text dark:text-dark-text">
			<strong>{users[1].networth}</strong> coins
		</p>
		<div
			class="bg-slate-50 dark:bg-slate-600 text-light-text dark:text-dark-text mt-3 px-3 py-1 rounded-full shadow"
		>
			2nd
		</div>
	</div>
	<div
		class="w-1/5 bg-light-primary dark:bg-dark-primary rounded-t-3xl shadow-2xl flex flex-col items-center justify-center p-6 h-full transform transition duration-500 hover:scale-110"
	>
		<img
			src={users[0].image}
			alt={users[0].username}
			class="w-24 h-24 rounded-full mb-3 border-4 border-yellow-500 dark:border-yellow-400 shadow-lg bg-slate-500"
		/>
		<h1 class="text-3xl font-bold text-light-text dark:text-dark-text">
			{users[0].username}
		</h1>
		<p class="text-light-text dark:text-dark-text">
			<strong>{users[0].networth}</strong> coins
		</p>
		<div
			class="bg-yellow-400 text-light-text dark:text-dark-text mt-3 px-3 py-1 rounded-full shadow"
		>
			1st
		</div>
	</div>
	<div
		class="w-1/5 bg-light-accent dark:bg-dark-accent/50 rounded-t-3xl shadow-lg flex flex-col items-center justify-center p-6 h-[60%] transform transition duration-500 hover:-translate-y-2"
	>
		<img
			src={users[2].image}
			alt={users[2].username}
			class="w-20 h-20 rounded-full mb-3 border-4 border-amber-600 dark:border-amber-800 shadow-lg bg-slate-500"
		/>
		<h2 class="text-2xl font-bold text-light-text dark:text-dark-text">
			{users[2].username}
		</h2>
		<p class="text-light-text dark:text-dark-text">
			<strong>{users[2].networth}</strong> coins
		</p>
		<div
			class="bg-amber-600 dark:bg-amber-800 text-light-text dark:text-dark-text mt-3 px-3 py-1 rounded-full shadow"
		>
			3rd
		</div>
	</div>
</div>
