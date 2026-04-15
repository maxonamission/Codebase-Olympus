import { useState, useEffect, useRef, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { getGraphData } from '../api'

const TYPE_COLORS = {
  G: { base: '#4a90d9', label: 'Grammatica' },
  V: { base: '#7c3aed', label: 'Vocabulaire' },
  C: { base: '#d97706', label: 'Cultuur' },
  I: { base: '#059669', label: 'Integratie' },
}

const STATUS_OPACITY = {
  mastered: 1.0,
  in_progress: 0.7,
  unseen: 0.15,
}

function masteryColor(type, mastery, status) {
  if (status === 'unseen') return '#d1d5db'
  const base = TYPE_COLORS[type]?.base || '#6b7280'
  if (status === 'mastered') return base
  // in_progress: interpolate between grey and base color
  const t = Math.max(0, Math.min(1, mastery / 0.75))
  return lerpColor('#d1d5db', base, t)
}

function lerpColor(a, b, t) {
  const ah = parseInt(a.slice(1), 16)
  const bh = parseInt(b.slice(1), 16)
  const ar = (ah >> 16) & 0xff, ag = (ah >> 8) & 0xff, ab = ah & 0xff
  const br = (bh >> 16) & 0xff, bg = (bh >> 8) & 0xff, bb = bh & 0xff
  const rr = Math.round(ar + (br - ar) * t)
  const rg = Math.round(ag + (bg - ag) * t)
  const rb = Math.round(ab + (bb - ab) * t)
  return `#${((rr << 16) | (rg << 8) | rb).toString(16).padStart(6, '0')}`
}

// Simple force-directed layout
function forceLayout(nodes, edges, width, height, iterations = 100) {
  const positions = {}
  // Initial random placement
  nodes.forEach((n, i) => {
    const angle = (i / nodes.length) * Math.PI * 2
    const r = Math.min(width, height) * 0.35
    positions[n.id] = {
      x: width / 2 + r * Math.cos(angle) + (Math.random() - 0.5) * 50,
      y: height / 2 + r * Math.sin(angle) + (Math.random() - 0.5) * 50,
      vx: 0, vy: 0,
    }
  })

  const edgeSet = new Set(edges.map(e => `${e.source}-${e.target}`))
  const k = Math.sqrt((width * height) / Math.max(nodes.length, 1)) * 0.8

  for (let iter = 0; iter < iterations; iter++) {
    const temp = 1 - iter / iterations

    // Repulsion between all pairs (use grid approximation for performance)
    for (let i = 0; i < nodes.length; i++) {
      const pi = positions[nodes[i].id]
      for (let j = i + 1; j < nodes.length; j++) {
        const pj = positions[nodes[j].id]
        let dx = pi.x - pj.x
        let dy = pi.y - pj.y
        const dist = Math.max(Math.sqrt(dx * dx + dy * dy), 1)
        const force = (k * k) / dist * 0.01
        const fx = (dx / dist) * force
        const fy = (dy / dist) * force
        pi.vx += fx; pi.vy += fy
        pj.vx -= fx; pj.vy -= fy
      }
    }

    // Attraction along edges
    edges.forEach(e => {
      const pa = positions[e.source]
      const pb = positions[e.target]
      if (!pa || !pb) return
      const dx = pb.x - pa.x
      const dy = pb.y - pa.y
      const dist = Math.max(Math.sqrt(dx * dx + dy * dy), 1)
      const force = dist / k * 0.5
      const fx = (dx / dist) * force
      const fy = (dy / dist) * force
      pa.vx += fx; pa.vy += fy
      pb.vx -= fx; pb.vy -= fy
    })

    // Center gravity
    nodes.forEach(n => {
      const p = positions[n.id]
      p.vx += (width / 2 - p.x) * 0.001
      p.vy += (height / 2 - p.y) * 0.001
    })

    // Apply velocities with damping
    nodes.forEach(n => {
      const p = positions[n.id]
      const speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy)
      const maxSpeed = 5 * temp + 0.5
      if (speed > maxSpeed) {
        p.vx = (p.vx / speed) * maxSpeed
        p.vy = (p.vy / speed) * maxSpeed
      }
      p.x += p.vx
      p.y += p.vy
      p.vx *= 0.8
      p.vy *= 0.8
      // Keep in bounds
      p.x = Math.max(20, Math.min(width - 20, p.x))
      p.y = Math.max(20, Math.min(height - 20, p.y))
    })
  }

  return positions
}

export default function GraphView() {
  const navigate = useNavigate()
  const canvasRef = useRef(null)
  const [graphData, setGraphData] = useState(null)
  const [positions, setPositions] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [hovered, setHovered] = useState(null)
  const [filter, setFilter] = useState('all') // 'all', 'G', 'V', 'C', 'I'

  useEffect(() => {
    async function load() {
      try {
        const data = await getGraphData()
        setGraphData(data)
        const w = 1200, h = 800
        const pos = forceLayout(data.nodes, data.edges, w, h, 150)
        setPositions(pos)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const draw = useCallback(() => {
    if (!canvasRef.current || !graphData || !positions) return
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    const w = canvas.width
    const h = canvas.height
    ctx.clearRect(0, 0, w, h)

    const filteredNodes = filter === 'all'
      ? graphData.nodes
      : graphData.nodes.filter(n => n.type === filter)
    const nodeIds = new Set(filteredNodes.map(n => n.id))

    // Draw edges
    ctx.lineWidth = 0.5
    graphData.edges.forEach(e => {
      if (!nodeIds.has(e.source) || !nodeIds.has(e.target)) return
      const pa = positions[e.source]
      const pb = positions[e.target]
      if (!pa || !pb) return
      ctx.beginPath()
      ctx.moveTo(pa.x, pa.y)
      ctx.lineTo(pb.x, pb.y)
      ctx.strokeStyle = e.type === 'transfer' ? '#a78bfa44' : '#9ca3af33'
      ctx.stroke()
    })

    // Draw nodes
    filteredNodes.forEach(n => {
      const p = positions[n.id]
      if (!p) return
      const r = n.status === 'mastered' ? 5 : n.status === 'in_progress' ? 4 : 3
      ctx.beginPath()
      ctx.arc(p.x, p.y, r, 0, Math.PI * 2)
      ctx.fillStyle = masteryColor(n.type, n.mastery, n.status)
      ctx.fill()
      if (hovered === n.id) {
        ctx.strokeStyle = '#1e293b'
        ctx.lineWidth = 2
        ctx.stroke()
      }
    })

    // Draw hovered tooltip
    if (hovered) {
      const node = graphData.nodes.find(n => n.id === hovered)
      const p = positions[hovered]
      if (node && p) {
        ctx.font = '12px sans-serif'
        const text = `${node.titel} (${Math.round(node.mastery * 100)}%)`
        const tw = ctx.measureText(text).width
        ctx.fillStyle = '#1e293bee'
        ctx.fillRect(p.x + 8, p.y - 20, tw + 12, 24)
        ctx.fillStyle = '#fff'
        ctx.fillText(text, p.x + 14, p.y - 3)
      }
    }
  }, [graphData, positions, filter, hovered])

  useEffect(() => { draw() }, [draw])

  function handleMouseMove(e) {
    if (!graphData || !positions) return
    const rect = canvasRef.current.getBoundingClientRect()
    const mx = e.clientX - rect.left
    const my = e.clientY - rect.top
    let found = null
    for (const n of graphData.nodes) {
      const p = positions[n.id]
      if (!p) continue
      const dx = mx - p.x, dy = my - p.y
      if (dx * dx + dy * dy < 64) { found = n.id; break }
    }
    if (found !== hovered) setHovered(found)
  }

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
          <button className={`btn btn-sm ${filter === 'all' ? 'btn-active' : ''}`} onClick={() => setFilter('all')}>Alles ({graphData.nodes.length})</button>
          {Object.entries(TYPE_COLORS).map(([type, { label }]) => {
            const count = graphData.nodes.filter(n => n.type === type).length
            return (
              <button key={type} className={`btn btn-sm ${filter === type ? 'btn-active' : ''}`} onClick={() => setFilter(type)}>
                <span className="filter-dot" style={{ background: TYPE_COLORS[type].base }} />
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
      </div>

      <canvas
        ref={canvasRef}
        width={1200}
        height={800}
        className="graph-canvas"
        onMouseMove={handleMouseMove}
        onMouseLeave={() => setHovered(null)}
      />
    </div>
  )
}
