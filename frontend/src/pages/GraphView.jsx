import { useState, useEffect, useRef, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { getGraphData } from '../api'

const TYPE_META = {
  G: { color: '#4a90d9', label: 'Grammatica' },
  V: { color: '#7c3aed', label: 'Vocabulaire' },
  C: { color: '#d97706', label: 'Cultuur' },
  I: { color: '#059669', label: 'Integratie' },
}

function nodeColor(type, mastery, status) {
  if (status === 'unseen') return '#d1d5db'
  const base = TYPE_META[type]?.color || '#6b7280'
  if (status === 'mastered') return base
  const t = Math.max(0, Math.min(1, mastery / 0.75))
  return lerpColor('#d1d5db', base, t)
}

function lerpColor(a, b, t) {
  const ah = parseInt(a.slice(1), 16)
  const bh = parseInt(b.slice(1), 16)
  const ar = (ah >> 16) & 0xff, ag = (ah >> 8) & 0xff, ab_ = ah & 0xff
  const br = (bh >> 16) & 0xff, bg = (bh >> 8) & 0xff, bb = bh & 0xff
  const rr = Math.round(ar + (br - ar) * t)
  const rg = Math.round(ag + (bg - ag) * t)
  const rb = Math.round(ab_ + (bb - ab_) * t)
  return `#${((rr << 16) | (rg << 8) | rb).toString(16).padStart(6, '0')}`
}

/**
 * Layout: group nodes by type into columns, spread vertically by
 * topological depth (approximated by longest path from roots).
 */
function computeLayout(nodes, edges, w, h) {
  const positions = {}
  const nodeMap = Object.fromEntries(nodes.map(n => [n.id, n]))

  // Build adjacency for depth computation (only prerequisite/enrichment)
  const children = {}
  const parents = {}
  nodes.forEach(n => { children[n.id] = []; parents[n.id] = [] })
  edges.forEach(e => {
    if (e.type === 'transfer') return
    if (children[e.source]) children[e.source].push(e.target)
    if (parents[e.target]) parents[e.target].push(e.source)
  })

  // Compute depth via BFS from roots
  const depth = {}
  const roots = nodes.filter(n => parents[n.id].length === 0)
  const queue = roots.map(n => ({ id: n.id, d: 0 }))
  const visited = new Set()
  while (queue.length > 0) {
    const { id, d } = queue.shift()
    if (visited.has(id)) { depth[id] = Math.max(depth[id] || 0, d); continue }
    visited.add(id)
    depth[id] = d
    for (const child of (children[id] || [])) {
      queue.push({ id: child, d: d + 1 })
    }
  }
  // Assign depth 0 to unvisited
  nodes.forEach(n => { if (depth[n.id] === undefined) depth[n.id] = 0 })

  const maxDepth = Math.max(...Object.values(depth), 1)

  // Group by type
  const typeGroups = { G: [], V: [], C: [], I: [] }
  nodes.forEach(n => {
    const g = typeGroups[n.type] || typeGroups.G
    g.push(n)
  })

  // Sort each group by depth
  Object.values(typeGroups).forEach(g => g.sort((a, b) => depth[a.id] - depth[b.id]))

  // Layout: 4 columns (G, V, C, I), nodes spread vertically
  const typeOrder = ['G', 'V', 'C', 'I']
  const margin = 60
  const colWidth = (w - margin * 2) / typeOrder.length

  typeOrder.forEach((type, colIdx) => {
    const group = typeGroups[type]
    const cx = margin + colWidth * colIdx + colWidth / 2
    const count = group.length || 1

    group.forEach((n, i) => {
      const y = margin + ((h - margin * 2) * i) / count
      // Add slight horizontal jitter based on depth to avoid perfect columns
      const jitterX = ((depth[n.id] % 5) - 2) * 15
      positions[n.id] = { x: cx + jitterX, y }
    })
  })

  return { positions, depth, maxDepth, typeGroups }
}

export default function GraphView() {
  const navigate = useNavigate()
  const canvasRef = useRef(null)
  const [graphData, setGraphData] = useState(null)
  const [layout, setLayout] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [selected, setSelected] = useState(null)
  const [hovered, setHovered] = useState(null)
  const [filter, setFilter] = useState('all')
  const [pan, setPan] = useState({ x: 0, y: 0 })
  const [zoom, setZoom] = useState(1)
  const dragRef = useRef({ dragging: false, lastX: 0, lastY: 0 })

  const W = 1400
  const H = 2400 // Tall canvas for 800 nodes

  useEffect(() => {
    async function load() {
      try {
        const data = await getGraphData()
        setGraphData(data)
        const l = computeLayout(data.nodes, data.edges, W, H)
        setLayout(l)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  // Find neighbors of selected node
  const neighbors = useCallback(() => {
    if (!selected || !graphData) return new Set()
    const ids = new Set()
    graphData.edges.forEach(e => {
      if (e.source === selected) ids.add(e.target)
      if (e.target === selected) ids.add(e.source)
    })
    return ids
  }, [selected, graphData])

  const draw = useCallback(() => {
    if (!canvasRef.current || !graphData || !layout) return
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    ctx.save()
    ctx.translate(pan.x, pan.y)
    ctx.scale(zoom, zoom)

    const positions = layout.positions
    const neighborSet = neighbors()

    const filteredNodes = filter === 'all'
      ? graphData.nodes
      : graphData.nodes.filter(n => n.type === filter)
    const nodeIds = new Set(filteredNodes.map(n => n.id))

    // Draw edges
    graphData.edges.forEach(e => {
      if (!nodeIds.has(e.source) || !nodeIds.has(e.target)) return
      const pa = positions[e.source]
      const pb = positions[e.target]
      if (!pa || !pb) return

      const isHighlighted = selected && (e.source === selected || e.target === selected)
      ctx.beginPath()
      ctx.moveTo(pa.x, pa.y)
      ctx.lineTo(pb.x, pb.y)
      ctx.strokeStyle = isHighlighted
        ? (e.type === 'transfer' ? '#a78bfa' : '#4a90d9')
        : (e.type === 'transfer' ? '#a78bfa22' : '#9ca3af18')
      ctx.lineWidth = isHighlighted ? 1.5 : 0.3
      ctx.stroke()
    })

    // Draw nodes
    filteredNodes.forEach(n => {
      const p = positions[n.id]
      if (!p) return

      const isSelected = n.id === selected
      const isNeighbor = neighborSet.has(n.id)
      const isHovered = n.id === hovered
      const dimmed = selected && !isSelected && !isNeighbor

      let r = n.status === 'mastered' ? 6 : n.status === 'in_progress' ? 5 : 3
      if (isSelected) r = 9
      if (isNeighbor) r = 6

      ctx.globalAlpha = dimmed ? 0.15 : 1.0
      ctx.beginPath()
      ctx.arc(p.x, p.y, r, 0, Math.PI * 2)
      ctx.fillStyle = nodeColor(n.type, n.mastery, n.status)
      ctx.fill()

      if (isSelected || isHovered) {
        ctx.strokeStyle = isSelected ? '#1e293b' : '#475569'
        ctx.lineWidth = isSelected ? 2.5 : 1.5
        ctx.stroke()
      }
      ctx.globalAlpha = 1.0
    })

    // Column headers
    const typeOrder = ['G', 'V', 'C', 'I']
    const colWidth = (W - 120) / 4
    ctx.font = 'bold 14px system-ui'
    ctx.textAlign = 'center'
    typeOrder.forEach((type, i) => {
      const x = 60 + colWidth * i + colWidth / 2
      ctx.fillStyle = TYPE_META[type].color
      ctx.fillText(TYPE_META[type].label, x, 30)
    })

    // Hover tooltip
    if (hovered && !selected) {
      const node = graphData.nodes.find(n => n.id === hovered)
      const p = positions[hovered]
      if (node && p) {
        ctx.font = '11px system-ui'
        const text = `${node.titel} (${Math.round(node.mastery * 100)}%)`
        const tw = ctx.measureText(text).width
        ctx.fillStyle = '#1e293bee'
        ctx.fillRect(p.x + 10, p.y - 18, tw + 12, 22)
        ctx.fillStyle = '#fff'
        ctx.textAlign = 'left'
        ctx.fillText(text, p.x + 16, p.y - 2)
      }
    }

    ctx.restore()
  }, [graphData, layout, filter, hovered, selected, pan, zoom, neighbors])

  useEffect(() => { draw() }, [draw])

  function screenToCanvas(e) {
    const rect = canvasRef.current.getBoundingClientRect()
    const scaleX = canvasRef.current.width / rect.width
    const scaleY = canvasRef.current.height / rect.height
    return {
      x: ((e.clientX - rect.left) * scaleX - pan.x) / zoom,
      y: ((e.clientY - rect.top) * scaleY - pan.y) / zoom,
    }
  }

  function findNodeAt(cx, cy) {
    if (!graphData || !layout) return null
    const threshold = 12 / zoom
    for (const n of graphData.nodes) {
      const p = layout.positions[n.id]
      if (!p) continue
      const dx = cx - p.x, dy = cy - p.y
      if (dx * dx + dy * dy < threshold * threshold) return n
    }
    return null
  }

  function handleClick(e) {
    const { x, y } = screenToCanvas(e)
    const node = findNodeAt(x, y)
    setSelected(node ? node.id : null)
  }

  function handleMouseMove(e) {
    if (dragRef.current.dragging) {
      const dx = e.clientX - dragRef.current.lastX
      const dy = e.clientY - dragRef.current.lastY
      dragRef.current.lastX = e.clientX
      dragRef.current.lastY = e.clientY
      setPan(p => ({ x: p.x + dx, y: p.y + dy }))
      return
    }
    const { x, y } = screenToCanvas(e)
    const node = findNodeAt(x, y)
    setHovered(node ? node.id : null)
  }

  function handleMouseDown(e) {
    const { x, y } = screenToCanvas(e)
    const node = findNodeAt(x, y)
    if (!node) {
      dragRef.current = { dragging: true, lastX: e.clientX, lastY: e.clientY }
    }
  }

  function handleMouseUp() {
    dragRef.current.dragging = false
  }

  function handleWheel(e) {
    e.preventDefault()
    const delta = e.deltaY > 0 ? 0.9 : 1.1
    setZoom(z => Math.max(0.2, Math.min(3, z * delta)))
  }

  // Get selected node data
  const selectedNode = selected ? graphData?.nodes.find(n => n.id === selected) : null
  const selectedNeighbors = selected ? (() => {
    const prereqs = []
    const postreqs = []
    graphData.edges.forEach(e => {
      if (e.source === selected) {
        const n = graphData.nodes.find(x => x.id === e.target)
        if (n) postreqs.push(n)
      }
      if (e.target === selected) {
        const n = graphData.nodes.find(x => x.id === e.source)
        if (n) prereqs.push(n)
      }
    })
    return { prereqs, postreqs }
  })() : { prereqs: [], postreqs: [] }

  if (loading) return <div className="page"><p>Graph laden...</p></div>
  if (error) return <div className="page"><div className="error-message">{error}</div></div>

  const stats = graphData ? {
    mastered: graphData.nodes.filter(n => n.status === 'mastered').length,
    in_progress: graphData.nodes.filter(n => n.status === 'in_progress').length,
    unseen: graphData.nodes.filter(n => n.status === 'unseen').length,
  } : {}

  return (
    <div className="page graph-page">
      <div className="graph-header">
        <button className="btn-link" onClick={() => navigate('/dashboard')}>← Dashboard</button>
        <h2>Knowledge Graph</h2>
      </div>

      <div className="graph-controls">
        <div className="graph-filters">
          <button className={`btn btn-sm ${filter === 'all' ? 'btn-active' : ''}`} onClick={() => setFilter('all')}>
            Alles ({graphData.nodes.length})
          </button>
          {Object.entries(TYPE_META).map(([type, { label, color }]) => {
            const count = graphData.nodes.filter(n => n.type === type).length
            return (
              <button key={type} className={`btn btn-sm ${filter === type ? 'btn-active' : ''}`} onClick={() => setFilter(type)}>
                <span className="filter-dot" style={{ background: color }} />
                {label} ({count})
              </button>
            )
          })}
        </div>
        <div className="graph-legend">
          <span className="legend-item"><span className="legend-dot" style={{ background: '#4a90d9' }} /> Beheerst</span>
          <span className="legend-item"><span className="legend-dot" style={{ background: '#9ca3af' }} /> Bezig</span>
          <span className="legend-item"><span className="legend-dot" style={{ background: '#d1d5db' }} /> Onbekend</span>
        </div>
      </div>

      <div className="graph-stats">
        <span className="stat-mini mastery-up">{stats.mastered} beheerst</span>
        <span className="stat-mini">{stats.in_progress} bezig</span>
        <span className="stat-mini" style={{ color: '#9ca3af' }}>{stats.unseen} onbekend</span>
        <span className="stat-mini" style={{ color: '#6b7280', fontSize: '0.75rem' }}>
          Zoom: {Math.round(zoom * 100)}% — sleep om te pannen, scroll om te zoomen
        </span>
      </div>

      <div className="graph-container">
        <canvas
          ref={canvasRef}
          width={W}
          height={H}
          className="graph-canvas"
          onClick={handleClick}
          onMouseMove={handleMouseMove}
          onMouseDown={handleMouseDown}
          onMouseUp={handleMouseUp}
          onMouseLeave={() => { setHovered(null); handleMouseUp() }}
          onWheel={handleWheel}
        />

        {selectedNode && (
          <div className="node-info-panel">
            <button className="panel-close" onClick={() => setSelected(null)}>×</button>
            <h3>{selectedNode.titel}</h3>
            <div className="panel-meta">
              <span className="panel-type" style={{ color: TYPE_META[selectedNode.type]?.color }}>
                {TYPE_META[selectedNode.type]?.label}
              </span>
              <span className="panel-lang">{selectedNode.taal === 'lat' ? 'Latijn' : selectedNode.taal === 'grc' ? 'Grieks' : 'Gedeeld'}</span>
            </div>
            <div className="panel-mastery">
              <div className="panel-mastery-bar">
                <div
                  className="panel-mastery-fill"
                  style={{
                    width: `${Math.round(selectedNode.mastery * 100)}%`,
                    background: nodeColor(selectedNode.type, selectedNode.mastery, selectedNode.status),
                  }}
                />
              </div>
              <span className="panel-mastery-label">{Math.round(selectedNode.mastery * 100)}% beheerst</span>
            </div>

            {selectedNeighbors.prereqs.length > 0 && (
              <div className="panel-section">
                <h4>Prerequisites ({selectedNeighbors.prereqs.length})</h4>
                <div className="panel-node-list">
                  {selectedNeighbors.prereqs.slice(0, 8).map(n => (
                    <button key={n.id} className="panel-node-btn" onClick={() => setSelected(n.id)}>
                      <span className="panel-node-dot" style={{ background: nodeColor(n.type, n.mastery, n.status) }} />
                      <span className="panel-node-title">{n.titel}</span>
                      <span className="panel-node-pct">{Math.round(n.mastery * 100)}%</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {selectedNeighbors.postreqs.length > 0 && (
              <div className="panel-section">
                <h4>Volgende stof ({selectedNeighbors.postreqs.length})</h4>
                <div className="panel-node-list">
                  {selectedNeighbors.postreqs.slice(0, 8).map(n => (
                    <button key={n.id} className="panel-node-btn" onClick={() => setSelected(n.id)}>
                      <span className="panel-node-dot" style={{ background: nodeColor(n.type, n.mastery, n.status) }} />
                      <span className="panel-node-title">{n.titel}</span>
                      <span className="panel-node-pct">{Math.round(n.mastery * 100)}%</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="panel-actions">
              <button
                className="btn btn-primary"
                onClick={() => navigate(`/session?focus=${selectedNode.id}`)}
              >
                Oefen deze knoop
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
