const BASE_URL = '/api';

export async function apiFetch(path, options = {}) {
  const token = localStorage.getItem('token');

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const message = body.detail || `Fout: ${response.status}`;
    throw new Error(message);
  }

  return response.json();
}

export function login(email, password) {
  return apiFetch('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
}

export function register(email, password) {
  return apiFetch('/auth/register', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
}

export function startSession() {
  return apiFetch('/session/start', { method: 'POST' });
}

export function submitAnswer(sessionId, { responseType, responseTimeMs, answer }) {
  return apiFetch('/session/answer', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionId,
      response: responseType,
      response_time_ms: responseTimeMs,
    }),
  });
}

export function getSessionSummary(sessionId) {
  return apiFetch(`/session/${sessionId}/summary`);
}

export function getProgressOverview() {
  return apiFetch('/progress/overview');
}

export function getGraphData() {
  return apiFetch('/progress/graph');
}
