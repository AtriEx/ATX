<script lang="ts">
	import '../app.css';
	import Header from '$lib/components/Header.svelte';
	import MobileNavigationBar from '$lib/components/MobileNavigationBar.svelte';
	import Login from '$lib/components/Login.svelte';
	import { loginDialog } from '$lib/stores/uiStates';
	import { onMount } from 'svelte';
	import { supabase, onLogin, onLogout } from '$lib/supabase';

	onMount(() => {
		supabase.auth.onAuthStateChange((event, session) => {
			if (event === 'SIGNED_IN') {
				try {
					onLogin();
				} catch (error) {
					console.error('Error in onAuthStateChange', error);
				}
			}
			if (event === 'SIGNED_OUT') {
				try {
					onLogout();
				} catch (error) {
					console.error();
				}
			}
		});
	});
</script>

<svelte:head>
	<title>ATX</title>
	<meta name="description" content="Get addicted to selling stocks." />
</svelte:head>

<div class="w-full" class:blur-sm={$loginDialog}>
	<Header />
	<slot />
	<MobileNavigationBar />
</div>

{#if $loginDialog}
	<Login />
{/if}
