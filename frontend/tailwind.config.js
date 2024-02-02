/** @type {import('tailwindcss').Config} */

export default {
	content: ['./index.html', './src/**/*.{svelte,js,ts,html}'],
	theme: {
		extend: {}
	},
	variants: {
		backgroundColor: ['responsive', 'hover', 'focus', 'active']
	},
	plugins: []
};
