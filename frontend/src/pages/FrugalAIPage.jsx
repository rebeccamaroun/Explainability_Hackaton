import { getFrugalAIMetrics } from '../services/api'

function FrugalAIPage() {
  const metrics = getFrugalAIMetrics()

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-[32px] border border-white/80 bg-white/95 shadow-panel">
        <div className="bg-gradient-to-r from-brand-900 via-brand-800 to-brand-700 px-6 py-4 text-white">
          <p className="text-sm font-semibold uppercase tracking-[0.32em] text-brand-100">
            Frugal AI
          </p>
        </div>
        <div className="p-6">
          <h1 className="mt-1 text-3xl font-semibold tracking-tight text-brand-900">
            Lightweight by design
          </h1>
          <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-600 sm:text-base">
            This project prioritizes efficient machine learning approaches rather
            than heavy deep learning models. The goal is faster experimentation,
            easier deployment, lower compute cost, and a smaller environmental
            footprint.
          </p>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {metrics.map((metric) => (
          <article
            key={metric.label}
            className="rounded-[28px] border border-white/80 bg-white/95 p-5 shadow-panel"
          >
            <p className="text-sm font-medium text-slate-500">{metric.label}</p>
            <p className="mt-3 text-3xl font-semibold text-brand-900">
              {metric.value}
            </p>
          </article>
        ))}
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-[28px] border border-white/80 bg-white/95 p-6 shadow-panel">
          <h2 className="text-lg font-semibold text-brand-900">
            Frugal AI principles
          </h2>
          <ul className="mt-4 space-y-3 text-sm leading-7 text-slate-600">
            <li>Use compact feature sets that still preserve useful signal.</li>
            <li>Prefer interpretable models that train faster and cost less.</li>
            <li>Reduce inference overhead for easier real-world HR adoption.</li>
            <li>Track efficiency metrics alongside accuracy during model work.</li>
          </ul>
        </div>
        <div className="rounded-[28px] border border-brand-100 bg-brand-50 p-6 shadow-panel">
          <h2 className="text-lg font-semibold text-brand-900">
            Placeholder model metrics
          </h2>
          <p className="mt-4 text-sm leading-7 text-brand-900">
            These values are intentionally marked as pending because the modeling
            team is still finalizing the approach. Once the API is ready, this
            page can display actual efficiency metrics without changing the UI
            layout.
          </p>
        </div>
      </section>
    </div>
  )
}

export default FrugalAIPage
