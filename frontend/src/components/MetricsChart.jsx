import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

const COLORS = {
  prosjecno_cekanje: '#646cff',
  p95_cekanje: '#f0b429',
  prosjecno_cekanje_urgent: '#ff6b6b',
}

export default function MetricsChart({ results }) {
  if (!results.length) return null

  const data = results.map((r) => ({
    name: r.label,
    'Avg wait': r.prosjecno_cekanje,
    'P95 wait': r.p95_cekanje,
    'Urgent avg wait': r.prosjecno_cekanje_urgent,
  }))

  return (
    <div className="panel chart-panel">
      <div className="eyebrow">Wait time by strategy</div>
      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={data} margin={{ top: 8, right: 16, left: 0, bottom: 8 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#3a3a3a" />
          <XAxis dataKey="name" tick={{ fontSize: 12, fill: 'rgba(255,255,255,0.6)' }} />
          <YAxis tick={{ fontSize: 12, fill: 'rgba(255,255,255,0.6)' }} />
          <Tooltip
            contentStyle={{ fontSize: 12, borderRadius: 8, background: '#1a1a1a', borderColor: '#3a3a3a' }}
            labelStyle={{ color: 'rgba(255,255,255,0.87)' }}
          />
          <Legend wrapperStyle={{ fontSize: 13, color: 'rgba(255,255,255,0.87)' }} />
          <Bar dataKey="Avg wait" fill={COLORS.prosjecno_cekanje} radius={[3, 3, 0, 0]} />
          <Bar dataKey="P95 wait" fill={COLORS.p95_cekanje} radius={[3, 3, 0, 0]} />
          <Bar dataKey="Urgent avg wait" fill={COLORS.prosjecno_cekanje_urgent} radius={[3, 3, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

