<script lang="ts">
    import Fa from 'svelte-fa'
    
    export let faIcon : any;
    export let label : string;
    export let link : string;
</script>
  
<a href={link}>
    <div class="flex flex-col items-center text-zinc-300 bg-blue-900 hover:bg-blue-600 rounded p-1 pt-2 text-xl w-20">
        <Fa icon={faIcon} />
        <span class="text-xs">{label}</span>
    </div>
</a>