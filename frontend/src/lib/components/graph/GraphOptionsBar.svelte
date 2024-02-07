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
    <span>Last Updated: X seconds ago</span>
</div>


<style>
    div {
        margin-top: 10px;
        display: flex;
        flex-direction: row;
        width: 100%;
        background-color: rgb(200,200,200,0.5);
        border:solid 1px black;
        padding: 10px 0px 10px 0px;
        border-radius: 0px 0px 10px 10px;
    }
    span {
        width:100%;
        text-align: right;
        margin-right:5px;
        font-style: italic;
    }
</style>