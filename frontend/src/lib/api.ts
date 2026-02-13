const API_BASE =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") || "http://localhost:8000"

function buildUrl(path: string) {
  // If callers passed absolute localhost URLs, rewrite to the configured base.
  if (path.startsWith("http://localhost:8000")) {
    return path.replace("http://localhost:8000", API_BASE)
  }
  if (path.startsWith("http") || path.startsWith("https")) {
    return path
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
    const msg = data?.detail || data?.error || `Request failed (${res.status})`
    throw new Error(msg)
  }

  return data as T
}
