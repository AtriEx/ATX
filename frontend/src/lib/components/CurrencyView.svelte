<script lang="ts">
	import Fa from "svelte-fa";
    import { faCoins} from '@fortawesome/free-solid-svg-icons'

    let currency = 1000;
</script>

<div class="flex flex-row text-zinc-300 mx-5 items-center">
    <span class="mx-2">{currency}</span>
    <Fa icon={faCoins}/>
</div>