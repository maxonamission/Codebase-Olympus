const POS_LABELS = {
  verb: 'werkwoord',
  noun: 'zn',
  adj: 'bn',
  pron: 'vnw',
  prep: 'voorz',
  adv: 'bw',
  conj: 'voegw',
  num: 'telw',
  interj: 'tw',
  part: 'partikel',
}

function formsLabel(pos) {
  switch (pos) {
    case 'verb':
      return 'Stamtijden'
    case 'noun':
    case 'adj':
    case 'pron':
      return 'Vormen'
    case 'prep':
      return 'Naamval'
    default:
      return 'Vorm'
  }
}

/**
 * Toon structured vocabulaire-metadata naast/onder een V-knoop:
 * lemma, woordsoort, vormen (stamtijden / genitief / naamval), betekenis
 * en optioneel een semantisch cluster.
 *
 * Rendert `null` wanneer geen metadata meegegeven is, zodat de caller
 * altijd `{metadata && <WoordKaart ... />}` kan schrijven.
 */
export default function WoordKaart({ metadata }) {
  if (!metadata) return null

  const posLabel = POS_LABELS[metadata.part_of_speech] || metadata.part_of_speech

  return (
    <div className="woordkaart" role="region" aria-label="Woordkaart">
      <div className="woordkaart-header">
        <span className="woordkaart-lemma">{metadata.lemma}</span>
        <span className="woordkaart-pos">{posLabel}</span>
      </div>
      <dl className="woordkaart-grid">
        {metadata.forms && (
          <>
            <dt>{formsLabel(metadata.part_of_speech)}</dt>
            <dd>{metadata.forms}</dd>
          </>
        )}
        {metadata.conjugation && (
          <>
            <dt>Klasse</dt>
            <dd>{metadata.conjugation}</dd>
          </>
        )}
        <dt>Betekenis</dt>
        <dd>{metadata.meaning}</dd>
        {metadata.cluster && (
          <>
            <dt>Cluster</dt>
            <dd>{metadata.cluster}</dd>
          </>
        )}
      </dl>
    </div>
  )
}
