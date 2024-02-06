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
        background-color: white;
        border:none;
    }

    button:hover {
        background-color: silver;
    }
</style>