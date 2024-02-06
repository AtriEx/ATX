<script lang="ts">
	import type { PageData } from './$types';
	import ProfileComponent from '$lib/components/ProfileComponent.svelte';

	export let data: PageData;
	$: profile = data.profile;
</script>

<svelte:head>
	<title>{profile.username}'s Profile</title>
	<meta name="description" content="{profile.username}'s profile page" />
</svelte:head>

<ProfileComponent {...profile} />
