let API_BASE = "http://localhost:8001";

async function loadConfig() {
  try {
    const basePath = process.env.NEXT_PUBLIC_BASE_PATH || "";
    const resp = await fetch(`${basePath}/api-config.json`, {
      signal: AbortSignal.timeout(2000),
    });
    if (resp.ok) {
      const cfg = await resp.json();
      if (cfg.apiBase) API_BASE = cfg.apiBase;
    }
  } catch {
    // use default
  }
}

let configLoaded = false;
async function ensureConfig() {
  if (!configLoaded) {
    await loadConfig();
    configLoaded = true;
  }
}

export async function apiGet<T>(endpoint: string): Promise<T> {
  await ensureConfig();
  const res = await fetch(`${API_BASE}${endpoint}`, {
    signal: AbortSignal.timeout(10000),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function apiPost<T>(endpoint: string, body: unknown): Promise<T> {
  await ensureConfig();
  const res = await fetch(`${API_BASE}${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(10000),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export { API_BASE };
