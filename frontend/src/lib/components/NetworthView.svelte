<script lang="ts">
	import { profile } from '$lib/stores/userData';
</script>

<p class="block sm:px-2 text-light-text dark:text-dark-text font-medium select-none max-lg:text-sm">
	Net-Worth:
	<span class="font-normal text-light-accent dark:text-dark-accent"> {$profile?.networth} </span>
</p>
