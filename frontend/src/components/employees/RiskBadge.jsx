import { RISK_BADGE_STYLES } from '../../utils/constants'

function RiskBadge({ level }) {
  return (
    <span
      className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${RISK_BADGE_STYLES[level] ?? RISK_BADGE_STYLES.Low}`}
    >
      {level}
    </span>
  )
}

export default RiskBadge
