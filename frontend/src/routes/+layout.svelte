<script lang="ts">
    import "../app.css";
    import Header from "$lib/components/Header.svelte";
	import MobileNavigationBar from "$lib/components/MobileNavigationBar.svelte";
</script>

<svelte:head>
	<title>ATX</title>
	<meta name="description" content="Get addicted to selling stocks." />
</svelte:head>

<div class="w-full">
    <Header />
    <slot />
    <MobileNavigationBar />
</div> 