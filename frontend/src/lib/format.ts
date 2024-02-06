export function formatDate(date: string | Date) {
	if (typeof date === 'string') date = new Date(date);
	return date.toLocaleDateString('en-US', {
		year: 'numeric',
		month: 'short',
		day: 'numeric'
	});
}

export function formatNumber(num: number) {
	return num.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
}
