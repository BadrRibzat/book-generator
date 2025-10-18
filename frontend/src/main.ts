import { createApp } from 'vue';
import { createPinia } from 'pinia';
import './style.css';
import App from './App.vue';
import router from './router';

// Font Awesome setup
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
  faBook,
  faPlus,
  faUser,
  faSignOutAlt,
  faDownload,
  faTrash,
  faSpinner,
  faCheckCircle,
  faExclamationCircle,
  faEye,
  faEyeSlash,
  faHome,
  faBars,
  faTimes,
  faEnvelope,
  faCode,
  faRocket,
  faPlayCircle,
  faBrain,
  faPalette,
  faFilePdf,
  faGaugeHigh,
  faMobileAlt,
  faDatabase,
  faChartLine,
  faBookOpen,
  faUsers,
  faAward,
  faArrowRight,
  faCheck,
  faMoon,
  faSun,
  faLock,
  faUserPlus,
  faSignInAlt,
  faAt,
  faShieldAlt,
  faUserCheck,
  faPlusCircle,
  faRoute,
  faMagic,
} from '@fortawesome/free-solid-svg-icons';

// Add icons to library
library.add(
  faBook,
  faPlus,
  faUser,
  faSignOutAlt,
  faDownload,
  faTrash,
  faSpinner,
  faCheckCircle,
  faExclamationCircle,
  faEye,
  faEyeSlash,
  faHome,
  faBars,
  faTimes,
  faEnvelope,
  faCode,
  faRocket,
  faPlayCircle,
  faBrain,
  faPalette,
  faFilePdf,
  faGaugeHigh,
  faMobileAlt,
  faDatabase,
  faChartLine,
  faBookOpen,
  faUsers,
  faAward,
  faArrowRight,
  faCheck,
  faMoon,
  faSun,
  faLock,
  faUserPlus,
  faSignInAlt,
  faAt,
  faShieldAlt,
  faUserCheck,
  faPlusCircle,
  faRoute,
  faMagic
);

const app = createApp(App);
const pinia = createPinia();

app.component('font-awesome-icon', FontAwesomeIcon);
app.use(pinia);
app.use(router);
app.mount('#app');
