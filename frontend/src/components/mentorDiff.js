/**
 * diffParts — split het leerling-antwoord in segmenten t.o.v. het
 * verwachte antwoord: gedeeld voor-/achterstuk ongewijzigd, het midden
 * gemarkeerd als afwijkend.  Gebruikt door MentorAttemptList (F2-02).
 */
export function diffParts(answer, expected) {
  if (!expected || answer === expected) {
    return [{ text: answer, changed: false }]
  }
  let prefix = 0
  while (prefix < answer.length && prefix < expected.length && answer[prefix] === expected[prefix]) {
    prefix++
  }
  let suffix = 0
  while (
    suffix < answer.length - prefix &&
    suffix < expected.length - prefix &&
    answer[answer.length - 1 - suffix] === expected[expected.length - 1 - suffix]
  ) {
    suffix++
  }
  const parts = []
  if (prefix > 0) parts.push({ text: answer.slice(0, prefix), changed: false })
  const middle = answer.slice(prefix, answer.length - suffix)
  if (middle) parts.push({ text: middle, changed: true })
  if (suffix > 0) parts.push({ text: answer.slice(answer.length - suffix), changed: false })
  return parts.length ? parts : [{ text: answer, changed: false }]
}
