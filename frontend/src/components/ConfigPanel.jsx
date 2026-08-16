export default function ConfigPanel({ strategies, config, onChange, onRun, loading }) {
  const toggleStrategy = (key) => {
    const selected = config.strategies.includes(key)
      ? config.strategies.filter((s) => s !== key)
      : [...config.strategies, key]
    onChange({ ...config, strategies: selected })
  }

  const updateAgent = (index, patch) => {
    const agents = config.agents.map((a, i) => (i === index ? { ...a, ...patch } : a))
    onChange({ ...config, agents })
  }

  const addAgent = () => {
    onChange({ ...config, agents: [...config.agents, { name: '', kapacitet: 2 }] })
  }

  const removeAgent = (index) => {
    onChange({ ...config, agents: config.agents.filter((_, i) => i !== index) })
  }

  const ticketTypes = [...new Set(config.agents.map((a) => a.name).filter(Boolean))]

  const updateWeight = (type, value) => {
    onChange({ ...config, tip_weights: { ...config.tip_weights, [type]: value } })
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
        <label className="field-label" htmlFor="ticket-gap">
          Avg. time between ticket arrivals <span className="field-value">{config.prosjecni_razmak.toFixed(1)}</span>
        </label>
        <input
          id="ticket-gap"
          type="range"
          min={0.2}
          max={3}
          step={0.1}
          value={config.prosjecni_razmak}
          onChange={(e) => onChange({ ...config, prosjecni_razmak: Number(e.target.value) })}
        />
        <span className="field-hint">
          Lower = tickets spawn more often (~{(1 / config.prosjecni_razmak).toFixed(2)} tickets/tick).
        </span>
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
        <span className="field-hint"></span>
      </div>

      <div className="field-group">
        <label className="field-label" htmlFor="proxy-capacity">
          Proxy capacity 
        </label>
        <input
          id="proxy-capacity"
          type="number"
          min={1}
          max={9999}
          value={config.proxy_kapacitet}
          onChange={(e) => onChange({ ...config, proxy_kapacitet: Number(e.target.value) })}
        />

      </div>

      <div className="field-group">
        <label className="field-label" htmlFor="urgent-ratio">
          Urgent ticket ratio <span className="field-value">{Math.round(config.postotak_urgent * 100)}%</span>
        </label>
        <input
          id="urgent-ratio"
          type="range"
          min={0}
          max={1}
          step={0.05}
          value={config.postotak_urgent}
          onChange={(e) => onChange({ ...config, postotak_urgent: Number(e.target.value) })}
        />
        <span className="field-hint">Rest of the tickets are NORMAL priority.</span>
      </div>

      <div className="field-group">
        <label className="checkbox-row" htmlFor="discard-full-proxy">
          <input
            id="discard-full-proxy"
            type="checkbox"
            checked={config.odbacuj_pune}
            onChange={(e) => onChange({ ...config, odbacuj_pune: e.target.checked })}
          />
          <span>Discard tickets when proxy is full</span>
        </label>
        <span className="field-hint">
          Instead of waiting for a free triage slot, the ticket is dropped and counted as discarded.
        </span>
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
        <span className="field-hint"></span>
      </div>

      <div className="field-group">
        <span className="field-label">Agents</span>
        {config.agents.map((agent, i) => (
          <div className="agent-row" key={i}>
            <input
              type="text"
              placeholder="name / skill"
              value={agent.name}
              onChange={(e) => updateAgent(i, { name: e.target.value })}
            />
            <input
              type="number"
              min={1}
              value={agent.kapacitet}
              onChange={(e) => updateAgent(i, { kapacitet: Number(e.target.value) })}
            />
            <button type="button" onClick={() => removeAgent(i)} aria-label="Remove agent">
              ×
            </button>
          </div>
        ))}
        <button type="button" className="add-agent-button" onClick={addAgent}>
          + Add agent
        </button>
        <span className="field-hint">
        </span>
      </div>

      {ticketTypes.length > 0 && (
        <div className="field-group">
          <span className="field-label">Ticket type distribution</span>
          {ticketTypes.map((type) => (
            <label key={type} className="weight-row">
              <span>{type}</span>
              <input
                type="number"
                min={0}
                step={0.1}
                value={config.tip_weights?.[type] ?? 1}
                onChange={(e) => updateWeight(type, Number(e.target.value))}
              />
            </label>
          ))}
          <span className="field-hint"></span>
        </div>
      )}

      <button
        className="run-button"
        onClick={onRun}
        disabled={loading || config.strategies.length === 0 || config.agents.length === 0}
      >
        {loading ? 'Running…' : 'Run simulation'}
      </button>
    </aside>
  )
}
