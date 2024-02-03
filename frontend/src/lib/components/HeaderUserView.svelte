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
    <button class="max-sm:hidden flex flex-row items-center" on:click={toggleDropdown}> <!-- This is the anchor that can open the dropdown.-->
        <div class="flex flex-row items-center space-x-2">
            <span>{$username}</span>
            <img src={$userPfp} class="rounded-full border-solid border-2 border-white object-fill h-10" alt="The user's twitch profile."/>
        </div>
    </button>
    <button on:click={toggleDropdown} type="button" class="sm:hidden text-gray-500 hover:text-white focus:text-white focus:outline-none">
        <svg class="h-8 w-8 fill-current" viewBox="0 0 24 24">
            <path class="{isDropdownVisible == true ? "block" : "hidden"}" fill-rule="evenodd" d="M18.278 16.864a1 1 0 0 1-1.414 1.414l-4.829-4.828-4.828 4.828a1 1 0 0 1-1.414-1.414l4.828-4.829-4.828-4.828a1 1 0 0 1 1.414-1.414l4.829 4.828 4.828-4.828a1 1 0 1 1 1.414 1.414l-4.828 4.829 4.828 4.828z"/>
            <path class="{isDropdownVisible == true ? "hidden" : "block"}" fill-rule="evenodd" d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z"/>
        </svg>
    </button>
    {#if isDropdownVisible}
    <div class="max-sm:hidden absolute top-16 right-0 bg-blue-950 rounded-b-lg drop-shadow-lg" transition:slide={{ delay: 0, duration: 300}}>
        <div class="flex flex-col items-start">
            <a class="hover:text-white hover:bg-slate-800 cursor-pointer w-full" href="/profile/{$username}"><div class="m-2">Profile</div></a>
            <a class="hover:text-white hover:bg-slate-800 cursor-pointer w-full" href="/settings"><div class="m-2">Account Settings</div></a>
            <div class="hover:text-white bg-slate-900 hover:bg-slate-950 w-full p-2 rounded-b-lg cursor-pointer"><a  href="">Sign Out</a></div>
        </div>
    </div>
    <div class="sm:hidden absolute top-16 right-0 px-4 py-5 border-t bg-blue-950 border-gray-800" transition:slide={{ delay: 0, duration: 300}}>
        <div class="flex items-center">
            <img class="h-8 w-8 rounded-full border-2 border-gray-600 object-cover" src="https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=256&q=80" alt="Your avatar">
            <span class="ml-3 font-semibold text-white">Jane Doe</span>
        </div>
        <div class="mt-4">
            <a href="/profile/{$username}" class="block text-gray-400 hover:text-white">Profile</a>
            <a href="/settings" class="block text-gray-400 hover:text-white">Account settings</a>
            <a href="#" class="mt-2 block text-gray-400 hover:text-white">Sign out</a>
        </div>
    </div>
    {/if}
    <!-- This is where the dropdown goes, that has more settings. -->
    {:else}
    <button class="bg-violet-900 rounded p-2 border-violet-600 border-4">Login via Twitch</button>
    {/if}
</div>