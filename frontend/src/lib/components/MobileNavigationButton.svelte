<script lang="ts">
    import Fa from 'svelte-fa'
    
    export let faIcon : any;
    export let label : string;
    export let link : string;
</script>

<a href={link}>
    <div class="flex flex-col items-center justify-center text-light-text dark:bg-dark-accent dark:hover:bg-dark-primary rounded p-1 pt-2 text-xl w-20 h-14">
        <Fa size="lg" icon={faIcon} />
    </div>
</a>