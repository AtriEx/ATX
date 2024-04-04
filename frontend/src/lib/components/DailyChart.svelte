<script lang="ts">
	import { Chart, type ChartArea, type CoreScaleOptions } from 'chart.js/auto';
	import { onMount } from 'svelte';

	type Props = {
		changed_at: string;
		price: number;
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
					new Date(d.changed_at).toLocaleDateString(undefined, {
						month: 'short',
						day: 'numeric',
						hour: 'numeric',
						minute: 'numeric'
					})
				),
				datasets: [
					{
						label: 'Price',
						data: data.map((d) => d.price),
						backgroundColor: 'rgba(75, 192, 192, 0.2)',
						borderColor:
							first.price < last.price ? 'green' : first.price > last.price ? 'red' : 'white',
						borderWidth: 2,
						tension: 0.1
					}
				]
			},
			options: {
				responsive: true,
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
									label += new Intl.NumberFormat().format(context.parsed.y);
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

<canvas bind:this={chart} width={400} height={200} class="bg-slate-900" />
