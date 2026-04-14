import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login, register } from '../api'

export default function Login() {
  const navigate = useNavigate()
  const [isRegister, setIsRegister] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const action = isRegister ? register : login
      const data = await action(email, password)
      localStorage.setItem('token', data.token)
      navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <div className="login-header">
        <h1>Gymnasium Classica</h1>
        <p className="subtitle">Adaptief leren voor Latijn en Grieks</p>
      </div>

      <div className="card">
        <h2>{isRegister ? 'Account aanmaken' : 'Inloggen'}</h2>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">E-mailadres</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="naam@voorbeeld.nl"
              required
              autoComplete="email"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Wachtwoord</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Minimaal 8 tekens"
              required
              minLength={8}
              autoComplete={isRegister ? 'new-password' : 'current-password'}
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading
              ? 'Bezig...'
              : isRegister
                ? 'Registreren'
                : 'Inloggen'}
          </button>
        </form>

        <div className="toggle-text">
          {isRegister ? (
            <>
              Al een account?{' '}
              <button onClick={() => { setIsRegister(false); setError('') }}>
                Inloggen
              </button>
            </>
          ) : (
            <>
              Nog geen account?{' '}
              <button onClick={() => { setIsRegister(true); setError('') }}>
                Registreren
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
