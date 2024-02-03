<script lang="ts">
	import HeaderUserView from "./HeaderUserView.svelte";
	import HeaderNavigationBar from "./HeaderNavigationBar.svelte";
</script>

<div class="py-2 px-3 bg-blue-950 flex flex-row flex-nowrap items-center justify-between">
    <a href="/"><img class="h-8" src="/logos/ATX_NameWhite.svg" alt="The ATX logo." /></a>
    <HeaderNavigationBar/>
    <HeaderUserView />
</div>