<script lang="ts">
	import CurrencyView from "./CurrencyView.svelte";
	import HeaderUserView from "./HeaderUserView.svelte";
	import NavigationBar from "./NavigationBar.svelte";
	import NetworthView from "./NetworthView.svelte";

    /*//If desktop, this will have navigation, currency, and profile status.
    //Mobile Header will NOT have navigation or currency.*/
    let isMobile : Boolean = false;
</script>

<div class="py-2 px-3 max-width bg-blue-950 flex flex-row flex-nowrap items-center">
    <img class="h-8" src="/logos/ATX_NameWhite.svg" alt="The ATX logo." />
    {#if !isMobile}
    <NavigationBar/>
    <div class="flex flex-row">
        <CurrencyView />
        <NetworthView />
    </div>
    {/if}
    <HeaderUserView />
</div>

<style>

</style>