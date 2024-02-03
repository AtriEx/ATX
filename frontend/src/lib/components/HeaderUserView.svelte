<script lang="ts">
    import { slide } from 'svelte/transition';

    import CurrencyView from "./CurrencyView.svelte";
	import NetworthView from "./NetworthView.svelte";

    import { isLoggedIn, username, userPfp} from '$lib/stores/userData.js';

    let isDropdownVisible : boolean = false;

    function toggleDropdown(e: Event) {
        console.log(e);
        isDropdownVisible = !isDropdownVisible;
    }
</script>

<div class="text-zinc-300 flex flex-row">
    {#if $isLoggedIn}
    <div class="flex flex-col mr-5">
        <CurrencyView />
        <NetworthView />
    </div>
    <button class="flex flex-row items-center" on:click={toggleDropdown}> <!-- This is the anchor that can open the dropdown.-->
        <div class="flex flex-row items-center space-x-2">
            <span>{$username}</span>
            <img src={$userPfp} class="rounded-full border-solid border-2 border-white object-fill h-10" alt="The user's twitch profile."/>
        </div>
    </button>
    {#if isDropdownVisible}
    <div class="absolute top-16 right-0 bg-blue-950 rounded-b-lg drop-shadow-lg" transition:slide={{ delay: 0, duration: 300}}>
        <div class="flex flex-col p-3 items-start space-y-5">
            <a class="hover:text-white" href="/settings">Account Settings</a>
            <a class="text-red-300 hover:text-red-500" href="">Sign Out</a>
        </div>
    </div>
    {/if}
    <!-- This is where the dropdown goes, that has more settings. -->
    {:else}
    <button class="bg-violet-900 rounded p-2 border-violet-600 border-4">Login via Twitch</button>
    {/if}
</div>