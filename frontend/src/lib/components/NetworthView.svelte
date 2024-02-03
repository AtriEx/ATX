<script lang="ts">
	import Fa from "svelte-fa";
    import {faSackDollar} from '@fortawesome/free-solid-svg-icons'

    let currency = 2000;
</script>

<div class="flex flex-row text-green-500 items-center">
    <span class="mr-2">{currency}</span>
    <Fa icon={faSackDollar}/>
</div>