/**
 * sortStruikelpunten — pure sorteerhulp voor de struikelpunten-tabel
 * (F2-03).  Numerieke kolommen numeriek, tekst/datum lexicaal.  Geeft een
 * nieuwe array terug; muteert de input niet.
 */
const NUMERIC = new Set(['error_rate', 'wrong_attempts', 'total_attempts', 'mastery'])

export function sortStruikelpunten(entries, column, direction = 'desc') {
  const factor = direction === 'asc' ? 1 : -1
  return [...entries].sort((a, b) => {
    const av = a[column]
    const bv = b[column]
    if (NUMERIC.has(column)) {
      return (av - bv) * factor
    }
    return String(av).localeCompare(String(bv)) * factor
  })
}
