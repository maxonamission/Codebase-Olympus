import { useState, useRef, useCallback } from 'react'

// Greek lowercase letters (keyboard layout order)
const LETTERS_LOWER = [
  [';', 'ς', 'ε', 'ρ', 'τ', 'υ', 'θ', 'ι', 'ο', 'π'],
  ['α', 'σ', 'δ', 'φ', 'γ', 'η', 'ξ', 'κ', 'λ'],
  ['ζ', 'χ', 'ψ', 'ω', 'β', 'ν', 'μ'],
]

const LETTERS_UPPER = [
  [':', 'Σ', 'Ε', 'Ρ', 'Τ', 'Υ', 'Θ', 'Ι', 'Ο', 'Π'],
  ['Α', 'Σ', 'Δ', 'Φ', 'Γ', 'Η', 'Ξ', 'Κ', 'Λ'],
  ['Ζ', 'Χ', 'Ψ', 'Ω', 'Β', 'Ν', 'Μ'],
]

// Combining diacritical marks (Unicode combining characters)
const DIACRITICS = [
  { label: '\u1FFE', mark: '\u0314', name: 'dasia (rough)' },       // ῾  → combining reversed comma above
  { label: '\u1FBF', mark: '\u0313', name: 'psili (smooth)' },      // ᾿  → combining comma above
  { label: '\u00B4', mark: '\u0301', name: 'oxia (acute)' },        // ´  → combining acute
  { label: '\u0060', mark: '\u0300', name: 'varia (grave)' },       // `  → combining grave
  { label: '\u1FC0', mark: '\u0342', name: 'perispomeni (circumflex)' }, // ῀ → combining Greek perispomeni
  { label: '\u037A', mark: '\u0345', name: 'iota subscript' },      // ͅ  → combining Greek ypogegrammeni
]

function normalizeNFC(text) {
  // NFC normalization: combines base char + combining marks into precomposed chars
  return text.normalize('NFC')
}

export default function GreekInput({ value, onChange, placeholder, disabled, id }) {
  const [showKeyboard, setShowKeyboard] = useState(false)
  const [uppercase, setUppercase] = useState(false)
  const inputRef = useRef(null)

  const insertAtCursor = useCallback((char) => {
    const input = inputRef.current
    if (!input) return

    const start = input.selectionStart ?? value.length
    const end = input.selectionEnd ?? value.length
    const newValue = value.slice(0, start) + char + value.slice(end)
    onChange(normalizeNFC(newValue))

    // Restore cursor position after React re-render
    requestAnimationFrame(() => {
      const pos = start + char.length
      input.setSelectionRange(pos, pos)
      input.focus()
    })
  }, [value, onChange])

  const applyDiacritic = useCallback((combiningMark) => {
    const input = inputRef.current
    if (!input || value.length === 0) return

    const cursor = input.selectionStart ?? value.length
    if (cursor === 0) return

    // Insert combining mark after the character before cursor, then normalize
    const before = value.slice(0, cursor)
    const after = value.slice(cursor)
    const newValue = before + combiningMark + after
    onChange(normalizeNFC(newValue))

    requestAnimationFrame(() => {
      // Cursor might shift due to NFC normalization (combining → precomposed)
      const normalized = normalizeNFC(newValue)
      const newPos = Math.min(cursor + 1, normalized.length)
      input.setSelectionRange(newPos, newPos)
      input.focus()
    })
  }, [value, onChange])

  function handleBackspace() {
    const input = inputRef.current
    if (!input || value.length === 0) return

    const start = input.selectionStart ?? value.length
    const end = input.selectionEnd ?? value.length

    let newValue
    let newPos
    if (start !== end) {
      // Delete selection
      newValue = value.slice(0, start) + value.slice(end)
      newPos = start
    } else if (start > 0) {
      // Delete one character before cursor (handle multi-codepoint chars via spread)
      const chars = [...value.slice(0, start)]
      chars.pop()
      const prefix = chars.join('')
      newValue = prefix + value.slice(start)
      newPos = prefix.length
    } else {
      return
    }

    onChange(newValue)
    requestAnimationFrame(() => {
      input.setSelectionRange(newPos, newPos)
      input.focus()
    })
  }

  const letters = uppercase ? LETTERS_UPPER : LETTERS_LOWER

  return (
    <div className="greek-input-wrapper">
      <div className="greek-input-field">
        <input
          ref={inputRef}
          id={id}
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          disabled={disabled}
          autoComplete="off"
          lang="grc"
        />
        <button
          type="button"
          className={`greek-toggle-btn${showKeyboard ? ' active' : ''}`}
          onClick={() => setShowKeyboard(!showKeyboard)}
          disabled={disabled}
          title="Grieks toetsenbord"
          aria-label="Grieks toetsenbord aan/uit"
        >
          &alpha;&beta;
        </button>
      </div>

      {showKeyboard && (
        <div className="greek-keyboard">
          <div className="greek-diacritics">
            {DIACRITICS.map((d) => (
              <button
                key={d.name}
                type="button"
                className="gk-key gk-diacritic"
                onClick={() => applyDiacritic(d.mark)}
                title={d.name}
              >
                {d.label}
              </button>
            ))}
          </div>

          {letters.map((row, ri) => (
            <div key={ri} className="greek-row">
              {ri === 2 && (
                <button
                  type="button"
                  className={`gk-key gk-shift${uppercase ? ' active' : ''}`}
                  onClick={() => setUppercase(!uppercase)}
                >
                  {'\u21E7'}
                </button>
              )}
              {row.map((letter) => (
                <button
                  key={letter}
                  type="button"
                  className="gk-key"
                  onClick={() => insertAtCursor(letter)}
                >
                  {letter}
                </button>
              ))}
              {ri === 2 && (
                <button
                  type="button"
                  className="gk-key gk-backspace"
                  onClick={handleBackspace}
                  title="Wis"
                >
                  {'\u232B'}
                </button>
              )}
            </div>
          ))}

          <div className="greek-row greek-bottom-row">
            <button
              type="button"
              className="gk-key gk-space"
              onClick={() => insertAtCursor(' ')}
            >
              spatie
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
