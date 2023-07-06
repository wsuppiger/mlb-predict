<template>
	<div class="scoreboard-wrapper" :class="{ 'flash-green': scoreIncreased }">
		<h2 class="scoreboard-heading">Top 5 User Scores</h2>
		<ul class="scoreboard">
			<li v-for="(user, index) in topUsers" :key="index" class="scoreboard-item">
				<span class="scoreboard-rank">{{ index + 1 }}.</span>
				<span class="scoreboard-name">
					{{ convertName(user.name) }}
				</span>
				<span class="scoreboard-score">{{ user.score }}</span>
			</li>
			<li class="scoreboard-item scoreboard-item--current-user">
				<span class="scoreboard-name">My Score</span>
				<span class="scoreboard-score">{{ currentUserScore }}</span>
			</li>
		</ul>
	</div>
</template>

<script>
import { db, auth } from '@/firebase';

export default {
	props: {
		gamePk: {
			type: String,
			required: true
		}
	},
	data() {
		return {
			topUsers: [],
			currentUserScore: null,
			currentUserName: '',
			currentUserInTop5: false,
			unsubscribeTopUsers: null,
			unsubscribeCurrentUserScore: null,
			scoreIncreased: false,

		};
	},
	mounted() {
		this.getUserScores();
	},
	destroyed() {
		if (this.unsubscribeTopUsers) {
			this.unsubscribeTopUsers();
		}
		if (this.unsubscribeCurrentUserScore) {
			this.unsubscribeCurrentUserScore();
		}
	},
	methods: {
		async getUserScores() {
			try {
				const usersRef = db
					.collection('mlb_play_by_play')
					.doc(this.gamePk)
					.collection('users');

				const currentUser = auth.currentUser;
				if (currentUser) {
					const currentUserId = currentUser.uid;

					const currentUserDoc = await usersRef.doc(currentUserId).get();
					if (currentUserDoc.exists) {
						this.currentUserScore = currentUserDoc.data().score;
					}

					this.unsubscribeTopUsers = usersRef
						.orderBy('score', 'desc')
						.limit(5)
						.onSnapshot((snapshot) => {
							const updatedUsers = [];
							let currentUserInTop5 = false;
							snapshot.forEach((doc, index) => {
								const userData = doc.data();
								if (userData.userId === currentUserId) {
									currentUserInTop5 = true;
									this.currentUserName = userData.name;
								}
								updatedUsers.push({
									name: userData.name,
									score: userData.score,
									isCurrentUser: false
								});
							});
							this.currentUserInTop5 = currentUserInTop5;
							this.topUsers = updatedUsers;
						});

					this.unsubscribeCurrentUserScore = usersRef
						.doc(currentUserId)
						.onSnapshot((doc) => {
							if (doc.exists) {
								const previousScore = this.currentUserScore;
								this.currentUserScore = doc.data().score;
								this.scoreIncreased = this.currentUserScore > previousScore;
								if (this.scoreIncreased) {
									setTimeout(() => {
										this.scoreIncreased = false;
									}, 1000);
								}
							}
						});

				}
			} catch (error) {
				console.error('Error retrieving user scores:', error);
			}
		},
		convertName(fullName) {
			const names = fullName.split(" ");
			const firstName = names[0];
			const lastName = names[names.length - 1];
			const lastInitial = lastName.charAt(0);
			return `${firstName} ${lastInitial}.`;
		},

	}
};
</script>

<style scoped>
.scoreboard {
	list-style-type: none;
	padding: 10px;
	margin: 0;
}

.scoreboard-item {
	display: flex;
	align-items: center;
	padding: 10px;
	border-bottom: 1px solid #ccc;
}

.scoreboard-rank {
	margin-right: 10px;
	font-weight: bold;
}

.scoreboard-name {
	margin-right: auto;
}

.scoreboard-name--underline {
	text-decoration: underline;
}

.scoreboard-score {
	font-weight: bold;
	text-align: right;
}

.scoreboard-item--current-user {
	border-top: 2px solid #000;
}

h2 {
	margin-top: 20px;
}

p {
	font-weight: bold;
	margin-bottom: 20px;
}

.flash-green {
	background-color: #a5d6a7;
}

.scoreboard-wrapper {
	transition: background-color 0.5s;
	border-radius: 3px;
}
</style>
