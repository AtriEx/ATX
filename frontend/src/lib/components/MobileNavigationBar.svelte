<script type="ts">
	import {faChartLine, faVault, faTrophy} from '@fortawesome/free-solid-svg-icons'
	import MobileNavigationButton from "./MobileNavigationButton.svelte";
</script>

<div class="w-full flex flex-row absolute bg-blue-950 bottom-0 left-0 sm:hidden place-content-evenly py-2">
    <MobileNavigationButton label="Portfolio" link="/" faIcon={faVault}/>
    <MobileNavigationButton label="Stocks" link="/stocks" faIcon={faChartLine}/>
    <MobileNavigationButton label="Leaderboard" link="/leaderboard" faIcon={faTrophy}/>
</div>