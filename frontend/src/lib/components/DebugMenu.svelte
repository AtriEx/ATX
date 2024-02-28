<script>
	import { profile, user, loggedIn } from '$lib/stores/userData';
	import { loginDialog, debugMenu } from '$lib/stores/uiStates';
	import { getProfile, getUser, supabase } from '$lib/supabase';

	function logProfile() {
		console.log($profile);
	}

	function logUser() {
		console.log($user);
	}

	function refresh() {
		getProfile();
		getUser();
	}

	function openLoginDialog() {
		$loginDialog = true;
		$debugMenu = false;
	}

	async function runExampleEdgeFunction() {
		try {
			const { data } = await supabase.functions.invoke('example-function', {
				body: { exampleParameter: 'exampleValue' }
			});
			console.log(data);
		} catch (error) {
			console.error(error);
		}
	}
</script>

<div class="absolute top-0 left-0 w-screen h-screen z-1 flex justify-center items-center">
	<div class=" bg-light-primary h-2/3 w-4/5 rounded-lg flex flex-col gap-2 p-4">
		<div class="text-2xl font-bold text-center">Debug Menu</div>
		<div class="gap-2 flex">
			<button
				class="bg-twitch text-white text-lg px-8 p-2 rounded-md flex flex-row items-center"
				on:click={logProfile}
			>
				Log Profile
			</button>
			<button
				class="bg-twitch text-white text-lg px-8 p-2 rounded-md flex flex-row items-center"
				on:click={logUser}
			>
				Log User
			</button>
			<button
				class="bg-twitch text-white text-lg px-8 p-2 rounded-md flex flex-row items-center"
				on:click={refresh}
			>
				Refresh
			</button>
			<button
				class="bg-twitch text-white text-lg px-8 p-2 rounded-md flex flex-row items-center"
				on:click={openLoginDialog}
			>
				Open login dialog
			</button>
			<button
				class="bg-twitch text-white text-lg px-8 p-2 rounded-md flex flex-row items-center"
				on:click={runExampleEdgeFunction}
			>
				Run Example Edge Function
			</button>
		</div>

		<div class="flex flex-col">
			<span class="text-lg font-bold">Stats</span>
			<span>LoggedIn: {$loggedIn}</span>
		</div>
	</div>
</div>
