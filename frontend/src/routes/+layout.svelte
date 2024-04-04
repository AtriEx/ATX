<script lang="ts">
	import '../app.css';
	import Header from '$lib/components/Header.svelte';
	import MobileNavigationBar from '$lib/components/MobileNavigationBar.svelte';
	import Login from '$lib/components/Login.svelte';
	import { loginDialog, debugMenu } from '$lib/stores/uiStates';
	import { onMount } from 'svelte';
	import { supabase, onLogin, onLogout } from '$lib/supabase';
	import { PUBLIC_ENVIRONMENT } from '$env/static/public';
	import DebugMenu from '$lib/components/DebugMenu.svelte';
	import { Toaster } from 'svelte-french-toast';

	onMount(() => {
		supabase.auth.onAuthStateChange((event, session) => {
			switch (event) {
				case 'INITIAL_SESSION':
					if(session === null)break;
				case 'SIGNED_IN':
					try {
						onLogin();
					} catch (error) {
						console.error('Error in onAuthStateChange', error);
					}
					break;

				case 'SIGNED_OUT':
					try {
						onLogout();
					} catch (error) {
						console.error();
					}
					break;
			}
		});
	});
</script>

<svelte:head>
	<title>ATX</title>
	<meta name="description" content="Get addicted to selling stocks." />
</svelte:head>

<div class="w-full" class:blur-sm={$loginDialog || $debugMenu}>
	<Header />
	<slot />
	<MobileNavigationBar />
</div>

{#if $loginDialog}
	<Login />
{/if}

{#if $debugMenu}
	<DebugMenu />
{/if}

{#if PUBLIC_ENVIRONMENT === 'development'}
	<div class="fixed bottom-0 right-0 p-2">
		<button
			class="bg-red-500 text-white p-2 rounded-md"
			on:click={() => ($debugMenu = !$debugMenu)}
		>
			Debug
		</button>
	</div>
{/if}

<Toaster />
