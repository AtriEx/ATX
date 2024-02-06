<!--
    Usage notes:
        - Graph component will fill the container that it's put in, and update reactively if the size changes.
-->
<script lang="ts">
    import { Line } from 'svelte-chartjs'
    import GraphOptionsBar from './GraphOptionsBar.svelte';

    export let stockTicker : string;

    import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale,
  } from 'chart.js';

  ChartJS.register(
    Title,
    Tooltip,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale
  );

    let data = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        datasets: [
        {
            data: [65.52, 59.51, 80.80, 51.91, 56.1, 55, 31.99, 55.52, 72],
            //GENERAL
            label: stockTicker,
            clip: {left: 5, top: false, right: false, bottom: false}, //Sets where the visuals get clipped. False means it doesn't get clipped at all.  
            
            //POINT STYLING. These represent each data point on the graph.
            pointBackgroundColor: 'rgba(255, 255, 255, 1)',
            pointBorderColor: 'rgba(255, 255, 255, 1)',
            pointBorderWidth: 1,
            pointHitRadius: 10, //Mouse detection radius for each point.
            pointRadius: 0,
            pointStyle: true, //Controls if the points are shown at all. (Note: hover tooltip still appears if set to false, but point itself wont be visible when hovered)

            //LINE STYLING.
            borderCapStyle: 'round', //Line ends style. Either 'butt', 'round', or 'square'.
            borderColor: 'rgb(0, 0, 0)', //The main chart line color.
            borderDash: [0], //Sets the pattern, if we want to make a dotted line.
            borderJoinStyle: "round", //Sets how the chart line 'joins' at each point. Either 'miter', 'round', or 'bevel'.
            borderWidth: 1,
            tension:0, //If we want the line to be loosey-goosey (Note: We probably do not want this.)

            //INTERACTIONS. These represent the points on the graph, while they are being hovered.
            pointHoverBackgroundColor: 'rgb(0, 0, 0)',
            pointHoverBorderColor: 'rgb(255, 255, 255)',
            pointHoverBorderWidth: 0,
            pointHoverRadius: 5,
        }]
    };

    function timeScaleChanged(e: any) {
        let timeScale : string = e.detail.timeScale;
        if(timeScale == '5y') {
            //TODO: Update graph based on this scale.
        }
        else if(timeScale == '1y') {
            //TODO: Update graph based on this scale.
        }
        else if(timeScale == '3m') {
            //TODO: Update graph based on this scale.
        }
        else if(timeScale == '1m') {
            //TODO: Update graph based on this scale.
        }
        else if(timeScale == '5d') {
            //TODO: Update graph based on this scale.
        }
        else if(timeScale == '1d') {
            //TODO: Update graph based on this scale.
        }
    }
</script>
  
<div class="w-full">
    <Line {data} options={{ responsive: true, maintainAspectRatio: false, 
        scales:{
            x:{
                border:{
                    color: 'grey'
                },
                grid: {
                    color: 'silver',
                    tickColor: 'silver'
                },
                min: 2,
                max:11
            },
            y:{
                border:{
                    color: 'grey'
                },
                grid: {
                    color: 'silver',
                    tickColor: 'silver'
                },
                min: 0,
                max: 100,
            }
        }}} />
    
    <GraphOptionsBar on:timeScaleChanged={timeScaleChanged}></GraphOptionsBar>
</div>

<style>
    div {
        height:100%;
        background-color: white;
        padding:10px;
        border-radius: 10px;
    }
</style>