import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  getBijspijkerProgress,
  getClusterProgress,
  getProgressOverview,
  getUserProfile,
  startBijspijker,
  updateSettings,
} from '../api'

const ROUTE_LABELS = {
  context_first: 'Beginnen met lezen',
  grammar_first: 'Beginnen met grammatica',
}

const DOMAIN_LABELS = {
  G: 'Grammatica',
  V: 'Vocabulaire',
  C: 'Cultuur',
  I: 'Integratie',
}

function DomainBar({ domain, mastered, total }) {
  const pct = total > 0 ? Math.round((mastered / total) * 100) : 0
  const label = DOMAIN_LABELS[domain] || domain

  return (
    <div className="domain-row">
      <span className="domain-label">{label}</span>
      <div className="domain-track">
        <div className="domain-fill" style={{ width: `${pct}%` }} />
      </div>
      <span className="domain-count">{mastered}/{total}</span>
    </div>
  )
}

function ClusterBar({ label, beschrijving, mastered, total, masteredPct }) {
  return (
    <div className="domain-row cluster-row" title={beschrijving}>
      <span className="domain-label cluster-label">{label}</span>
      <div className="domain-track">
        <div className="domain-fill" style={{ width: `${masteredPct}%` }} />
      </div>
      <span className="domain-count">{mastered}/{total}</span>
    </div>
  )
}

export default function Dashboard() {
  const navigate = useNavigate()
  const [overview, setOverview] = useState(null)
  const [clusters, setClusters] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [learningRoute, setLearningRoute] = useState(null)
  const [switchingRoute, setSwitchingRoute] = useState(false)
  const [bijspijker, setBijspijker] = useState(null)
  const [bumping, setBumping] = useState(false)

  useEffect(() => {
    async function load() {
      try {
        const [data, profile, clusterData, bij] = await Promise.all([
          getProgressOverview(),
          getUserProfile(),
          getClusterProgress().catch(() => ({ clusters: [] })),
          getBijspijkerProgress().catch(() => null),
        ])
        setOverview(data)
        setLearningRoute(profile.learning_route)
        setClusters(clusterData.clusters || [])
        setBijspijker(bij)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  async function handleBumpChapter() {
    if (!bijspijker) return
    setBumping(true)
    setError('')
    try {
      await startBijspijker({
        methodeLat: bijspijker.methode_lat,
        hoofdstukLat: bijspijker.hoofdstuk_lat ? bijspijker.hoofdstuk_lat + 1 : null,
        methodeGrc: bijspijker.methode_grc,
        hoofdstukGrc: bijspijker.hoofdstuk_grc ? bijspijker.hoofdstuk_grc + 1 : null,
        resetPriors: false,
      })
      setBijspijker(await getBijspijkerProgress())
    } catch (err) {
      setError(err.message)
    } finally {
      setBumping(false)
    }
  }

  async function handleToggleRoute() {
    const newRoute = learningRoute === 'grammar_first' ? 'context_first' : 'grammar_first'
    setSwitchingRoute(true)
    try {
      await updateSettings(newRoute)
      setLearningRoute(newRoute)
    } catch (err) {
      setError(err.message)
    } finally {
      setSwitchingRoute(false)
    }
  }

  function handleLogout() {
    localStorage.removeItem('token')
    navigate('/login')
  }

  function handleStartSession() {
    navigate('/session')
  }

  if (loading) {
    return (
      <div className="page dashboard-page">
        <p className="loading-text">Dashboard laden...</p>
      </div>
    )
  }

  const domains = overview?.domains || {}
  const totalMastered = overview?.mastered || 0
  const totalNodes = overview?.total_nodes || 0
  const streak = overview?.streak_days || 0
  const totalPct = totalNodes > 0 ? Math.round((totalMastered / totalNodes) * 100) : 0

  return (
    <div className="page dashboard-page">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <button className="btn-link" onClick={handleLogout}>Uitloggen</button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {bijspijker && (
        <div className="bijspijker-widget">
          {bijspijker.is_bij ? (
            <p className="bijspijker-headline">
              Je bent bij! Je beheerst alles tot je huidige hoofdstuk. 🎉
            </p>
          ) : (
            <p className="bijspijker-headline">
              Nog <strong>{bijspijker.diagnose_size}</strong> onderdelen tot je bij bent
              {bijspijker.hoofdstuk_grc ? ` met hoofdstuk ${bijspijker.hoofdstuk_grc}` : ''}
              {bijspijker.hoofdstuk_lat ? ` (Latijn h${bijspijker.hoofdstuk_lat})` : ''}.
            </p>
          )}
          <p className="bijspijker-eta">
            {Math.round(bijspijker.fractie_bij * 100)}% groen
            {!bijspijker.is_bij && ` · nog ± ${bijspijker.eta_dagen} dagen bij 30 min/dag`}
          </p>
          {bijspijker.suggest_chapter_bump && (
            <button
              className="btn btn-secondary"
              disabled={bumping}
              onClick={handleBumpChapter}
            >
              {bumping ? 'Bezig...' : 'Update mijn hoofdstuk (klas is verder)'}
            </button>
          )}
        </div>
      )}

      <div className="dashboard-stats">
        <div className="stat-card">
          <span className="stat-number">{totalPct}%</span>
          <span className="stat-label">Beheerst</span>
        </div>
        <div className="stat-card">
          <span className="stat-number">{totalMastered}</span>
          <span className="stat-label">van {totalNodes} knopen</span>
        </div>
        <div className="stat-card">
          <span className="stat-number">{streak}</span>
          <span className="stat-label">{streak === 1 ? 'dag' : 'dagen'} streak</span>
        </div>
      </div>

      <div className="card dashboard-domains">
        <h2>Voortgang per domein</h2>
        {Object.entries(domains).length > 0 ? (
          Object.entries(domains).map(([domain, { mastered, total }]) => (
            <DomainBar
              key={domain}
              domain={domain}
              mastered={mastered}
              total={total}
            />
          ))
        ) : (
          <p className="text-muted">Nog geen voortgang. Start je eerste sessie!</p>
        )}
      </div>

      {clusters.some(c => c.total > 0) && (
        <div className="card dashboard-clusters">
          <h2>Vocabulaire per thema</h2>
          {clusters
            .filter(c => c.total > 0)
            .map(c => (
              <ClusterBar
                key={c.label}
                label={c.label}
                beschrijving={c.beschrijving}
                mastered={c.mastered}
                total={c.total}
                masteredPct={c.mastered_pct}
              />
            ))}
        </div>
      )}

      {learningRoute && (
        <div className="card dashboard-settings">
          <h2>Leerroute</h2>
          <div className="route-current">
            Huidige route: <strong>{ROUTE_LABELS[learningRoute] || learningRoute}</strong>
          </div>
          <button
            className="btn btn-secondary"
            onClick={handleToggleRoute}
            disabled={switchingRoute}
            style={{ width: '100%' }}
          >
            {switchingRoute
              ? 'Wijzigen...'
              : `Wissel naar ${ROUTE_LABELS[learningRoute === 'grammar_first' ? 'context_first' : 'grammar_first']}`
            }
          </button>
        </div>
      )}

      <div className="dashboard-actions">
        <button className="btn btn-primary" onClick={handleStartSession}>
          Start sessie
        </button>
        <button className="btn btn-secondary" onClick={() => navigate('/graph')}>
          Bekijk knowledge graph
        </button>
        <button className="btn btn-secondary" onClick={() => navigate('/route-select')}>
          Leerroute instellen
        </button>
      </div>
    </div>
  )
}
