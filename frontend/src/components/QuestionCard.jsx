export default function QuestionCard({ question, showDescription = true }) {
  const { titel, beschrijving, stimulus } = question

  return (
    <div className="card question-card">
      <h2 className="question-title">{titel}</h2>
      {showDescription && beschrijving && (
        <p className="question-description">{beschrijving}</p>
      )}
      {stimulus && (
        <div className="question-stimulus">
          {typeof stimulus === 'string' ? (
            <p>{stimulus}</p>
          ) : stimulus?.text ? (
            <p>{stimulus.text}</p>
          ) : null}
        </div>
      )}
    </div>
  )
}
