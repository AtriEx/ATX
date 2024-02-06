<script>
    import GraphTimeScaleButton from "./GraphTimeScaleButton.svelte";
</script>

<div>
    <GraphTimeScaleButton text={'5y'} on:timeScaleChanged></GraphTimeScaleButton>
    <GraphTimeScaleButton text={'1y'} on:timeScaleChanged></GraphTimeScaleButton>
    <GraphTimeScaleButton text={'3m'} on:timeScaleChanged></GraphTimeScaleButton>
    <GraphTimeScaleButton text={'1m'} on:timeScaleChanged></GraphTimeScaleButton>
    <GraphTimeScaleButton text={'5d'} on:timeScaleChanged></GraphTimeScaleButton>
    <GraphTimeScaleButton text={'1d'} on:timeScaleChanged></GraphTimeScaleButton>
</div>