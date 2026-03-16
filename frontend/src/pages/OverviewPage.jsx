import RiskDistributionChart from '../components/dashboard/RiskDistributionChart'
import TopFactorsChart from '../components/dashboard/TopFactorsChart'
import StatCard from '../components/common/StatCard'
import { getDashboardData } from '../services/api'

function OverviewPage() {
  const { overviewStats, riskDistribution, topResignationFactors } =
    getDashboardData()

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-[32px] border border-white/80 bg-white/95 shadow-panel">
        <div className="bg-gradient-to-r from-brand-900 via-brand-800 to-brand-700 px-6 py-4 text-white">
          <p className="text-sm font-semibold uppercase tracking-[0.32em] text-brand-100">
            Overview
          </p>
        </div>
        <div className="p-6">
          <div className="mt-1 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl">
              <h1 className="text-3xl font-semibold tracking-tight text-brand-900 sm:text-4xl">
                Capgemini client dashboard for retention intelligence
              </h1>
              <p className="mt-3 text-sm leading-7 text-slate-600 sm:text-base">
                This dashboard uses mock data to show how employee turnover risk,
                explainability, and frugal AI reporting can be presented in a
                client-ready format without exposing sensitive personal information.
              </p>
            </div>
            <div className="rounded-2xl border border-brand-100 bg-brand-50 px-4 py-3 text-sm font-medium text-brand-800">
              Mock mode active. Model integration is pending.
            </div>
          </div>
          <div className="mt-6 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
                Client lens
              </p>
              <p className="mt-2 text-sm text-slate-600">
                Organized for HR leaders, delivery teams, and hackathon judges.
              </p>
            </div>
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
                Explainability
              </p>
              <p className="mt-2 text-sm text-slate-600">
                Transparent drivers support trust and clearer interventions.
              </p>
            </div>
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
                Efficiency
              </p>
              <p className="mt-2 text-sm text-slate-600">
                Frugal AI framing keeps the product lightweight and practical.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {overviewStats.map((stat) => (
          <StatCard key={stat.title} {...stat} />
        ))}
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.05fr_1fr]">
        <RiskDistributionChart data={riskDistribution} />
        <TopFactorsChart data={topResignationFactors} />
      </section>
    </div>
  )
}

export default OverviewPage
