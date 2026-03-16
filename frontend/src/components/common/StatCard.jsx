function StatCard({ title, value, subtitle, accent = 'bg-brand-500' }) {
  return (
    <article className="rounded-[28px] border border-white/80 bg-white/95 p-5 shadow-panel">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-slate-500">{title}</p>
          <p className="mt-3 text-3xl font-semibold text-brand-900">{value}</p>
        </div>
        <span className={`mt-1 h-3 w-3 rounded-full ${accent}`} />
      </div>
      <div className="mt-4 border-t border-slate-100 pt-4">
        <p className="text-sm text-slate-500">{subtitle}</p>
      </div>
    </article>
  )
}

export default StatCard
