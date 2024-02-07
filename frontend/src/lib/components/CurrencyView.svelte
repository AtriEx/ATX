<script lang="ts">
	import { profile } from '$lib/stores/userData';
</script>

<p
	class="block sm:px-2 mr-3 text-light-text dark:text-dark-text font-medium select-none max-lg:text-sm"
>
	AtriCoins:
	<span class="font-normal text-light-accent dark:text-dark-accent"> {$profile?.balance} </span>
</p>
