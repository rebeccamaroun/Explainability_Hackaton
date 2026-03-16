import TopFactorsChart from '../components/dashboard/TopFactorsChart'
import EmployeeDetailsPanel from '../components/employees/EmployeeDetailsPanel'
import { getEmployees, getGlobalFeatureImportance } from '../services/api'

function ExplainableAIPage() {
  const featureImportance = getGlobalFeatureImportance()
  const exampleEmployee = getEmployees()[0]

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-[32px] border border-white/80 bg-white/95 shadow-panel">
        <div className="bg-gradient-to-r from-brand-900 via-brand-800 to-brand-700 px-6 py-4 text-white">
          <p className="text-sm font-semibold uppercase tracking-[0.32em] text-brand-100">
            Explainable AI
          </p>
        </div>
        <div className="p-6">
          <h1 className="mt-1 text-3xl font-semibold tracking-tight text-brand-900">
            Predictions people can understand
          </h1>
          <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-600 sm:text-base">
            Explainable AI helps HR teams understand why a resignation risk score
            appears, instead of treating the system like a black box. This makes
            the dashboard more trustworthy and easier to act on responsibly.
          </p>
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.05fr_1fr]">
        <TopFactorsChart
          data={featureImportance}
          title="Global Feature Importance"
          description="These are the strongest features the future model is expected to rely on across the organization."
        />
        <div className="rounded-[28px] border border-white/80 bg-white/95 p-6 shadow-panel">
          <h2 className="text-lg font-semibold text-brand-900">
            Why this matters
          </h2>
          <div className="mt-4 space-y-4 text-sm leading-7 text-slate-600">
            <p>
              HR can justify interventions with clear factors such as
              satisfaction, absences, and workload instead of opaque outputs.
            </p>
            <p>
              Employees remain anonymized in the dashboard, reducing exposure of
              sensitive personal information during demos and stakeholder reviews.
            </p>
            <p>
              The same structure can later receive SHAP-like factors or other
              explanation outputs directly from the API without redesigning the
              interface.
            </p>
          </div>
        </div>
      </section>

      <EmployeeDetailsPanel employee={exampleEmployee} />
    </div>
  )
}

export default ExplainableAIPage
