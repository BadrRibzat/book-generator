import { createApp } from 'vue';
import { createPinia } from 'pinia';
import './style.css';
import App from './App.vue';
import router from './router';

// Font Awesome setup - simplified working version
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
  faHome,
  faBars,
  faTimes,
  faEnvelope,
  faCode,
  faRocket,
  faBrain,
  faPalette,
  faFilePdf,
  faChartLine,
  faBookOpen,
  faUsers,
  faAward,
  faArrowRight,
  faCheck,
  faLock,
  faUserPlus,
  faSignInAlt,
  faAt,
  faShieldAlt,
  faUserCheck,
  faPlusCircle,
  faMagic,
  faCalendar,
  faStar,
  faUpload,
  faEdit,
  faImage,
  faSave,
  faSearch,
  faFilter,
  faInfoCircle,
  faQuestionCircle,
  faHeart,
  faShare,
  faCopy,
  faUserCircle,
  faCrown,
  faGem,
  faCreditCard,
  faShoppingCart,
  faChartBar,
  faCalendarAlt,
  faGift,
  fas,
  faAppleAlt,
  faSpa,
  faDumbbell,
  faBullseye,
  faCheckSquare,
  faCompass,
  faClock,
  faRobot,
  faChild,
  faSun,

} from '@fortawesome/free-solid-svg-icons';

// Add icons to library
library.add(
  faBook, faPlus, faUser, faSignOutAlt, faDownload, faTrash, faSpinner,
  faCheckCircle, faExclamationCircle, faEye, faHome, faBars, faTimes,
  faEnvelope, faCode, faRocket, faBrain, faPalette, faFilePdf, faChartLine,
  faBookOpen, faUsers, faAward, faArrowRight, faCheck, faLock, faUserPlus,
  faSignInAlt, faAt, faShieldAlt, faUserCheck, faPlusCircle, faMagic,
  faCalendar, faStar, faUpload, faEdit, faImage, faSave, faSearch,
  faFilter, faInfoCircle, faQuestionCircle, faHeart, faShare, faCopy,
  faUserCircle, faCrown, faGem, faCreditCard, faShoppingCart, faChartBar,
  faCalendarAlt, faGift, fas, faAppleAlt, faSpa, faDumbbell, faBullseye, faCheckSquare, faCompass, faClock, faRobot, faChild, faSun,

);

const app = createApp(App);
const pinia = createPinia();

app.component('font-awesome-icon', FontAwesomeIcon);
app.use(pinia);
app.use(router);
app.mount('#app');
