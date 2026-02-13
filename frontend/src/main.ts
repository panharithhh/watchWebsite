import { createApp } from "vue"
import App from "./App.vue"
import router from "./router"
import "./style.css"
import "./assets/auth.css"

console.log("VITE_API_BASE_URL =", import.meta.env.VITE_API_BASE_URL)

createApp(App).use(router).mount("#app")
