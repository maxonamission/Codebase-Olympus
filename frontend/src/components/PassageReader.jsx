import { useState, useRef, useEffect } from 'react'

/**
 * PassageReader — displays a Latin/Greek passage with per-word annotations.
 *
 * Props:
 *   passage     — { id, taal, titel, tekst, annotaties, knoop_ids, moeilijkheid }
 *   masteredIds — Set<string> of mastered knoop IDs (for highlighting unknown grammar)
 *   onKnoopClick — optional callback(knoopId) when user clicks "Bekijk grammatica"
 */
export default function PassageReader({ passage, masteredIds = new Set(), onKnoopClick }) {
  const [activeWord, setActiveWord] = useState(null)
  const popupRef = useRef(null)

  // Close popup on outside click
  useEffect(() => {
    function handleClickOutside(e) {
      if (popupRef.current && !popupRef.current.contains(e.target)) {
        setActiveWord(null)
      }
    }
    if (activeWord !== null) {
      document.addEventListener('mousedown', handleClickOutside)
    }
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [activeWord])

  if (!passage) return null

  // Build a lookup from surface form → annotation (by position)
  const words = passage.tekst.split(/(\s+)/)

  // Match words to annotations in order
  let annotationIndex = 0
  const tokens = words.map((token, i) => {
    if (/^\s+$/.test(token)) {
      return { type: 'space', text: token, key: `s-${i}` }
    }

    // Strip punctuation to match annotation woord
    const cleaned = token.replace(/[.,;:!?()[\]"'—–-]+$/g, '').replace(/^[.,;:!?()[\]"'—–-]+/g, '')
    const trailing = token.slice(cleaned.length)
    const leading = token.slice(0, token.length - cleaned.length - trailing.length)

    let annotation = null
    if (annotationIndex < passage.annotaties.length) {
      const candidate = passage.annotaties[annotationIndex]
      if (candidate.woord.toLowerCase() === cleaned.toLowerCase()) {
        annotation = candidate
        annotationIndex++
      }
    }

    // Determine if grammar is unknown: check if any linked knoop is NOT mastered
    const isUnknown = annotation && passage.knoop_ids
      ? passage.knoop_ids.some(kid => !masteredIds.has(kid))
      : false

    return {
      type: 'word',
      text: cleaned,
      leading,
      trailing,
      annotation,
      isUnknown,
      index: i,
      key: `w-${i}`,
    }
  })

  function handleWordClick(token) {
    if (token.annotation) {
      setActiveWord(activeWord === token.index ? null : token.index)
    }
  }

  return (
    <div className="passage-reader">
      <div className="passage-header">
        <h3 className="passage-title">{passage.titel}</h3>
        <span className="passage-difficulty">
          {'*'.repeat(passage.moeilijkheid)}{'*'.repeat(0)}
          <span className="passage-difficulty-label"> niveau {passage.moeilijkheid}</span>
        </span>
      </div>

      <div className="passage-text">
        {tokens.map(token => {
          if (token.type === 'space') {
            return <span key={token.key}>{token.text}</span>
          }

          const classes = ['passage-word']
          if (token.annotation) classes.push('passage-word--annotated')
          if (token.isUnknown) classes.push('passage-word--unknown')
          if (activeWord === token.index) classes.push('passage-word--active')

          return (
            <span key={token.key} className="passage-word-wrapper">
              {token.leading}
              <span
                className={classes.join(' ')}
                onClick={() => handleWordClick(token)}
                title={token.annotation
                  ? `${token.annotation.lemma} — ${token.annotation.vertaling}`
                  : undefined
                }
              >
                {token.text}
              </span>
              {token.trailing}

              {activeWord === token.index && token.annotation && (
                <span className="passage-popup" ref={popupRef}>
                  <span className="passage-popup-row">
                    <strong>Lemma:</strong> {token.annotation.lemma}
                  </span>
                  {token.annotation.naamval && (
                    <span className="passage-popup-row">
                      <strong>Vorm:</strong> {token.annotation.naamval}
                    </span>
                  )}
                  <span className="passage-popup-row">
                    <strong>Vertaling:</strong> {token.annotation.vertaling}
                  </span>
                  {onKnoopClick && passage.knoop_ids && passage.knoop_ids.length > 0 && (
                    <button
                      className="passage-popup-link"
                      onClick={(e) => {
                        e.stopPropagation()
                        onKnoopClick(passage.knoop_ids[0])
                      }}
                    >
                      Bekijk grammatica
                    </button>
                  )}
                </span>
              )}
            </span>
          )
        })}
      </div>
    </div>
  )
}
