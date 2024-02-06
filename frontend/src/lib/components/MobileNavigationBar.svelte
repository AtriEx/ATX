<script type="ts">
	import {faChartLine, faVault, faTrophy} from '@fortawesome/free-solid-svg-icons'
	import MobileNavigationButton from "./MobileNavigationButton.svelte";
</script>

<div class="w-full flex flex-row absolute bg-light-background dark:bg-dark-background bottom-0 left-0 sm:hidden place-content-evenly py-2 drop-shadow-lg border-t-[1px] dark:border-dark-secondary">
    <MobileNavigationButton label="Portfolio" link="/" faIcon={faVault}/>
    <MobileNavigationButton label="Stocks" link="/stocks" faIcon={faChartLine}/>
    <MobileNavigationButton label="Leaderboard" link="/leaderboard" faIcon={faTrophy}/>
</div>