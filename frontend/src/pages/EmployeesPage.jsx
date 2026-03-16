import { useMemo, useState } from 'react'
import EmployeeDetailsPanel from '../components/employees/EmployeeDetailsPanel'
import EmployeeTable from '../components/employees/EmployeeTable'
import { getEmployees } from '../services/api'

function EmployeesPage() {
  const employees = getEmployees()
  const [search, setSearch] = useState('')
  const [riskLevel, setRiskLevel] = useState('All')
  const [selectedEmployeeId, setSelectedEmployeeId] = useState(
    employees[0]?.employee_id ?? null,
  )

  const filteredEmployees = useMemo(() => {
    const normalizedSearch = search.trim().toLowerCase()

    return employees.filter((employee) => {
      const matchesSearch =
        normalizedSearch.length === 0 ||
        employee.employee_id.toLowerCase().includes(normalizedSearch) ||
        employee.department.toLowerCase().includes(normalizedSearch) ||
        employee.position.toLowerCase().includes(normalizedSearch)

      const matchesRisk =
        riskLevel === 'All' || employee.risk_level === riskLevel

      return matchesSearch && matchesRisk
    })
  }, [employees, riskLevel, search])

  const selectedEmployee =
    filteredEmployees.find(
      (employee) => employee.employee_id === selectedEmployeeId,
    ) ?? filteredEmployees[0] ?? null

  return (
    <div className="space-y-6">
      <section className="overflow-hidden rounded-[32px] border border-white/80 bg-white/95 shadow-panel">
        <div className="bg-gradient-to-r from-brand-900 via-brand-800 to-brand-700 px-6 py-4 text-white">
          <p className="text-sm font-semibold uppercase tracking-[0.32em] text-brand-100">
            Employees
          </p>
        </div>
        <div className="p-6">
          <h1 className="mt-1 text-3xl font-semibold tracking-tight text-brand-900">
            Individual risk review
          </h1>
          <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-600 sm:text-base">
            Anonymized employee records keep the demo safe while still showing how
            HR can inspect risk scores, explanation factors, and actionable next
            steps from the future model API.
          </p>
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.25fr_0.9fr]">
        <EmployeeTable
          employees={filteredEmployees}
          filters={{ search, riskLevel }}
          onSearchChange={setSearch}
          onFilterChange={setRiskLevel}
          onSelectEmployee={setSelectedEmployeeId}
          selectedEmployeeId={selectedEmployee?.employee_id ?? null}
        />
        <EmployeeDetailsPanel employee={selectedEmployee} />
      </section>
    </div>
  )
}

export default EmployeesPage
