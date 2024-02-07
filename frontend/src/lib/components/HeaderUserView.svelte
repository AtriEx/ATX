<script lang="ts">
    import { slide } from 'svelte/transition';

    import CurrencyView from "./CurrencyView.svelte";
	import NetworthView from "./NetworthView.svelte";

    import { isLoggedIn, username, userPfp} from '$lib/stores/userData';

    let isDropdownVisible : boolean = false;

    function toggleDropdown(e: Event) {
        isDropdownVisible = !isDropdownVisible;
    }
</script>

{#if $isLoggedIn}
<div class="sm:hidden {isDropdownVisible == true ? "hidden" : "block"}">
    <NetworthView />
</div>
{/if}

<div class="flex flex-row justify-between items-center">
    {#if $isLoggedIn}
    <div class="flex flex-row items-center mr-5 max-sm:hidden">
        <CurrencyView />
        <NetworthView />
    </div>
    <button class="max-sm:hidden flex flex-row items-center" on:click={toggleDropdown}> <!-- This is the anchor that can open the dropdown.-->
        <div class="flex flex-row items-center space-x-2">
            <span class="text-light-text dark:text-dark-text" >{$username}</span>
            <img src={$userPfp} class="rounded-full border-solid border-2 border-light-secondary dark:border-dark-secondary object-fill h-10" alt="The user's twitch profile."/>
        </div>
    </button>
    <button on:click={toggleDropdown} type="button" class="sm:hidden text-light-text focus:text-light-secondary dark:text-dark-text dark:focus:text-dark-secondary focus:outline-none">
        <svg class="h-8 w-8 fill-current" viewBox="0 0 24 24">
            <path class="{isDropdownVisible == true ? "block" : "hidden"}" fill-rule="evenodd" d="M18.278 16.864a1 1 0 0 1-1.414 1.414l-4.829-4.828-4.828 4.828a1 1 0 0 1-1.414-1.414l4.828-4.829-4.828-4.828a1 1 0 0 1 1.414-1.414l4.829 4.828 4.828-4.828a1 1 0 1 1 1.414 1.414l-4.828 4.829 4.828 4.828z"/>
            <path class="{isDropdownVisible == false ? "block" : "hidden"}" fill-rule="evenodd" d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z"/>
        </svg>
    </button>
    {#if isDropdownVisible}
    <div class="max-sm:hidden absolute top-[68px] right-0 bg-light-background dark:bg-dark-background dark:border-dark-secondary rounded-bl-lg drop-shadow-lg border-0 dark:border-l-[1px] dark:border-b-[1px]" transition:slide={{ delay: 0, duration: 300}}>
        <div class="flex flex-col items-start">
            <a class="text-light-text hover:text-light-primary hover:bg-light-background dark:text-dark-text dark:hover:text-dark-primary dark:hover:bg-dark-background cursor-pointer w-full" href="/profile/{$username}"><div class="m-2">Profile</div></a>
            <a class="text-light-text hover:text-light-primary hover:bg-light-background dark:text-dark-text dark:hover:text-dark-primary dark:hover:bg-dark-background cursor-pointer w-full" href="/settings"><div class="m-2">Account Settings</div></a>
            <div class="text-light-text hover:text-light-primary hover:bg-light-background dark:text-dark-text dark:hover:text-dark-primary dark:hover:bg-dark-background w-full p-2 rounded-b-lg cursor-pointer"><a  href="">Sign Out</a></div>
        </div>
    </div>
    <div class="sm:hidden absolute top-12 right-0 px-4 pb-4 bg-light-background dark:bg-dark-background dark:border-dark-secondary rounded-bl-lg border-0 dark:border-l-[1px] dark:border-b-[1px]" transition:slide={{ delay: 0, duration: 300}}>
        <div class="flex items-center pt-2">
            <img class="h-8 w-8 rounded-full border-2 border-light-secondary dark:border-dark-secondary object-cover" src={$userPfp} alt="The user's twitch profile.">
            <span class="ml-3 font-semibold text-light-text dark:text-dark-text">{$username}</span>
        </div>
        <div class="flex flex-col mt-3 py-2 border-t border-light-secondary dark:border-dark-secondary">
            <CurrencyView />
            <NetworthView />
        </div>
        <div class="pt-2 border-t border-light-secondary dark:border-dark-secondary">
            <a href="/profile/{$username}" class="block text-light-text hover:text-light-primary dark:text-dark-text dark:hover:text-dark-primary">Profile</a>
            <a href="/settings" class="mt-2 block text-light-text hover:text-light-primary dark:text-dark-text dark:hover:text-dark-primary">Account settings</a>
            <a href="#" class="mt-2 block text-light-text hover:text-light-primary dark:text-dark-text dark:hover:text-dark-primary">Sign out</a>
        </div>
    </div>
    {/if}
    <!-- This is where the dropdown goes, that has more settings. -->
    {:else}
    <button class="bg-violet-900 rounded p-2 border-violet-600 border-4">Login via Twitch</button>
    {/if}
</div>