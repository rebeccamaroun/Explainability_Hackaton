import {
  frugalAIMetrics,
  globalFeatureImportance,
  overviewStats,
  riskDistribution,
  topResignationFactors,
} from '../data/dashboard'
import { employees } from '../data/employees'

export function getEmployees() {
  // Future API integration: replace this mock return with a fetch call.
  return employees
}

export function getEmployeeById(employeeId) {
  // Future API integration: fetch a single employee explanation payload here.
  return employees.find((employee) => employee.employee_id === employeeId) ?? null
}

export function getDashboardData() {
  // Future API integration: aggregate overview metrics from the backend service.
  return { overviewStats, riskDistribution, topResignationFactors }
}

export function getGlobalFeatureImportance() {
  // Future API integration: return model-level explainability metrics here.
  return globalFeatureImportance
}

export function getFrugalAIMetrics() {
  // Future API integration: surface model efficiency metrics when available.
  return frugalAIMetrics
}
