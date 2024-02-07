<script lang="ts">
	import Fa from 'svelte-fa';
	import { faSackDollar } from '@fortawesome/free-solid-svg-icons';

	import { profile } from '$lib/stores/userData.js';
</script>

<div class="flex flex-row text-green-500 items-center">
	<span class="mr-2">{$profile?.networth}</span>
	<Fa icon={faSackDollar} />
</div>
