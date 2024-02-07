<script lang="ts">
	import Fa from 'svelte-fa';
	import { faCoins } from '@fortawesome/free-solid-svg-icons';
	import { profile } from '$lib/stores/userData.js';
</script>

<div class="flex flex-row text-yellow-300 items-center">
	<span class="mr-2">{$profile?.balance}</span>
	<Fa icon={faCoins} />
</div>
