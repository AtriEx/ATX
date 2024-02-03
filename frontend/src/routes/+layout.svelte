<script lang="ts">
    import "../app.css";
    import Header from "$lib/components/Header.svelte";
	import MobileNavigationBar from "$lib/components/MobileNavigationBar.svelte";

    let isMobile : Boolean = false;
</script>

<Header />
<slot />
{#if !isMobile}
    <MobileNavigationBar />
{/if}


<style>

</style>