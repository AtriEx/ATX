<script lang="ts">
	import { page } from '$app/stores';

	export let userName: string;

	let buttonText = 'Share';

	async function copyToClipboard() {
		const shareLink = `${$page.url.origin}/profile/${userName}`;
		if ('canShare' in navigator && navigator.canShare()) {
			await navigator.share({
				title: 'Check out this profile!',
				text: `Check out ${userName}'s profile on our site!`,
				url: shareLink
			});
			return;
		}

		try {
			await navigator.clipboard.writeText(shareLink);
		} catch (err) {
			console.error('Failed to copy: ', err);
		}

		buttonText = 'Copied!';
		setTimeout(() => {
			buttonText = 'Share';
		}, 2000);
	}
</script>

<button
	class="bg-light-secondary dark:bg-dark-secondary text-light-text dark:text-dark-text px-3 py-1 rounded transition ease-in-out active:scale-95 active:shadow-inner"
	on:click={copyToClipboard}>{buttonText}</button
>
