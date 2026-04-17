import { useState } from 'react'
import AudioPlayer from './AudioPlayer'
import GreekInput from './GreekInput'

const MC_TYPES = ['herkenning', 'luister_herkenning']
const TEXT_TYPES = ['productie', 'luister_productie']

export default function AnswerInput({ question, onAnswer, disabled }) {
  const [textAnswer, setTextAnswer] = useState('')
  const [showAnswer, setShowAnswer] = useState(false)

  const itemType = question.item_type
  const isMultipleChoice = MC_TYPES.includes(itemType) && question.options?.length > 0
  const isTextInput = TEXT_TYPES.includes(itemType)
  const isGreek = question.knoop_id?.startsWith('GRC-')
  const audioSrc = question.audio_ref ? `/audio/${question.audio_ref}` : null

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
        {audioSrc && <AudioPlayer src={audioSrc} label="Luister naar de opname" />}
        <p className="answer-instruction">{question.instruction || 'Kies het juiste antwoord:'}</p>
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
        {audioSrc && <AudioPlayer src={audioSrc} label="Luister naar de opname" />}
        {question.instruction && (
          <p className="answer-instruction">{question.instruction}</p>
        )}
        <form onSubmit={handleTextSubmit}>
          <div className="form-group">
            <label htmlFor="answer-text">Jouw antwoord:</label>
            {isGreek ? (
              <GreekInput
                id="answer-text"
                value={textAnswer}
                onChange={setTextAnswer}
                placeholder="Typ je antwoord in het Grieks..."
                disabled={disabled}
              />
            ) : (
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
            )}
            {question.hint && (
              <p className="answer-hint">Hint (Nederlands): <strong>{question.hint}</strong></p>
            )}
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

  // Fallback: self-assessment with reveal step
  if (!showAnswer) {
    return (
      <div className="answer-input">
        <p className="answer-instruction">Denk na over het antwoord en klik dan op &quot;Toon antwoord&quot;.</p>
        <button
          className="btn btn-primary"
          onClick={() => setShowAnswer(true)}
          disabled={disabled}
        >
          Toon antwoord
        </button>
      </div>
    )
  }

  return (
    <div className="answer-input">
      <div className="model-answer">
        <p className="answer-label">Antwoord:</p>
        <p className="answer-text">{question.beschrijving}</p>
      </div>
      <p className="answer-instruction">Hoe goed kwam jouw antwoord overeen?</p>
      <div className="self-assess-options">
        <button
          className="btn self-assess self-assess-correct"
          onClick={() => { handleSelfAssess('correct'); setShowAnswer(false); }}
          disabled={disabled}
        >
          Goed — ik wist het
        </button>
        <button
          className="btn self-assess self-assess-slow"
          onClick={() => { handleSelfAssess('slow_correct'); setShowAnswer(false); }}
          disabled={disabled}
        >
          Twijfel — ik moest nadenken
        </button>
        <button
          className="btn self-assess self-assess-incorrect"
          onClick={() => { handleSelfAssess('incorrect'); setShowAnswer(false); }}
          disabled={disabled}
        >
          Fout — ik wist het niet
        </button>
      </div>
    </div>
  )
}
