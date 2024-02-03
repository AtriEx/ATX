<script lang="ts">
    import Fa from 'svelte-fa'
    
    export let faIcon : any;
    export let label : String;
</script>
  
<a href="/">
    <div class="flex flex-col text-zinc-300 bg-blue-900 hover:bg-blue-600 rounded p-1 pt-2 text-sm">
        <Fa icon={faIcon} />
        {label}
    </div>
</a>