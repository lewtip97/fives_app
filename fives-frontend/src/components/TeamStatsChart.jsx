import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts'
import { theme } from '../theme'

function TeamStatsChart({ data, title = "Team Performance" }) {
  if (!data || data.length === 0) {
    return (
      <div style={{ 
        textAlign: 'center', 
        padding: 40,
        color: theme.colors.textSecondary,
        fontFamily: theme.typography.fontFamily,
      }}>
        <div style={{ fontSize: '16px', marginBottom: 8 }}>No data available</div>
        <div style={{ fontSize: '14px' }}>Add some matches to see team performance</div>
      </div>
    )
  }

  // Transform data for the chart
  const chartData = data.map(item => ({
    gameweek: item.gameweek,
    goalsScored: item.goals_scored,
    goalsConceded: item.goals_conceded,
    wins: item.wins,
    losses: item.losses,
    draws: item.draws,
    winRate: item.win_rate,
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
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
        {/* Goals Chart */}
        <div>
          <h4 style={{ 
            fontSize: '16px', 
            fontWeight: theme.typography.fontWeights.medium,
            color: theme.colors.textPrimary,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 12,
            textAlign: 'center',
          }}>
            Goals Scored vs Conceded
          </h4>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke={theme.colors.border} />
              <XAxis 
                dataKey="gameweek" 
                stroke={theme.colors.textSecondary}
                fontFamily={theme.typography.fontFamily}
                fontSize={10}
              />
              <YAxis 
                stroke={theme.colors.textSecondary}
                fontFamily={theme.typography.fontFamily}
                fontSize={10}
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
                  fontSize: 10,
                }}
              />
              <Bar 
                dataKey="goalsScored" 
                fill={theme.colors.primary} 
                name="Goals Scored"
              />
              <Bar 
                dataKey="goalsConceded" 
                fill={theme.colors.error} 
                name="Goals Conceded"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Win Rate Chart */}
        <div>
          <h4 style={{ 
            fontSize: '16px', 
            fontWeight: theme.typography.fontWeights.medium,
            color: theme.colors.textPrimary,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 12,
            textAlign: 'center',
          }}>
            Win Rate Over Time
          </h4>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke={theme.colors.border} />
              <XAxis 
                dataKey="gameweek" 
                stroke={theme.colors.textSecondary}
                fontFamily={theme.typography.fontFamily}
                fontSize={10}
              />
              <YAxis 
                stroke={theme.colors.textSecondary}
                fontFamily={theme.typography.fontFamily}
                fontSize={10}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: theme.colors.card,
                  border: `1px solid ${theme.colors.border}`,
                  borderRadius: 8,
                  color: theme.colors.textPrimary,
                  fontFamily: theme.typography.fontFamily,
                }}
                formatter={(value) => [`${(value * 100).toFixed(1)}%`, 'Win Rate']}
              />
              <Line 
                type="monotone" 
                dataKey="winRate" 
                stroke={theme.colors.primary} 
                strokeWidth={2}
                dot={{ fill: theme.colors.primary, strokeWidth: 2, r: 3 }}
                activeDot={{ r: 5, stroke: theme.colors.primary, strokeWidth: 2 }}
                name="Win Rate"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}

export default TeamStatsChart 