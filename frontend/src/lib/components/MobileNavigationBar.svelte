<script type="ts">
	import {faChartLine, faVault, faTrophy} from '@fortawesome/free-solid-svg-icons'
	import MobileNavigationButton from "./MobileNavigationButton.svelte";
</script>

<div class="w-full flex flex-row fixed bg-light-background dark:bg-dark-background bottom-0 left-0 sm:hidden place-content-evenly py-2 drop-shadow-lg border-t-[1px] dark:border-dark-secondary">
    <MobileNavigationButton link="/" faIcon={faVault}/>
    <MobileNavigationButton link="/stocks" faIcon={faChartLine}/>
    <MobileNavigationButton link="/leaderboard" faIcon={faTrophy}/>
</div>