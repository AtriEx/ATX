<script lang="ts">
    import Fa from 'svelte-fa';
    import {faTwitter, faGithub, faDiscord} from '@fortawesome/free-brands-svg-icons'

    export let name: string | null;
    export let description: string | null;
    export let image: string | null;
    export let role: string | null;
    export let twitterUsername: string | null;
    export let discordUserID: string | null;
    export let githubUsername: string | null;
</script>

<div class="relative w-60 h-80 bg-light-accent/5 dark:bg-dark-accent/5 border-light-accent dark:border-dark-accent rounded-lg border-[1px]">
    <div class="flex flex-col items-center">
        <img class="w-20 h-20 rounded-3xl mt-5" src={image} alt="contributor profile"/>
        <p class="font-semibold text-2xl select-none text-light-text dark:text-dark-text truncate w-52">{name}</p>
        <p class="font-medium text-xl select-none text-light-primary dark:text-dark-primary">{role}</p>
        <p class="font-normal text-lg select-none px-3 h-28 text-light-text dark:text-dark-text text-pretty text-ellipsis overflow-hidden">{description}</p>
    </div>
    <div class="mx-3 pt-1 absolute bottom-2 left-0 right-0 self-end border-t-[1px] flex flex-row justify-center border-light-accent dark:border-dark-accent {twitterUsername == null && githubUsername == null && discordUserID == null ? "mb-[21.333px]" : ""}">
        {#if (twitterUsername != null)}
            <a href="https://twitter.com/{twitterUsername}" target="_blank"><Fa class="text-light-accent dark:text-dark-accent mx-1" size="lg" icon={faTwitter} /></a>
        {/if}
        {#if (githubUsername != null)}
            <a href="https://github.com/{githubUsername}" target="_blank"><Fa class="text-light-accent dark:text-dark-accent mx-1" size="lg" icon={faGithub} /></a>
        {/if}
        {#if (discordUserID != null)}
            <a href="https://discordlookup.com/user/{discordUserID}" target="_blank"><Fa class="text-light-accent dark:text-dark-accent mx-1" size="lg" icon={faDiscord} /></a>
        {/if}
    </div>
</div>