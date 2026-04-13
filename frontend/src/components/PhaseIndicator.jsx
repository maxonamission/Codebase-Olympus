const PHASE_LABELS = {
  warmup: 'Opwarming',
  new_material: 'Nieuwe stof',
  deepening: 'Verdieping',
  cooldown: 'Afkoeling',
}

const PHASE_ORDER = ['warmup', 'new_material', 'deepening', 'cooldown']

export default function PhaseIndicator({ currentPhase }) {
  return (
    <div className="phase-indicator">
      {PHASE_ORDER.map((phase) => (
        <div
          key={phase}
          className={`phase-step${phase === currentPhase ? ' phase-active' : ''}`}
        >
          {PHASE_LABELS[phase]}
        </div>
      ))}
    </div>
  )
}
