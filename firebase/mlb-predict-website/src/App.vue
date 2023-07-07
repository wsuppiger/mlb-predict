<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <!-- <a class="navbar-brand" href="#">MLB Play By Play</a> -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/about" class="nav-link">About</router-link>
          </li>
          <li v-if="isLoggedIn">
            <a @click="signOut" class="nav-item nav-link btn btn-link">Sign Out</a>
          </li>
          <li v-else>
            <a v-show="!isLoggedIn" @click="openSignInPopover" class="nav-item nav-link btn btn-link">Sign
              In</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <router-view />

  <!-- Google Sign-In Popover -->
  <google-sign-in-popover v-if="showSignInPopover" @signed-in="handleSignIn" @close="closeSignInPopover" />
</template>

<script>
import { auth } from '@/firebase';
import GoogleSignInPopover from '@/components/GoogleSignInPopover.vue';

export default {
  data() {
    return {
      isLoggedIn: null, // Set the initial value to null
      showSignInPopover: false,
    };
  },
  components: {
    GoogleSignInPopover,
  },
  methods: {
    handleSignIn() {
      this.isLoggedIn = true;
      this.showSignInPopover = false;
    },
    openSignInPopover() {
      this.showSignInPopover = true;
    },
    closeSignInPopover() {
      this.showSignInPopover = false; // Close the popover when the close event is emitted
    },
    signOut() {
      auth
        .signOut()
        .then(() => {
          this.isLoggedIn = false;
        })
        .catch((error) => {
          console.error('Error signing out:', error);
        });
    },
  },
  created() {
    auth.onAuthStateChanged((user) => {
      this.isLoggedIn = !!user;
    });
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.navbar {
  background: #F8F8FF;
  margin-bottom: 10px;
}

.nav-link,
.navbar-brand {
  color: black !important;
}

.nav-link:hover {
  position: relative;
}

.nav-link:hover::after {
  content: "";
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(to right,
      #880000 0%,
      #880000 20%,
      white 20%,
      white 40%,
      #880000 40%,
      #880000 60%,
      white 60%,
      white 80%,
      #880000 80%,
      #880000 100%);
  background-size: 40px 2px;
}
</style>
