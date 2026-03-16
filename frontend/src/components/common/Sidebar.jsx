import { NavLink } from 'react-router-dom'
import { NAV_ITEMS } from '../../utils/constants'

function Sidebar() {
  return (
    <aside className="border-b border-slate-200 bg-white/95 text-slate-900 backdrop-blur lg:min-h-screen lg:w-80 lg:border-b-0 lg:border-r lg:border-r-slate-200">
      <div className="sticky top-0 p-4 sm:p-6">
        <div
          className="rounded-[28px] border p-6 text-white shadow-executive"
          style={{
            background:
              'linear-gradient(135deg, #072b57 0%, #0c3c78 55%, #0070ad 100%)',
            borderColor: 'rgba(7, 43, 87, 0.22)',
          }}
        >
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-white/85">
            Capgemini
          </p>
          <h1 className="mt-3 text-2xl font-semibold">
            Employee Retention Dashboard
          </h1>
          <p className="mt-3 text-sm leading-6 text-white/92">
            Client-facing prototype for employee turnover insights, explainability, and efficient AI.
          </p>
          <div
            className="mt-5 rounded-2xl border p-4"
            style={{
              backgroundColor: 'rgba(255, 255, 255, 0.12)',
              borderColor: 'rgba(255, 255, 255, 0.22)',
            }}
          >
            <p className="text-[11px] font-semibold uppercase tracking-[0.28em] text-white/80">
              Client context
            </p>
            <p className="mt-2 text-sm leading-6 text-white/92">
              Structured for stakeholder demos, executive reviews, and later API integration.
            </p>
          </div>
        </div>

        <nav className="mt-6 space-y-2">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                [
                  'flex items-center justify-between rounded-2xl border px-4 py-3 text-sm font-medium transition',
                  isActive
                    ? 'border-brand-200 bg-brand-50 text-brand-900 shadow-sm'
                    : 'border-transparent bg-slate-50 text-slate-700 hover:border-slate-200 hover:bg-white hover:text-slate-900',
                ].join(' ')
              }
            >
              <span>{item.label}</span>
              <span className="text-xs uppercase tracking-[0.2em] text-slate-400">
                {item.shortLabel}
              </span>
            </NavLink>
          ))}
        </nav>

        <div className="mt-6 rounded-[28px] border border-brand-100 bg-brand-50 p-5">
          <p className="text-xs font-semibold uppercase tracking-[0.3em] text-brand-800">
            Delivery principles
          </p>
          <ul className="mt-3 space-y-3 text-sm leading-6 text-brand-900">
            <li>Explain predictions with transparent feature drivers.</li>
            <li>Favor lightweight models with lower compute cost.</li>
            <li>Protect privacy with anonymized employee records.</li>
          </ul>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
