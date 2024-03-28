<script lang="ts">
	import { onMount } from 'svelte';

	let newReward: Date = new Date();
	let claimed = false;

	function calculateString() {
		const now = new Date();
		if (newReward <= now) {
			claimed = false;
			return '';
		}

		const diff = newReward.getTime() - now.getTime();
		const hours = Math.floor(diff / (1000 * 60 * 60))
			.toString()
			.padStart(2, '0');
		const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
			.toString()
			.padStart(2, '0');
		const seconds = Math.floor((diff % (1000 * 60)) / 1000)
			.toString()
			.padStart(2, '0');
		return `${hours}:${minutes}:${seconds}`;
	}

	// TODO - Implement
	function claimReward() {
		if (claimed) return;
		// Simulate a server request
		setTimeout(() => {
			claimed = true;
		}, 1000);

		const today = new Date();
		const tomorrow = new Date(today);
		tomorrow.setDate(tomorrow.getDate() + 1);
		newReward = tomorrow;
	}

	let timerString = newReward ? calculateString() : '';

	onMount(() => {
		const interval = setInterval(() => {
			timerString = calculateString();
		}, 1000);

		return () => clearInterval(interval);
	});
</script>

{#if !claimed}
	<button
		on:click={claimReward}
		class="bg-violet-500 hover:bg-violet-600 text-white px-2 md:px-4 py-2 rounded-md shadow transition ease-in-out duration-300 text-xs md:text-base active:scale-95 active:shadow-inner active:bg-violet-700"
		class:animate-pulse={!claimed}
	>
		Claim Reward
	</button>
{:else}
	<p class="text-sm text-gray-600" aria-live="polite">
		Next reward: {timerString}
	</p>
{/if}
