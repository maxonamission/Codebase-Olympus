import { useState, useEffect } from 'react'
import { getMentees, getStruikelpunten, getMentorAttempts } from '../api'
import MentorStruikelpunten from '../components/MentorStruikelpunten'
import MentorAttemptList from '../components/MentorAttemptList'

/**
 * MentorView — capstone van Sprint 5 (F1-13).  Brengt de mentor-
 * diagnostiek samen: kies een gekoppelde leerling, bekijk diens
 * struikelpunten (F2-03) en klik door naar de letterlijke pogingen per
 * knoop (F2-02).
 */
export default function MentorView() {
  const [mentees, setMentees] = useState([])
  const [selectedMentee, setSelectedMentee] = useState(null)
  const [struikelpunten, setStruikelpunten] = useState([])
  const [attempts, setAttempts] = useState(null) // { knoop_title, attempts }
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function load() {
      try {
        const data = await getMentees()
        setMentees(data.mentees || [])
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  async function selectMentee(mentee) {
    setSelectedMentee(mentee)
    setAttempts(null)
    setError('')
    try {
      const data = await getStruikelpunten(mentee.user_id)
      setStruikelpunten(data.struikelpunten || [])
    } catch (err) {
      setError(err.message)
    }
  }

  async function selectKnoop(knoopId) {
    if (!selectedMentee) return
    setError('')
    try {
      const data = await getMentorAttempts(selectedMentee.user_id, knoopId)
      setAttempts({ knoop_title: data.knoop_title, attempts: data.attempts })
    } catch (err) {
      setError(err.message)
    }
  }

  if (loading) {
    return <div className="mentor-view">Bezig met laden…</div>
  }

  return (
    <div className="mentor-view">
      <h1>Mentor-overzicht</h1>
      {error && <p className="mentor-view-error">{error}</p>}

      <section className="mentor-view-mentees">
        <h2>Mijn leerlingen</h2>
        {mentees.length === 0 ? (
          <p>Nog geen gekoppelde leerlingen.</p>
        ) : (
          <ul className="mentee-list">
            {mentees.map((m) => (
              <li key={m.user_id}>
                <button
                  type="button"
                  className={
                    selectedMentee && selectedMentee.user_id === m.user_id ? 'is-selected' : ''
                  }
                  onClick={() => selectMentee(m)}
                >
                  {m.email}
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>

      {selectedMentee && (
        <section className="mentor-view-struikelpunten">
          <h2>Struikelpunten — {selectedMentee.email}</h2>
          <MentorStruikelpunten struikelpunten={struikelpunten} onSelect={selectKnoop} />
        </section>
      )}

      {attempts && (
        <section className="mentor-view-attempts">
          <h2>Laatste antwoorden</h2>
          <MentorAttemptList attempts={attempts.attempts} title={attempts.knoop_title} />
        </section>
      )}
    </div>
  )
}
