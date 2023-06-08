<template>
	<div class="mlb-box">
		<h2 class="mlb-heading">Today's MLB Games</h2>
		<ul class="mlb-games-list">
			<li v-for="game in upcomingGames" :key="game.gamePk" class="mlb-game">
				<router-link :to="'/predict-game/' + game.gamePk" class="mlb-game-link">
					<div class="mlb-game-row">
						<div class="mlb-team-container">
							<span class="mlb-team mlb-home-team" :style="{ backgroundColor: getTeamColor(game.homeTeam) }">
								{{ game.homeTeam }}
							</span>
							<span class="mlb-vs">vs</span>
							<span class="mlb-team mlb-away-team" :style="{ backgroundColor: getTeamColor(game.awayTeam) }">
								{{ game.awayTeam }}
							</span>
						</div>
						<div class="mlb-game-details">
							<span class="mlb-game-time">{{ formatTime(game.gameDate) }}</span>
							<font-awesome-icon icon="chevron-right" />
						</div>
					</div>
				</router-link>
			</li>
		</ul>
		<div class="loading-icon" v-if="isLoading">
			<div class="spinner"></div>
		</div>
	</div>
</template>

<script>
import { db, functions } from '@/firebase';

export default {
	data() {
		return {
			upcomingGames: [],
			teamColors: {
				'Arizona Diamondbacks': '#A71930',
				'Atlanta Braves': '#CE1141',
				'Baltimore Orioles': '#DF4601',
				'Boston Red Sox': '#BD3039',
				'Chicago White Sox': '#27251F',
				'Chicago Cubs': '#0E3386',
				'Cincinnati Reds': '#C6011F',
				'Cleveland Guardians': '#0C2340',
				'Colorado Rockies': '#33006F',
				'Detroit Tigers': '#0C2340',
				'Houston Astros': '#002D62',
				'Kansas City Royals': '#004687',
				'Los Angeles Angels': '#BA0021',
				'Los Angeles Dodgers': '#005A9C',
				'Miami Marlins': '#00A3E0',
				'Milwaukee Brewers': '#12284B',
				'Minnesota Twins': '#002B5C',
				'New York Yankees': '#003087',
				'New York Mets': '#FF5910',
				'Oakland Athletics': '#003831',
				'Philadelphia Phillies': '#E81828',
				'Pittsburgh Pirates': '#FDB827',
				'San Diego Padres': '#002D62',
				'San Francisco Giants': '#FD5A1E',
				'Seattle Mariners': '#0C2C56',
				'St. Louis Cardinals': '#C41E3A',
				'Tampa Bay Rays': '#092C5C',
				'Texas Rangers': '#C0111F',
				'Toronto Blue Jays': '#134A8E',
				'Washington Nationals': '#AB0003',
			},
			isLoading: true, // flag to indicate if games are being loaded
		};
	},
	mounted() {
		this.fetchUpcomingGames();
	},
	methods: {
		async fetchUpcomingGames() {
			try {
				this.isLoading = true; // Set isLoading flag to true

				const snapshot = await db.collection('mlb_games').get();
				const games = [];
				const today = (new Date()).toLocaleDateString("fr-CA");

				if (snapshot.empty) {
					// Call the Firebase function to store MLB games for today
					const storeMlbGamesEndpoint = functions.httpsCallable('store_mlb_games_endpoint');
					await storeMlbGamesEndpoint({ date: today });
				}

				const updatedSnapshot = await db.collection('mlb_games').get();
				updatedSnapshot.forEach((doc) => {
					const gamesData = doc.data().games;
					gamesData.forEach((game) => {
						const { gamePk, gameDate, teams } = game;
						const homeTeam = teams.home.team.name;
						const awayTeam = teams.away.team.name;
						const formattedGame = { gamePk, gameDate, homeTeam, awayTeam };
						games.push(formattedGame);
					});
				});
				this.upcomingGames = games;
			} catch (error) {
				console.error('Error fetching/updating upcoming games:', error);
			} finally {
				this.isLoading = false; // Set isLoading flag to false when done loading
			}
		},
		formatTime(date) {
			const gameDate = new Date(date);
			return gameDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
		},
		getTeamColor(team) {
			return this.teamColors[team] || '#000000'; // Default color if not found in the teamColors object
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

.mlb-games-list {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 0;
	list-style-type: none;
	/* Remove bullet points */
}

.mlb-game {
	margin-bottom: 10px;
	text-align: left;
}

.mlb-game-link {
	text-decoration: none;
	color: #000000;
}

.mlb-game-row {
	display: flex;
	align-items: center;
	justify-content: space-between;
	background-color: #F5F5F5;
	padding: 10px;
	border-radius: 5px;
}

.mlb-team-container {
	display: flex;
	align-items: center;
}

.mlb-team {
	display: inline-block;
	padding: 2px 10px;
	color: #ffffff;
	/* Update to white */
	font-weight: bold;
	border-radius: 3px;
	margin-right: 5px;
}

.mlb-home-team {
	/* Add home team color */
}

.mlb-away-team {
	/* Add away team color */
}

.mlb-vs {
	margin: 0 5px;
	font-weight: bold;
}

.mlb-game-time {
	font-size: 14px;
	white-space: nowrap;
	margin-left: 10px;
}

.mlb-game-details {
	display: flex;
	align-items: center;
}

.mlb-predict-button {
	cursor: pointer;
}

.mlb-predict-button:focus,
.mlb-predict-button:active {
	outline: none;
	box-shadow: none;
}

.loading-icon {
	text-align: center;
	margin-top: 20px;
}

.spinner {
	display: inline-block;
	width: 40px;
	height: 40px;
	border-radius: 50%;
	border: 4px solid #ccc;
	border-top-color: #333;
	animation: spin 1s infinite ease-in-out;
}

@keyframes spin {
	0% {
		transform: rotate(0deg);
	}

	100% {
		transform: rotate(360deg);
	}
}
</style>
