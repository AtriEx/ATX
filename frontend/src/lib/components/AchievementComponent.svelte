<script lang="ts">
	import type { Database } from '$lib/supabase.types';
	export let achievement: Database['public']['Tables']['flags']['Row'];
</script>

<div class="flex items-center space-x-5 w-full">
	<img
		src={achievement.image}
		alt="{achievement.name} Image"
		class="w-10 h-10 md:w-16 md:h-16 rounded-xl bg-gray-200 dark:bg-gray-700 border-light-accent dark:border-dark-accent border-2 shadow-sm"
	/>
	<div class="flex-grow">
		<h1 class="text-2xl md:text-3xl font-bold text-light-primary dark:text-dark-primary">
			{achievement.name}
		</h1>
		<p class="text-sm md:text-lg text-light-text dark:text-dark-text mt-1">
			{achievement.description}
		</p>
	</div>
</div>
