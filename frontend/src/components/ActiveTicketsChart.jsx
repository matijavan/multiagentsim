import { Bar, BarChart, Brush, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

const SERIES_COLORS = ['#646cff', '#f0b429', '#ff6b6b', '#2dd4bf', '#a78bfa', '#fb923c']

export default function ActiveTicketsChart({ results }) {
  if (!results.length) return null

  const maxTick = Math.max(...results.map((r) => (r.aktivni_tiketi?.length ?? 0) - 1), 0)

  const data = []
  for (let tick = 0; tick <= maxTick; tick++) {
    const row = { tick }
    for (const r of results) {
      const entry = r.aktivni_tiketi?.[tick]
      row[r.label] = entry ? entry.aktivno : 0
    }
    data.push(row)
  }

  return (
    <div className="panel chart-panel">
      <div className="eyebrow">Active (in-flight) tickets over time</div>
      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={data} margin={{ top: 8, right: 16, left: 0, bottom: 8 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#3a3a3a" />
          <XAxis dataKey="tick" tick={{ fontSize: 11, fill: 'rgba(255,255,255,0.6)' }} />
          <YAxis tick={{ fontSize: 12, fill: 'rgba(255,255,255,0.6)' }} />
          <Tooltip
            contentStyle={{ fontSize: 12, borderRadius: 8, background: '#1a1a1a', borderColor: '#3a3a3a' }}
            labelStyle={{ color: 'rgba(255,255,255,0.87)' }}
          />
          <Legend wrapperStyle={{ fontSize: 13, color: 'rgba(255,255,255,0.87)' }} />
          {results.map((r, i) => (
            <Bar key={r.strategy} dataKey={r.label} fill={SERIES_COLORS[i % SERIES_COLORS.length]} />
          ))}
          <Brush
            dataKey="tick"
            height={24}
            stroke="#646cff"
            fill="#1a1a1a"
            travellerWidth={8}
            tickFormatter={(tick) => tick}
          />
        </BarChart>
      </ResponsiveContainer>
      <span className="field-hint">Drag the handles below the chart to zoom into a tick range.</span>
    </div>
  )
}
