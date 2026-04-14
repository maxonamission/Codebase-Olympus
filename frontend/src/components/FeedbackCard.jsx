export default function FeedbackCard({ feedback }) {
  const { correct, explanation, correct_answer, mastery_before, mastery_after } = feedback

  return (
    <div className={`card feedback-card ${correct ? 'feedback-correct' : 'feedback-incorrect'}`}>
      <div className="feedback-header">
        <span className="feedback-icon">{correct ? '\u2713' : '\u2717'}</span>
        <span className="feedback-label">
          {correct ? 'Goed!' : 'Helaas, dat is niet juist.'}
        </span>
      </div>

      {!correct && correct_answer && (
        <p className="feedback-answer">
          <strong>Juiste antwoord:</strong> {correct_answer}
        </p>
      )}

      {explanation && (
        <p className="feedback-explanation">{explanation}</p>
      )}

      {mastery_before != null && mastery_after != null && (
        <div className="feedback-mastery">
          <span className="mastery-label">Beheersing:</span>
          <span className="mastery-value">
            {Math.round(mastery_before * 100)}%
          </span>
          <span className="mastery-arrow">{'\u2192'}</span>
          <span className={`mastery-value ${mastery_after > mastery_before ? 'mastery-up' : 'mastery-down'}`}>
            {Math.round(mastery_after * 100)}%
          </span>
        </div>
      )}
    </div>
  )
}
