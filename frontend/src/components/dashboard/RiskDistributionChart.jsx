import {
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from 'recharts'

const COLORS = ['#0070ad', '#12abdb', '#7ed8f1']

function RiskDistributionChart({ data }) {
  return (
    <div className="rounded-[28px] border border-white/80 bg-white/95 p-5 shadow-panel">
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-slate-900">
          Risk Distribution
        </h2>
        <p className="mt-1 text-sm text-slate-500">
          Current employee turnover exposure split by risk level.
        </p>
      </div>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              innerRadius={70}
              outerRadius={100}
              paddingAngle={4}
            >
              {data.map((entry, index) => (
                <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => [`${value} employees`, 'Count']} />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4 grid gap-3 sm:grid-cols-3">
        {data.map((item, index) => (
          <div key={item.name} className="rounded-2xl bg-slate-50 p-3">
            <div className="flex items-center gap-2">
              <span
                className="h-2.5 w-2.5 rounded-full"
                style={{ backgroundColor: COLORS[index % COLORS.length] }}
              />
              <p className="text-sm font-medium text-slate-700">{item.name}</p>
            </div>
            <p className="mt-2 text-2xl font-semibold text-brand-900">
              {item.value}
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default RiskDistributionChart
