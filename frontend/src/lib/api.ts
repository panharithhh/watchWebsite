const API_BASE = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "")

function buildUrl(path: string) {
  if (/^https?:\/\//i.test(path)) {
    return path
  }

  if (!API_BASE) {
    throw new Error("VITE_API_BASE_URL is not set")
  }

  return `${API_BASE}${path.startsWith("/") ? "" : "/"}${path}`
}

export async function api<T>(path: string, options: RequestInit = {}) {
  const token =
    localStorage.getItem("auth_token") || sessionStorage.getItem("auth_token")

  const res = await fetch(buildUrl(path), {
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
    ...options,
  })

  const text = await res.text()

  let data: any
  try {
    data = text ? JSON.parse(text) : null
  } catch {
    data = text
  }

  if (!res.ok) {
    const msg =
      data?.detail || data?.error || `Request failed (${res.status} ${res.statusText})`
    throw new Error(msg)
  }

  return data as T
}
