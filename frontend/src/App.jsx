import { Suspense, lazy } from 'react'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import Sidebar from './components/common/Sidebar'

const OverviewPage = lazy(() => import('./pages/OverviewPage'))
const EmployeesPage = lazy(() => import('./pages/EmployeesPage'))
const ExplainableAIPage = lazy(() => import('./pages/ExplainableAIPage'))
const FrugalAIPage = lazy(() => import('./pages/FrugalAIPage'))

function AppLayout() {
  return (
    <div className="min-h-screen bg-transparent text-slate-900">
      <div className="mx-auto flex min-h-screen max-w-[1440px] flex-col lg:flex-row">
        <Sidebar />
        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          <Suspense
            fallback={
              <div className="rounded-[28px] border border-white/70 bg-white/90 p-6 text-sm text-slate-500 shadow-panel">
                Loading dashboard...
              </div>
            }
          >
            <Routes>
              <Route path="/" element={<Navigate to="/overview" replace />} />
              <Route path="/overview" element={<OverviewPage />} />
              <Route path="/employees" element={<EmployeesPage />} />
              <Route
                path="/explainable-ai"
                element={<ExplainableAIPage />}
              />
              <Route path="/frugal-ai" element={<FrugalAIPage />} />
            </Routes>
          </Suspense>
        </main>
      </div>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <AppLayout />
    </BrowserRouter>
  )
}

export default App
