import React, { useState, useEffect } from 'react'
import { statsApi } from '../services/api'
import { theme } from '../theme'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const PlayerStats = ({ onNavigate }) => {
  console.log('PlayerStats component rendered with onNavigate:', onNavigate)
  const [playerStats, setPlayerStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [playerId, setPlayerId] = useState(null)

  useEffect(() => {
    const storedPlayerId = localStorage.getItem('selectedPlayerId')
    if (storedPlayerId) {
      setPlayerId(storedPlayerId)
      loadPlayerStats(storedPlayerId)
    } else {
      setError('No player selected')
      setLoading(false)
    }
  }, [])

  const loadPlayerStats = async (id) => {
    try {
      setLoading(true)
      const data = await statsApi.getPlayerStats(id)
      setPlayerStats(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const formatPercentage = (value) => {
    return `${(value * 100).toFixed(1)}%`
  }

  const formatDecimal = (value) => {
    return value.toFixed(2)
  }

  const getFormColor = (result) => {
    switch (result) {
      case 'W': return theme.colors.success
      case 'D': return theme.colors.warning
      case 'L': return theme.colors.error
      default: return theme.colors.textSecondary
    }
  }

  if (loading) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <div style={{ fontSize: '18px', color: theme.colors.textSecondary }}>Loading player stats...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <div style={{ fontSize: '18px', color: theme.colors.error }}>Error: {error}</div>
        <button
          onClick={() => onNavigate('teams')}
          style={{
            marginTop: '10px',
            padding: '8px 16px',
            backgroundColor: theme.colors.primary,
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Go Back
        </button>
      </div>
    )
  }

  if (!playerStats) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <div style={{ fontSize: '18px', color: theme.colors.textSecondary }}>No player stats found</div>
        <button
          onClick={() => onNavigate('teams')}
          style={{
            marginTop: '10px',
            padding: '8px 16px',
            backgroundColor: theme.colors.primary,
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Go Back
        </button>
      </div>
    )
  }

  const { player, form = [], goals_over_time = [] } = playerStats

  // Transform goals_over_time to include gameweek for x-axis
  const goalsChartData = goals_over_time.map((match, index) => ({
    ...match,
    gameweek: index + 1, // Use index + 1 as gameweek
    displayName: `GW${index + 1}` // Display name for x-axis
  }))

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ marginBottom: '30px' }}>
        <button
          onClick={() => onNavigate('teams')}
          style={{
            padding: '8px 16px',
            backgroundColor: 'transparent',
            color: theme.colors.primary,
            border: `1px solid ${theme.colors.primary}`,
            borderRadius: '4px',
            cursor: 'pointer',
            marginBottom: '20px'
          }}
        >
          ← Back
        </button>

        <h1 style={{
          fontSize: '32px',
          fontWeight: theme.typography.fontWeights.bold,
          color: theme.colors.textPrimary,
          margin: '0 0 10px 0'
        }}>
          {player.name} - Player Statistics
        </h1>
      </div>

      {/* Key Metrics Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '20px',
        marginBottom: '30px'
      }}>
        <MetricCard
          title="Total Appearances"
          value={playerStats.total_appearances}
          unit="games"
        />
        <MetricCard
          title="Total Goals"
          value={playerStats.total_goals}
          unit="goals"
        />
        <MetricCard
          title="Goals Per Game"
          value={formatDecimal(playerStats.goals_per_game)}
          unit="goals/game"
        />
        <MetricCard
          title="Win Rate"
          value={formatPercentage(playerStats.win_rate)}
          unit=""
        />
        <MetricCard
          title="Avg Goals Scored (Team)"
          value={formatDecimal(playerStats.avg_goals_scored_when_playing)}
          unit="goals/game"
        />
        <MetricCard
          title="Avg Goals Conceded (Team)"
          value={formatDecimal(playerStats.avg_goals_conceded_when_playing)}
          unit="goals/game"
        />
      </div>

      {/* Charts Section */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
        gap: '30px',
        marginBottom: '30px'
      }}>
        {/* Goals Over Time Chart */}
        <div style={{
          backgroundColor: theme.colors.backgroundSecondary,
          borderRadius: '8px',
          padding: '20px',
          border: `1px solid ${theme.colors.border}`
        }}>
          <h3 style={{
            fontSize: '20px',
            fontWeight: theme.typography.fontWeights.semibold,
            color: theme.colors.textPrimary,
            margin: '0 0 20px 0'
          }}>
            Goals Over Time
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={goalsChartData}>
              <CartesianGrid strokeDasharray="3 3" stroke={theme.colors.border} />
              <XAxis
                dataKey="displayName"
                angle={0}
                textAnchor="middle"
                height={60}
                fontSize={12}
                tick={{ fill: theme.colors.textSecondary }}
              />
              <YAxis tick={{ fill: theme.colors.textSecondary }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: theme.colors.backgroundPrimary,
                  border: `1px solid ${theme.colors.border}`,
                  borderRadius: '4px',
                  color: theme.colors.textPrimary
                }}
                labelStyle={{ color: theme.colors.textSecondary }}
                formatter={(value, name, props) => [
                  `${value} goals vs ${props.payload.opponent}`,
                  'Goals'
                ]}
                labelFormatter={(label) => `Gameweek ${label.replace("GW", "")} - ${goalsChartData.find(item => item.displayName === label)?.opponent || "Unknown"}`}
              />
              <Line
                type="monotone"
                dataKey="goals"
                stroke={theme.colors.primary}
                strokeWidth={3}
                dot={{ fill: theme.colors.primary, strokeWidth: 2, r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Form Chart */}
        <div style={{
          backgroundColor: theme.colors.backgroundSecondary,
          borderRadius: '8px',
          padding: '20px',
          border: `1px solid ${theme.colors.border}`
        }}>
          <h3 style={{
            fontSize: '20px',
            fontWeight: theme.typography.fontWeights.semibold,
            color: theme.colors.textPrimary,
            margin: '0 0 20px 0'
          }}>
            Recent Form (Last 5 Games)
          </h3>
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            height: '300px'
          }}>
            <div style={{
              display: 'flex',
              gap: '15px',
              flexWrap: 'wrap',
              justifyContent: 'center'
            }}>
              {form.map((result, index) => (
                <div
                  key={index}
                  style={{
                    width: '60px',
                    height: '60px',
                    borderRadius: '50%',
                    backgroundColor: getFormColor(result),
                    color: 'white',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '24px',
                    fontWeight: theme.typography.fontWeights.bold,
                    boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
                  }}
                >
                  {result}
                </div>
              ))}
            </div>
          </div>
          <div style={{
            textAlign: 'center',
            marginTop: '20px',
            fontSize: '14px',
            color: theme.colors.textSecondary
          }}>
            <span style={{ color: theme.colors.success }}>●</span> Win
            <span style={{ color: theme.colors.warning, marginLeft: '15px' }}>●</span> Draw
            <span style={{ color: theme.colors.error, marginLeft: '15px' }}>●</span> Loss
          </div>
        </div>
      </div>

      {/* Recent Matches Table */}
      <div style={{
        backgroundColor: theme.colors.backgroundSecondary,
        borderRadius: '8px',
        padding: '20px',
        border: `1px solid ${theme.colors.border}`
      }}>
        <h3 style={{
          fontSize: '20px',
          fontWeight: theme.typography.fontWeights.semibold,
          color: theme.colors.textPrimary,
          margin: '0 0 20px 0'
        }}>
          Recent Matches
        </h3>
        <div style={{ overflowX: 'auto' }}>
          <table style={{
            width: '100%',
            borderCollapse: 'collapse',
            fontSize: '14px'
          }}>
            <thead>
              <tr style={{
                backgroundColor: theme.colors.backgroundPrimary,
                borderBottom: `1px solid ${theme.colors.border}`
              }}>
                <th style={{ padding: '12px', textAlign: 'left', fontWeight: theme.typography.fontWeights.semibold, color: theme.colors.textPrimary }}>Date</th>
                <th style={{ padding: '12px', textAlign: 'left', fontWeight: theme.typography.fontWeights.semibold, color: theme.colors.textPrimary }}>Opponent</th>
                <th style={{ padding: '12px', textAlign: 'center', fontWeight: theme.typography.fontWeights.semibold, color: theme.colors.textPrimary }}>Score</th>
                <th style={{ padding: '12px', textAlign: 'center', fontWeight: theme.typography.fontWeights.semibold, color: theme.colors.textPrimary }}>Your Goals</th>
                <th style={{ padding: '12px', textAlign: 'center', fontWeight: theme.typography.fontWeights.semibold, color: theme.colors.textPrimary }}>Result</th>
              </tr>
            </thead>
            <tbody>
              {playerStats.recent_matches.map((match, index) => {
                const score1 = match.score1 || 0
                const score2 = match.score2 || 0
                const result = score1 > score2 ? 'W' : score1 === score2 ? 'D' : 'L'
                const resultColor = getFormColor(result)

                return (
                  <tr key={index} style={{
                    borderBottom: `1px solid ${theme.colors.border}`,
                    '&:hover': { backgroundColor: theme.colors.backgroundPrimary }
                  }}>
                    <td style={{ padding: '12px', color: theme.colors.textPrimary }}>
                      {new Date(match.played_at).toLocaleDateString()}
                    </td>
                    <td style={{ padding: '12px', color: theme.colors.textPrimary }}>
                      {match.opponents?.name || 'Unknown'}
                    </td>
                    <td style={{ padding: '12px', textAlign: 'center', color: theme.colors.textPrimary }}>
                      {score1} - {score2}
                    </td>
                    <td style={{ padding: '12px', textAlign: 'center', fontWeight: theme.typography.fontWeights.semibold, color: theme.colors.textPrimary }}>
                      {match.goals || 0}
                    </td>
                    <td style={{ padding: '12px', textAlign: 'center' }}>
                      <span style={{
                        color: resultColor,
                        fontWeight: theme.typography.fontWeights.bold
                      }}>
                        {result}
                      </span>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

const MetricCard = ({ title, value, unit }) => (
  <div style={{
    backgroundColor: theme.colors.backgroundSecondary,
    borderRadius: '8px',
    padding: '20px',
    border: `1px solid ${theme.colors.border}`,
    textAlign: 'center'
  }}>
    <div style={{
      fontSize: '14px',
      color: theme.colors.textSecondary,
      marginBottom: '8px',
      fontWeight: theme.typography.fontWeights.medium
    }}>
      {title}
    </div>
    <div style={{
      fontSize: '28px',
      fontWeight: theme.typography.fontWeights.bold,
      color: theme.colors.textPrimary,
      marginBottom: '4px'
    }}>
      {value}
    </div>
    <div style={{
      fontSize: '12px',
      color: theme.colors.textSecondary
    }}>
      {unit}
    </div>
  </div>
)

export default PlayerStats 