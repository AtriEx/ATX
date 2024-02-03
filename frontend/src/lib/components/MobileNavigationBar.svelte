<script type="ts">
	import CurrencyView from "./CurrencyView.svelte";
	import NavigationBar from "./NavigationBar.svelte";
	import NetworthView from "./NetworthView.svelte";


</script>

<div class="max-width" id="container">
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
    }
</style>