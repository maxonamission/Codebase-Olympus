import { useState } from 'react'

const MC_TYPES = ['herkenning', 'luister_herkenning']
const TEXT_TYPES = ['productie', 'luister_productie']

export default function AnswerInput({ question, onAnswer, disabled }) {
  const [textAnswer, setTextAnswer] = useState('')

  const itemType = question.item_type
  const isMultipleChoice = MC_TYPES.includes(itemType) && question.options?.length > 0
  const isTextInput = TEXT_TYPES.includes(itemType)

  function handleMcSelect(option) {
    if (disabled) return
    onAnswer('selected', option)
  }

  function handleTextSubmit(e) {
    e.preventDefault()
    if (disabled || !textAnswer.trim()) return
    onAnswer('typed', textAnswer.trim())
    setTextAnswer('')
  }

  function handleSelfAssess(responseType) {
    if (disabled) return
    onAnswer(responseType, null)
  }

  if (isMultipleChoice) {
    return (
      <div className="answer-input">
        <p className="answer-instruction">Kies het juiste antwoord:</p>
        <div className="mc-options">
          {question.options.map((option, i) => (
            <button
              key={i}
              className="btn mc-option"
              onClick={() => handleMcSelect(option)}
              disabled={disabled}
            >
              {option}
            </button>
          ))}
        </div>
      </div>
    )
  }

  if (isTextInput) {
    return (
      <div className="answer-input">
        <form onSubmit={handleTextSubmit}>
          <div className="form-group">
            <label htmlFor="answer-text">Jouw antwoord:</label>
            <input
              id="answer-text"
              type="text"
              value={textAnswer}
              onChange={(e) => setTextAnswer(e.target.value)}
              placeholder="Typ je antwoord..."
              disabled={disabled}
              autoFocus
              autoComplete="off"
            />
          </div>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={disabled || !textAnswer.trim()}
          >
            {disabled ? 'Bezig...' : 'Controleer'}
          </button>
        </form>
      </div>
    )
  }

  // Fallback: self-assessment for all other types
  return (
    <div className="answer-input">
      <p className="answer-instruction">Hoe ging het?</p>
      <div className="self-assess-options">
        <button
          className="btn self-assess self-assess-correct"
          onClick={() => handleSelfAssess('correct')}
          disabled={disabled}
        >
          Goed
        </button>
        <button
          className="btn self-assess self-assess-slow"
          onClick={() => handleSelfAssess('slow_correct')}
          disabled={disabled}
        >
          Te langzaam
        </button>
        <button
          className="btn self-assess self-assess-incorrect"
          onClick={() => handleSelfAssess('incorrect')}
          disabled={disabled}
        >
          Fout
        </button>
      </div>
    </div>
  )
}
