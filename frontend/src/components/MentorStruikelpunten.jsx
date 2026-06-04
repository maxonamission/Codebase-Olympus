/**
 * MentorStruikelpunten — sorteerbare tabel met de probleemknopen van één
 * leerling (F2-03).  Per knoop: foutpercentage, aantal foute pogingen,
 * recency en huidige mastery.  Een rij aanklikken roept onSelect(knoop_id)
 * aan, zodat de parent kan doorlinken naar de F2-02-pogingenweergave.
 *
 * Presentational: krijgt de al-opgehaalde struikelpunten als prop.
 */
import { useState } from 'react'
import { sortStruikelpunten } from './struikelpuntSort'

const COLUMNS = [
  { key: 'knoop_title', label: 'Knoop', numeric: false },
  { key: 'error_rate', label: 'Fout%', numeric: true },
  { key: 'wrong_attempts', label: 'Fout', numeric: true },
  { key: 'last_attempt', label: 'Laatste fout', numeric: false },
  { key: 'mastery', label: 'Mastery', numeric: true },
]

function formatDate(iso) {
  if (!iso) return '—'
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return iso
  return d.toLocaleDateString('nl-NL', { day: 'numeric', month: 'short' })
}

export default function MentorStruikelpunten({ struikelpunten, onSelect }) {
  const [sortColumn, setSortColumn] = useState('last_attempt')
  const [sortDir, setSortDir] = useState('desc')

  if (!struikelpunten || struikelpunten.length === 0) {
    return (
      <div className="struikelpunten struikelpunten--empty">
        <p>Geen struikelpunten gevonden.</p>
      </div>
    )
  }

  function toggleSort(key) {
    if (key === sortColumn) {
      setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'))
    } else {
      setSortColumn(key)
      setSortDir('desc')
    }
  }

  const rows = sortStruikelpunten(struikelpunten, sortColumn, sortDir)

  return (
    <table className="struikelpunten-table">
      <thead>
        <tr>
          {COLUMNS.map((col) => (
            <th
              key={col.key}
              className={col.numeric ? 'is-numeric' : ''}
              aria-sort={sortColumn === col.key ? (sortDir === 'asc' ? 'ascending' : 'descending') : 'none'}
            >
              <button type="button" onClick={() => toggleSort(col.key)}>
                {col.label}
                {sortColumn === col.key && <span aria-hidden="true">{sortDir === 'asc' ? ' ▲' : ' ▼'}</span>}
              </button>
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((s) => (
          <tr
            key={s.knoop_id}
            className="struikelpunt-row"
            onClick={() => onSelect && onSelect(s.knoop_id)}
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && onSelect) onSelect(s.knoop_id)
            }}
          >
            <td>{s.knoop_title}</td>
            <td className="is-numeric">{Math.round(s.error_rate * 100)}%</td>
            <td className="is-numeric">
              {s.wrong_attempts}/{s.total_attempts}
            </td>
            <td>{formatDate(s.last_attempt)}</td>
            <td className="is-numeric">{Math.round(s.mastery * 100)}%</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
