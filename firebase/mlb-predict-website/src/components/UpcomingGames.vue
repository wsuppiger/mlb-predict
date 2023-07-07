<template>
	<div class="mlb-box">
		<h2 class="mlb-heading">Today's MLB Games</h2>
		<ul class="mlb-games-list">
			<li v-for="game in upcomingGames" :key="game.gamePk" class="mlb-game">
				<router-link :to="'/predict-game/' + today + '/' + game.gamePk" class="mlb-game-link">
					<div :class="['mlb-game-row', { 'live-game': game.status === 'Live' }]">
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
							<font-awesome-icon v-if="game.status === 'Live'" icon="chevron-right" class="mlb-icon-spacing" />
						</div>
					</div>
				</router-link>
			</li>
		</ul>
		<loading-icon :is-loading="isLoading" />
	</div>
</template>

<script>
import { db, functions } from '@/firebase';
import getTeamColor from '@/teamColors.js';
import LoadingIcon from '@/components/LoadingIcon.vue';

export default {
	components: {
		LoadingIcon
	},
	data() {
		return {
			upcomingGames: [],
			isLoading: true, // flag to indicate if games are being loaded
			today: new Date().toLocaleDateString("fr-CA"),
		};
	},
	mounted() {
		this.fetchUpcomingGames();
	},
	methods: {
		async fetchUpcomingGames() {
			try {
				this.isLoading = true; // Set isLoading flag to true

				const today = this.today;
				const snapshot = await db.collection('mlb_games').doc(today).get();
				const games = [];

				if (!snapshot.exists) {
					// Call the Firebase function to store MLB games for local today if not stored yet.
					// This is only for the case where the local time is a day ahead
					// of the server's schedule (1am EST local, but 10pm PST server)
					const storeMlbGamesEndpoint = functions.httpsCallable('store_mlb_games_endpoint');
					try {
						const response = await storeMlbGamesEndpoint({ date: today });
						console.log(response.data);
					} catch (error) {
						console.error(error);
					}
				}

				const updatedSnapshot = await db.collection('mlb_games').doc(today).get();
				const gamesData = updatedSnapshot.data().games;
				gamesData.forEach((formattedGame) => {
					games.push(formattedGame);
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
		getTeamColor,
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

.live-game {
	background-color: #FFFFCC;
	/* Light yellow background for live games */
}

.mlb-icon-spacing {
	margin-left: 10px;
	/* Adjust the spacing value as needed */
}
</style>
