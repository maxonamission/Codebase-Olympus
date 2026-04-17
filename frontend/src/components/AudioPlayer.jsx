import { useRef, useState } from 'react'

/**
 * Minimale audio-player voor luister-items.  Geen autoplay — leerling
 * drukt zelf op play (WCAG).  Een losse replay-knop spoelt altijd terug
 * naar het begin en speelt opnieuw af.
 *
 * Props:
 *   src   — pad naar audiobestand, bv. "/audio/LAT-V-F01-SUM.wav".
 *   label — optioneel aria-label voor de play-knop.
 */
export default function AudioPlayer({ src, label = 'Speel audio af' }) {
  const audioRef = useRef(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [error, setError] = useState(null)

  if (!src) return null

  async function play() {
    const el = audioRef.current
    if (!el) return
    try {
      setError(null)
      await el.play()
    } catch {
      setError('Kon audio niet afspelen.')
    }
  }

  async function handleTogglePlay() {
    const el = audioRef.current
    if (!el) return
    if (isPlaying) {
      el.pause()
    } else {
      await play()
    }
  }

  async function handleReplay() {
    const el = audioRef.current
    if (!el) return
    el.currentTime = 0
    await play()
  }

  return (
    <div className="audio-player">
      <audio
        ref={audioRef}
        src={src}
        preload="none"
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
        onEnded={() => setIsPlaying(false)}
        onError={() => setError('Audio niet beschikbaar.')}
      />
      <button
        type="button"
        className="btn audio-play"
        onClick={handleTogglePlay}
        aria-label={isPlaying ? 'Pauzeer audio' : label}
      >
        {isPlaying ? '⏸ Pauze' : '▶ Afspelen'}
      </button>
      <button
        type="button"
        className="btn audio-replay"
        onClick={handleReplay}
        aria-label="Speel opnieuw af"
      >
        ↺ Opnieuw
      </button>
      {error && <p className="audio-error" role="alert">{error}</p>}
    </div>
  )
}
