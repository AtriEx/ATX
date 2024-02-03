<script lang="ts">
	import CurrencyView from "./CurrencyView.svelte";
	import HeaderUserView from "./HeaderUserView.svelte";
	import NavigationBar from "./NavigationBar.svelte";
	import NetworthView from "./NetworthView.svelte";

    /*//If desktop, this will have navigation, currency, and profile status.
    //Mobile Header will NOT have navigation or currency.*/
    let isMobile : Boolean = false;
</script>

<div>
    <span>ATX</span>
    {#if !isMobile}
    <NavigationBar />
    <CurrencyView />
    <NetworthView />
    {/if}
    <HeaderUserView />
</div>

<style>
    div{
        position: relative;
        width:100%;
        left: 0px;
        top:0px;
        background-color: silver;
    }
</style>