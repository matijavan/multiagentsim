import { useEffect, useState } from 'react'
import ConfigPanel from './components/ConfigPanel.jsx'
import SummaryCards from './components/SummaryCards.jsx'
import MetricsChart from './components/MetricsChart.jsx'
import ResultsTable from './components/ResultsTable.jsx'
import { fetchStrategies, runCompare } from './api.js'
import './App.css'

const DEFAULT_CONFIG = {
  strategies: ['round_robin', 'least_loaded', 'skill_based', 'hybrid'],
  broj_tiketa: 200,
  seed: 42,
  tocnost_proxyja: 1,
  duljina_tiketa: 6,
  agents: [
    { name: 'tehnicki', kapacitet: 3 },
    { name: 'naplata', kapacitet: 2 },
    { name: 'opci', kapacitet: 4 },
  ],
  tip_weights: {},
}

export default function App() {
  const [strategies, setStrategies] = useState([])
  const [config, setConfig] = useState(DEFAULT_CONFIG)
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [hasRun, setHasRun] = useState(false)

  useEffect(() => {
    fetchStrategies()
      .then(setStrategies)
      .catch(() => setError('Could not reach the backend. Is it running on port 8000?'))
  }, [])

  const handleRun = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await runCompare(config)
      setResults(data)
      setHasRun(true)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>Multi-agent scheduling simulator</h1>
        {/* <p className="app-subtitle">
          Compare routing strategies for ticket assignment, including the effect of an imperfect
          triage classifier on where tickets end up.
        </p> */}
      </header>

      <div className="app-layout">
        <ConfigPanel
          strategies={strategies}
          config={config}
          onChange={setConfig}
          onRun={handleRun}
          loading={loading}
        />

        <main className="results-area">
          {error && <div className="error-banner">{error}</div>}

          {!hasRun && !error && (
            <div className="panel empty-state">
              <div className="eyebrow">No run yet</div>
              <p>Pick strategies and settings on the left, then run a comparison to see results here.</p>
            </div>
          )}

          {hasRun && (
            <>
              <SummaryCards results={results} />
              <MetricsChart results={results} />
              <ResultsTable results={results} />
            </>
          )}
        </main>
      </div>
    </div>
  )
}
