<script lang="ts">
    import "../app.css";
    import Header from "$lib/components/Header.svelte";
	import MobileNavigationBar from "$lib/components/MobileNavigationBar.svelte";
</script>

<div class="max-w-full">
    <Header />
    <slot />
    <MobileNavigationBar />
</div>