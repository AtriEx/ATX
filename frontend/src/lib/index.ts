// place files you want to import through the `$lib` alias in this folder.
export function transformAmount(amount: number) {
	const suffixes = ['', 'K', 'M', 'B', 'T'];
	let suffixNum = 0;
	while (amount >= 1000) {
		amount /= 1000;
		suffixNum++;
	}

	if (suffixNum === 0) return amount.toFixed(0);

	return `${amount.toFixed(2)}${suffixes[suffixNum]}`;
}
