<script lang="ts">

	import { rewardsDialog } from  '$lib/stores/uiStates';
	import { claimReward } from'$lib/supabase';
	import { loggedIn, user, profile } from '../stores/userData';

	const handleReward = () => {
		claimReward();
	};
</script>

<div class="absolute top-0 left-0 w-screen h-screen z-1 flex justify-center items-center">
	<div
		class=" bg-light-background dark:bg-dark-secondary/20 h-3/8 md:h-1/5  lg:w-1/3 md:w-2/4 w-4/5 rounded-xl relative flex border-2 border-dark-accent"
	>
		<div class="flex flex-col justify-between items-center w-full grow pt-5 pb-2">

			<span class=" flex flex-col items-center w-full border-b-2 border-dark-secondary text-light-text dark:text-dark-text ">

				<h1 class="text-3xl pt-2 font-extrabold pb-2">
					Daily Login Reward
				</h1>

				<p>*this is a dark pattern to keep you trading*</p>

			</span>

			<div class="text-green-500">
				&lt;Money or Stock PlaceHolder&gt;
			</div>

			<div class="p-2">
				<button
					class="bg-dark-primary text-light-text text-lg px-8 p-2 rounded-md flex flex-row items-center md:scale-125 mb-2 hover:bg-dark-primary/70"
					on:click={handleReward}
				>
					Claim
				</button>
			</div>
		</div>
	</div>
</div>