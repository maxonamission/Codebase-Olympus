import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import ScaffoldingPanel from './ScaffoldingPanel'
import { stripFrontmatter } from './scaffoldingContent'

const SAMPLE = `---
knoop_id: LAT-G-MORF-DECL1-PARAD
laatst_bijgewerkt: 2026-04-13
auteur: handmatig
---

# Paradigma 1e declinatie

De 1e declinatie bevat voornamelijk **feminina**.

| Naamval     | Enkelvoud | Meervoud |
|-------------|-----------|----------|
| Nominativus | puella    | puellae  |
| Genitivus   | puellae   | puellarum|
`

describe('stripFrontmatter', () => {
  it('verwijdert een leidend YAML-frontmatter-blok', () => {
    const stripped = stripFrontmatter(SAMPLE)
    expect(stripped.startsWith('# Paradigma')).toBe(true)
    expect(stripped).not.toContain('knoop_id:')
  })

  it('laat markdown zonder frontmatter ongemoeid', () => {
    const plain = '# Kop\n\nTekst.'
    expect(stripFrontmatter(plain)).toBe(plain)
  })

  it('geeft lege string terug bij niet-string invoer', () => {
    expect(stripFrontmatter(null)).toBe('')
    expect(stripFrontmatter(undefined)).toBe('')
  })
})

describe('ScaffoldingPanel', () => {
  it('rendert null wanneer content leeg is', () => {
    const { container } = render(<ScaffoldingPanel content="" />)
    expect(container.firstChild).toBeNull()
  })

  it('rendert null wanneer content alleen frontmatter bevat', () => {
    const { container } = render(
      <ScaffoldingPanel content={'---\nkey: val\n---\n'} />
    )
    expect(container.firstChild).toBeNull()
  })

  it('rendert markdown-koppen als <h1>', () => {
    const { container } = render(<ScaffoldingPanel content={SAMPLE} />)
    const h1 = container.querySelector('h1')
    expect(h1).not.toBeNull()
    expect(h1.textContent).toBe('Paradigma 1e declinatie')
  })

  it('rendert GFM-tabellen met <thead>, <tbody> en cellen', () => {
    const { container } = render(<ScaffoldingPanel content={SAMPLE} />)
    const table = container.querySelector('table')
    expect(table).not.toBeNull()
    expect(container.querySelectorAll('thead th').length).toBe(3)
    // Twee datarijen (Nominativus, Genitivus) × 3 cellen = 6
    expect(container.querySelectorAll('tbody td').length).toBe(6)
    const firstCell = container.querySelector('tbody td')
    expect(firstCell.textContent).toBe('Nominativus')
  })

  it('rendert **vet** als <strong>', () => {
    const { container } = render(<ScaffoldingPanel content={SAMPLE} />)
    const strong = container.querySelector('strong')
    expect(strong).not.toBeNull()
    expect(strong.textContent).toBe('feminina')
  })

  it('voegt de scaffolding-panel CSS-klasse toe', () => {
    const { container } = render(<ScaffoldingPanel content={SAMPLE} />)
    expect(container.querySelector('.scaffolding-panel')).not.toBeNull()
    expect(container.querySelector('.scaffolding-content')).not.toBeNull()
  })
})
