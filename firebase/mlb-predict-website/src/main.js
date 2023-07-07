import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faChevronRight, faUser } from '@fortawesome/free-solid-svg-icons'

import BootstrapVue3 from 'bootstrap-vue-3'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'

import GoogleSignInPopover from '@/components/GoogleSignInPopover.vue';

/* add icons to the library */
library.add(faChevronRight, faUser)


createApp(App)
	.use(router)
	.use(BootstrapVue3)
	.component('font-awesome-icon', FontAwesomeIcon)
	.component('google-sign-in-popover', GoogleSignInPopover)
	.mount('#app')