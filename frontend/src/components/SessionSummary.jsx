export default function SessionSummary({ summary, onBack }) {
  return (
    <div className="card">
      <h2>Sessie afgerond</h2>
      <p>Samenvatting — wordt uitgewerkt.</p>
      <button className="btn btn-primary" onClick={onBack}>
        Terug naar dashboard
      </button>
    </div>
  )
}
