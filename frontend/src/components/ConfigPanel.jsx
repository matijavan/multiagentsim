export default function ConfigPanel({ strategies, config, onChange, onRun, loading }) {
  const toggleStrategy = (key) => {
    const selected = config.strategies.includes(key)
      ? config.strategies.filter((s) => s !== key)
      : [...config.strategies, key]
    onChange({ ...config, strategies: selected })
  }

  return (
    <aside className="panel config-panel">
      <div className="eyebrow">Run configuration</div>

      <div className="field-group">
        <span className="field-label">Strategies to compare</span>
        <div className="checkbox-list">
          {strategies.map((s) => (
            <label key={s.key} className="checkbox-row">
              <input
                type="checkbox"
                checked={config.strategies.includes(s.key)}
                onChange={() => toggleStrategy(s.key)}
              />
              <span>{s.label}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="field-group">
        <label className="field-label" htmlFor="ticket-count">
          Ticket volume <span className="field-value">{config.broj_tiketa}</span>
        </label>
        <input
          id="ticket-count"
          type="range"
          min={20}
          max={1000}
          step={20}
          value={config.broj_tiketa}
          onChange={(e) => onChange({ ...config, broj_tiketa: Number(e.target.value) })}
        />
      </div>

      <div className="field-group">
        <label className="field-label" htmlFor="ticket-length">
          Ticket processing length <span className="field-value">{config.duljina_tiketa}</span>
        </label>
        <input
          id="ticket-length"
          type="range"
          min={3}
          max={9}
          step={1}
          value={config.duljina_tiketa}
          onChange={(e) => onChange({ ...config, duljina_tiketa: Number(e.target.value) })}
        />
      </div>

      <div className="field-group">
        <label className="field-label" htmlFor="proxy-accuracy">
          Classifier accuracy <span className="field-value">{Math.round(config.tocnost_proxyja * 100)}%</span>
        </label>
        <input
          id="proxy-accuracy"
          type="range"
          min={0}
          max={1}
          step={0.05}
          value={config.tocnost_proxyja}
          onChange={(e) => onChange({ ...config, tocnost_proxyja: Number(e.target.value) })}
        />
        <span className="field-hint">How often the general agent correctly identifies the ticket type.</span>
      </div>

      <div className="field-group">
        <label className="field-label" htmlFor="seed">
          Random seed
        </label>
        <input
          id="seed"
          type="number"
          min={0}
          value={config.seed}
          onChange={(e) => onChange({ ...config, seed: Number(e.target.value) })}
        />
        <span className="field-hint">Same seed with same config = identical simulation</span>
      </div>

      <button className="run-button" onClick={onRun} disabled={loading || config.strategies.length === 0}>
        {loading ? 'Running…' : 'Run simulation'}
      </button>
    </aside>
  )
}
