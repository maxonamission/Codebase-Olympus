import { useMemo } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

import { stripFrontmatter } from './scaffoldingContent'

/**
 * Render didactische scaffolding-content (paradigma-tabellen, herkenningstips)
 * als markdown boven de vraag. Alleen zichtbaar wanneer content aanwezig is.
 */
export default function ScaffoldingPanel({ content }) {
  const cleaned = useMemo(() => stripFrontmatter(content), [content])

  if (!cleaned.trim()) return null

  return (
    <div className="card scaffolding-panel" aria-label="Uitleg">
      <div className="scaffolding-content">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{cleaned}</ReactMarkdown>
      </div>
    </div>
  )
}
