import TopFactorsChart from '../dashboard/TopFactorsChart'
import RiskBadge from './RiskBadge'

function EmployeeDetailsPanel({ employee }) {
  if (!employee) {
    return (
      <aside className="rounded-[28px] border border-dashed border-slate-300 bg-white/75 p-6 shadow-panel">
        <h2 className="text-lg font-semibold text-slate-900">
          Employee Detail Panel
        </h2>
        <p className="mt-2 text-sm leading-6 text-slate-500">
          Select an employee from the table to inspect explainable AI factors
          and suggested HR actions.
        </p>
      </aside>
    )
  }

  const chartData = employee.top_factors.map((factor) => ({
    name: factor.name,
    value: Number((factor.impact * 100).toFixed(0)),
  }))

  return (
    <aside className="space-y-6 rounded-[28px] border border-white/80 bg-white/95 p-6 shadow-panel">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">
          Selected employee
        </p>
        <div className="mt-3 flex flex-wrap items-center gap-3">
          <h2 className="text-2xl font-semibold text-slate-900">
            {employee.employee_id}
          </h2>
          <RiskBadge level={employee.risk_level} />
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div className="rounded-2xl bg-slate-50 p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-slate-400">
            Department
          </p>
          <p className="mt-2 font-semibold text-slate-900">
            {employee.department}
          </p>
        </div>
        <div className="rounded-2xl bg-slate-50 p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-slate-400">
            Position
          </p>
          <p className="mt-2 font-semibold text-slate-900">
            {employee.position}
          </p>
        </div>
        <div className="rounded-2xl bg-slate-50 p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-slate-400">
            Risk score
          </p>
          <p className="mt-2 font-semibold text-slate-900">
            {(employee.risk_score * 100).toFixed(0)}%
          </p>
        </div>
        <div className="rounded-2xl bg-slate-50 p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-slate-400">
            Status
          </p>
          <p className="mt-2 font-semibold text-slate-900">
            {employee.risk_level} attention needed
          </p>
        </div>
      </div>

      <TopFactorsChart
        data={chartData}
        title="Explainable AI Factors"
        description="Top drivers contributing to this employee's predicted turnover risk."
      />

      <div className="rounded-[28px] border border-brand-100 bg-brand-50 p-5">
        <h3 className="text-lg font-semibold text-brand-900">
          HR Recommendations
        </h3>
        <ul className="mt-4 space-y-3 text-sm text-brand-900">
          {employee.recommendations.map((recommendation) => (
            <li key={recommendation} className="rounded-2xl border border-white bg-white/80 p-3">
              {recommendation}
            </li>
          ))}
        </ul>
      </div>
    </aside>
  )
}

export default EmployeeDetailsPanel
