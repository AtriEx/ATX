<script lang="ts">
    import {faChartLine, faVault, faTrophy} from '@fortawesome/free-solid-svg-icons'
	import HeaderNavigationButton from "./HeaderNavigationButton.svelte";
</script>

<div class="flex flex-auto space-x-20 mx-20 max-sm:hidden max-lg:space-x-10 max-lg:mx-10">
    <HeaderNavigationButton label="Portfolio" link="/" faIcon={faVault}/>
    <HeaderNavigationButton label="Stocks" link="/stocks" faIcon={faChartLine}/>
    <HeaderNavigationButton label="Leaderboard" link="/leaderboard" faIcon={faTrophy}/>
</div>