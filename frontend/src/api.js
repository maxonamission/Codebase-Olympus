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
    if (response.status === 401) {
      // Token is invalid or expired — clear it and redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
      throw new Error('Sessie verlopen. Log opnieuw in.');
    }
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

/**
 * Submit an answer to the current session question.
 *
 * Two shapes:
 * - { answerText, responseTimeMs }: literal answer, server grades.
 * - { response, responseTimeMs }: self-assess outcome ('correct',
 *   'slow_correct' or 'incorrect').
 */
export function submitAnswer(sessionId, { answerText, response, responseTimeMs }) {
  const body = {
    session_id: sessionId,
    response_time_ms: responseTimeMs,
  };
  if (answerText != null) body.answer_text = answerText;
  if (response != null) body.response = response;
  return apiFetch('/session/answer', {
    method: 'POST',
    body: JSON.stringify(body),
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

export function getUserProfile() {
  return apiFetch('/user/profile');
}

export function updateLearningRoute(learningRoute) {
  return apiFetch('/user/learning-route', {
    method: 'PUT',
    body: JSON.stringify({ learning_route: learningRoute }),
  });
}

export function updateSettings(learningRoute) {
  return apiFetch('/auth/settings', {
    method: 'POST',
    body: JSON.stringify({ learning_route: learningRoute }),
  });
}
