<script lang="ts">
    import { faHouse, faChartLine, faVault} from '@fortawesome/free-solid-svg-icons'
	import NavigationButton from "./NavigationButton.svelte";
</script>

<div class="flex flex-auto space-x-10 mx-10">
    <NavigationButton label="Home" faIcon={faHouse}/>
    <NavigationButton label="Stocks" faIcon={faChartLine}/>
    <NavigationButton label="Portfolio" faIcon={faVault}/>
</div>