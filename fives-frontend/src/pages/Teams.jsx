import { useState, useEffect } from 'react'
import { theme } from '../theme'
import { teamsApi, playersApi } from '../services/api'
import PlayerPictureUpload from '../components/PlayerPictureUpload'

function Teams({ user, onViewTeam, onViewPlayerStats }) {
  const [teams, setTeams] = useState([])
  const [loading, setLoading] = useState(false)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [newTeamName, setNewTeamName] = useState('')
  const [teamSize, setTeamSize] = useState(5)
  const [players, setPlayers] = useState([])
  const [newPlayerName, setNewPlayerName] = useState('')
  const [existingPlayers, setExistingPlayers] = useState({}) // teamId -> players[]
  const [deleteConfirm, setDeleteConfirm] = useState({ show: false, teamId: null, teamName: '', type: '' })

  // Load teams on component mount
  useEffect(() => {
    loadTeams()
  }, [])

  const loadTeams = async () => {
    setLoading(true)
    try {
      const teamsData = await teamsApi.getTeams()
      
      // For each team, get the player count and players
      const teamsWithPlayerCount = await Promise.all(
        teamsData.map(async (team) => {
          try {
            const players = await playersApi.getPlayers()
            const teamPlayers = players.filter(player => player.team_id === team.id)
            
            // Store existing players for this team
            setExistingPlayers(prev => ({
              ...prev,
              [team.id]: teamPlayers
            }))
            
            return {
              ...team,
              playerCount: teamPlayers.length
            }
          } catch (error) {
            console.error(`Error loading players for team ${team.id}:`, error)
            return {
              ...team,
              playerCount: 0
            }
          }
        })
      )
      
      setTeams(teamsWithPlayerCount)
    } catch (error) {
      console.error('Error loading teams:', error)
      alert('Failed to load teams: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateTeam = async (e) => {
    e.preventDefault()
    if (!newTeamName.trim()) return
    if (players.length === 0) {
      alert('Please add at least one player to the team')
      return
    }

    setLoading(true)
    try {
      // First create the team
      const teamData = {
        name: newTeamName,
        team_size: teamSize,
      }
      
      const createdTeam = await teamsApi.createTeam(teamData)
      
      // Then create all the players for this team
      const playerPromises = players.map(player => 
        playersApi.createPlayer({
          name: player.name,
          team_id: createdTeam.id
        })
      )
      
      await Promise.all(playerPromises)
      
      // Reload teams to get the updated list
      await loadTeams()
      
      // Reset form
      setNewTeamName('')
      setTeamSize(5)
      setPlayers([])
      setShowCreateForm(false)
      
      alert('Team created successfully!')
    } catch (error) {
      console.error('Error creating team:', error)
      alert('Failed to create team: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const handleAddPlayer = (e) => {
    e.preventDefault()
    e.stopPropagation()
    
    if (!newPlayerName.trim()) return

    
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

  const handlePictureUpdated = (teamId, playerId, newPictureUrl) => {
    setExistingPlayers(prev => ({
      ...prev,
      [teamId]: prev[teamId]?.map(player => 
        player.id === playerId 
          ? { ...player, profile_picture: newPictureUrl }
          : player
      ) || []
    }))
  }

  const handleAddPlayerToTeam = async (teamId, playerName) => {
    if (!playerName.trim()) return
    
    try {
      const newPlayer = await playersApi.createPlayer({
        name: playerName.trim(),
        team_id: teamId
      })
      
      // Update existing players for this team
      setExistingPlayers(prev => ({
        ...prev,
        [teamId]: [...(prev[teamId] || []), newPlayer]
      }))
      
      // Update team player count
      setTeams(prev => prev.map(team => 
        team.id === teamId 
          ? { ...team, playerCount: (team.playerCount || 0) + 1 }
          : team
      ))
      
      return newPlayer
    } catch (error) {
      console.error('Error adding player:', error)
      alert('Failed to add player: ' + error.message)
      return null
    }
  }

  const handleRemovePlayerFromTeam = async (teamId, playerId) => {
    try {
      await playersApi.deletePlayer(playerId)
      
      // Update existing players for this team
      setExistingPlayers(prev => ({
        ...prev,
        [teamId]: prev[teamId]?.filter(player => player.id !== playerId) || []
      }))
      
      // Update team player count
      setTeams(prev => prev.map(team => 
        team.id === teamId 
          ? { ...team, playerCount: Math.max(0, (team.playerCount || 0) - 1) }
          : team
      ))
    } catch (error) {
      console.error('Error removing player:', error)
      alert('Failed to remove player: ' + error.message)
    }
  }

  const handleDeleteTeam = (teamId, teamName) => {
    setDeleteConfirm({ show: true, teamId, teamName, type: 'team' })
  }

  const confirmDelete = async () => {
    if (deleteConfirm.type === 'team') {
      try {
        await teamsApi.deleteTeam(deleteConfirm.teamId)
        await loadTeams()
        alert('Team deleted successfully!')
      } catch (error) {
        console.error('Error deleting team:', error)
        alert('Failed to delete team: ' + error.message)
      }
    }
    setDeleteConfirm({ show: false, teamId: null, teamName: '', type: '' })
  }

  const cancelDelete = () => {
    setDeleteConfirm({ show: false, teamId: null, teamName: '', type: '' })
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
          onClick={loadTeams}
          style={{
            ...theme.styles.button.secondary,
            padding: '16px 32px',
            fontSize: '16px',
            fontFamily: theme.typography.fontFamily,
            fontWeight: theme.typography.fontWeights.semibold,
          }}
        >
          {loading ? 'Loading...' : 'View All Teams'}
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
                Match Format (players per side)
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
                  Players ({players.length})
                </label>

              </div>

              {/* Add Player Form */}
              {(
                <div style={{ marginBottom: 16 }}>
                  <div style={{ display: 'flex', gap: 12, alignItems: 'flex-end' }}>
                    <div style={{ flex: 1 }}>
                      <input
                        type="text"
                        value={newPlayerName}
                        onChange={(e) => setNewPlayerName(e.target.value)}
                        onKeyPress={(e) => {
                          if (e.key === 'Enter') {
                            e.preventDefault()
                            handleAddPlayer(e)
                          }
                        }}
                        placeholder="Enter player name..."
                        style={{
                          ...theme.styles.input,
                          width: '100%',
                        }}
                      />
                    </div>
                    <button
                      type="button"
                      onClick={handleAddPlayer}
                      style={{
                        ...theme.styles.button.primary,
                        padding: '12px 16px',
                        fontSize: '14px',
                      }}
                    >
                      Add Player
                    </button>
                  </div>
                </div>
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
                      <TeamCard
          key={team.id}
          team={team}
          players={existingPlayers[team.id] || []}
          onViewTeam={onViewTeam}
          onDeleteTeam={handleDeleteTeam}
          onAddPlayer={handleAddPlayerToTeam}
          onRemovePlayer={handleRemovePlayerFromTeam}
          onPictureUpdated={handlePictureUpdated}
          onViewPlayerStats={onViewPlayerStats}
        />
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
              {deleteConfirm.type === 'team' && 
                `Are you sure you want to delete "${deleteConfirm.teamName}"? This will also delete all players, matches, and stats associated with this team. This action cannot be undone.`
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
                Delete {deleteConfirm.type === 'team' ? 'Team' : 'Player'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

// TeamCard component for displaying team information and managing players
function TeamCard({ team, players, onViewTeam, onDeleteTeam, onAddPlayer, onRemovePlayer, onPictureUpdated, onViewPlayerStats }) {
  console.log('TeamCard rendering:', { team, players, showPlayers: false })
  const [showPlayers, setShowPlayers] = useState(false)
  const [newPlayerName, setNewPlayerName] = useState('')
  const [addingPlayer, setAddingPlayer] = useState(false)

  const handleAddPlayerToExistingTeam = async (e) => {
    e.preventDefault()
    if (!newPlayerName.trim()) return
    
    setAddingPlayer(true)
    try {
      await onAddPlayer(team.id, newPlayerName)
      setNewPlayerName('')
    } finally {
      setAddingPlayer(false)
    }
  }

  return (
    <div style={{
      padding: 20,
      background: theme.colors.content,
      borderRadius: 12,
      border: `1px solid ${theme.colors.border}`,
    }}>
      {/* Team Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 16,
      }}>
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
            {team.playerCount || 0} players • {team.team_size}-a-side format
          </p>
          <p style={{ 
            fontSize: '12px', 
            color: theme.colors.textMuted,
            fontFamily: theme.typography.fontFamily,
          }}>
            Created {new Date(team.created_at).toLocaleDateString()}
          </p>
        </div>
        
        <div style={{ display: 'flex', gap: 8 }}>
          <button
            onClick={() => {
              console.log('Manage Players clicked, current showPlayers:', showPlayers)
              setShowPlayers(!showPlayers)
            }}
            style={{
              ...theme.styles.button.secondary,
              padding: '8px 16px',
              fontSize: '14px',
            }}
          >
            {showPlayers ? 'Hide Players' : 'Manage Players'}
          </button>
          <button
            onClick={() => onViewTeam(team.id)}
            style={{
              ...theme.styles.button.secondary,
              padding: '8px 16px',
              fontSize: '14px',
            }}
          >
            View Details
          </button>
          <button
            onClick={() => onViewPlayerStats(team.id)}
            style={{
              ...theme.styles.button.secondary,
              padding: '8px 16px',
              fontSize: '14px',
            }}
          >
            View Stats
          </button>
          <button
            onClick={() => onDeleteTeam(team.id, team.name)}
            style={{
              background: 'none',
              border: 'none',
              color: theme.colors.error,
              cursor: 'pointer',
              fontSize: '14px',
              fontFamily: theme.typography.fontFamily,
              padding: '8px 16px',
              borderRadius: 4,
            }}
            onMouseEnter={(e) => e.target.style.background = 'rgba(255, 107, 107, 0.1)'}
            onMouseLeave={(e) => e.target.style.background = 'none'}
          >
            Delete
          </button>
        </div>
      </div>

      {/* Players Management Section */}
      {showPlayers && (
        <div style={{
          borderTop: `1px solid ${theme.colors.border}`,
          paddingTop: 16,
        }}>
          {console.log('Rendering players section, players:', players)}
          <h5 style={{
            fontSize: '16px',
            fontWeight: theme.typography.fontWeights.semibold,
            color: theme.colors.textPrimary,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 16,
          }}>
            Players Management
          </h5>
          
          {/* Debug info */}
          <div style={{ 
            fontSize: '12px', 
            color: theme.colors.textMuted, 
            marginBottom: 16,
            padding: '8px',
            background: theme.colors.card,
            borderRadius: 4,
          }}>
            Debug: {players.length} players loaded for team {team.id}
          </div>

          {/* Add New Player Form */}
          <form onSubmit={handleAddPlayerToExistingTeam} style={{ marginBottom: 20 }}>
            <div style={{ display: 'flex', gap: 12, alignItems: 'flex-end' }}>
              <div style={{ flex: 1 }}>
                <input
                  type="text"
                  value={newPlayerName}
                  onChange={(e) => setNewPlayerName(e.target.value)}
                  placeholder="Enter new player name..."
                  style={{
                    ...theme.styles.input,
                    width: '100%',
                  }}
                />
              </div>
              <button
                type="submit"
                disabled={addingPlayer || !newPlayerName.trim()}
                style={{
                  ...theme.styles.button.primary,
                  padding: '12px 16px',
                  fontSize: '14px',
                  opacity: addingPlayer || !newPlayerName.trim() ? 0.6 : 1,
                }}
              >
                {addingPlayer ? 'Adding...' : 'Add Player'}
              </button>
            </div>
          </form>

          {/* Players List with Picture Upload */}
          {players.length > 0 ? (
            <div style={{ display: 'grid', gap: 16 }}>
              {players.map((player) => (
                <div key={player.id} style={{
                  padding: 16,
                  background: theme.colors.card,
                  borderRadius: 8,
                  border: `1px solid ${theme.colors.border}`,
                }}>
                  <div style={{ marginBottom: 8, fontSize: '12px', color: theme.colors.textMuted }}>
                    Player ID: {player.id} | Name: {player.name}
                  </div>
                  {(() => {
                    try {
                      return (
                        <PlayerPictureUpload 
                          player={player}
                          onPictureUpdated={(newPictureUrl) => onPictureUpdated(team.id, player.id, newPictureUrl)}
                        />
                      )
                    } catch (error) {
                      console.error('Error rendering PlayerPictureUpload:', error)
                      return (
                        <div style={{ color: theme.colors.error, padding: '8px' }}>
                          Error rendering player picture upload: {error.message}
                        </div>
                      )
                    }
                  })()}
                  <div style={{ marginTop: 12, textAlign: 'right', display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
                    <button
                      onClick={() => onRemovePlayer(team.id, player.id)}
                      style={{
                        background: 'none',
                        border: 'none',
                        color: theme.colors.error,
                        cursor: 'pointer',
                        fontSize: '14px',
                        fontFamily: theme.typography.fontFamily,
                        padding: '8px 16px',
                        borderRadius: 4,
                      }}
                      onMouseEnter={(e) => e.target.style.background = 'rgba(255, 107, 107, 0.1)'}
                      onMouseLeave={(e) => e.target.style.background = 'none'}
                    >
                      Remove Player
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div style={{
              padding: 20,
              textAlign: 'center',
              color: theme.colors.textSecondary,
              fontFamily: theme.typography.fontFamily,
            }}>
              No players yet. Add your first player above!
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default Teams 