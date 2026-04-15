const FEEDBACK_MESSAGES = {
  correct: {
    icon: '\u2713',
    label: 'Goed!',
    className: 'feedback-correct',
  },
  slow_correct: {
    icon: '\u2713',
    label: 'Correct, maar oefen dit nog.',
    className: 'feedback-slow',
  },
  incorrect: {
    icon: '\u2717',
    label: 'Helaas, dat is niet juist.',
    className: 'feedback-incorrect',
  },
}

export default function FeedbackCard({ feedback }) {
  const { response_type, correct_answer, explanation, mastery_before, mastery_after } = feedback

  const msg = FEEDBACK_MESSAGES[response_type] || FEEDBACK_MESSAGES[feedback.correct ? 'correct' : 'incorrect']

  return (
    <div className={`card feedback-card ${msg.className}`}>
      <div className="feedback-header">
        <span className="feedback-icon">{msg.icon}</span>
        <span className="feedback-label">{msg.label}</span>
      </div>

      {!feedback.correct && correct_answer && (
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
