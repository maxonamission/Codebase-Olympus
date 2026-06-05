import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { startBijspijker } from '../api'

// Methods with a chapter mapping (PoC). Kept in sync with data/methode_mapping.json.
const LAT_METHODS = [
  { value: 'fortuna', label: 'Fortuna' },
  { value: 'spqr', label: 'SPQR' },
]
const GRC_METHODS = [{ value: 'pallas', label: 'Pallas' }]

const MODES = [
  {
    value: 'bijspijker',
    title: 'Ik wil bijblijven met mijn klas',
    description:
      'Geef je schoolmethode en hoofdstuk op. We plannen een versneld inhaalpad ' +
      'richting dat hoofdstuk, zodat je weer bij bent met de klas.',
  },
  {
    value: 'staatsexamen',
    title: 'Ik bereid me voor op een (staats)examen',
    description:
      'We werken op de lange termijn naar beheersing van alle eindtermen toe, ' +
      'in jouw eigen tempo.',
  },
]

export default function BijspijkerSetup() {
  const navigate = useNavigate()
  const [mode, setMode] = useState(null)
  const [methodeLat, setMethodeLat] = useState('')
  const [hoofdstukLat, setHoofdstukLat] = useState('')
  const [methodeGrc, setMethodeGrc] = useState('')
  const [hoofdstukGrc, setHoofdstukGrc] = useState('')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  const hasLat = methodeLat && Number(hoofdstukLat) >= 1
  const hasGrc = methodeGrc && Number(hoofdstukGrc) >= 1

  async function handleConfirm() {
    if (mode === 'staatsexamen') {
      navigate('/route-select?onboarding=1')
      return
    }
    if (!hasLat && !hasGrc) {
      setError('Kies voor minstens één taal een methode én hoofdstuk.')
      return
    }
    setSaving(true)
    setError('')
    try {
      await startBijspijker({
        methodeLat: hasLat ? methodeLat : null,
        hoofdstukLat: hasLat ? Number(hoofdstukLat) : null,
        methodeGrc: hasGrc ? methodeGrc : null,
        hoofdstukGrc: hasGrc ? Number(hoofdstukGrc) : null,
      })
      navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="page bijspijker-setup-page">
      <h1>Hoe wil je leren?</h1>
      <p className="route-select-intro">
        Kies waar je nu naartoe werkt. Je kunt dit later altijd wijzigen.
      </p>

      {error && <div className="error-message">{error}</div>}

      <div className="route-options">
        {MODES.map(m => (
          <button
            key={m.value}
            className={`route-option${mode === m.value ? ' route-option--selected' : ''}`}
            onClick={() => setMode(m.value)}
          >
            <p className="route-option-title">{m.title}</p>
            <p className="route-option-desc">{m.description}</p>
          </button>
        ))}
      </div>

      {mode === 'bijspijker' && (
        <div className="bijspijker-method-form">
          <MethodPicker
            label="Latijn"
            methods={LAT_METHODS}
            methode={methodeLat}
            hoofdstuk={hoofdstukLat}
            onMethode={setMethodeLat}
            onHoofdstuk={setHoofdstukLat}
          />
          <MethodPicker
            label="Grieks"
            methods={GRC_METHODS}
            methode={methodeGrc}
            hoofdstuk={hoofdstukGrc}
            onMethode={setMethodeGrc}
            onHoofdstuk={setHoofdstukGrc}
          />
          <p className="route-option-desc">Vul minstens één taal in.</p>
        </div>
      )}

      <button
        className="btn btn-primary route-confirm-btn"
        disabled={!mode || saving}
        onClick={handleConfirm}
      >
        {saving ? 'Bezig...' : 'Doorgaan'}
      </button>
    </div>
  )
}

function MethodPicker({ label, methods, methode, hoofdstuk, onMethode, onHoofdstuk }) {
  return (
    <div className="method-picker">
      <label className="method-picker-label">{label}</label>
      <select value={methode} onChange={e => onMethode(e.target.value)}>
        <option value="">— geen —</option>
        {methods.map(m => (
          <option key={m.value} value={m.value}>
            {m.label}
          </option>
        ))}
      </select>
      <input
        type="number"
        min="1"
        placeholder="Hoofdstuk"
        value={hoofdstuk}
        onChange={e => onHoofdstuk(e.target.value)}
        disabled={!methode}
      />
    </div>
  )
}
