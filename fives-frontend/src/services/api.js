import { supabase } from '../supabaseClient'

const API_BASE_URL = 'http://localhost:8000'

// Helper function to get auth token
const getAuthToken = async () => {
  const { data: { session } } = await supabase.auth.getSession()
  return session?.access_token
}

// Helper function for API calls
const apiCall = async (endpoint, options = {}) => {
  const token = await getAuthToken()
  
  // Don't set Content-Type for FormData (let browser set it)
  const isFormData = options.body instanceof FormData
  
  const headers = {}
  
  // Only set Content-Type for non-FormData requests
  if (!isFormData) {
    headers['Content-Type'] = 'application/json'
  }
  
  // Add Authorization header if token exists
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  
  // Add any custom headers
  if (options.headers) {
    Object.assign(headers, options.headers)
  }
  
  const config = {
    headers: headers,
    ...options,
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config)
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    console.error('API Error:', errorData)
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
  }
  
  return response.json()
}

// Teams API
export const teamsApi = {
  // Get all teams for the current user
  getTeams: async () => {
    return apiCall('/teams/')
  },

  // Create a new team
  createTeam: async (teamData) => {
    return apiCall('/teams/', {
      method: 'POST',
      body: JSON.stringify(teamData),
    })
  },

  // Get a specific team
  getTeam: async (teamId) => {
    return apiCall(`/teams/${teamId}`)
  },

  // Update a team
  updateTeam: async (teamId, teamData) => {
    return apiCall(`/teams/${teamId}`, {
      method: 'PUT',
      body: JSON.stringify(teamData),
    })
  },

  // Delete a team
  deleteTeam: async (teamId) => {
    return apiCall(`/teams/${teamId}`, {
      method: 'DELETE',
    })
  },

  // Get team stats
  getTeamStats: async (teamId) => {
    return apiCall(`/teams/${teamId}/stats`)
  },


}

// Players API
export const playersApi = {
  // Get all players for the current user
  getPlayers: async () => {
    return apiCall('/players/')
  },

  // Create a new player
  createPlayer: async (playerData) => {
    return apiCall('/players/', {
      method: 'POST',
      body: JSON.stringify(playerData),
    })
  },

  // Update player profile picture via URL
  updatePlayerPicture: async (playerId, profilePicture) => {
    return apiCall(`/players/${playerId}`, {
      method: 'PUT',
      body: JSON.stringify({ profile_picture: profilePicture }),
    })
  },

  // Upload player picture
  async uploadPlayerPicture(playerId, file) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('player_id', playerId);

      const response = await fetch(`/api/players/${playerId}/picture`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Error uploading player picture:', error);
      throw error;
    }
  },

  // Get a specific player
  getPlayer: async (playerId) => {
    return apiCall(`/players/${playerId}`)
  },

  // Update a player
  updatePlayer: async (playerId, playerData) => {
    return apiCall(`/players/${playerId}`, {
      method: 'PUT',
      body: JSON.stringify(playerData),
    })
  },

  // Delete a player
  deletePlayer: async (playerId) => {
    return apiCall(`/players/${playerId}`, {
      method: 'DELETE',
    })
  },
}

// Matches API
export const matchesApi = {
  // Get all matches for the current user
  getMatches: async () => {
    return apiCall('/matches/')
  },

  // Create a new match with all data (match + appearances)
  createFullMatch: async (matchData) => {
    return apiCall('/matches/full', {
      method: 'POST',
      body: JSON.stringify(matchData),
    })
  },

  // Create a new match (legacy - not used)
  createMatch: async (matchData) => {
    return apiCall('/matches/', {
      method: 'POST',
      body: JSON.stringify(matchData),
    })
  },

  // Create an appearance for a player (legacy - not used)
  createAppearance: async (appearanceData) => {
    return apiCall('/appearances/', {
      method: 'POST',
      body: JSON.stringify(appearanceData),
    })
  },

  // Get a specific match
  getMatch: async (matchId) => {
    return apiCall(`/matches/${matchId}`)
  },

  // Update a match
  updateMatch: async (matchId, matchData) => {
    return apiCall(`/matches/${matchId}`, {
      method: 'PUT',
      body: JSON.stringify(matchData),
    })
  },


}

// Opponents API
export const opponentsApi = {
  // Get all opponents for a team
  getOpponents: async (teamId) => {
    return apiCall(`/opponents/?team_id=${teamId}`)
  },

  // Create a new opponent
  createOpponent: async (opponentData) => {
    return apiCall('/opponents/', {
      method: 'POST',
      body: JSON.stringify(opponentData),
    })
  },

  // Get a specific opponent
  getOpponent: async (opponentId) => {
    return apiCall(`/opponents/${opponentId}`)
  },

  // Delete an opponent
  deleteOpponent: async (opponentId) => {
    return apiCall(`/opponents/${opponentId}`, {
      method: 'DELETE',
    })
  },
}

// Stats API
export const statsApi = {
  // Generate all stats
  generateStats: async (teamId = null) => {
    const params = teamId ? `?team_id=${teamId}` : ''
    return apiCall(`/stats/generate${params}`, {
      method: 'POST',
    })
  },

  // Generate player stats
  generatePlayerStats: async (teamId = null) => {
    const params = teamId ? `?team_id=${teamId}` : ''
    return apiCall(`/stats/generate/players${params}`, {
      method: 'POST',
    })
  },

  // Generate team stats
  generateTeamStats: async (teamId = null) => {
    const params = teamId ? `?team_id=${teamId}` : ''
    return apiCall(`/stats/generate/teams${params}`, {
      method: 'POST',
    })
  },

  // Get player stats for a team
  getTeamPlayerStats: async (teamId) => {
    return apiCall(`/stats/players/${teamId}`)
  },

  // Get team stats for a team
  getTeamStats: async (teamId) => {
    return apiCall(`/stats/teams/${teamId}`)
  },

  // Get comprehensive team overview
  getTeamOverview: async (teamId) => {
    return apiCall(`/stats/overview/${teamId}`)
  },

  // Get individual player stats
  getPlayerStats: async (playerId) => {
    return apiCall(`/stats/player/${playerId}`)
  },

  // Predict match outcome
  predictMatch: async (teamId, opponentId, selectedPlayers) => {
    return apiCall('/stats/predict', {
      method: 'POST',
      body: JSON.stringify({
        team_id: teamId,
        opponent_id: opponentId,
        selected_players: selectedPlayers
      }),
    })
  },

  // Get recent activities for home page
  getRecentActivities: async () => {
    return apiCall('/stats/recent-activities')
  },
} 