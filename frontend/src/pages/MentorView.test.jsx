import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import MentorView from './MentorView'
import * as api from '../api'

vi.mock('../api')

const MENTEES = [
  { user_id: 'u1', email: 'leerling1@school.nl' },
  { user_id: 'u2', email: 'leerling2@school.nl' },
]

const STRUIKELPUNTEN = [
  {
    knoop_id: 'LAT-G-MORF-NAAMVAL-INTRO',
    knoop_title: 'Naamvallen',
    total_attempts: 4,
    wrong_attempts: 3,
    error_rate: 0.75,
    last_attempt: '2026-06-03T12:00:00',
    mastery: 0.2,
  },
]

const ATTEMPTS = {
  knoop_title: 'Naamvallen',
  attempts: [
    {
      item_id: 'I1',
      timestamp: '2026-06-03T12:00:00',
      answer_text: 'puellae',
      correct_answer: 'puellam',
      correct: false,
      response_time_ms: 4000,
      item_type: 'production',
    },
  ],
}

beforeEach(() => {
  vi.clearAllMocks()
  api.getMentees.mockResolvedValue({ mentees: MENTEES })
  api.getStruikelpunten.mockResolvedValue({ struikelpunten: STRUIKELPUNTEN })
  api.getMentorAttempts.mockResolvedValue(ATTEMPTS)
})

describe('MentorView', () => {
  it('lists the mentees after loading', async () => {
    render(<MentorView />)
    expect(await screen.findByText('leerling1@school.nl')).toBeTruthy()
    expect(screen.getByText('leerling2@school.nl')).toBeTruthy()
  })

  it('loads struikelpunten when a mentee is selected', async () => {
    render(<MentorView />)
    fireEvent.click(await screen.findByText('leerling1@school.nl'))
    expect(await screen.findByText('Naamvallen')).toBeTruthy()
    expect(api.getStruikelpunten).toHaveBeenCalledWith('u1')
  })

  it('loads attempts when a struikelpunt row is clicked', async () => {
    render(<MentorView />)
    fireEvent.click(await screen.findByText('leerling1@school.nl'))
    fireEvent.click((await screen.findByText('Naamvallen')).closest('tr'))
    await waitFor(() =>
      expect(api.getMentorAttempts).toHaveBeenCalledWith('u1', 'LAT-G-MORF-NAAMVAL-INTRO'),
    )
    // The wrong answer's diff mark surfaces in the attempt list
    await screen.findByText('puellam')
  })

  it('shows an empty state when there are no mentees', async () => {
    api.getMentees.mockResolvedValue({ mentees: [] })
    render(<MentorView />)
    expect(await screen.findByText(/nog geen gekoppelde leerlingen/i)).toBeTruthy()
  })

  it('surfaces an error from the mentees call', async () => {
    api.getMentees.mockRejectedValue(new Error('403 verboden'))
    render(<MentorView />)
    expect(await screen.findByText('403 verboden')).toBeTruthy()
  })
})
