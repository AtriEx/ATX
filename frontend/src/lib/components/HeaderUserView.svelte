<script lang="ts">
    let isLoggedIn : Boolean = false;
</script>

<div>
    {#if isLoggedIn}
    <span>CraaazySteeeve</span>
    <!-- This is where the dropdown goes, that has more settings. -->
    {:else}
    <button>Login via Twitch</button>
    {/if}
</div>

<style>

</style>