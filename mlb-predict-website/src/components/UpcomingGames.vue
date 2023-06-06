<template>
	<div class="mlb-box">
		<h2 class="mlb-heading">Upcoming MLB Games</h2>
		<ul>
			<li v-for="game in upcomingGames" :key="game.id">
				<span class="mlb-team" :style="{ backgroundColor: game.homeTeamColor }">{{ game.homeTeam }}</span>
				vs
				<span class="mlb-team" :style="{ backgroundColor: game.awayTeamColor }">{{ game.awayTeam }}</span>
				- {{ game.date }}
			</li>
		</ul>
	</div>
</template>

<script>
export default {
	data() {
		return {
			upcomingGames: [],
		};
	},
	mounted() {
		// Fetch MLB game data from an API
		this.fetchUpcomingGames();
	},
	methods: {
		fetchUpcomingGames() {
			// Make an API call to retrieve the upcoming MLB games
			// Replace this with your actual API call implementation
			// For simplicity, let's assume the API returns an array of game objects
			const apiResponse = [
				{
					id: 1,
					homeTeam: 'New York Yankees',
					homeTeamColor: '#003087', // Yankees' color
					awayTeam: 'Boston Red Sox',
					awayTeamColor: '#BD3039', // Red Sox's color
					date: '2023-06-07',
				},
				{
					id: 2,
					homeTeam: 'Los Angeles Dodgers',
					homeTeamColor: '#005A9C', // Dodgers' color
					awayTeam: 'San Francisco Giants',
					awayTeamColor: '#FD5A1E', // Giants' color
					date: '2023-06-08',
				},
				{
					id: 3,
					homeTeam: 'Chicago Cubs',
					homeTeamColor: '#0E3386', // Cubs' color
					awayTeam: 'St. Louis Cardinals',
					awayTeamColor: '#C41E3A', // Cardinals' color
					date: '2023-06-09',
				},
				// Add more game objects as needed
			];

			// Update the upcomingGames array with the API response data
			this.upcomingGames = apiResponse;
		},
	},
};
</script>

<style scoped>
.mlb-box {
	border: 2px solid #000000;
	padding: 10px;
	border-radius: 5px;
	background-color: #EEEEEE;
}

.mlb-heading {
	font-size: 20px;
	margin-bottom: 10px;
}

ul {
	list-style-type: none;
	padding: 0;
}

li {
	margin-bottom: 5px;
}

.mlb-team {
	display: inline-block;
	padding: 2px 5px;
	color: #FFFFFF;
	font-weight: bold;
	border-radius: 3px;
	margin-right: 5px;
}
</style>
