import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import WoordKaart from './WoordKaart'

const VERB = {
  lemma: 'sum',
  part_of_speech: 'verb',
  conjugation: 'irreg',
  forms: 'esse',
  meaning: 'zijn',
  cluster: null,
}

const NOUN = {
  lemma: 'puella',
  part_of_speech: 'noun',
  conjugation: '1',
  forms: 'puellae',
  meaning: 'meisje',
  cluster: 'familie',
}

const PREP = {
  lemma: 'in',
  part_of_speech: 'prep',
  conjugation: null,
  forms: '+acc/abl',
  meaning: 'in, naar; in, op',
  cluster: null,
}

describe('WoordKaart', () => {
  it('rendert null zonder metadata', () => {
    const { container } = render(<WoordKaart metadata={null} />)
    expect(container.firstChild).toBeNull()
  })

  it('toont lemma + Nederlandse woordsoort-afkorting', () => {
    render(<WoordKaart metadata={VERB} />)
    expect(screen.getByText('sum')).toBeTruthy()
    expect(screen.getByText('werkwoord')).toBeTruthy()
  })

  it('toont "Stamtijden" voor een werkwoord met forms', () => {
    render(<WoordKaart metadata={VERB} />)
    expect(screen.getByText('Stamtijden')).toBeTruthy()
    expect(screen.getByText('esse')).toBeTruthy()
  })

  it('toont "Vormen" voor een zelfstandig naamwoord met forms', () => {
    render(<WoordKaart metadata={NOUN} />)
    expect(screen.getByText('Vormen')).toBeTruthy()
    expect(screen.getByText('puellae')).toBeTruthy()
  })

  it('toont "Naamval" voor een voorzetsel met forms', () => {
    render(<WoordKaart metadata={PREP} />)
    expect(screen.getByText('Naamval')).toBeTruthy()
    expect(screen.getByText('+acc/abl')).toBeTruthy()
  })

  it('rendert de betekenis altijd', () => {
    render(<WoordKaart metadata={VERB} />)
    expect(screen.getByText('Betekenis')).toBeTruthy()
    expect(screen.getByText('zijn')).toBeTruthy()
  })

  it('toont cluster alleen wanneer gevuld', () => {
    const { container: withCluster } = render(<WoordKaart metadata={NOUN} />)
    expect(withCluster.textContent).toContain('familie')

    const { container: without } = render(<WoordKaart metadata={VERB} />)
    expect(without.textContent).not.toContain('Cluster')
  })

  it('laat conjugation/klasse weg wanneer null (prep)', () => {
    const { container } = render(<WoordKaart metadata={PREP} />)
    expect(container.textContent).not.toContain('Klasse')
  })

  it('geeft het kaart-element de juiste aria-label', () => {
    render(<WoordKaart metadata={VERB} />)
    expect(screen.getByRole('region', { name: 'Woordkaart' })).toBeTruthy()
  })
})
