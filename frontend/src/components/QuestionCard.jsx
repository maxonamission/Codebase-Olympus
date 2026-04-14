export default function QuestionCard({ question }) {
  const { titel, beschrijving, stimulus } = question

  return (
    <div className="card question-card">
      <h2 className="question-title">{titel}</h2>
      {beschrijving && (
        <p className="question-description">{beschrijving}</p>
      )}
      <div className="question-stimulus">
        {typeof stimulus === 'string' ? (
          <p>{stimulus}</p>
        ) : (
          <p>{stimulus?.text || JSON.stringify(stimulus)}</p>
        )}
      </div>
    </div>
  )
}
