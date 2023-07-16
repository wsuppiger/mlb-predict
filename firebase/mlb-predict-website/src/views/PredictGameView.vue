<template>
  <div v-if="isUserSignedIn">
    <div v-if="liveData">
      <b-container>
        <b-row justify-content="left">
          <b-col lg="6">
            <h2 class="section-title">Predict Play</h2>
            <ChoosePlay :gamePk="this.gamePk" :atBatIndex="liveData.live.atBatIndex" :decisionTime="this.decisionTime" />
            <PlayerScoreboard style="margin-top: 50px;" :game-pk="this.gamePk" />
          </b-col>
          <b-col lg="6">
            <h2 class="section-title">Live Data</h2>
            <b-row class="live-info" justify-content="left">
              <b-col lg="6">
                <div class="info-container">
                  <div class="game-status">
                    <div class="inning-info">
                      <div class="inning">
                        {{ liveData.live.inning }}
                      </div>
                      <div class="arrow" :class="{ up: liveData.live.isTopInning, down: !liveData.live.isTopInning }">
                      </div>
                    </div>
                    <div class="team-info-box team-info">
                      <div class="team-info-grid team-info">
                        <div class="team-info-item"><span class="mlb-team mlb-away-team"
                            :style="{ backgroundColor: getTeamColor(this.awayTeam) }">
                            {{ this.awayTeam }}
                          </span></div>
                        <div class="team-info-item">
                          <div class="team-score">
                            {{ liveData.live.awayScore }}
                          </div>
                        </div>
                        <div class="team-info-item"><span class="mlb-team mlb-home-team"
                            :style="{ backgroundColor: getTeamColor(this.homeTeam) }">
                            {{ this.homeTeam }}
                          </span></div>
                        <div class="team-info-item">
                          <div class="team-score">
                            {{ liveData.live.homeScore }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="count-info">
                    <div class="count-item">
                      <span class="count-label">O:</span>
                      <div class="dots">
                        <div class="dot" v-for="n in 3" :key="n" :class="{ active: n <= liveData.live.count.outs }"></div>
                      </div>
                    </div>
                    <div class="count-item">
                      <span class="count-label">S:</span>
                      <div class="dots">
                        <div class="dot" v-for="n in 2" :key="n" :class="{ active: n <= liveData.live.count.strikes }">
                        </div>
                      </div>
                    </div>
                    <div class="count-item">
                      <span class="count-label">B:</span>
                      <div class="dots">
                        <div class="dot" v-for="n in 3" :key="n" :class="{ active: n <= liveData.live.count.balls }">
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="pitcher-batter-info">
                  <div class="pitcher-info">
                    <span class="label">Pitcher:</span>
                    <span class="name" v-if="liveData.live.pitcher">
                      <a class="player-link" :href="'https://www.mlb.com/player/' + liveData.live.pitcher.id"
                        target="_blank" rel="noopener noreferrer">
                        {{ liveData.live.pitcher.fullName }}
                      </a>
                    </span>
                  </div>
                  <div class="batter-info">
                    <span class="label">Batter:</span>
                    <span class="name" v-if="liveData.live.batter">
                      <a class="player-link" :href="'https://www.mlb.com/player/' + liveData.live.batter.id"
                        target="_blank" rel="noopener noreferrer">
                        {{ liveData.live.batter.fullName }}
                      </a>
                    </span>
                  </div>
                </div>

              </b-col>
              <b-col lg="6" justify-content="left">
                <div class="diamond-wrapper">
                  <DiamondShape :leftColor="getBaseColor('third-base')" :topColor="getBaseColor('second-base')"
                    :rightColor="getBaseColor('first-base')" />
                </div>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
        <!-- <b-row>
          <b-col lg="6" v-if="this.gamePk">
            <PlayerScoreboard :game-pk="this.gamePk" />
          </b-col>
        </b-row> -->
      </b-container>
    </div>
    <div v-else class="loading-container">
      <LoadingIcon :is-loading="true" />
    </div>

    <!-- <button @click="TestUpdate">Tests Backend Heartbeat</button> -->

  </div>
  <GoogleSignInPopover v-else />
</template>

<script>
import { auth, db, functions } from '@/firebase';
import GoogleSignInPopover from '@/components/GoogleSignInPopover.vue';
import getTeamColor from '@/teamColors.js';
import { useRoute } from "vue-router";
import LoadingIcon from '@/components/LoadingIcon.vue';
import DiamondShape from '@/components/DiamondShape.vue'
import ChoosePlay from '@/components/ChoosePlay.vue';
import PlayerScoreboard from '@/components/PlayerScoreboard.vue';

export default {
  components: {
    GoogleSignInPopover,
    LoadingIcon,
    DiamondShape,
    ChoosePlay,
    PlayerScoreboard
  },
  data() {
    return {
      isUserSignedIn: false,
      homeTeam: '',
      awayTeam: '',
      gamePk: null,
      date: null,
      liveData: null,
      decisionTime: 0,
    };
  },
  mounted() {
    // Check if user is already signed in
    auth.onAuthStateChanged((user) => {
      this.isUserSignedIn = !!user;
    });

    // Construct the document reference using the date
    const gameRef = db.collection('mlb_games').doc(this.date);

    // Get the document snapshot and retrieve the game info based on the gamePk
    gameRef
      .get()
      .then((doc) => {
        if (doc.exists) {
          const game = doc.data().games.find((g) => g.gamePk == this.gamePk);
          if (game) {
            this.homeTeam = game.homeTeam;
            this.awayTeam = game.awayTeam;
          }
        } else {
          console.log('Document does not exist');
        }
      })
      .catch((error) => {
        console.error('Error retrieving game data:', error);
      });
  },
  setup() {
    const route = useRoute();
    const gamePk = route.params.gamePk;
    const date = route.params.date;
    return { gamePk, date }
  },
  created() {
    this.checkGameReadiness().then((documentExists) => {
      if (this.isUserSignedIn && !documentExists) {
        const updatePlayByPlay = functions.httpsCallable('backend_CPR_heartbeat');
        updatePlayByPlay({ gamepk: this.gamePk });
      }
    });
    this.subscribeToLiveUpdates();
    this.subscribeToAtBatChanges();
  },
  methods: {
    getTeamColor,
    getBaseColor(base) {
      if (base === 'first-base' && this.liveData.live.postOnFirst) {
        return '#ff9800';
      }
      if (base === 'second-base' && this.liveData.live.postOnSecond) {
        return '#ff9800';
      }
      if (base === 'third-base' && this.liveData.live.postOnThird) {
        return '#ff9800';
      }
      return '';
    },
    async checkGameReadiness() {
      const liveDocRef = db.collection("mlb_play_by_play").doc(this.gamePk);
      const doc = await liveDocRef.get();
      this.liveData = doc.data();
      return doc.exists;
    },
    async subscribeToLiveUpdates() {
      const liveDocRef = db.collection("mlb_play_by_play").doc(this.gamePk);
      liveDocRef.onSnapshot((snap) => {
        this.liveData = snap.data();
      });
    },
    async subscribeToAtBatChanges() {
      const liveDocRef = db.collection("scoring_index").doc(this.gamePk);
      liveDocRef.onSnapshot((snap) => {
        const data = snap.data();
        if (data && data.decisionTime) {
          this.decisionTime = data.decisionTime;
        }
      });
    },
    // async TestUpdate() {
    //   const updatePlayByPlay = functions.httpsCallable('backend_heartbeat');
    //   await updatePlayByPlay({});
    // },
  },
};
</script>

<style scoped>
.mlb-team {
  display: inline-block;
  padding: 2px 10px;
  color: #ffffff;
  /* Update to white */
  font-weight: bold;
  border-radius: 3px;
  margin-right: 5px;
  font-size: .9em;
}

.live-info {
  display: flex;
  justify-content: left;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
}

.info-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  flex-grow: 1;
}

.game-status {
  display: flex;
  align-items: center;
}

.inning-info {
  display: flex;
  align-items: center;
  margin-right: 10px;
}

.inning {
  font-weight: bold;
  font-size: 20px;
}

.arrow {
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
}

.up {
  border-bottom: 12px solid #212529;
}

.down {
  border-top: 12px solid #212529;
}

.team-info-box {
  display: flex;
  flex-direction: column;
}

.team-info {
  display: block;
  align-items: center;
  margin-bottom: 5px;
}

.team-name {
  font-weight: bold;
  margin-right: 10px;
}

.team-score {
  font-size: 20px;
}

.count-info {
  display: flex;
  flex-direction: row;
}

.count-item {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.count-label {
  font-weight: bold;
  margin-right: 5px;
}

.dots {
  display: flex;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #ccc;
  margin-right: 5px;
}

.active {
  background-color: #ff9800;
}

.team-info-grid {
  display: grid;
  grid-template-columns: repeat(2, auto);
  gap: 10px;
  width: max-content;
}

.team-info-item {
  border: 1px solid transparent;
  background-color: transparent;
}

.pitcher-batter-info {
  margin-top: 5px;
}

.pitcher-info,
.batter-info {
  display: flex;
  align-items: left;
  margin-bottom: 10px;
}

.label {
  font-weight: bold;
  margin-right: 5px;
}

.player-link {
  text-decoration: underline;
  color: inherit;
}

.player-link:hover,
.player-link:focus {
  text-decoration: none;
}
</style>