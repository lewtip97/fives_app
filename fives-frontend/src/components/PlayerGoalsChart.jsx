import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { theme } from '../theme'

function PlayerGoalsChart({ data, title = "Player Goals Over Time" }) {
  if (!data || data.length === 0) {
    return (
      <div style={{ 
        textAlign: 'center', 
        padding: 40,
        color: theme.colors.textSecondary,
        fontFamily: theme.typography.fontFamily,
      }}>
        <div style={{ fontSize: '16px', marginBottom: 8 }}>No data available</div>
        <div style={{ fontSize: '14px' }}>Add some matches to see player goals</div>
      </div>
    )
  }

  // Transform data for the chart
  const chartData = data.map(item => ({
    gameweek: item.gameweek,
    goals: item.goals,
    cumulativeGoals: item.cumulative_goals,
  }))

  return (
    <div style={{
      ...theme.styles.card,
      padding: 24,
      marginBottom: 24,
    }}>
      <h3 style={{ 
        fontSize: '18px', 
        fontWeight: theme.typography.fontWeights.semibold,
        color: theme.colors.textPrimary,
        fontFamily: theme.typography.fontFamily,
        marginBottom: 16,
      }}>
        {title}
      </h3>
      
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke={theme.colors.border} />
          <XAxis 
            dataKey="gameweek" 
            stroke={theme.colors.textSecondary}
            fontFamily={theme.typography.fontFamily}
            fontSize={12}
          />
          <YAxis 
            stroke={theme.colors.textSecondary}
            fontFamily={theme.typography.fontFamily}
            fontSize={12}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: theme.colors.card,
              border: `1px solid ${theme.colors.border}`,
              borderRadius: 8,
              color: theme.colors.textPrimary,
              fontFamily: theme.typography.fontFamily,
            }}
          />
          <Legend 
            wrapperStyle={{
              fontFamily: theme.typography.fontFamily,
              color: theme.colors.textPrimary,
            }}
          />
          <Line 
            type="monotone" 
            dataKey="goals" 
            stroke={theme.colors.primary} 
            strokeWidth={2}
            dot={{ fill: theme.colors.primary, strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6, stroke: theme.colors.primary, strokeWidth: 2 }}
            name="Goals This Week"
          />
          <Line 
            type="monotone" 
            dataKey="cumulativeGoals" 
            stroke={theme.colors.error} 
            strokeWidth={2}
            dot={{ fill: theme.colors.error, strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6, stroke: theme.colors.error, strokeWidth: 2 }}
            name="Total Goals"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default PlayerGoalsChart 