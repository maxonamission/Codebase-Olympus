import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { startSession, submitAnswer, getSessionSummary } from '../api'
import PhaseIndicator from '../components/PhaseIndicator'
import ProgressBar from '../components/ProgressBar'
import QuestionCard from '../components/QuestionCard'
import AnswerInput from '../components/AnswerInput'
import FeedbackCard from '../components/FeedbackCard'
import SessionSummary from '../components/SessionSummary'

export default function Session() {
  const navigate = useNavigate()
  const [sessionId, setSessionId] = useState(null)
  const [question, setQuestion] = useState(null)
  const [feedback, setFeedback] = useState(null)
  const [summary, setSummary] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [progress, setProgress] = useState({ current: 0, total: 0 })
  const questionStartTime = useRef(Date.now())

  useEffect(() => {
    async function init() {
      try {
        const data = await startSession()
        setSessionId(data.session_id)
        setQuestion(data.question)
        setProgress({ current: 1, total: data.estimated_total || 20 })
        questionStartTime.current = Date.now()
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    init()
  }, [])

  async function handleAnswer(responseType, answer) {
    setSubmitting(true)
    setError('')
    const responseTimeMs = Date.now() - questionStartTime.current

    try {
      const data = await submitAnswer(sessionId, {
        responseType,
        responseTimeMs,
        answer,
      })

      setFeedback(data.feedback)

      if (data.session_ended) {
        const summaryData = await getSessionSummary(sessionId)
        setSummary(summaryData)
      } else {
        setQuestion(data.next_question)
        setProgress((prev) => ({
          ...prev,
          current: prev.current + 1,
          total: data.estimated_total || prev.total,
        }))
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  function handleNext() {
    setFeedback(null)
    questionStartTime.current = Date.now()
  }

  if (loading) {
    return (
      <div className="page session-page">
        <p className="loading-text">Sessie wordt gestart...</p>
      </div>
    )
  }

  if (error && !question) {
    return (
      <div className="page session-page">
        <div className="error-message">{error}</div>
        <button className="btn btn-primary" onClick={() => navigate('/dashboard')}>
          Terug naar dashboard
        </button>
      </div>
    )
  }

  if (summary) {
    return (
      <div className="page session-page">
        <SessionSummary summary={summary} onBack={() => navigate('/dashboard')} />
      </div>
    )
  }

  return (
    <div className="page session-page">
      {question && (
        <>
          <PhaseIndicator currentPhase={question.phase} />
          <ProgressBar current={progress.current} total={progress.total} />

          {error && <div className="error-message">{error}</div>}

          <QuestionCard question={question} />

          {feedback ? (
            <>
              <FeedbackCard feedback={feedback} />
              <button className="btn btn-primary" onClick={handleNext}>
                Volgende
              </button>
            </>
          ) : (
            <AnswerInput
              question={question}
              onAnswer={handleAnswer}
              disabled={submitting}
            />
          )}
        </>
      )}
    </div>
  )
}
