<script lang="ts">
    import MeetTheTeamCard from '$lib/components/meetTheTeamCard.svelte';
    import type { PageData } from './$types';
    
    export let data: PageData;

    
</script>

<main class="mt-2 mb-6 max-sm:mb-24 flex flex-col items-center text-center">
    <p class="text-6xl max-sm:text-[42px] font-semibold text-light-text dark:text-dark-text">Meet the <span class="font-bold text-light-accent dark:text-dark-accent">team.</span></p>
    <div class="mt-8 mx-5 grid grid-cols-4 max-lg:grid-cols-3 max-md:grid-cols-2 max-sm:grid-cols-1 grid-flow-row gap-8">
        {#each data.data as contributor}
            <MeetTheTeamCard name={contributor.name} description={contributor.description} image={contributor.image} role={contributor.role} twitterUsername={contributor.twitterUsername} discordUserID={contributor.discordUserID} githubUsername={contributor.githubUsername} />
        {/each}
    </div>
</main>