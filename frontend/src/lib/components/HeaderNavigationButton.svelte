<script lang="ts">
    import Fa from 'svelte-fa'
    
    export let faIcon : any;
    export let label : String;
    export let link : string;
</script>

<a href={link}>
    <div class="flex flex-col items-center text-light-text hover:text-light-primary dark:text-dark-text dark:hover:text-dark-primary p-1 pt-2 text-xl">
        <Fa icon={faIcon} />
        <span class="text-sm">{label}</span>
    </div>
</a>