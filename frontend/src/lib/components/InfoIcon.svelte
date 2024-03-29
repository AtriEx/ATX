<script>
	export let primary = '#348fff';
	export let secondary = '#fff';
</script>

<div style:--primary={primary} style:--secondary={secondary} />

<style>
	div {
		width: 20px;
		opacity: 0;
		height: 20px;
		border-radius: 10px;
		background: var(--primary, #348fff);
		position: relative;
		animation: circleAnimation 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
		animation-delay: 100ms;
	}

	div::before {
		content: '';
		animation: DotAnimation 0.2s ease-out forwards;
		animation-delay: 150ms;
		position: absolute;
		opacity: 0;
		background: var(--secondary, #fff);
        border-radius: 4px;
		top: 4px;
		left: 8px;
		height: 4px;
		width: 4px;
	}

    div::after {
      content: '';
  		animation: firstLineAnimation 0.2s ease-out forwards;
  		animation-delay: 150ms;
  		position: absolute;
  		border-radius: 4px;
  		opacity: 0;
  		background: var(--secondary, #fff);
  		bottom: 4px;
  		left: 8px;
  		height: 7px;
  		width: 4px;
    }

	@keyframes circleAnimation {
		from {
			transform: scale(0);
			opacity: 0;
		}
		to {
			transform: scale(1);
			opacity: 1;
		}
	}

	@keyframes firstLineAnimation {
		from {
			transform: scale(0);
      height: 0px;
			opacity: 0;
		}
		to {
			transform: scale(1);
			opacity: 1;
		}
	}

	@keyframes DotAnimation {
		from {
			transform: scale(0);
			opacity: 0;
		}
		to {
			transform: scale(1);
			opacity: 1;
		}
	}
</style>
