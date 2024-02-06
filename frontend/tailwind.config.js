/** @type {import('tailwindcss').Config} */

export default {
	content: ['./index.html', './src/**/*.{svelte,js,ts,html}'],
	theme: {
		extend: {
			colors: {
				/* Light Mode */
				'light-text': '#031516',
				'light-background': '#fbfbfe',
				'light-primary': '#27bace',
				'light-secondary': '#abcace',
				'light-accent': '#3de8ff',

				/* Dark Mode */
				'dark-text': '#e9fbfc',
				'dark-background': '#010104',
				'dark-primary': '#31c4d8',
				'dark-secondary': '#315054',
				'dark-accent': '#00abc2',
			}
		}
	},
	variants: {
		backgroundColor: ['responsive', 'hover', 'focus', 'active']
	},
	plugins: []
};
