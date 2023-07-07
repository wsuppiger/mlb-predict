<template>
	<div class="shape-section">
		<div class="container">
			<div class="diamond-container">
				<div class="diamond-shape top-middle" :style="{ background: getBackgroundColor(topColor) }"></div>
				<div class="diamond-shape left" :style="{ background: getBackgroundColor(leftColor) }"></div>
				<div class="diamond-shape right" :style="{ background: getBackgroundColor(rightColor) }"></div>
			</div><!-- .diamond-container -->
		</div><!-- .container -->
	</div><!-- .shape-section -->
</template>

<script>
export default {
	props: {
		topColor: {
			type: String,
			default: ''
		},
		leftColor: {
			type: String,
			default: ''
		},
		rightColor: {
			type: String,
			default: ''
		}
	},
	methods: {
		getBackgroundColor(color) {
			if (color.trim() === '') {
				return '#aaa';
			} else {
				return color;
			}
		}
	}
};
</script>

<style>
/* #Shape Styles
  –––––––––––––––––––––––––––––––––––––––––––––––––– */
.shape-section {
	margin-top: 30px;
	padding: 40px 0;
	display: flex;
	justify-content: center;
	align-items: center;
}

.diamond-container {
	position: relative;
	width: 92px;
	/* (30px + 1px + 30px + 1px + 30px) */
	height: 92px;
	/* (30px + 1px + 30px + 1px + 30px) */
}

.diamond-shape {
	height: 30px;
	position: absolute;
	width: 30px;
	transform: rotate(45deg);
}

.top-middle {
	top: -31px;
	/* (30px + 1px) */
	left: 31px;
	/* (30px + 1px) */
}

.left {
	top: 0;
	left: 0;
}

.right {
	top: 0;
	left: 62px;
}
</style>
