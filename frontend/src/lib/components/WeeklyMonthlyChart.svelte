<script lang="ts">
	import { Chart } from 'chart.js/auto';
	import { onMount } from 'svelte';

	type Props = {
		starting_hour: string;
		average_price: number;
		id: number;
	};

	export let data: Props[];

	$: first = data[0];
	$: last = data[data.length - 1];

	let chart: any = null;

	onMount(() => {
		const ctx = chart?.getContext('2d');
		if (!ctx) return;

		new Chart(ctx, {
			type: 'line',
			data: {
				labels: data.map((d) =>
					new Date(d.starting_hour).toLocaleDateString(undefined, {
						month: 'short',
						day: 'numeric',
						hour: 'numeric',
						minute: 'numeric'
					})
				),
				datasets: [
					{
						label: 'Price',
						data: data.map((d) => d.average_price.toFixed(2)),
						backgroundColor: 'rgba(75, 192, 192, 0.2)',
						borderColor:
							first.average_price < last.average_price
								? 'rgba(34, 197, 94, 1)'
								: first.average_price > last.average_price
									? 'rgba(239, 68, 68, 1)'
									: 'rgba(255, 255, 255, 1)',
						borderWidth: 2,
						tension: 0.1
					}
				]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				scales: {
					y: {
						beginAtZero: false,
						grid: {
							color: 'rgba(255,255,255,0.1)'
						},
						ticks: {
							color: '#fff'
						}
					},
					x: {
						ticks: {
							color: '#fff'
						}
					}
				},
				plugins: {
					legend: {
						display: false,
						labels: {
							color: '#fff'
						}
					},
					tooltip: {
						mode: 'index',
						intersect: false,
						callbacks: {
							label: function (context) {
								let label = context.dataset.label || '';
								if (label) {
									label += ': ';
								}
								if (context.parsed.y !== null) {
									label += context.parsed.y.toFixed(2);
								}
								return label + ' coins';
							}
						}
					}
				},
				interaction: {
					mode: 'nearest',
					axis: 'x',
					intersect: false
				}
			}
		});
	});
</script>

<div class="flex justify-center items-center p-4">
	<div class="relative w-full max-w-4xl">
		<canvas bind:this={chart} class="bg-slate-900 p-2 rounded-lg shadow-lg w-full h-96" />
	</div>
</div>
