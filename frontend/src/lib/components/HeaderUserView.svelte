<script lang="ts">
    import CurrencyView from "./CurrencyView.svelte";
	import NetworthView from "./NetworthView.svelte";

    import { isLoggedIn, username, userPfp} from '$lib/stores/userData.js';
</script>

<div class="text-zinc-300 flex flex-row">
    {#if $isLoggedIn}
    <div class="flex flex-col mr-5">
        <CurrencyView />
        <NetworthView />
    </div>
    <div class="flex flex-row items-center space-x-2">
        <span>{$username}</span>
        <img src={$userPfp} class="rounded-full border-solid border-2 border-white object-fill h-10" alt="The user's twitch profile."/>
    </div>
    <!-- This is where the dropdown goes, that has more settings. -->
    {:else}
    <button class="bg-violet-900 rounded p-2 border-violet-600 border-4">Login via Twitch</button>
    {/if}
</div>