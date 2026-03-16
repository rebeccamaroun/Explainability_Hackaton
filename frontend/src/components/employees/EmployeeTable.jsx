import RiskBadge from './RiskBadge'

function EmployeeTable({
  employees,
  filters,
  onSearchChange,
  onFilterChange,
  onSelectEmployee,
  selectedEmployeeId,
}) {
  return (
    <section className="rounded-[28px] border border-white/80 bg-white/95 p-5 shadow-panel">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            Employee Risk Dashboard
          </h2>
          <p className="mt-1 text-sm text-slate-500">
            Review anonymized employees and inspect individual risk drivers.
          </p>
        </div>
        <div className="flex flex-col gap-3 sm:flex-row">
          <input
            type="search"
            value={filters.search}
            onChange={(event) => onSearchChange(event.target.value)}
            placeholder="Search employee or department"
            className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700 outline-none transition focus:border-brand-500 focus:bg-white sm:w-72"
          />
          <select
            value={filters.riskLevel}
            onChange={(event) => onFilterChange(event.target.value)}
            className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700 outline-none transition focus:border-brand-500 focus:bg-white"
          >
            <option value="All">All risk levels</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
        </div>
      </div>

      <div className="mt-6 overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200">
          <thead>
            <tr className="text-left text-xs uppercase tracking-[0.2em] text-slate-400">
              <th className="pb-3 pr-4">Employee ID</th>
              <th className="pb-3 pr-4">Department</th>
              <th className="pb-3 pr-4">Position</th>
              <th className="pb-3 pr-4">Risk Score</th>
              <th className="pb-3 pr-4">Risk Level</th>
              <th className="pb-3 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {employees.map((employee) => (
              <tr key={employee.employee_id} className="text-sm text-slate-600">
                <td className="py-4 pr-4 font-semibold text-slate-900">
                  {employee.employee_id}
                </td>
                <td className="py-4 pr-4">{employee.department}</td>
                <td className="py-4 pr-4">{employee.position}</td>
                <td className="py-4 pr-4">
                  {(employee.risk_score * 100).toFixed(0)}%
                </td>
                <td className="py-4 pr-4">
                  <RiskBadge level={employee.risk_level} />
                </td>
                <td className="py-4 text-right">
                  <button
                    type="button"
                    onClick={() => onSelectEmployee(employee.employee_id)}
                    className={`rounded-2xl px-4 py-2 text-sm font-medium transition ${
                      selectedEmployeeId === employee.employee_id
                        ? 'bg-brand-700 text-white'
                        : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                    }`}
                  >
                    Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {employees.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-slate-200 bg-slate-50 px-4 py-10 text-center text-sm text-slate-500">
            No employees match the current filters.
          </div>
        ) : null}
      </div>
    </section>
  )
}

export default EmployeeTable
