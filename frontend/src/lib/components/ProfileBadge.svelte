<script lang="ts">
	export let name: string;
	export let dateObtained: Date;
	export let iconImage: string | undefined = undefined;

	$: formattedDate = dateObtained.toLocaleDateString('en-US', {
		year: 'numeric',
		month: 'long',
		day: 'numeric'
	});
</script>

<div
	class="bg-white rounded-lg shadow-md p-2 sm:p-4 my-3 mx-auto flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-6 max-w-lg"
>
	{#if iconImage}
		<img
			src={iconImage}
			alt="{name} Icon"
			class="w-8 h-8 rounded-full bg-gray-200 border-violet-500 border-2 p-2"
		/>
	{:else}
		<div class="w-12 h-12 rounded-full bg-gray-200 border-violet-500 border-2 p-2" />
	{/if}
	<div class="flex flex-col items-start space-y-1 w-full">
		<h1 class="text-xl font-semibold text-gray-800">{name}</h1>
		<p class="text-sm text-gray-600">
			Achieved on:
			<span class="text-violet-600 font-medium">{formattedDate}</span>
		</p>
	</div>
</div>
