export default function ResultsTable({ results }) {
  if (!results.length) return null

  return (
    <div className="panel table-panel">
      <div className="eyebrow">Full results</div>
      <div className="table-scroll">
        <table>
          <thead>
            <tr>
              <th>Strategy</th>
              <th>Avg wait</th>
              <th>Avg response</th>
              <th>Max wait</th>
              <th>P95 wait</th>
              <th>Urgent avg wait</th>
              <th>Tickets served</th>
            </tr>
          </thead>
          <tbody>
            {results.map((r) => (
              <tr key={r.strategy}>
                <td className="table-strategy">{r.label}</td>
                <td>{r.prosjecno_cekanje.toFixed(2)}</td>
                <td>{r.prosjecan_odziv.toFixed(2)}</td>
                <td>{r.max_cekanje.toFixed(2)}</td>
                <td>{r.p95_cekanje.toFixed(2)}</td>
                <td>{r.prosjecno_cekanje_urgent.toFixed(2)}</td>
                <td>{r.broj_tiketa_obradeno}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
