<script lang="ts">
    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    export let text : string;

    function timeScaleChanged() {
		dispatch('timeScaleChanged', {
			timeScale: text
		});
	}
</script>

<button on:click={timeScaleChanged}>
    {text}
</button>

<style>
    button {
        background-color: rgb(233, 247, 255);
        border-radius: 2px;
        border:none;
        margin:0px 10px;
        cursor: pointer;
    }

    button:hover {
        background-color: silver;
    }
</style>