const PHASES = {
  warmup: {
    label: 'Opwarming',
    description: 'Snelle herhaling van eerder geleerde stof',
  },
  new_material: {
    label: 'Nieuwe stof',
    description: 'Introductie van nieuwe leerstof',
  },
  deepening: {
    label: 'Verdieping',
    description: 'Oefeningen die nieuw en oud combineren',
  },
  cooldown: {
    label: 'Afkoeling',
    description: 'Herhaling voor langetermijngeheugen',
  },
}

const PHASE_ORDER = ['warmup', 'new_material', 'deepening', 'cooldown']

export default function PhaseIndicator({ currentPhase }) {
  const current = PHASES[currentPhase]

  return (
    <div className="phase-indicator">
      <div className="phase-steps">
        {PHASE_ORDER.map((phase) => (
          <div
            key={phase}
            className={`phase-step${phase === currentPhase ? ' phase-active' : ''}`}
          >
            {PHASES[phase].label}
          </div>
        ))}
      </div>
      {current && (
        <p className="phase-description">{current.description}</p>
      )}
    </div>
  )
}
