/**
 * Strip a leading YAML-frontmatter block ("---\n...\n---\n") from markdown.
 * The didactische content-bestanden in data/content/ starten met een
 * frontmatter-blok (knoop_id, laatst_bijgewerkt, auteur) die niet zinvol
 * is voor de leerling. react-markdown zou deze anders als <hr> + platte
 * regels renderen.
 */
export function stripFrontmatter(markdown) {
  if (typeof markdown !== 'string') return ''
  const match = markdown.match(/^---\r?\n[\s\S]*?\r?\n---[ \t]*\r?\n?/)
  const body = match ? markdown.slice(match[0].length) : markdown
  return body.replace(/^\s+/, '')
}
