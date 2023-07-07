<template>
	<div class="loading-icon" v-if="isLoading">
		<div class="spinner"></div>
	</div>
</template>

<script>
export default {
	props: {
		isLoading: {
			type: Boolean,
			required: true
		}
	}
};
</script>

<style scoped>
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
