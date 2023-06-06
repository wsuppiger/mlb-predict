<template>
  <div class="predict-game">
    <ChoosePlay />
  </div>
</template>

<script>
// @ is an alias to /src
import ChoosePlay from '@/components/ChoosePlay.vue'

export default {
  name: 'HomeView',
  components: {
    ChoosePlay
  }
}
</script>
