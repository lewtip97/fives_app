import { useState, useEffect } from 'react'
import { theme } from '../theme'
import { statsApi, teamsApi, playersApi } from '../services/api'
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

function Stats({ user, selectedTeamId, onViewPlayerStats }) {
  const [teams, setTeams] = useState([])
  const [selectedTeam, setSelectedTeam] = useState(null)
  const [teamStats, setTeamStats] = useState(null)
  const [playerStats, setPlayerStats] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadTeams()
  }, [])

  useEffect(() => {
    if (selectedTeamId && teams.length > 0) {
      const team = teams.find(t => t.id === selectedTeamId)
      if (team) {
        setSelectedTeam(team)
      }
    } else if (teams.length > 0 && !selectedTeam) {
      setSelectedTeam(teams[0])
    }
  }, [selectedTeamId, teams])

  useEffect(() => {
    if (selectedTeam) {
      loadTeamStats()
    }
  }, [selectedTeam])

  const loadTeams = async () => {
    try {
      const teamsData = await teamsApi.getTeams()
      setTeams(teamsData)
      if (teamsData.length > 0) {
        setSelectedTeam(teamsData[0])
      }
    } catch (error) {
      console.error('Error loading teams:', error)
      setError('Failed to load teams')
    }
  }

  const loadTeamStats = async () => {
    if (!selectedTeam) return
    
    setLoading(true)
    setError(null)
    
    try {
      // Load comprehensive team overview
      const teamOverview = await statsApi.getTeamOverview(selectedTeam.id)
      
      setTeamStats(teamOverview)
      setPlayerStats(teamOverview.player_stats || [])
    } catch (error) {
      console.error('Error loading team stats:', error)
      setError('Failed to load team statistics')
    } finally {
      setLoading(false)
    }
  }

  const calculateTeamForm = (matches) => {
    if (!matches || matches.length === 0) return []
    
    // Sort matches by date (most recent first)
    const sortedMatches = matches.sort((a, b) => new Date(b.played_at) - new Date(a.played_at))
    
    // Take last 5 matches
    const last5Matches = sortedMatches.slice(0, 5)
    
    return last5Matches.map(match => {
      const isWin = match.score1 > match.score2
      const isDraw = match.score1 === match.score2
      const isLoss = match.score1 < match.score2
      
      return {
        gameweek: match.gameweek,
        result: isWin ? 'W' : isDraw ? 'D' : 'L',
        score: `${match.score1}-${match.score2}`,
        opponent: match.opponent_name,
        color: isWin ? theme.colors.success : isDraw ? theme.colors.warning : theme.colors.error
      }
    })
  }

  const calculatePointsOverTime = (matches) => {
    if (!matches || matches.length === 0) return []
    
    // Sort matches by gameweek
    const sortedMatches = matches.sort((a, b) => a.gameweek - b.gameweek)
    
    let cumulativePoints = 0
    return sortedMatches.map(match => {
      const isWin = match.score1 > match.score2
      const isDraw = match.score1 === match.score2
      
      if (isWin) cumulativePoints += 3
      else if (isDraw) cumulativePoints += 1
      // Loss = 0 points
      
      return {
        gameweek: match.gameweek,
        points: cumulativePoints,
        matchResult: isWin ? 'W' : isDraw ? 'D' : 'L'
      }
    })
  }

  const getTopPlayers = () => {
    try {
      
      if (!playerStats || playerStats.length === 0) {
        return { appearances: [], goals: [] }
      }
      
      const playerTotals = {}
      
      playerStats.forEach((stat, index) => {
        if (!stat || !stat.player_id) {
          return
        }
        
        const playerId = stat.player_id
        if (!playerTotals[playerId]) {
          playerTotals[playerId] = {
            player_id: playerId,
            player_name: stat.player_name || 'Unknown',
            profile_picture: stat.profile_picture,
            total_appearances: stat.total_appearances || 0,  // Use the backend's calculated total
            total_goals: stat.total_goals || 0              // Use the backend's calculated total
          }
        }
        // No need to modify totals - they're already correct from the backend
        
      })
      
      const players = Object.values(playerTotals)
      
      return {
        appearances: players
          .sort((a, b) => b.total_appearances - a.total_appearances)
          .slice(0, 5),
        goals: players
          .sort((a, b) => b.total_goals - a.total_goals)
          .slice(0, 5)
      }
    } catch (error) {
      console.error('Error in getTopPlayers:', error)
      return { appearances: [], goals: [] }
    }
  }

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: 40 }}>
        <div style={{ color: theme.colors.textSecondary }}>Loading statistics...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div style={{ textAlign: 'center', padding: 40 }}>
        <div style={{ color: theme.colors.error }}>{error}</div>
        <button
          onClick={loadTeamStats}
          style={{
            ...theme.styles.button.primary,
            marginTop: 16,
          }}
        >
          Retry
        </button>
      </div>
    )
  }

  if (!selectedTeam) {
    return (
      <div style={{ textAlign: 'center', padding: 40 }}>
        <div style={{ color: theme.colors.textSecondary }}>No teams available</div>
      </div>
    )
  }

  if (!teamStats) {
    return (
      <div style={{ textAlign: 'center', padding: 40 }}>
        <div style={{ color: theme.colors.textSecondary }}>No team statistics available</div>
      </div>
    )
  }

  const topPlayers = getTopPlayers()
  const teamForm = calculateTeamForm(teamStats?.matches || [])
  const pointsOverTime = calculatePointsOverTime(teamStats?.matches || [])

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto' }}>
      {/* Header */}
      <div style={{ marginBottom: 32 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 16 }}>
          <h1 style={{ 
            fontSize: '32px', 
            fontWeight: theme.typography.fontWeights.bold,
            color: theme.colors.primary,
            fontFamily: theme.typography.fontFamily,
            margin: 0,
          }}>
            Team Statistics
          </h1>
          
          <select
            value={selectedTeam?.id || ''}
            onChange={(e) => setSelectedTeam(teams.find(t => t.id === e.target.value))}
            style={{
              ...theme.styles.input,
              minWidth: 200,
            }}
          >
            {teams.map(team => (
              <option key={team.id} value={team.id}>
                {team.name}
              </option>
            ))}
          </select>
        </div>
        
        <p style={{ 
          fontSize: '16px', 
          color: theme.colors.textSecondary,
          fontFamily: theme.typography.fontFamily,
        }}>
          Comprehensive statistics and performance analytics for {selectedTeam.name}
        </p>
      </div>

      {/* Key Metrics */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: 24,
        marginBottom: 32,
      }}>
        <div style={{
          ...theme.styles.card,
          padding: 24,
          textAlign: 'center',
        }}>
          <div style={{
            fontSize: '32px',
            fontWeight: theme.typography.fontWeights.bold,
            color: theme.colors.primary,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 8,
          }}>
            {teamStats?.total_matches || 0}
          </div>
          <div style={{
            fontSize: '14px',
            color: theme.colors.textSecondary,
            fontFamily: theme.typography.fontFamily,
          }}>
            Total Matches
          </div>
        </div>

        <div style={{
          ...theme.styles.card,
          padding: 24,
          textAlign: 'center',
        }}>
          <div style={{
            fontSize: '32px',
            fontWeight: theme.typography.fontWeights.bold,
            color: theme.colors.success,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 8,
          }}>
            {teamStats?.win_percentage ? `${(teamStats.win_percentage * 100).toFixed(1)}%` : '0%'}
          </div>
          <div style={{
            fontSize: '14px',
            color: theme.colors.textSecondary,
            fontFamily: theme.typography.fontFamily,
          }}>
            Win Rate
          </div>
        </div>

        <div style={{
          ...theme.styles.card,
          padding: 24,
          textAlign: 'center',
        }}>
          <div style={{
            fontSize: '32px',
            fontWeight: theme.typography.fontWeights.bold,
            color: theme.colors.primary,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 8,
          }}>
            {teamStats?.total_goals_scored || 0}
          </div>
          <div style={{
            fontSize: '14px',
            color: theme.colors.textSecondary,
            fontFamily: theme.typography.fontFamily,
          }}>
            Goals Scored
          </div>
        </div>

        <div style={{
          ...theme.styles.card,
          padding: 24,
          textAlign: 'center',
        }}>
          <div style={{
            fontSize: '32px',
            fontWeight: theme.typography.fontWeights.bold,
            color: theme.colors.error,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 8,
          }}>
            {teamStats?.total_goals_conceded || 0}
          </div>
          <div style={{
            fontSize: '14px',
            color: theme.colors.textSecondary,
            fontFamily: theme.typography.fontFamily,
          }}>
            Goals Conceded
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))',
        gap: 32,
        marginBottom: 32,
      }}>
        {/* Team Form - Last 5 Games */}
        <div style={{
          ...theme.styles.card,
          padding: 24,
        }}>
          <h3 style={{
            fontSize: '20px',
            fontWeight: theme.typography.fontWeights.semibold,
            color: theme.colors.textPrimary,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 16,
          }}>
            Team Form - Last 5 Games
          </h3>
          
          <div style={{
            display: 'flex',
            gap: 12,
            justifyContent: 'center',
            flexWrap: 'wrap',
          }}>
            {teamForm.map((match, index) => (
              <div
                key={index}
                style={{
                  width: 60,
                  height: 60,
                  borderRadius: '50%',
                  background: match.color,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontSize: '20px',
                  fontWeight: theme.typography.fontWeights.bold,
                  fontFamily: theme.typography.fontFamily,
                  boxShadow: theme.colors.shadowLight,
                }}
                title={`Gameweek ${match.gameweek}: ${match.result} ${match.score} vs ${match.opponent}`}
              >
                {match.result}
              </div>
            ))}
            {teamForm.length === 0 && (
              <div style={{
                color: theme.colors.textMuted,
                fontFamily: theme.typography.fontFamily,
                fontStyle: 'italic',
              }}>
                No recent matches
              </div>
            )}
          </div>
        </div>

        {/* Points Over Time */}
        <div style={{
          ...theme.styles.card,
          padding: 24,
        }}>
          <h3 style={{
            fontSize: '20px',
            fontWeight: theme.typography.fontWeights.semibold,
            color: theme.colors.textPrimary,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 16,
          }}>
            Points Over Time
          </h3>
          
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={pointsOverTime}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="gameweek" />
              <YAxis />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="points" 
                stroke={theme.colors.primary} 
                strokeWidth={3}
                dot={{ fill: theme.colors.primary, strokeWidth: 2, r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Player Statistics */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
        gap: 32,
      }}>
        {/* Most Appearances */}
        <div style={{
          ...theme.styles.card,
          padding: 24,
        }}>
          <h3 style={{
            fontSize: '20px',
            fontWeight: theme.typography.fontWeights.semibold,
            color: theme.colors.textPrimary,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 16,
          }}>
            Most Appearances
          </h3>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {topPlayers.appearances.map((player, index) => (
              <div key={player.player_id} style={{
                display: 'flex',
                alignItems: 'center',
                gap: 12,
                padding: 12,
                background: theme.colors.content,
                borderRadius: 8,
                border: `1px solid ${theme.colors.border}`,
              }}>
                <div style={{
                  width: 40,
                  height: 40,
                  borderRadius: '50%',
                  overflow: 'hidden',
                  background: theme.colors.primary,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontSize: '16px',
                  fontWeight: theme.typography.fontWeights.bold,
                }}>
                  {player.profile_picture ? (
                    <img 
                      src={player.profile_picture} 
                      alt={player.player_name}
                      style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                    />
                  ) : (
                    player.player_name.charAt(0).toUpperCase()
                  )}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{
                    fontSize: '16px',
                    fontWeight: theme.typography.fontWeights.semibold,
                    color: theme.colors.textPrimary,
                    fontFamily: theme.typography.fontFamily,
                  }}>
                    {player.player_name}
                  </div>
                  <div style={{
                    fontSize: '14px',
                    color: theme.colors.textSecondary,
                    fontFamily: theme.typography.fontFamily,
                  }}>
                    {player.total_appearances} appearances
                  </div>
                </div>
                <button
                  onClick={() => onViewPlayerStats(player.player_id)}
                  style={{
                    padding: '6px 12px',
                    fontSize: '12px',
                    backgroundColor: theme.colors.primary,
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontFamily: theme.typography.fontFamily,
                  }}
                >
                  View Stats
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Most Goals */}
        <div style={{
          ...theme.styles.card,
          padding: 24,
        }}>
          <h3 style={{
            fontSize: '20px',
            fontWeight: theme.typography.fontWeights.semibold,
            color: theme.colors.textPrimary,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 16,
          }}>
            Most Goals
          </h3>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {topPlayers.goals.map((player, index) => (
              <div key={player.player_id} style={{
                display: 'flex',
                alignItems: 'center',
                gap: 12,
                padding: 12,
                background: theme.colors.content,
                borderRadius: 8,
                border: `1px solid ${theme.colors.border}`,
              }}>
                <div style={{
                  width: 40,
                  height: 40,
                  borderRadius: '50%',
                  overflow: 'hidden',
                  background: theme.colors.success,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontSize: '16px',
                  fontWeight: theme.typography.fontWeights.bold,
                }}>
                  {player.profile_picture ? (
                    <img 
                      src={player.profile_picture} 
                      alt={player.player_name}
                      style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                    />
                  ) : (
                    player.player_name.charAt(0).toUpperCase()
                  )}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{
                    fontSize: '16px',
                    fontWeight: theme.typography.fontWeights.semibold,
                    color: theme.colors.textPrimary,
                    fontFamily: theme.typography.fontFamily,
                  }}>
                    {player.player_name}
                  </div>
                  <div style={{
                    fontSize: '14px',
                    color: theme.colors.textSecondary,
                    fontFamily: theme.typography.fontFamily,
                  }}>
                    {player.total_goals} goals
                  </div>
                </div>
                <button
                  onClick={() => onViewPlayerStats(player.player_id)}
                  style={{
                    padding: '6px 12px',
                    fontSize: '12px',
                    backgroundColor: theme.colors.primary,
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontFamily: theme.typography.fontFamily,
                  }}
                >
                  View Stats
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Stats 