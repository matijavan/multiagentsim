function SignalMeter({ accuracy }) {
  const segments = 10
  const filled = Math.round(accuracy * segments)
  return (
    <div className="signal-meter" title={`${(accuracy * 100).toFixed(1)}% correct`}>
      {Array.from({ length: segments }).map((_, i) => (
        <span key={i} className={`signal-bar ${i < filled ? 'filled' : ''}`} />
      ))}
    </div>
  )
}

export default function SummaryCards({ results }) {
  if (!results.length) return null

  const fastest = results.reduce((a, b) => (a.prosjecno_cekanje <= b.prosjecno_cekanje ? a : b))
  const proxyAccuracy = results[0].proxy_tocnost

  return (
    <div className="summary-block">

      <div className="card-grid">
        {results.map((r) => (
          <div className={`card ${r.strategy === fastest.strategy ? 'card-best' : ''}`} key={r.strategy}>
            {r.strategy === fastest.strategy && <span className="card-badge">Lowest avg wait</span>}
            <div className="card-title">{r.label}</div>
            <div className="card-metric">
              <span className="metric-value">{r.prosjecno_cekanje.toFixed(2)}</span>
              <span className="metric-label">avg wait</span>
            </div>
            <div className="card-metric-row">
              <div>
                <span className="metric-value-sm">{r.p95_cekanje.toFixed(2)}</span>
                <span className="metric-label">P95 wait</span>
              </div>
              <div>
                <span className="metric-value-sm">{r.prosjecno_cekanje_urgent.toFixed(2)}</span>
                <span className="metric-label">urgent wait</span>
              </div>
              <div>
                <span className="metric-value-sm">{r.max_cekanje.toFixed(2)}</span>
                <span className="metric-label">max wait</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
