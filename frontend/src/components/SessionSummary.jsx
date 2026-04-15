export default function SessionSummary({ summary, onBack }) {
  const {
    total_items,
    items_count,
    nodes_introduced = [],
    nodes_reviewed = [],
    mastery_changes = {},
  } = summary

  const itemCount = total_items ?? items_count ?? 0

  // mastery_changes can be {id: {before, after}} or {id: [before, after]}
  const changes = Object.entries(mastery_changes).map(([id, val]) => {
    if (Array.isArray(val)) return [id, val[0], val[1]]
    if (val && typeof val === 'object') return [id, val.before, val.after]
    return [id, 0, 0]
  })

  const improved = changes.filter(([, before, after]) => after > before)
  const declined = changes.filter(([, before, after]) => after < before)

  return (
    <div className="session-summary">
      <h2>Sessie afgerond!</h2>

      <div className="summary-stats">
        <div className="stat-card">
          <span className="stat-number">{itemCount || changes.length}</span>
          <span className="stat-label">Vragen beantwoord</span>
        </div>
        <div className="stat-card">
          <span className="stat-number">{nodes_introduced.length}</span>
          <span className="stat-label">Nieuwe knopen</span>
        </div>
        <div className="stat-card">
          <span className="stat-number">{nodes_reviewed.length}</span>
          <span className="stat-label">Herhaald</span>
        </div>
      </div>

      {improved.length > 0 && (
        <div className="card summary-mastery-card">
          <h3>Verbeterd ({improved.length})</h3>
          <div className="mastery-list">
            {improved.map(([knoopId, before, after]) => (
              <div key={knoopId} className="mastery-row">
                <span className="mastery-knoop-id">{knoopId}</span>
                <span className="mastery-change">
                  <span>{Math.round(before * 100)}%</span>
                  <span className="mastery-arrow">{'\u2192'}</span>
                  <span className="mastery-up">{Math.round(after * 100)}%</span>
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {declined.length > 0 && (
        <div className="card summary-mastery-card">
          <h3>Aandachtspunten ({declined.length})</h3>
          <div className="mastery-list">
            {declined.map(([knoopId, before, after]) => (
              <div key={knoopId} className="mastery-row">
                <span className="mastery-knoop-id">{knoopId}</span>
                <span className="mastery-change">
                  <span>{Math.round(before * 100)}%</span>
                  <span className="mastery-arrow">{'\u2192'}</span>
                  <span className="mastery-down">{Math.round(after * 100)}%</span>
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {changes.length === 0 && (
        <p className="summary-empty">Geen beheersingsveranderingen in deze sessie.</p>
      )}

      <button className="btn btn-primary" onClick={onBack}>
        Terug naar dashboard
      </button>
    </div>
  )
}
