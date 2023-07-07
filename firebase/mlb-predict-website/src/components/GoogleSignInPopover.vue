<template>
	<div class="popover-overlay" @click="closePopover">
		<div class="popover-content" @click.stop>
			<p>Please sign in with Google to play.</p>
			<button class="google-signin-button" @click="signInWithGoogle">Sign In with Google</button>
		</div>
	</div>
</template>

<script>
import { signInWithGoogle } from '@/firebase';

export default {
	methods: {
		signInWithGoogle() {
			signInWithGoogle()
				.then(() => {
					this.$emit('signed-in'); // Emit the 'signed-in' event to the parent component
				})
				.catch((error) => {
					console.error('Error signing in:', error);
				});
		},
		closePopover() {
			this.$emit('close'); // Emit the 'close' event to the parent component
		},
	},
};
</script>

<style scoped>
.popover-overlay {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background-color: rgba(0, 0, 0, 0.5);
	display: flex;
	justify-content: center;
	align-items: center;
}

.popover-content {
	background-color: #ffffff;
	padding: 20px;
	border-radius: 5px;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
	border: 2px solid #42a5f5;
}

.google-signin-button {
	background-color: #ffffff;
	color: #4285f4;
	/* Google Blue color */
	border: 1px solid #4285f4;
	/* Google Blue color */
	border-radius: 4px;
	font-size: 14px;
	font-weight: 500;
	height: 36px;
	padding: 0 16px;
	display: flex;
	align-items: center;
	justify-content: center;
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	width: fit-content;
	margin: 0 auto;
}

.google-signin-button:hover {
	background-color: rgba(66, 133, 244, 0.04);
	/* Lighter shade of Google Blue color */
}

.google-signin-button:focus {
	outline: none;
	box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.3);
	/* Google Blue color with opacity */
}
</style>
