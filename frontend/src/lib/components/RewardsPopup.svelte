<script lang="ts">

	import { rewardsDialog } from  '$lib/stores/uiStates';
	import { claimReward } from'$lib/supabase';
	import { loggedIn, user, profile } from '../stores/userData';
	import { Confetti } from "svelte-confetti"

	const handleReward = () => {
		claimReward();
	};
	
</script>

<div class="absolute top-0 left-0 w-screen h-screen z-1 flex justify-center items-center overflow-hidden">

	<div
		class="bg-light-background dark:bg-dark-primary/5 w-4/5 h-3/8 md:h-1/5 md:w-2/4 lg:w-1/3 min-h-64 rounded-xl relative flex border border-dark-accent"
	>

		<div class="flex flex-col justify-between items-center w-full grow pt-5 pb-2 px-6">
			<span class=" flex flex-col items-center w-full px-4 border-b-2 border-dark-secondary text-light-text dark:text-dark-text ">

				<h1 class="text-l md:text-xl lg:text-3xl pt-2 font-extrabold pb-2">
					Daily Login Reward
				</h1>
			</span>
			<p class="text-light-text dark:text-dark-text">*we're manipulating you*</p>
			<!-- STOCK OR MONEY VALUES GOES IN THIS DIV -->
			<div class="text-green-500">
				&lt;Money or Stock PlaceHolder&gt;
			</div>

			<div class="p-2">
				<button
					class="bg-dark-primary text-light-text text-lg px-8 p-2 rounded-md flex flex-row items-center md:scale-125 mb-2 hover:bg-dark-primary/70"
					on:click={handleReward}
				>
					<Confetti x={[-3, 3]} y={[-3,3]}/>
					Claim
				</button>

			</div>
		</div>
	</div>
</div>