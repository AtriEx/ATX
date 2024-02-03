<script lang="ts">
	import '../app.css';
	import { invalidate } from '$app/navigation';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';

	export let data: PageData;

	let { supabase, session } = data;
	$: ({ supabase, session } = data);

	onMount(() => {
		const { data } = supabase.auth.onAuthStateChange((event, _session) => {
			if (_session?.expires_at !== session?.expires_at) invalidate('supabase:auth');
		});

		return () => data.subscription.unsubscribe();
	});
</script>

<slot />
