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
			buttonText = 'Shared!';
			setTimeout(() => {
				buttonText = 'Share';
			}, 2000);
			return;
		}

		try {
			await navigator.clipboard.writeText(shareLink);
			buttonText = 'Copied!';
		} catch (err) {
			console.error('Failed to copy: ', err);
			buttonText = 'Failed!';
		}

		setTimeout(() => {
			buttonText = 'Share';
		}, 2000);
	}
</script>

<button
	class="bg-light-secondary dark:bg-dark-secondary text-light-text dark:text-dark-text px-4 py-2 rounded-full transition ease-in-out duration-300 hover:bg-light-primary dark:hover:bg-dark-primary hover:text-white active:scale-95 active:shadow-inner font-bold"
	on:click={copyToClipboard}>{buttonText}</button
>
