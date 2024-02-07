<script lang="ts">
	import HeaderUserView from "./HeaderUserView.svelte";
	import HeaderNavigationBar from "./HeaderNavigationBar.svelte";
</script>

<div class="py-2 px-3 bg-light-background border-0 dark:bg-dark-background dark:border-dark-secondary dark:border-b-[1px] flex flex-row flex-nowrap items-center justify-between drop-shadow-lg">
    <div class="max-sm:hidden">
        <a class="hidden dark:block" href="/"><img class="h-8" src="/logos/ATX_NameWhite.svg" alt="The ATX logo." /></a>
        <a class="block dark:hidden" href="/"><img class="h-8" src="/logos/ATX_NameBlack.svg" alt="The ATX logo." /></a>
    </div>
    <a class="sm:hidden" href="/"><img class="h-8" src="/logos/ATX_Logo_Standalone.svg" alt="The ATX logo." /></a>
    <HeaderNavigationBar/>
    <HeaderUserView />
</div>