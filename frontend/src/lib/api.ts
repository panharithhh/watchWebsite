export async function api<T>(path: string, options: RequestInit = {}) {
    const token =
      localStorage.getItem("auth_token") || sessionStorage.getItem("auth_token")
    const res = await fetch(path, {
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
    } // check https 
  
    return data as T
  }
