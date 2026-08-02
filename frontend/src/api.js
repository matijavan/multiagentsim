const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function handle(res) {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `Request failed (${res.status})`)
  }
  return res.json()
}

export async function fetchStrategies() {
  const res = await fetch(`${API_BASE}/api/strategies`)
  return handle(res)
}

export async function runCompare(config) {
  const res = await fetch(`${API_BASE}/api/compare`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(config),
  })
  return handle(res)
}
