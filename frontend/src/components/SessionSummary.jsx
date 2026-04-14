export default function SessionSummary({ summary, onBack }) {
  const {
    items_count,
    nodes_introduced = [],
    nodes_reviewed = [],
    mastery_changes = {},
  } = summary

  const changes = Object.entries(mastery_changes)
  const improved = changes.filter(([, [before, after]]) => after > before)
  const declined = changes.filter(([, [before, after]]) => after < before)

  return (
    <div className="session-summary">
      <h2>Sessie afgerond</h2>

      <div className="summary-stats">
        <div className="stat-card">
          <span className="stat-number">{items_count ?? changes.length}</span>
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

      {changes.length > 0 && (
        <div className="card summary-mastery-card">
          <h3>Beheersingsveranderingen</h3>
          <div className="mastery-list">
            {changes.map(([knoopId, [before, after]]) => {
              const diff = after - before
              let diffClass = 'mastery-neutral'
              if (diff > 0) diffClass = 'mastery-up'
              else if (diff < 0) diffClass = 'mastery-down'

              return (
                <div key={knoopId} className="mastery-row">
                  <span className="mastery-knoop-id">{knoopId}</span>
                  <span className="mastery-change">
                    <span>{Math.round(before * 100)}%</span>
                    <span className="mastery-arrow">{'\u2192'}</span>
                    <span className={diffClass}>{Math.round(after * 100)}%</span>
                  </span>
                </div>
              )
            })}
          </div>

          {(improved.length > 0 || declined.length > 0) && (
            <div className="mastery-totals">
              {improved.length > 0 && (
                <span className="mastery-up">{improved.length} verbeterd</span>
              )}
              {declined.length > 0 && (
                <span className="mastery-down">{declined.length} gedaald</span>
              )}
            </div>
          )}
        </div>
      )}

      <button className="btn btn-primary" onClick={onBack}>
        Terug naar dashboard
      </button>
    </div>
  )
}
