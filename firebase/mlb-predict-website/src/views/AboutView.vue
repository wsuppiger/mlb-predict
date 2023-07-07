<template>
  <div class="about-page">
    <div class="section">
      <h2>Overview</h2>
      <p>
        This is a free game where users can pick the result of an upcoming at bat in any MLB game to earn points and
        compete against friends and the public.
      </p>
    </div>

    <div class="section">
      <h2>How To Play</h2>
      <p>
        On the <router-link to="/">home page</router-link>, select any MLB game scheduled for today and log in with your
        Google account to get started. Once you're in the game, choose the play for the next at bat under <strong>"Predict
          Play"</strong>. Remember, you have 10 seconds to make your selection, so be quick! Make sure to choose one of
        the options: <strong>"hit"</strong>, <strong>"out"</strong>, or <strong>"other"</strong> and one of their
        respective sub-options. Note that just selecting the main option without a sub-option will not submit your pick.
      </p>
    </div>

    <div class="section">
      <h2>Scoring</h2>
      <p>
        As you can see next to each option under <strong>"Predict Play"</strong>, you will be rewarded points for choosing
        correctly. For example, if you choose <strong>"hit (+25)"</strong> -> <strong>"single (+40)"</strong> and the play
        result is a single, you will earn <strong>25 + 40 = 65</strong> points. If you had chosen any other type of hit,
        you would only be rewarded 25 points. You can track your score under <strong>"My
          Score"</strong> and see the top 5 current users for each game.
      </p>
    </div>

    <div class="section">
      <h2>Live Data</h2>
      <p>
        The live data section fetches updates every 10 seconds from the unofficial MLB.com API. Please note that there
        might be occasional outages or mistakes due to the data source. Rest assured, the same data is used to calculate
        scores.
      </p>
    </div>

    <div class="section">
      <h2>Recommendations</h2>
      <p>
        If you have any recommendations or encounter any issues while using the app, please submit them to the <a
          href="https://github.com/wsuppiger/mlb-predict/issues" target="_blank">GitHub repository</a>.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutPage',
};
</script>

<style scoped>
.about-page {
  max-width: 800px;
  margin: 0 auto;
}

.section {
  margin-bottom: 30px;
}

h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

p {
  line-height: 1.5;
}
</style>
