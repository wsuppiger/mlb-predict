<template>
	<div class="live-info">
		<!-- Display timer -->
		<div class="timer" :style="{ transitionDuration: transitionDuration, width: timerWidth }"></div>

		<!-- Display main options -->
		<div class="primary-options">
			<button v-for="option in options" :key="option" @click="makeSelection(option)" class="primary-option"
				:class="{ active: selectedOption === option, disabled: isSelectionMade && chosenPlay !== '' }"
				:disabled="isSelectionMade && chosenPlay !== ''">
				{{ getButtonText(option) }}
			</button>
		</div>

		<!-- Display sub-options -->
		<div v-if="isSelectionMade" class="sub-options">
			<button v-for="option in subOptions" :key="option" @click="choosePlay(option)" class="sub-option"
				:class="{ active: chosenPlay === option, disabled: chosenPlay !== '' }" :disabled="chosenPlay !== ''">
				{{ getButtonText(option) }}
			</button>
		</div>
		<div class="alert" :class="{ show: showAlert }">
			<span>{{ alertMessage }}</span>
			<button class="close-button" @click="hideNotification">X</button>
		</div>
	</div>
</template>

<script>
import { auth, functions } from '@/firebase';
export default {
	data() {
		return {
			isSelectionMade: false,
			selectedOption: '',
			options: ['hit', 'out', 'other'],
			hitSubOptions: ['single', 'double', 'triple', 'homerun'],
			outSubOptions: ['strikeout', 'groundout', 'DP', 'flyout'],
			chosenPlay: '',
			transitionDuration: '0s', // Transition duration for timer expansion
			timerWidth: '100%', // Timer width
			showAlert: false,
			alertMessage: '',
		};
	},
	props: {
		gamePk: {
			type: String,
		},
		atBatIndex: {
			type: Number,
			default: 0,
		},
		decisionTime: {
			type: Number,
			required: true,
		},
	},
	computed: {
		subOptions() {
			if (this.selectedOption === 'hit') {
				return this.hitSubOptions;
			} else if (this.selectedOption === 'out') {
				return this.outSubOptions;
			} else {
				return ['walk', 'error', 'HBP'];
			}
		},
	},
	methods: {
		makeSelection(option) {
			this.selectedOption = option;
			this.isSelectionMade = true;
			this.chosenPlay = '';
		},
		async MakePlayPick(option, atBatIndex, gamePk) {
			const callMakePlayPick = functions.httpsCallable('make_play_pick');
			const result = await callMakePlayPick({
				gamepk: gamePk,
				atBatIndex: atBatIndex.toString(),
				uid: auth.currentUser.uid,
				name: auth.currentUser.displayName,
				pick: option
			});
			const success = result.data.success;
			if (success === true) {
				console.log("Success: true");
			} else {
				this.showNotification(result.data.message);
			}
		},
		async choosePlay(option) {
			this.chosenPlay = option;
			this.MakePlayPick(option, this.atBatIndex, this.gamePk);
		},
		getButtonText(option) {
			const pointsTable = {
				other: 100,
				single: 40,
				double: 125,
				triple: 500,
				homerun: 250,
				out: 15,
				strikeout: 40,
				groundout: 35,
				flyout: 40,
				hit: 100,
				HBP: 500,
				DP: 70,
				walk: 100,
				error: 500,
			};

			const points = pointsTable[option];
			return `${option} (+${points})`;
		},
		calculateAndStartTimer(decisionTime) {
			const now = new Date().getTime();
			const timoutDelay = 100;
			const timeRemaining = decisionTime - now - timoutDelay;
			console.log(timeRemaining);
			console.log(now);
			console.log(decisionTime);
			this.transitionDuration = '0s';
			this.timerWidth = '100%';

			setTimeout(() => {
				this.transitionDuration = `${timeRemaining}ms`;
				this.timerWidth = '0%';
			}, timoutDelay);
		},
		updateDecisionTime(newDecisionTime) {
			this.isSelectionMade = false;
			this.selectedOption = '';
			this.chosenPlay = '';
			this.calculateAndStartTimer(newDecisionTime);
		},
		showNotification(message) {
			this.alertMessage = message;
			this.showAlert = true;

			setTimeout(() => {
				this.hideNotification();
			}, 10000);
		},
		hideNotification() {
			this.showAlert = false;
			this.alertMessage = '';
		}
	},
	mounted() {
		this.calculateAndStartTimer(this.decisionTime);
	},
	watch: {
		decisionTime(newDecisionTime) {
			this.updateDecisionTime(newDecisionTime);
		},
	},
};
</script>

<style scoped>
.live-info {
	display: flex;
	flex-direction: column;
	align-items: stretch;
	border: 1px solid #ccc;
	border-radius: 5px;
	padding: 10px;
}

.timer {
	height: 5px;
	background-color: #ccc;
	margin-bottom: 10px;
	transition: width;
	transition-timing-function: linear;
}

.primary-options {
	display: flex;
	justify-content: left;
	align-items: center;
	border-radius: 5px;
	padding: 10px;
	margin-bottom: 10px;
}

.primary-option {
	background-color: #fff;
	border: 1px solid #ccc;
	border-radius: 5px;
	padding: 10px;
	cursor: pointer;
	margin-right: 10px;
}

.primary-option.active {
	background-color: #ccc;
}

.primary-option.disabled {
	opacity: 0.5;
	cursor: not-allowed;
	transition: opacity;
}

.sub-options {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	grid-gap: 10px;
}

.sub-option {
	background-color: #fff;
	border: 1px solid #ccc;
	border-radius: 5px;
	padding: 10px;
	cursor: pointer;
}

.sub-option.active {
	background-color: #ccc;
}

.sub-option.disabled {
	opacity: 0.5;
	cursor: not-allowed;
}

.chosen-play {
	margin-top: 10px;
}

.alert {
	position: fixed;
	top: 20px;
	left: 50%;
	transform: translateX(-50%);
	background-color: #f8d7da;
	color: #721c24;
	border: 1px solid #f5c6cb;
	border-radius: 4px;
	padding: 10px;
	text-align: center;
	opacity: 0;
	visibility: hidden;
	transition: opacity 0.3s ease, visibility 0.3s ease;
}

.show {
	opacity: 1;
	visibility: visible;
}

.close-button {
	position: absolute;
	top: 2px;
	left: 2px;
	background: none;
	border: none;
	font-size: 14px;
	cursor: pointer;
}
</style>
