<script type="ts">
	import CurrencyView from "./CurrencyView.svelte";
	import NavigationBar from "./NavigationBar.svelte";
	import NetworthView from "./NetworthView.svelte";


</script>

<div id="container">
    <div>
        <CurrencyView />
        <NetworthView />
    </div>
    <div>
        <NavigationBar />
    </div>
</div>

<style>
    #container {
        position:absolute;
        bottom: 0px;
        left: 0px;
        width: 100%;
    }
</style>