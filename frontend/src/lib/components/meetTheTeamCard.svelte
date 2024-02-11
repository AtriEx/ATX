<script lang="ts">
    import Fa from 'svelte-fa';
    import {faTwitter, faGithub, faDiscord} from '@fortawesome/free-brands-svg-icons'

    export let name: string;
    export let description: string;
    export let image: string;
    export let role: string;
    export let twitterUsername: string;
    export let discordUserID: string;
    export let githubUsername: string;
</script>

<div class="relative w-60 h-80 bg-light-accent/5 dark:bg-dark-accent/5 border-light-accent dark:border-dark-accent rounded-lg border-[1px]">
    <div class="flex flex-col items-center">
        <img class="w-20 h-20 rounded-3xl mt-5" src={image} alt="contributor profile"/>
        <p class="font-semibold text-2xl select-none text-light-text dark:text-dark-text">{name}</p>
        <p class="font-medium text-xl select-none text-light-primary dark:text-dark-primary">{role}</p>
        <p class="font-normal text-lg select-none px-3 text-light-text dark:text-dark-text">{description}</p>
    </div>
    <div class="mx-3 pt-1 absolute bottom-2 left-0 right-0 self-end border-t-[1px] flex flex-row justify-center border-light-accent dark:border-dark-accent {twitterUsername == null && githubUsername == null && discordUserID == null ? "mb-[21.333px]" : "block"}">
        <a class="{twitterUsername == null ? "hidden" : "block"}"  href="https://twitter.com/{twitterUsername}" target="_blank"><Fa class="text-light-accent dark:text-dark-accent mx-1" size="lg" icon={faTwitter} /></a>
        <a class="{githubUsername == null ? "hidden" : "block"}"  href="https://github.com/{githubUsername}" target="_blank"><Fa class="text-light-accent dark:text-dark-accent mx-1" size="lg" icon={faGithub} /></a>
        <a class="{discordUserID == null ? "hidden" : "block"}"  href="https://discordlookup.com/user/{discordUserID}" target="_blank"><Fa class="text-light-accent dark:text-dark-accent mx-1" size="lg" icon={faDiscord} /></a>
    </div>
</div>