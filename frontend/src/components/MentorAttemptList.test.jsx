import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import MentorAttemptList from './MentorAttemptList'
import { diffParts } from './mentorDiff'

describe('diffParts', () => {
  it('marks only the differing middle', () => {
    const parts = diffParts('puellae', 'puellam')
    expect(parts).toEqual([
      { text: 'puella', changed: false },
      { text: 'e', changed: true },
    ])
  })

  it('returns the whole answer unchanged when equal', () => {
    expect(diffParts('sum', 'sum')).toEqual([{ text: 'sum', changed: false }])
  })

  it('handles a missing expected answer gracefully', () => {
    expect(diffParts('amo', '')).toEqual([{ text: 'amo', changed: false }])
  })

  it('captures a differing prefix and shared suffix', () => {
    const parts = diffParts('xanus', 'manus')
    expect(parts[0]).toEqual({ text: 'x', changed: true })
    expect(parts[parts.length - 1]).toEqual({ text: 'anus', changed: false })
  })
})

describe('MentorAttemptList', () => {
  const wrong = {
    item_id: 'I1',
    timestamp: '2026-06-01T12:00:00',
    answer_text: 'puellae',
    correct_answer: 'puellam',
    correct: false,
    response_time_ms: 4000,
    item_type: 'production',
  }

  it('shows an empty state without attempts', () => {
    render(<MentorAttemptList attempts={[]} />)
    expect(screen.getByText(/nog geen letterlijke antwoorden/i)).toBeTruthy()
  })

  it('renders the title when provided', () => {
    render(<MentorAttemptList attempts={[wrong]} title="Naamval-intro" />)
    expect(screen.getByText('Naamval-intro')).toBeTruthy()
  })

  it('highlights the wrong part of an incorrect answer', () => {
    const { container } = render(<MentorAttemptList attempts={[wrong]} />)
    const mark = container.querySelector('mark.diff-wrong')
    expect(mark).not.toBeNull()
    expect(mark.textContent).toBe('e')
  })

  it('shows the correct answer for a wrong attempt', () => {
    render(<MentorAttemptList attempts={[wrong]} />)
    expect(screen.getByText('puellam')).toBeTruthy()
  })

  it('renders a correct attempt without a diff mark', () => {
    const right = { ...wrong, answer_text: 'puellam', correct: true }
    const { container } = render(<MentorAttemptList attempts={[right]} />)
    expect(container.querySelector('mark.diff-wrong')).toBeNull()
  })
})
