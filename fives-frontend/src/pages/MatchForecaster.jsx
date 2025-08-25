import React, { useState, useEffect } from 'react'
import { teamsApi, statsApi } from '../services/api'
import { theme } from '../theme'

const MatchForecaster = ({ user, onNavigate, goBack }) => {
  const [teams, setTeams] = useState([])
  const [selectedTeam, setSelectedTeam] = useState(null)
  const [opponents, setOpponents] = useState([])
  const [selectedOpponent, setSelectedOpponent] = useState(null)
  const [availablePlayers, setAvailablePlayers] = useState([])
  const [selectedPlayers, setSelectedPlayers] = useState([])
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadTeams()
  }, [])

  const loadTeams = async () => {
    try {
      const teamsData = await teamsApi.getTeams()
      setTeams(teamsData)
    } catch (err) {
      setError('Failed to load teams')
    }
  }

  const handleTeamSelect = async (teamId) => {
    const team = teams.find(t => t.id === teamId)
    setSelectedTeam(team)
    setSelectedOpponent(null)
    setPrediction(null)
    
    if (team) {
      try {
        // Load team overview to get players and opponents
        const overview = await statsApi.getTeamOverview(teamId)
        setAvailablePlayers(overview.player_stats || [])
        setOpponents(overview.matches?.map(m => m.opponents).filter(Boolean) || [])
      } catch (err) {
        setError('Failed to load team data')
      }
    }
  }

  const handleOpponentSelect = (opponentId) => {
    const opponent = opponents.find(o => o.id === opponentId)
    setSelectedOpponent(opponent)
    setPrediction(null)
  }

  const handlePlayerToggle = (playerId) => {
    setSelectedPlayers(prev => {
      if (prev.includes(playerId)) {
        return prev.filter(id => id !== playerId)
      } else {
        return prev.concat(playerId)
      }
    })
  }

  const generatePrediction = async () => {
    if (!selectedTeam || !selectedOpponent || selectedPlayers.length === 0) {
      setError('Please select a team, opponent, and at least one player')
      return
    }

    setLoading(true)
    setError(null)

    try {
      // Call the real prediction API
      const prediction = await statsApi.predictMatch(
        selectedTeam.id,
        selectedOpponent.id,
        selectedPlayers
      )
      
      setPrediction(prediction)
    } catch (err) {
      setError('Failed to generate prediction: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const getResultColor = (teamScore, opponentScore) => {
    if (teamScore > opponentScore) return theme.colors.success
    if (teamScore === opponentScore) return theme.colors.warning
    return theme.colors.error
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ marginBottom: '30px' }}>
        <button
          onClick={goBack || (() => onNavigate('landing'))}
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
          Match Forecaster
        </h1>
        <p style={{
          fontSize: '16px',
          color: theme.colors.textSecondary,
          margin: '0 0 20px 0'
        }}>
          Predict match outcomes and player performance using our AI models
        </p>
      </div>

      {/* Configuration Section */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '24px',
        marginBottom: '30px'
      }}>
        {/* Team Selection */}
        <div style={{
          backgroundColor: theme.colors.backgroundSecondary,
          borderRadius: '8px',
          padding: '20px',
          border: `1px solid ${theme.colors.border}`
        }}>
          <h3 style={{
            fontSize: '18px',
            fontWeight: theme.typography.fontWeights.semibold,
            color: theme.colors.textPrimary,
            margin: '0 0 16px 0'
          }}>
            Select Your Team
          </h3>
          <select
            value={selectedTeam?.id || ''}
            onChange={(e) => handleTeamSelect(e.target.value)}
            style={{
              width: '100%',
              padding: '12px',
              borderRadius: '6px',
              border: `1px solid ${theme.colors.border}`,
              backgroundColor: theme.colors.backgroundPrimary,
              color: theme.colors.textPrimary,
              fontSize: '14px'
            }}
          >
            <option value="">Choose a team...</option>
            {teams.map(team => (
              <option key={team.id} value={team.id}>{team.name}</option>
            ))}
          </select>
        </div>

        {/* Opponent Selection */}
        <div style={{
          backgroundColor: theme.colors.backgroundSecondary,
          borderRadius: '8px',
          padding: '20px',
          border: `1px solid ${theme.colors.border}`
        }}>
          <h3 style={{
            fontSize: '18px',
            fontWeight: theme.typography.fontWeights.semibold,
            color: theme.colors.textPrimary,
            margin: '0 0 16px 0'
          }}>
            Select Opponent
          </h3>
          <select
            value={selectedOpponent?.id || ''}
            onChange={(e) => handleOpponentSelect(e.target.value)}
            disabled={!selectedTeam}
            style={{
              width: '100%',
              padding: '12px',
              borderRadius: '6px',
              border: `1px solid ${theme.colors.border}`,
              backgroundColor: selectedTeam ? theme.colors.backgroundPrimary : theme.colors.backgroundSecondary,
              color: theme.colors.textPrimary,
              fontSize: '14px',
              opacity: selectedTeam ? 1 : 0.6
            }}
          >
            <option value="">Choose opponent...</option>
            {opponents.map(opponent => (
              <option key={opponent.id} value={opponent.id}>{opponent.name}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Player Selection */}
      {selectedTeam && (
        <div style={{
          backgroundColor: theme.colors.backgroundSecondary,
          borderRadius: '8px',
          padding: '20px',
          border: `1px solid ${theme.colors.border}`,
          marginBottom: '30px'
        }}>
          <h3 style={{
            fontSize: '18px',
            fontWeight: theme.typography.fontWeights.semibold,
            color: theme.colors.textPrimary,
            margin: '0 0 16px 0'
          }}>
            Select Players for Prediction
          </h3>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
            gap: '12px'
          }}>
            {availablePlayers.map(player => (
              <label
                key={player.player_id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '8px 12px',
                  backgroundColor: selectedPlayers.includes(player.player_id) 
                    ? theme.colors.primary 
                    : theme.colors.backgroundPrimary,
                  color: selectedPlayers.includes(player.player_id) ? 'white' : theme.colors.textPrimary,
                  borderRadius: '6px',
                  cursor: 'pointer',
                  border: `1px solid ${theme.colors.border}`,
                  transition: 'all 0.2s ease'
                }}
              >
                <input
                  type="checkbox"
                  checked={selectedPlayers.includes(player.player_id)}
                  onChange={() => handlePlayerToggle(player.player_id)}
                  style={{ margin: 0 }}
                />
                <span style={{ fontSize: '14px' }}>
                  {player.player_name}
                </span>
              </label>
            ))}
          </div>
        </div>
      )}

      {/* Generate Prediction Button */}
      {selectedTeam && selectedOpponent && selectedPlayers.length > 0 && (
        <div style={{ textAlign: 'center', marginBottom: '30px' }}>
          <button
            onClick={generatePrediction}
            disabled={loading}
            style={{
              padding: '16px 32px',
              backgroundColor: theme.colors.primary,
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '16px',
              fontWeight: theme.typography.fontWeights.semibold,
              cursor: loading ? 'not-allowed' : 'pointer',
              opacity: loading ? 0.7 : 1,
              transition: 'all 0.2s ease'
            }}
          >
            {loading ? 'Generating Prediction...' : 'Generate Match Prediction'}
          </button>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div style={{
          backgroundColor: theme.colors.error,
          color: 'white',
          padding: '16px',
          borderRadius: '8px',
          marginBottom: '20px',
          textAlign: 'center'
        }}>
          {error}
        </div>
      )}

      {/* Prediction Results */}
      {prediction && (
        <div style={{
          backgroundColor: theme.colors.backgroundSecondary,
          borderRadius: '8px',
          padding: '24px',
          border: `1px solid ${theme.colors.border}`
        }}>
          <h3 style={{
            fontSize: '24px',
            fontWeight: theme.typography.fontWeights.bold,
            color: theme.colors.textPrimary,
            margin: '0 0 20px 0',
            textAlign: 'center'
          }}>
            Match Prediction
          </h3>

          {/* Score Prediction */}
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            gap: '20px',
            marginBottom: '30px'
          }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{
                fontSize: '48px',
                fontWeight: theme.typography.fontWeights.bold,
                color: theme.colors.primary
              }}>
                {prediction.team_score}
              </div>
              <div style={{ fontSize: '14px', color: theme.colors.textSecondary }}>
                {selectedTeam?.name}
              </div>
            </div>
            
            <div style={{
              fontSize: '24px',
              fontWeight: theme.typography.fontWeights.bold,
              color: theme.colors.textSecondary
            }}>
              vs
            </div>
            
            <div style={{ textAlign: 'center' }}>
              <div style={{
                fontSize: '48px',
                fontWeight: theme.typography.fontWeights.bold,
                color: theme.colors.error
              }}>
                {prediction.opponent_score}
              </div>
              <div style={{ fontSize: '14px', color: theme.colors.textSecondary }}>
                {selectedOpponent?.name}
              </div>
            </div>
          </div>

          {/* Result and Confidence */}
          <div style={{
            textAlign: 'center',
            marginBottom: '30px'
          }}>
            <div style={{
              fontSize: '18px',
              fontWeight: theme.typography.fontWeights.semibold,
              color: getResultColor(prediction.team_score, prediction.opponent_score),
              marginBottom: '8px'
            }}>
              {prediction.team_score > prediction.opponent_score ? 'Predicted Win' : 
               prediction.team_score === prediction.opponent_score ? 'Predicted Draw' : 'Predicted Loss'}
            </div>
            <div style={{
              fontSize: '14px',
              color: theme.colors.textSecondary
            }}>
              Match Confidence: {(prediction.match_confidence * 100).toFixed(0)}%
            </div>
          </div>

          {/* Player Predictions */}
          <div>
            <h4 style={{
              fontSize: '18px',
              fontWeight: theme.typography.fontWeights.semibold,
              color: theme.colors.textPrimary,
              margin: '0 0 16px 0'
            }}>
              Player Goal Predictions
            </h4>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
              gap: '16px'
            }}>
              {prediction.player_predictions.map(player => (
                <div
                  key={player.player_id}
                  style={{
                    backgroundColor: theme.colors.backgroundPrimary,
                    padding: '16px',
                    borderRadius: '6px',
                    border: `1px solid ${theme.colors.border}`,
                    textAlign: 'center'
                  }}
                >
                  <div style={{
                    fontSize: '16px',
                    fontWeight: theme.typography.fontWeights.semibold,
                    color: theme.colors.textPrimary,
                    marginBottom: '8px'
                  }}>
                    {player.player_name}
                  </div>
                  <div style={{
                    fontSize: '24px',
                    fontWeight: theme.typography.fontWeights.bold,
                    color: theme.colors.primary,
                    marginBottom: '4px'
                  }}>
                    {player.predicted_goals}
                  </div>
                  <div style={{
                    fontSize: '12px',
                    color: theme.colors.textSecondary
                  }}>
                    predicted goals
                  </div>
                  <div style={{
                    fontSize: '12px',
                    color: theme.colors.textSecondary,
                    marginTop: '8px'
                  }}>
                    Confidence: {(player.confidence * 100).toFixed(0)}%
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default MatchForecaster
