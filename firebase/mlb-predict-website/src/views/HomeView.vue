<template>
  <div class="home">
    <UpcomingGames />
  </div>
</template>

<script>
// @ is an alias to /src
import UpcomingGames from '@/components/UpcomingGames.vue'

export default {
  name: 'HomeView',
  components: {
    UpcomingGames
  }
}
</script>
