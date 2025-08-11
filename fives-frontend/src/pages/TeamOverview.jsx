import { useState, useEffect } from 'react'
import { theme } from '../theme'
import { teamsApi, playersApi, statsApi } from '../services/api'
import PlayerGoalsChart from '../components/PlayerGoalsChart'
import TeamStatsChart from '../components/TeamStatsChart'

function TeamOverview({ user, teamId, onBack }) {
  const [team, setTeam] = useState(null)
  const [players, setPlayers] = useState([])
  const [playerStats, setPlayerStats] = useState([])
  const [teamStats, setTeamStats] = useState([])
  const [loading, setLoading] = useState(true)
  const [deleteConfirm, setDeleteConfirm] = useState({ show: false, playerId: null, playerName: '', type: '' })

  useEffect(() => {
    loadTeamData()
  }, [teamId])

  const loadTeamData = async () => {
    setLoading(true)
    try {
      // Load team details
      const teamData = await teamsApi.getTeam(teamId)
      setTeam(teamData)

      // Load players for this team
      const allPlayers = await playersApi.getPlayers()
      const teamPlayers = allPlayers.filter(player => player.team_id === teamId)
      setPlayers(teamPlayers)

      // Load player stats and team stats
      try {
        const [playerStatsData, teamStatsData] = await Promise.all([
          statsApi.getPlayerStats(teamId),
          statsApi.getTeamStats(teamId)
        ])
        setPlayerStats(playerStatsData)
        setTeamStats(teamStatsData)
      } catch (error) {
        console.error('Error loading stats:', error)
        // If stats don't exist yet, that's okay - they'll be generated when needed
        setPlayerStats([])
        setTeamStats([])
      }
    } catch (error) {
      console.error('Error loading team data:', error)
      alert('Failed to load team data: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const handleDeletePlayer = (playerId, playerName) => {
    setDeleteConfirm({ show: true, playerId, playerName, type: 'player' })
  }

  const confirmDelete = async () => {
    if (deleteConfirm.type === 'player') {
      try {
        await playersApi.deletePlayer(deleteConfirm.playerId)
        await loadTeamData() // Reload data to update player list
        alert('Player removed successfully!')
      } catch (error) {
        console.error('Error deleting player:', error)
        alert('Failed to remove player: ' + error.message)
      }
    }
    setDeleteConfirm({ show: false, playerId: null, playerName: '', type: '' })
  }

  const cancelDelete = () => {
    setDeleteConfirm({ show: false, playerId: null, playerName: '', type: '' })
  }

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: 40 }}>
        <div style={{ color: theme.colors.textSecondary }}>Loading team details...</div>
      </div>
    )
  }

  if (!team) {
    return (
      <div style={{ textAlign: 'center', padding: 40 }}>
        <div style={{ color: theme.colors.error }}>Team not found</div>
        <button 
          onClick={onBack}
          style={{
            ...theme.styles.button.secondary,
            marginTop: 16,
          }}
        >
          Back to Teams
        </button>
      </div>
    )
  }

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto' }}>
      {/* Header Section */}
      <div style={{ marginBottom: 32 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 16 }}>
          <button 
            onClick={onBack}
            style={{
              ...theme.styles.button.secondary,
              padding: '8px 16px',
              fontSize: '14px',
            }}
          >
            ← Back
          </button>
          <h1 style={{ 
            fontSize: '32px', 
            fontWeight: theme.typography.fontWeights.bold, 
            color: theme.colors.primary,
            fontFamily: theme.typography.fontFamily,
            letterSpacing: theme.typography.letterSpacing.tight,
            margin: 0,
          }}>
            {team.name}
          </h1>
        </div>
        <p style={{ 
          fontSize: '16px', 
          color: theme.colors.textSecondary,
          fontFamily: theme.typography.fontFamily,
          fontWeight: theme.typography.fontWeights.normal,
        }}>
          {team.team_size}-a-side team • {players.length} players
        </p>
      </div>

      {/* Team Stats Overview */}
      <div style={{
        ...theme.styles.card,
        padding: 24,
        marginBottom: 32,
      }}>
        <h3 style={{ 
          fontSize: '20px', 
          fontWeight: theme.typography.fontWeights.semibold,
          color: theme.colors.textPrimary,
          fontFamily: theme.typography.fontFamily,
          marginBottom: 16,
        }}>
          Team Overview
        </h3>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 24 }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ 
              fontSize: '32px', 
              fontWeight: theme.typography.fontWeights.bold,
              color: theme.colors.primary,
              fontFamily: theme.typography.fontFamily,
            }}>
              {players.length}
            </div>
            <div style={{ 
              fontSize: '14px', 
              color: theme.colors.textSecondary,
              fontFamily: theme.typography.fontFamily,
            }}>
              Players
            </div>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ 
              fontSize: '32px', 
              fontWeight: theme.typography.fontWeights.bold,
              color: theme.colors.primary,
              fontFamily: theme.typography.fontFamily,
            }}>
              {team.team_size}
            </div>
            <div style={{ 
              fontSize: '14px', 
              color: theme.colors.textSecondary,
              fontFamily: theme.typography.fontFamily,
            }}>
              Match Format
            </div>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ 
              fontSize: '32px', 
              fontWeight: theme.typography.fontWeights.bold,
              color: theme.colors.primary,
              fontFamily: theme.typography.fontFamily,
            }}>
              0
            </div>
            <div style={{ 
              fontSize: '14px', 
              color: theme.colors.textSecondary,
              fontFamily: theme.typography.fontFamily,
            }}>
              Matches Played
            </div>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ 
              fontSize: '32px', 
              fontWeight: theme.typography.fontWeights.bold,
              color: theme.colors.primary,
              fontFamily: theme.typography.fontFamily,
            }}>
              0
            </div>
            <div style={{ 
              fontSize: '14px', 
              color: theme.colors.textSecondary,
              fontFamily: theme.typography.fontFamily,
            }}>
              Goals Scored
            </div>
          </div>
        </div>
      </div>

      {/* Players Section */}
      <div style={{
        ...theme.styles.card,
        padding: 24,
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
          <h3 style={{ 
            fontSize: '20px', 
            fontWeight: theme.typography.fontWeights.semibold,
            color: theme.colors.textPrimary,
            fontFamily: theme.typography.fontFamily,
            margin: 0,
          }}>
            Players ({players.length})
          </h3>
          <button
            style={{
              ...theme.styles.button.primary,
              padding: '8px 16px',
              fontSize: '14px',
            }}
          >
            + Add Player
          </button>
        </div>

        {players.length === 0 ? (
          <div style={{ 
            textAlign: 'center', 
            padding: 40,
            color: theme.colors.textSecondary,
            fontFamily: theme.typography.fontFamily,
          }}>
            <div style={{ fontSize: '18px', marginBottom: 8 }}>No players yet</div>
            <div style={{ fontSize: '14px' }}>Add players to get started</div>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: 16 }}>
            {players.map((player) => (
              <div
                key={player.id}
                style={{
                  padding: 16,
                  background: theme.colors.content,
                  borderRadius: 8,
                  border: `1px solid ${theme.colors.border}`,
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div>
                  <h4 style={{ 
                    fontSize: '16px', 
                    fontWeight: theme.typography.fontWeights.semibold,
                    color: theme.colors.textPrimary,
                    fontFamily: theme.typography.fontFamily,
                    margin: '0 0 4px 0',
                  }}>
                    {player.name}
                  </h4>
                  <p style={{ 
                    fontSize: '12px', 
                    color: theme.colors.textMuted,
                    fontFamily: theme.typography.fontFamily,
                    margin: 0,
                  }}>
                    Player since {new Date(player.created_at).toLocaleDateString()}
                  </p>
                </div>
                
                <div style={{ display: 'flex', gap: 8 }}>
                  <button
                    style={{
                      ...theme.styles.button.secondary,
                      padding: '6px 12px',
                      fontSize: '12px',
                    }}
                  >
                    View Stats
                  </button>
                  <button
                    onClick={() => handleDeletePlayer(player.id, player.name)}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: theme.colors.error,
                      cursor: 'pointer',
                      fontSize: '12px',
                      fontFamily: theme.typography.fontFamily,
                      padding: '6px 12px',
                      borderRadius: 4,
                    }}
                    onMouseEnter={(e) => e.target.style.background = 'rgba(255, 107, 107, 0.1)'}
                    onMouseLeave={(e) => e.target.style.background = 'none'}
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Charts Section */}
      <div style={{ marginTop: 32 }}>
        <h2 style={{ 
          fontSize: '24px', 
          fontWeight: theme.typography.fontWeights.bold,
          color: theme.colors.textPrimary,
          fontFamily: theme.typography.fontFamily,
          marginBottom: 24,
        }}>
          Team Analytics
        </h2>

        {/* Team Performance Chart */}
        <TeamStatsChart 
          data={teamStats} 
          title={`${team.name} Performance`}
        />

        {/* Generate Stats Button */}
        {(playerStats.length === 0 || teamStats.length === 0) && (
          <div style={{
            ...theme.styles.card,
            padding: 24,
            marginBottom: 24,
            textAlign: 'center',
          }}>
            <h3 style={{ 
              fontSize: '18px', 
              fontWeight: theme.typography.fontWeights.semibold,
              color: theme.colors.textPrimary,
              fontFamily: theme.typography.fontFamily,
              marginBottom: 16,
            }}>
              No Stats Available
            </h3>
            <p style={{ 
              fontSize: '14px', 
              color: theme.colors.textSecondary,
              fontFamily: theme.typography.fontFamily,
              marginBottom: 16,
            }}>
              Generate stats from your match data to see charts and analytics.
            </p>
            <button
              onClick={async () => {
                try {
                  await statsApi.generateStats(teamId)
                  await loadTeamData() // Reload data to show new stats
                  alert('Stats generated successfully!')
                } catch (error) {
                  console.error('Error generating stats:', error)
                  alert('Failed to generate stats: ' + error.message)
                }
              }}
              style={{
                ...theme.styles.button.primary,
                padding: '12px 24px',
                fontSize: '14px',
              }}
            >
              Generate Stats
            </button>
          </div>
        )}

        {/* Player Goals Charts */}
        {players.length > 0 && (
          <div style={{
            ...theme.styles.card,
            padding: 24,
          }}>
            <h3 style={{ 
              fontSize: '20px', 
              fontWeight: theme.typography.fontWeights.semibold,
              color: theme.colors.textPrimary,
              fontFamily: theme.typography.fontFamily,
              marginBottom: 24,
            }}>
              Player Performance
            </h3>
            
            {players.map((player) => (
              <div key={player.id} style={{ marginBottom: 32 }}>
                <PlayerGoalsChart 
                  data={playerStats.filter(stat => stat.player_id === player.id)}
                  title={`${player.name} - Goals Over Time`}
                />
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Delete Confirmation Modal */}
      {deleteConfirm.show && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 1000,
        }}>
          <div style={{
            background: theme.colors.card,
            padding: 32,
            borderRadius: 12,
            maxWidth: 400,
            width: '90%',
            border: `1px solid ${theme.colors.border}`,
            boxShadow: theme.colors.shadow,
          }}>
            <h3 style={{
              fontSize: '20px',
              fontWeight: theme.typography.fontWeights.bold,
              color: theme.colors.error,
              fontFamily: theme.typography.fontFamily,
              marginBottom: 16,
            }}>
              Confirm Deletion
            </h3>
            
            <p style={{
              fontSize: '16px',
              color: theme.colors.textSecondary,
              fontFamily: theme.typography.fontFamily,
              marginBottom: 24,
              lineHeight: 1.5,
            }}>
              {deleteConfirm.type === 'player' && 
                `Are you sure you want to remove "${deleteConfirm.playerName}" from the team? This will also delete all their match appearances and stats. This action cannot be undone.`
              }
            </p>
            
            <div style={{ display: 'flex', gap: 12, justifyContent: 'flex-end' }}>
              <button
                onClick={cancelDelete}
                style={{
                  ...theme.styles.button.secondary,
                  padding: '10px 20px',
                }}
              >
                Cancel
              </button>
              <button
                onClick={confirmDelete}
                style={{
                  background: theme.colors.error,
                  color: 'white',
                  border: 'none',
                  padding: '10px 20px',
                  borderRadius: 6,
                  fontSize: '14px',
                  fontWeight: theme.typography.fontWeights.medium,
                  fontFamily: theme.typography.fontFamily,
                  cursor: 'pointer',
                }}
                onMouseEnter={(e) => e.target.style.background = '#d32f2f'}
                onMouseLeave={(e) => e.target.style.background = theme.colors.error}
              >
                Remove Player
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default TeamOverview 