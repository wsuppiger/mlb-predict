<template>
	<div>
		<h2 v-if="!isSelectionMade">Choose an option:</h2>

		<!-- Display main options -->
		<div v-if="!isSelectionMade">
			<button v-for="option in options" :key="option" @click="makeSelection(option)">
				{{ option }}
			</button>
		</div>

		<!-- Display sub-options -->
		<div v-if="isSelectionMade && selectedOption !== 'walk' && !chosenPlay">
			<h2>{{ selectedOption === 'hit' ? 'Choose hit type:' : 'Choose out type:' }}</h2>
			<button v-for="option in subOptions" :key="option" @click="chooseSubOption(option)">
				{{ option }}
			</button>
		</div>

		<!-- Display chosen play -->
		<div v-if="chosenPlay">
			<h3>Chosen Play:</h3>
			<input type="text" v-model="chosenPlay" disabled>
		</div>
	</div>
</template>

<script>
export default {
	data() {
		return {
			isSelectionMade: false,
			selectedOption: '',
			options: ['hit', 'out', 'walk'],
			hitSubOptions: ['single', 'double', 'triple', 'homerun'],
			outSubOptions: ['strikeout', 'groundout', 'popout', 'flyout'],
			chosenPlay: '',
		};
	},
	computed: {
		subOptions() {
			return this.selectedOption === 'hit' ? this.hitSubOptions : this.outSubOptions;
		},
	},
	methods: {
		makeSelection(option) {
			this.selectedOption = option;
			this.isSelectionMade = true;
			this.chosenPlay = option === 'walk' ? 'walk' : '';
		},
		chooseSubOption(option) {
			this.chosenPlay = option;
		},
	},
};
</script>
