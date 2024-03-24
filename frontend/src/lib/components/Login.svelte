<script>
	import { faTwitch } from '@fortawesome/free-brands-svg-icons';
	import { faXmark } from '@fortawesome/free-solid-svg-icons';
	import Fa from 'svelte-fa';
	import { login } from '$lib/supabase';
	import { loginDialog } from '$lib/stores/uiStates';

	const handleLogin = () => {
		login();
	};
</script>

<div class="absolute top-0 left-0 w-screen h-screen z-1 flex justify-center items-center">
	<div
		class=" bg-light-background dark:bg-dark-primary/5 h-3/8 md:h-1/5  lg:w-1/3 md:w-2/4 w-4/5 rounded-xl relative flex border border-dark-accent"
	>
		<div class="absolute scale-50 right-0 mr-1 text-light-text dark:text-dark-text">
			<button on:click={() => ($loginDialog = false)}>
				<Fa icon={faXmark} class="text-5xl" />
			</button>
		</div>
		<div class="flex flex-col justify-between items-center w-full grow pt-5 pb-2 px-6">

			<span class=" flex flex-col items-center w-full border-b-2 border-dark-secondary text-light-text dark:text-dark-text ">

				<h1 class="text-3xl pt-2 font-extrabold pb-2">Login with Twitch</h1>

			</span>
			<div class="p-2">
				<button
					class="bg-twitch text-dark-text text-lg px-8 p-2 rounded-md flex flex-row items-center md:scale-125"
					on:click={handleLogin}
				>
					<Fa icon={faTwitch} class="mr-2" />
					Login
				</button>
			</div>
			<span class="text-light-text dark:text-dark-text text-xs p-2">
				We are not affiliated with Twitch in any way!
			</span>
		</div>
	</div>
</div>
