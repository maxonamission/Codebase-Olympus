/**
 * MentorAttemptList — toont de laatste letterlijke antwoorden van een
 * leerling op één knoop (F2-02).  Per poging een visuele diff tussen wat
 * de leerling inttypte en het juiste antwoord, zodat een mentor concreet
 * kan coachen ("je typte `puellae` i.p.v. `puellam`").
 *
 * Presentational: krijgt de al-opgehaalde attempts als prop.  De
 * data-fetch (api.getMentorAttempts) hoort thuis in de parent-pagina.
 */
import { diffParts } from './mentorDiff'

function formatTimestamp(iso) {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return iso
  return d.toLocaleString('nl-NL', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export default function MentorAttemptList({ attempts, title }) {
  if (!attempts || attempts.length === 0) {
    return (
      <div className="mentor-attempts mentor-attempts--empty">
        <p>Nog geen letterlijke antwoorden op deze knoop.</p>
      </div>
    )
  }

  return (
    <div className="mentor-attempts">
      {title && <h3 className="mentor-attempts-title">{title}</h3>}
      <ul className="mentor-attempts-list">
        {attempts.map((a, i) => (
          <li
            key={`${a.item_id}-${a.timestamp}-${i}`}
            className={`mentor-attempt ${a.correct ? 'is-correct' : 'is-wrong'}`}
          >
            <span className="mentor-attempt-badge" aria-label={a.correct ? 'goed' : 'fout'}>
              {a.correct ? '✓' : '✗'}
            </span>
            <span className="mentor-attempt-answer">
              {a.correct
                ? a.answer_text
                : diffParts(a.answer_text, a.correct_answer || '').map((part, j) =>
                    part.changed ? (
                      <mark key={j} className="diff-wrong">
                        {part.text}
                      </mark>
                    ) : (
                      <span key={j}>{part.text}</span>
                    ),
                  )}
            </span>
            {!a.correct && a.correct_answer && (
              <span className="mentor-attempt-expected">
                correct: <strong>{a.correct_answer}</strong>
              </span>
            )}
            <span className="mentor-attempt-meta">{formatTimestamp(a.timestamp)}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
