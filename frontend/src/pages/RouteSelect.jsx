import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { getUserProfile, updateLearningRoute } from '../api'

const ROUTES = [
  {
    value: 'context_first',
    title: 'Beginnen met lezen',
    description:
      'Je leest korte Latijnse en Griekse teksten en leert de grammatica in context. ' +
      'Aanbevolen als je liever meteen met echte teksten aan de slag gaat.',
  },
  {
    value: 'grammar_first',
    title: 'Beginnen met grammatica',
    description:
      'Je leert eerst de grammaticaregels en oefent daarna met teksten. ' +
      'Aanbevolen als je liever stap voor stap de regels beheerst.',
  },
]

export default function RouteSelect() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const isOnboarding = searchParams.get('onboarding') === '1'

  const [selected, setSelected] = useState(null)
  const [currentRoute, setCurrentRoute] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    async function load() {
      try {
        const profile = await getUserProfile()
        setCurrentRoute(profile.learning_route)
        setSelected(profile.learning_route)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  async function handleConfirm() {
    if (!selected) return
    setSaving(true)
    setError('')
    try {
      await updateLearningRoute(selected)
      setCurrentRoute(selected)
      if (isOnboarding) {
        navigate('/dashboard')
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="page route-select-page">
        <p className="loading-text">Laden...</p>
      </div>
    )
  }

  const changed = selected !== currentRoute

  return (
    <div className="page route-select-page">
      <h1>{isOnboarding ? 'Kies je leerroute' : 'Leerroute'}</h1>
      <p className="route-select-intro">
        {isOnboarding
          ? 'Hoe wil je Latijn en Grieks leren? Je kunt dit later altijd wijzigen.'
          : 'Pas je leerroute aan. Dit verandert hoe nieuwe stof wordt aangeboden.'}
      </p>

      {!isOnboarding && currentRoute && (
        <div className="route-current">
          Huidige route: <strong>{ROUTES.find(r => r.value === currentRoute)?.title || currentRoute}</strong>
        </div>
      )}

      {error && <div className="error-message">{error}</div>}

      <div className="route-options">
        {ROUTES.map(route => (
          <button
            key={route.value}
            className={`route-option${selected === route.value ? ' route-option--selected' : ''}`}
            onClick={() => setSelected(route.value)}
          >
            <p className="route-option-title">{route.title}</p>
            <p className="route-option-desc">{route.description}</p>
          </button>
        ))}
      </div>

      <button
        className="btn btn-primary route-confirm-btn"
        disabled={!selected || saving || (!isOnboarding && !changed)}
        onClick={handleConfirm}
      >
        {saving ? 'Opslaan...' : isOnboarding ? 'Doorgaan' : 'Opslaan'}
      </button>

      {!isOnboarding && (
        <button
          className="btn btn-secondary"
          style={{ width: '100%', marginTop: '0.5rem' }}
          onClick={() => navigate('/dashboard')}
        >
          Terug naar dashboard
        </button>
      )}
    </div>
  )
}
