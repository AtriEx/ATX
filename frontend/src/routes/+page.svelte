<script>
    import Graph from "$lib/components/graph/Graph.svelte";
</script>

<main>
    <h1>Welcome to SvelteKit</h1>
    <p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

    <div><Graph stockTicker = "ATL"/></div>
</main>

<style>
    div {
        width:600px;
        height:400px;
    }
    :global(body) {
        background-color: rgba(100,100,100,1);
    }
</style>

