import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent, within } from '@testing-library/react'
import MentorStruikelpunten from './MentorStruikelpunten'
import { sortStruikelpunten } from './struikelpuntSort'

const ENTRIES = [
  {
    knoop_id: 'A',
    knoop_title: 'Alfa',
    total_attempts: 4,
    wrong_attempts: 1,
    error_rate: 0.25,
    last_attempt: '2026-06-01T12:00:00',
    mastery: 0.8,
  },
  {
    knoop_id: 'B',
    knoop_title: 'Beta',
    total_attempts: 4,
    wrong_attempts: 3,
    error_rate: 0.75,
    last_attempt: '2026-06-03T12:00:00',
    mastery: 0.2,
  },
]

describe('sortStruikelpunten', () => {
  it('sorts numeric column descending without mutating input', () => {
    const copy = [...ENTRIES]
    const sorted = sortStruikelpunten(ENTRIES, 'error_rate', 'desc')
    expect(sorted.map((e) => e.knoop_id)).toEqual(['B', 'A'])
    expect(ENTRIES).toEqual(copy) // not mutated
  })

  it('sorts numeric column ascending', () => {
    const sorted = sortStruikelpunten(ENTRIES, 'wrong_attempts', 'asc')
    expect(sorted.map((e) => e.knoop_id)).toEqual(['A', 'B'])
  })

  it('sorts a text column lexically', () => {
    const sorted = sortStruikelpunten(ENTRIES, 'knoop_title', 'asc')
    expect(sorted.map((e) => e.knoop_title)).toEqual(['Alfa', 'Beta'])
  })
})

describe('MentorStruikelpunten', () => {
  it('shows an empty state', () => {
    render(<MentorStruikelpunten struikelpunten={[]} />)
    expect(screen.getByText(/geen struikelpunten/i)).toBeTruthy()
  })

  it('renders a row per node with formatted percentages', () => {
    render(<MentorStruikelpunten struikelpunten={ENTRIES} />)
    expect(screen.getByText('Alfa')).toBeTruthy()
    expect(screen.getByText('75%')).toBeTruthy() // error_rate of Beta
    expect(screen.getByText('3/4')).toBeTruthy() // wrong/total of Beta
  })

  it('calls onSelect with the knoop_id when a row is clicked', () => {
    const onSelect = vi.fn()
    render(<MentorStruikelpunten struikelpunten={ENTRIES} onSelect={onSelect} />)
    fireEvent.click(screen.getByText('Beta').closest('tr'))
    expect(onSelect).toHaveBeenCalledWith('B')
  })

  it('re-sorts when a column header is clicked', () => {
    render(<MentorStruikelpunten struikelpunten={ENTRIES} />)
    // Default sort is last_attempt desc → Beta (Jun 3) first
    let rows = screen.getAllByRole('row').slice(1) // skip header
    expect(within(rows[0]).getByText('Beta')).toBeTruthy()
    // Sort by mastery desc → Alfa (0.8) first
    fireEvent.click(screen.getByRole('button', { name: /mastery/i }))
    rows = screen.getAllByRole('row').slice(1)
    expect(within(rows[0]).getByText('Alfa')).toBeTruthy()
  })
})
