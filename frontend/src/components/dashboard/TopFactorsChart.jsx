import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

function TopFactorsChart({
  data,
  title = 'Top Resignation Factors',
  description,
}) {
  return (
    <div className="rounded-[28px] border border-white/80 bg-white/95 p-5 shadow-panel">
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-slate-900">{title}</h2>
        <p className="mt-1 text-sm text-slate-500">
          {description ??
            'Most influential factors connected to predicted resignation.'}
        </p>
      </div>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ left: 12 }}>
            <CartesianGrid stroke="#e2e8f0" horizontal={false} />
            <XAxis type="number" tick={{ fill: '#64748b', fontSize: 12 }} />
            <YAxis
              dataKey="name"
              type="category"
              width={120}
              tick={{ fill: '#475569', fontSize: 12 }}
            />
            <Tooltip />
            <Bar dataKey="value" radius={[0, 8, 8, 0]} fill="#0070ad" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default TopFactorsChart
