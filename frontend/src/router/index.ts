import { createRouter, createWebHistory } from "vue-router"
import LoginView from "@/views/LoginView.vue"
import SignupView from "@/views/SignupView.vue"
import AuthenticationView from "@/views/AuthenticationView.vue"
import SignupCodeView from "@/views/SignupCodeView.vue"
import AdminDashboardView from "@/views/AdminDashboardView.vue"
import UserHomeView from "@/views/UserHomeView.vue"
import RepairView from "@/views/RepairView.vue"
import WishlistView from "@/views/WishlistView.vue"
import SellWatchView from "@/views/SellWatchView.vue"

const router = createRouter({
  history: createWebHistory(), // clean url
  routes: [
    { path: "/", redirect: "/login" },
    { path: "/login", component: LoginView },
    { path: "/authentication", component: AuthenticationView },
    { path: "/signup", component: SignupView },
    { path: "/signup-code", component: SignupCodeView },
    { path: "/admin", component: AdminDashboardView, meta: { requiresAdmin: true } },
    { path: "/home", component: UserHomeView },
    { path: "/repair", component: RepairView },
    { path: "/wishlist", component: WishlistView, meta: { requiresAuth: true } },
    { path: "/sell", component: SellWatchView },
  ],
})

router.beforeEach((to) => {
  const token =
    localStorage.getItem("auth_token") ||
    sessionStorage.getItem("auth_token")

  if (to.meta.requiresAdmin) {
    const role =
      localStorage.getItem("role") ||
      sessionStorage.getItem("role")

    if (role === "admin") return true
    return "/login"
  }

  if (to.meta.requiresAuth) {
    if (token) return true
    return "/login"
  }

  return true
})

export default router
