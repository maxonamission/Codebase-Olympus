import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, fireEvent, screen } from '@testing-library/react'
import AudioPlayer from './AudioPlayer'

/**
 * jsdom stubbt HTMLMediaElement niet volledig — play() geeft een
 * rejected promise.  We vervangen de methodes door spies zodat we
 * gedrag kunnen verifiëren zonder echte media-pipeline.
 */
beforeEach(() => {
  window.HTMLMediaElement.prototype.play = vi.fn().mockResolvedValue(undefined)
  window.HTMLMediaElement.prototype.pause = vi.fn()
})

describe('AudioPlayer', () => {
  it('rendert null zonder src', () => {
    const { container } = render(<AudioPlayer src={null} />)
    expect(container.firstChild).toBeNull()
  })

  it('rendert <audio> met src en preload=none', () => {
    const { container } = render(<AudioPlayer src="/audio/LAT-V-F01-SUM.wav" />)
    const audio = container.querySelector('audio')
    expect(audio).not.toBeNull()
    expect(audio.getAttribute('src')).toBe('/audio/LAT-V-F01-SUM.wav')
    expect(audio.getAttribute('preload')).toBe('none')
  })

  it('rendert geen autoplay-attribuut', () => {
    const { container } = render(<AudioPlayer src="/audio/a.wav" />)
    const audio = container.querySelector('audio')
    expect(audio.hasAttribute('autoplay')).toBe(false)
  })

  it('toont play- en replay-knop met herkenbare labels', () => {
    render(<AudioPlayer src="/audio/a.wav" label="Luister naar de opname" />)
    expect(screen.getByRole('button', { name: 'Luister naar de opname' })).toBeTruthy()
    expect(screen.getByRole('button', { name: 'Speel opnieuw af' })).toBeTruthy()
  })

  it('play-klik roept HTMLMediaElement.play() aan', () => {
    render(<AudioPlayer src="/audio/a.wav" />)
    const playBtn = screen.getByRole('button', { name: 'Speel audio af' })
    fireEvent.click(playBtn)
    expect(window.HTMLMediaElement.prototype.play).toHaveBeenCalledTimes(1)
  })

  it('replay zet currentTime terug naar 0 en start play opnieuw', () => {
    const { container } = render(<AudioPlayer src="/audio/a.wav" />)
    const audio = container.querySelector('audio')
    audio.currentTime = 5

    const replayBtn = screen.getByRole('button', { name: 'Speel opnieuw af' })
    fireEvent.click(replayBtn)

    expect(audio.currentTime).toBe(0)
    expect(window.HTMLMediaElement.prototype.play).toHaveBeenCalled()
  })

  it('tweede klik op play (tijdens spelen) pauzeert', () => {
    const { container } = render(<AudioPlayer src="/audio/a.wav" />)
    const audio = container.querySelector('audio')
    const playBtn = screen.getByRole('button', { name: 'Speel audio af' })

    // Simuleer dat audio aan het spelen is door het onPlay-event handmatig te vuren.
    fireEvent.play(audio)

    // Knop-label wisselt naar 'Pauzeer audio' — klik opnieuw.
    const pauseBtn = screen.getByRole('button', { name: 'Pauzeer audio' })
    fireEvent.click(pauseBtn)

    expect(window.HTMLMediaElement.prototype.pause).toHaveBeenCalledTimes(1)

    // Voorkom unused-var lint op playBtn (hij wordt enkel gebruikt om het element te pakken).
    expect(playBtn).toBeTruthy()
  })

  it('toont foutmelding wanneer audio onError vuurt', () => {
    const { container } = render(<AudioPlayer src="/audio/missing.wav" />)
    const audio = container.querySelector('audio')
    fireEvent.error(audio)
    expect(screen.getByRole('alert').textContent).toContain('niet beschikbaar')
  })
})
