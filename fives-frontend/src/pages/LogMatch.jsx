import { useState, useEffect } from 'react'
import { theme } from '../theme'
import { teamsApi, playersApi, opponentsApi, matchesApi, statsApi } from '../services/api'
import { useMatchCache } from '../contexts/MatchCacheContext'

function LogMatch({ user, onBack }) {
  const [teams, setTeams] = useState([])
  const [selectedTeam, setSelectedTeam] = useState(null)
  const [teamPlayers, setTeamPlayers] = useState([])
  const [opponents, setOpponents] = useState([])
  const [loading, setLoading] = useState(false)
  
  // Match details
  const [matchData, setMatchData] = useState({
    opponent_name: '',
    score_home: '',
    score_away: '',
    gameweek: '',
    season: '',
    played_at: new Date().toISOString().split('T')[0],
  })
  
  const { getLastMatchInfo, updateCacheAfterMatch } = useMatchCache()
  
  // Player selections
  const [selectedPlayers, setSelectedPlayers] = useState([])
  const [playerGoals, setPlayerGoals] = useState({})
  
  // Form states
  const [showNewOpponent, setShowNewOpponent] = useState(false)
  const [newOpponentName, setNewOpponentName] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [showSuccess, setShowSuccess] = useState(false)

  useEffect(() => {
    loadTeams()
  }, [])

  useEffect(() => {
    if (selectedTeam) {
      loadTeamData()
    }
  }, [selectedTeam])

  const loadTeams = async () => {
    setLoading(true)
    try {
      const teamsData = await teamsApi.getTeams()
      setTeams(teamsData)
    } catch (error) {
      console.error('Error loading teams:', error)
      alert('Failed to load teams: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const loadTeamData = async () => {
    if (!selectedTeam) return
    
    try {
      // Load team players
      const allPlayers = await playersApi.getPlayers()
      const teamPlayersData = allPlayers.filter(player => player.team_id === selectedTeam.id)
      setTeamPlayers(teamPlayersData)
      
      // Load existing opponents for this team
      const opponentsData = await opponentsApi.getOpponents(selectedTeam.id)
      setOpponents(opponentsData)
      
      // Load last match info for this team using cache
      const lastMatchInfo = await getLastMatchInfo(selectedTeam.id)
      
      // Auto-populate the form with next gameweek
      setMatchData(prev => ({
        ...prev,
        season: lastMatchInfo.season,
        gameweek: lastMatchInfo.gameweek + 1,
      }))
    } catch (error) {
      console.error('Error loading team data:', error)
      alert('Failed to load team data: ' + error.message)
    }
  }





  const handleTeamSelect = (teamId) => {
    const team = teams.find(t => t.id === teamId)
    setSelectedTeam(team)
    setSelectedPlayers([])
    setPlayerGoals({})
    setMatchData(prev => ({ ...prev, opponent_name: '' }))
  }

  const handlePlayerToggle = (playerId) => {
    setSelectedPlayers(prev => {
      if (prev.includes(playerId)) {
        const newSelected = prev.filter(id => id !== playerId)
        // Remove goals for this player
        const newGoals = { ...playerGoals }
        delete newGoals[playerId]
        setPlayerGoals(newGoals)
        return newSelected
      } else {
        return [...prev, playerId]
      }
    })
  }

  const handlePlayerGoalsChange = (playerId, goals) => {
    setPlayerGoals(prev => ({
      ...prev,
      [playerId]: parseInt(goals) || 0
    }))
  }

  const handleOpponentSelect = (opponentName) => {
    setMatchData(prev => ({ ...prev, opponent_name: opponentName }))
    setShowNewOpponent(false)
    setNewOpponentName('')
  }

  const handleCreateOpponent = async () => {
    if (!newOpponentName.trim()) return
    
    try {
      await opponentsApi.createOpponent({
        name: newOpponentName.trim(),
        team_id: selectedTeam.id
      })
      
      // Reload opponents
      await loadTeamData()
      
      // Select the new opponent
      setMatchData(prev => ({ ...prev, opponent_name: newOpponentName.trim() }))
      setShowNewOpponent(false)
      setNewOpponentName('')
    } catch (error) {
      console.error('Error creating opponent:', error)
      alert('Failed to create opponent: ' + error.message)
    }
  }

  const validateForm = () => {
    if (!selectedTeam) {
      alert('Please select a team')
      return false
    }
    if (!matchData.opponent_name.trim()) {
      alert('Please enter or select an opponent')
      return false
    }
    if (!matchData.score_home || !matchData.score_away) {
      alert('Please enter both home and away scores')
      return false
    }
    if (selectedPlayers.length === 0) {
      alert('Please select at least one player who played')
      return false
    }
    
    // Validate that goals match the score
    const totalGoals = Object.values(playerGoals).reduce((sum, goals) => sum + goals, 0)
    if (totalGoals !== parseInt(matchData.score_home)) {
      alert(`Total player goals (${totalGoals}) must match the home score (${matchData.score_home})`)
      return false
    }
    
    return true
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) return
    
    setIsSubmitting(true)
    try {
      // Prepare appearances data
      const appearances = selectedPlayers.map(playerId => ({
        player_id: playerId,
        goals: playerGoals[playerId] || 0,
      }))
      
      // Create the match with all data in one request
      const matchResponse = await matchesApi.createFullMatch({
        team_id: selectedTeam.id,
        opponent_name: matchData.opponent_name,
        score1: parseInt(matchData.score_home),
        score2: parseInt(matchData.score_away),
        gameweek: parseInt(matchData.gameweek) || 1,
        season: matchData.season || '2024',
        played_at: matchData.played_at,
        appearances: appearances,
      })
      
      // Update the cache with the new match info
      updateCacheAfterMatch(selectedTeam.id, matchData.season, matchData.gameweek)
      
      // Show success state instead of alert
      setShowSuccess(true)
      
      // Now trigger stats generation in the background (don't wait for it)
      statsApi.generateStats(selectedTeam.id).catch(statsError => {
        console.warn('Background stats generation failed:', statsError)
        // Don't show error to user since match was already logged successfully
      })
    } catch (error) {
      console.error('Error logging match:', error)
      alert('Failed to log match: ' + error.message)
    } finally {
      setIsSubmitting(false)
    }
  }



  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: 40 }}>
        <div style={{ color: theme.colors.textSecondary }}>Loading teams...</div>
      </div>
    )
  }

  if (showSuccess) {
    return (
      <div style={{ maxWidth: 600, margin: '0 auto', textAlign: 'center' }}>
        <div style={{
          ...theme.styles.card,
          padding: 48,
          marginBottom: 32,
        }}>
          <div style={{
            width: 80,
            height: 80,
            borderRadius: '50%',
            background: theme.colors.success,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 24px auto',
            boxShadow: theme.colors.shadow,
          }}>
            <svg 
              width="40" 
              height="40" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="white" 
              strokeWidth="2" 
              strokeLinecap="round" 
              strokeLinejoin="round"
            >
              <path d="M20 6L9 17l-5-5"/>
            </svg>
          </div>
          
          <h1 style={{
            fontSize: '32px',
            fontWeight: theme.typography.fontWeights.bold,
            color: theme.colors.success,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 16,
          }}>
            Match Logged Successfully!
          </h1>
          
          <p style={{
            fontSize: '18px',
            color: theme.colors.textSecondary,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 32,
            lineHeight: 1.6,
          }}>
            Your match result has been recorded and player statistics are being updated in the background.
          </p>
          
          <div style={{ display: 'flex', gap: 16, justifyContent: 'center' }}>
            <button
              onClick={() => {
                setShowSuccess(false)
                setSelectedTeam(null)
                setSelectedPlayers([])
                setPlayerGoals({})
                setMatchData({
                  opponent_name: '',
                  score_home: '',
                  score_away: '',
                  gameweek: '',
                  season: '',
                  played_at: new Date().toISOString().split('T')[0],
                })
              }}
              style={{
                ...theme.styles.button.secondary,
                padding: '12px 24px',
                fontSize: '16px',
              }}
            >
              Log Another Match
            </button>
            
            <button
              onClick={onBack}
              style={{
                ...theme.styles.button.primary,
                padding: '12px 24px',
                fontSize: '16px',
              }}
            >
              Return to Dashboard
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div style={{ maxWidth: 800, margin: '0 auto' }}>
      {/* Header */}
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
            margin: 0,
          }}>
            Log Match Result
          </h1>
        </div>
        <p style={{ 
          fontSize: '16px', 
          color: theme.colors.textSecondary,
          fontFamily: theme.typography.fontFamily,
        }}>
          Record your match details, scores, and player performances
        </p>
      </div>

      <form onSubmit={handleSubmit}>
        {/* Team Selection */}
        <div style={{
          ...theme.styles.card,
          padding: 24,
          marginBottom: 24,
        }}>
          <h3 style={{ 
            fontSize: '20px', 
            fontWeight: theme.typography.fontWeights.semibold,
            color: theme.colors.textPrimary,
            fontFamily: theme.typography.fontFamily,
            marginBottom: 16,
          }}>
            Select Your Team
          </h3>
          
          <select
            value={selectedTeam?.id || ''}
            onChange={(e) => handleTeamSelect(e.target.value)}
            style={{
              ...theme.styles.input,
              width: '100%',
              maxWidth: 400,
            }}
            required
          >
            <option value="">Choose a team...</option>
            {teams.map(team => (
              <option key={team.id} value={team.id}>
                {team.name} ({team.team_size}-a-side)
              </option>
            ))}
          </select>
        </div>

        {selectedTeam && (
          <>
            {/* Match Details */}
            <div style={{
              ...theme.styles.card,
              padding: 24,
              marginBottom: 24,
            }}>
              <h3 style={{ 
                fontSize: '20px', 
                fontWeight: theme.typography.fontWeights.semibold,
                color: theme.colors.textPrimary,
                fontFamily: theme.typography.fontFamily,
                marginBottom: 16,
              }}>
                Match Details
              </h3>
              
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 16 }}>
                <div>
                  <label style={{ 
                    display: 'block',
                    marginBottom: 8,
                    color: theme.colors.textSecondary,
                    fontFamily: theme.typography.fontFamily,
                    fontWeight: theme.typography.fontWeights.medium,
                  }}>
                    {selectedTeam.name} Score
                  </label>
                  <input
                    type="number"
                    min="0"
                    value={matchData.score_home}
                    onChange={(e) => setMatchData(prev => ({ ...prev, score_home: e.target.value }))}
                    style={{
                      ...theme.styles.input,
                      width: '100%',
                    }}
                    required
                  />
                </div>
                
                <div>
                  <label style={{ 
                    display: 'block',
                    marginBottom: 8,
                    color: theme.colors.textSecondary,
                    fontFamily: theme.typography.fontFamily,
                    fontWeight: theme.typography.fontWeights.medium,
                  }}>
                    Opponent Score
                  </label>
                  <input
                    type="number"
                    min="0"
                    value={matchData.score_away}
                    onChange={(e) => setMatchData(prev => ({ ...prev, score_away: e.target.value }))}
                    style={{
                      ...theme.styles.input,
                      width: '100%',
                    }}
                    required
                  />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 16 }}>
                               <div>
                 <label style={{ 
                   display: 'block',
                   marginBottom: 8,
                   color: theme.colors.textSecondary,
                   fontFamily: theme.typography.fontFamily,
                   fontWeight: theme.typography.fontWeights.medium,
                 }}>
                   Gameweek
                 </label>
                 <input
                   type="number"
                   min="1"
                   value={matchData.gameweek}
                   onChange={(e) => setMatchData(prev => ({ ...prev, gameweek: e.target.value }))}
                   style={{
                     ...theme.styles.input,
                     width: '100%',
                   }}
                 />

               </div>
               
               <div>
                 <label style={{ 
                   display: 'block',
                   marginBottom: 8,
                   color: theme.colors.textSecondary,
                   fontFamily: theme.typography.fontFamily,
                   fontWeight: theme.typography.fontWeights.medium,
                 }}>
                   Season
                 </label>
                 <input
                   type="text"
                   value={matchData.season}
                   onChange={(e) => setMatchData(prev => ({ ...prev, season: e.target.value }))}
                   style={{
                     ...theme.styles.input,
                     width: '100%',
                   }}
                 />

               </div>
              </div>

              <div>
                <label style={{ 
                  display: 'block',
                  marginBottom: 8,
                  color: theme.colors.textSecondary,
                  fontFamily: theme.typography.fontFamily,
                  fontWeight: theme.typography.fontWeights.medium,
                }}>
                  Match Date
                </label>
                <input
                  type="date"
                  value={matchData.played_at}
                  onChange={(e) => setMatchData(prev => ({ ...prev, played_at: e.target.value }))}
                  style={{
                    ...theme.styles.input,
                    width: '100%',
                    maxWidth: 200,
                  }}
                  required
                />
              </div>
            </div>

            {/* Opponent Selection */}
            <div style={{
              ...theme.styles.card,
              padding: 24,
              marginBottom: 24,
            }}>
              <h3 style={{ 
                fontSize: '20px', 
                fontWeight: theme.typography.fontWeights.semibold,
                color: theme.colors.textPrimary,
                fontFamily: theme.typography.fontFamily,
                marginBottom: 16,
              }}>
                Opponent
              </h3>
              
              {!showNewOpponent ? (
                <div>
                  <select
                    value={matchData.opponent_name}
                    onChange={(e) => handleOpponentSelect(e.target.value)}
                    style={{
                      ...theme.styles.input,
                      width: '100%',
                      maxWidth: 400,
                      marginBottom: 16,
                    }}
                    required
                  >
                    <option value="">Select opponent...</option>
                    {opponents.map(opponent => (
                      <option key={opponent.id} value={opponent.name}>
                        {opponent.name}
                      </option>
                    ))}
                  </select>
                  
                  <button
                    type="button"
                    onClick={() => setShowNewOpponent(true)}
                    style={{
                      ...theme.styles.button.secondary,
                      padding: '8px 16px',
                      fontSize: '14px',
                    }}
                  >
                    + Add New Opponent
                  </button>
                </div>
              ) : (
                <div>
                  <input
                    type="text"
                    value={newOpponentName}
                    onChange={(e) => setNewOpponentName(e.target.value)}
                    placeholder="Enter opponent name..."
                    style={{
                      ...theme.styles.input,
                      width: '100%',
                      maxWidth: 400,
                      marginBottom: 16,
                    }}
                  />
                  
                  <div style={{ display: 'flex', gap: 8 }}>
                    <button
                      type="button"
                      onClick={handleCreateOpponent}
                      style={{
                        ...theme.styles.button.primary,
                        padding: '8px 16px',
                        fontSize: '14px',
                      }}
                    >
                      Add Opponent
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setShowNewOpponent(false)
                        setNewOpponentName('')
                      }}
                      style={{
                        ...theme.styles.button.secondary,
                        padding: '8px 16px',
                        fontSize: '14px',
                      }}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Player Selection */}
            <div style={{
              ...theme.styles.card,
              padding: 24,
              marginBottom: 24,
            }}>
              <h3 style={{ 
                fontSize: '20px', 
                fontWeight: theme.typography.fontWeights.semibold,
                color: theme.colors.textPrimary,
                fontFamily: theme.typography.fontFamily,
                marginBottom: 16,
              }}>
                Players & Goals
              </h3>
              
              <p style={{ 
                fontSize: '14px', 
                color: theme.colors.textSecondary,
                fontFamily: theme.typography.fontFamily,
                marginBottom: 16,
              }}>
                Select players who played and record their goals
              </p>
              
              <div style={{ display: 'grid', gap: 12 }}>
                {teamPlayers.map(player => (
                  <div
                    key={player.id}
                    style={{
                      padding: 16,
                      background: selectedPlayers.includes(player.id) ? theme.colors.primary + '10' : theme.colors.content,
                      borderRadius: 8,
                      border: `2px solid ${selectedPlayers.includes(player.id) ? theme.colors.primary : theme.colors.border}`,
                      display: 'flex',
                      alignItems: 'center',
                      gap: 16,
                    }}
                  >
                    <input
                      type="checkbox"
                      checked={selectedPlayers.includes(player.id)}
                      onChange={() => handlePlayerToggle(player.id)}
                      style={{
                        width: 20,
                        height: 20,
                        cursor: 'pointer',
                      }}
                    />
                    
                    <div style={{ flex: 1 }}>
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
                        {player.position || 'Player'}
                      </p>
                    </div>
                    
                    {selectedPlayers.includes(player.id) && (
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <label style={{ 
                          fontSize: '14px',
                          color: theme.colors.textSecondary,
                          fontFamily: theme.typography.fontFamily,
                        }}>
                          Goals:
                        </label>
                        <input
                          type="number"
                          min="0"
                          max={parseInt(matchData.score_home) || 99}
                          value={playerGoals[player.id] || 0}
                          onChange={(e) => handlePlayerGoalsChange(player.id, e.target.value)}
                          style={{
                            ...theme.styles.input,
                            width: 60,
                            textAlign: 'center',
                          }}
                        />
                      </div>
                    )}
                  </div>
                ))}
              </div>
              
              {selectedPlayers.length > 0 && (
                <div style={{
                  marginTop: 16,
                  padding: 16,
                  background: theme.colors.success + '10',
                  borderRadius: 8,
                  border: `1px solid ${theme.colors.success}`,
                }}>
                  <p style={{ 
                    fontSize: '14px', 
                    color: theme.colors.success,
                    fontFamily: theme.typography.fontFamily,
                    margin: 0,
                    textAlign: 'center',
                  }}>
                    Total Goals: {Object.values(playerGoals).reduce((sum, goals) => sum + goals, 0)} / {matchData.score_home || 0}
                  </p>
                </div>
              )}
            </div>
          </>
        )}

        {/* Submit Button */}
        <div style={{ display: 'flex', gap: 16, justifyContent: 'flex-end' }}>
          <button
            type="button"
            onClick={onBack}
            style={{
              ...theme.styles.button.secondary,
              padding: '12px 24px',
              fontSize: '16px',
            }}
          >
            Cancel
          </button>
          

          
          <button
            type="submit"
            disabled={!selectedTeam || isSubmitting}
            style={{
              ...theme.styles.button.primary,
              padding: '12px 24px',
              fontSize: '16px',
              opacity: (!selectedTeam || isSubmitting) ? 0.6 : 1,
            }}
          >
            {isSubmitting ? 'Logging Match...' : 'Log Match Result'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default LogMatch 