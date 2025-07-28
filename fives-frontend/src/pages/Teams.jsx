import { useState } from 'react'
import { theme } from '../theme'

function Teams({ user }) {
  const [teams, setTeams] = useState([])
  const [loading, setLoading] = useState(false)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [newTeamName, setNewTeamName] = useState('')
  const [teamSize, setTeamSize] = useState(5)
  const [players, setPlayers] = useState([])
  const [newPlayerName, setNewPlayerName] = useState('')

  const handleCreateTeam = async (e) => {
    e.preventDefault()
    if (!newTeamName.trim()) return
    if (players.length === 0) {
      alert('Please add at least one player to the team')
      return
    }

    setLoading(true)
    try {
      // TODO: Call your backend API to create team
      const newTeam = {
        id: Date.now().toString(), // Temporary ID
        name: newTeamName,
        teamSize: teamSize,
        players: players,
        created_at: new Date().toISOString(),
      }
      
      setTeams([...teams, newTeam])
      setNewTeamName('')
      setTeamSize(5)
      setPlayers([])
      setShowCreateForm(false)
    } catch (error) {
      console.error('Error creating team:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAddPlayer = (e) => {
    e.preventDefault()
    if (!newPlayerName.trim()) return
    if (players.length >= teamSize) {
      alert(`Team is full (${teamSize} players maximum)`)
      return
    }
    
    const newPlayer = {
      id: Date.now().toString(),
      name: newPlayerName.trim(),
    }
    
    setPlayers([...players, newPlayer])
    setNewPlayerName('')
  }

  const handleRemovePlayer = (playerId) => {
    setPlayers(players.filter(player => player.id !== playerId))
  }

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto' }}>
      {/* Header Section */}
      <div style={{ marginBottom: 32 }}>
        <h1 style={{ 
          fontSize: '32px', 
          fontWeight: theme.typography.fontWeights.bold, 
          color: theme.colors.primary,
          fontFamily: theme.typography.fontFamily,
          letterSpacing: theme.typography.letterSpacing.tight,
          marginBottom: 8,
        }}>
          Teams
        </h1>
        <p style={{ 
          fontSize: '16px', 
          color: theme.colors.textSecondary,
          fontFamily: theme.typography.fontFamily,
          fontWeight: theme.typography.fontWeights.normal,
        }}>
          Manage your teams and players
        </p>
      </div>

      {/* Action Buttons */}
      <div style={{ 
        display: 'flex', 
        gap: 16, 
        marginBottom: 32,
        flexWrap: 'wrap',
      }}>
        <button
          onClick={() => setShowCreateForm(true)}
          style={{
            ...theme.styles.button.primary,
            padding: '16px 32px',
            fontSize: '16px',
            fontFamily: theme.typography.fontFamily,
            fontWeight: theme.typography.fontWeights.semibold,
          }}
        >
          + Create New Team
        </button>
        
        <button
          onClick={() => {/* TODO: Load teams */}}
          style={{
            ...theme.styles.button.secondary,
            padding: '16px 32px',
            fontSize: '16px',
            fontFamily: theme.typography.fontFamily,
            fontWeight: theme.typography.fontWeights.semibold,
          }}
        >
          View All Teams
        </button>
      </div>

      {/* Create Team Form */}
      {showCreateForm && (
        <div style={{
          ...theme.styles.card,
          padding: 32,
          marginBottom: 32,
        }}>
          <h3 style={{ 
            fontSize: '20px', 
            fontWeight: theme.typography.fontWeights.semibold,
            color: theme.colors.textPrimary,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 24,
          }}>
            Create New Team
          </h3>
          
          <form onSubmit={handleCreateTeam}>
            {/* Team Name */}
            <div style={{ marginBottom: 24 }}>
              <label style={{ 
                display: 'block',
                marginBottom: 8,
                color: theme.colors.textSecondary,
                fontFamily: theme.typography.fontFamily,
                fontWeight: theme.typography.fontWeights.medium,
              }}>
                Team Name
              </label>
              <input
                type="text"
                value={newTeamName}
                onChange={(e) => setNewTeamName(e.target.value)}
                placeholder="Enter team name..."
                style={{
                  ...theme.styles.input,
                  width: '100%',
                  maxWidth: 400,
                }}
                required
              />
            </div>

            {/* Team Size */}
            <div style={{ marginBottom: 24 }}>
              <label style={{ 
                display: 'block',
                marginBottom: 8,
                color: theme.colors.textSecondary,
                fontFamily: theme.typography.fontFamily,
                fontWeight: theme.typography.fontWeights.medium,
              }}>
                Team Size (players per side)
              </label>
              <select
                value={teamSize}
                onChange={(e) => setTeamSize(parseInt(e.target.value))}
                style={{
                  ...theme.styles.input,
                  width: '100%',
                  maxWidth: 400,
                }}
              >
                <option value={5}>5-a-side</option>
                <option value={6}>6-a-side</option>
                <option value={7}>7-a-side</option>
                <option value={8}>8-a-side</option>
                <option value={9}>9-a-side</option>
                <option value={10}>10-a-side</option>
                <option value={11}>11-a-side</option>
              </select>
            </div>

            {/* Players Section */}
            <div style={{ marginBottom: 24 }}>
              <div style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center',
                marginBottom: 16,
              }}>
                <label style={{ 
                  color: theme.colors.textSecondary,
                  fontFamily: theme.typography.fontFamily,
                  fontWeight: theme.typography.fontWeights.medium,
                }}>
                  Players ({players.length}/{teamSize})
                </label>
                {players.length > 0 && (
                  <span style={{ 
                    fontSize: '14px', 
                    color: theme.colors.textSecondary,
                    fontFamily: theme.typography.fontFamily,
                  }}>
                    {teamSize - players.length} spots remaining
                  </span>
                )}
              </div>

              {/* Add Player Form */}
              {players.length < teamSize && (
                <form onSubmit={handleAddPlayer} style={{ marginBottom: 16 }}>
                  <div style={{ display: 'flex', gap: 12, alignItems: 'flex-end' }}>
                    <div style={{ flex: 1 }}>
                      <input
                        type="text"
                        value={newPlayerName}
                        onChange={(e) => setNewPlayerName(e.target.value)}
                        placeholder="Enter player name..."
                        style={{
                          ...theme.styles.input,
                          width: '100%',
                        }}
                        required
                      />
                    </div>
                    <button
                      type="submit"
                      style={{
                        ...theme.styles.button.primary,
                        padding: '12px 16px',
                        fontSize: '14px',
                      }}
                    >
                      Add Player
                    </button>
                  </div>
                </form>
              )}

              {/* Players List */}
              {players.length > 0 && (
                <div style={{ 
                  background: theme.colors.content,
                  borderRadius: 8,
                  padding: 16,
                  border: `1px solid ${theme.colors.border}`,
                }}>
                  {players.map((player, index) => (
                    <div
                      key={player.id}
                      style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        padding: '8px 0',
                        borderBottom: index < players.length - 1 ? `1px solid ${theme.colors.border}` : 'none',
                      }}
                    >
                      <span style={{ 
                        color: theme.colors.textPrimary,
                        fontFamily: theme.typography.fontFamily,
                        fontWeight: theme.typography.fontWeights.medium,
                      }}>
                        {player.name}
                      </span>
                      <button
                        type="button"
                        onClick={() => handleRemovePlayer(player.id)}
                        style={{
                          background: 'none',
                          border: 'none',
                          color: theme.colors.error,
                          cursor: 'pointer',
                          fontSize: '14px',
                          fontFamily: theme.typography.fontFamily,
                          padding: '4px 8px',
                          borderRadius: 4,
                        }}
                        onMouseEnter={(e) => e.target.style.background = 'rgba(255, 107, 107, 0.1)'}
                        onMouseLeave={(e) => e.target.style.background = 'none'}
                      >
                        Remove
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
            
            {/* Submit Buttons */}
            <div style={{ display: 'flex', gap: 12 }}>
              <button
                type="submit"
                disabled={loading || !newTeamName.trim() || players.length === 0}
                style={{
                  ...theme.styles.button.primary,
                  padding: '12px 24px',
                  opacity: loading || !newTeamName.trim() || players.length === 0 ? 0.6 : 1,
                }}
              >
                {loading ? 'Creating...' : 'Create Team'}
              </button>
              
              <button
                type="button"
                onClick={() => {
                  setShowCreateForm(false)
                  setNewTeamName('')
                  setTeamSize(5)
                  setPlayers([])
                }}
                style={{
                  ...theme.styles.button.secondary,
                  padding: '12px 24px',
                }}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Teams List */}
      {teams.length > 0 && (
        <div style={{
          ...theme.styles.card,
          padding: 32,
        }}>
          <h3 style={{ 
            fontSize: '20px', 
            fontWeight: theme.typography.fontWeights.semibold,
            color: theme.colors.textPrimary,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 24,
          }}>
            Your Teams
          </h3>
          
          <div style={{ display: 'grid', gap: 16 }}>
            {teams.map((team) => (
              <div
                key={team.id}
                style={{
                  padding: 20,
                  background: theme.colors.content,
                  borderRadius: 12,
                  border: `1px solid ${theme.colors.border}`,
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div>
                  <h4 style={{ 
                    fontSize: '18px', 
                    fontWeight: theme.typography.fontWeights.semibold,
                    color: theme.colors.textPrimary,
                    fontFamily: theme.typography.fontFamily,
                    marginBottom: 4,
                  }}>
                    {team.name}
                  </h4>
                  <p style={{ 
                    fontSize: '14px', 
                    color: theme.colors.textSecondary,
                    fontFamily: theme.typography.fontFamily,
                    marginBottom: 4,
                  }}>
                    {team.teamSize}-a-side • {team.players?.length || 0} players
                  </p>
                  <p style={{ 
                    fontSize: '12px', 
                    color: theme.colors.textMuted,
                    fontFamily: theme.typography.fontFamily,
                  }}>
                    Created {new Date(team.created_at).toLocaleDateString()}
                  </p>
                </div>
                
                <button
                  style={{
                    ...theme.styles.button.secondary,
                    padding: '8px 16px',
                    fontSize: '14px',
                  }}
                >
                  View Details
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {teams.length === 0 && !showCreateForm && (
        <div style={{
          ...theme.styles.card,
          padding: 48,
          textAlign: 'center',
        }}>
          <h3 style={{ 
            fontSize: '24px', 
            fontWeight: theme.typography.fontWeights.semibold,
            color: theme.colors.textPrimary,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 16,
          }}>
            No Teams Yet
          </h3>
          <p style={{ 
            fontSize: '16px', 
            color: theme.colors.textSecondary,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 24,
            lineHeight: theme.typography.lineHeights.normal,
          }}>
            Get started by creating your first team to manage players and track stats.
          </p>
          <button
            onClick={() => setShowCreateForm(true)}
            style={{
              ...theme.styles.button.primary,
              padding: '16px 32px',
              fontSize: '16px',
              fontFamily: theme.typography.fontFamily,
              fontWeight: theme.typography.fontWeights.semibold,
            }}
          >
            Create Your First Team
          </button>
        </div>
      )}
    </div>
  )
}

export default Teams 