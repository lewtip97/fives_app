import { createContext, useContext, useState, useEffect } from 'react'
import { supabase } from '../supabaseClient'

const MatchCacheContext = createContext()

export const useMatchCache = () => {
  const context = useContext(MatchCacheContext)
  if (!context) {
    throw new Error('useMatchCache must be used within a MatchCacheProvider')
  }
  return context
}

export const MatchCacheProvider = ({ children }) => {
  const [lastMatchCache, setLastMatchCache] = useState({})
  const [isLoading, setIsLoading] = useState(false)
  const [cacheStats, setCacheStats] = useState({ hits: 0, misses: 0, size: 0 })
  const [requestQueue, setRequestQueue] = useState(new Set())
  const [lastRequestTime, setLastRequestTime] = useState(0)

  // Load cached data from localStorage on mount
  useEffect(() => {
    const cached = localStorage.getItem('fives_last_match_cache')
    if (cached) {
      try {
        setLastMatchCache(JSON.parse(cached))
      } catch (error) {
        console.error('Failed to parse cached match data:', error)
      }
    }
  }, [])

  // Save cache to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('fives_last_match_cache', JSON.stringify(lastMatchCache))
  }, [lastMatchCache])

  // Get last match info for a team (from cache or fetch if needed)
  const getLastMatchInfo = async (teamId) => {
    // Check cache first
    if (lastMatchCache[teamId] && !isStale(lastMatchCache[teamId])) {
      // Cache hit - update stats
      setCacheStats(prev => ({
        ...prev,
        hits: prev.hits + 1
      }))
      return lastMatchCache[teamId]
    }

    // Rate limiting: max 10 requests per minute per user
    const now = Date.now()
    const oneMinuteAgo = now - 60 * 1000
    
    if (now - lastRequestTime < 6000) { // 6 seconds between requests
      // Return cached data if available, otherwise wait
      if (lastMatchCache[teamId]) {
        return lastMatchCache[teamId]
      }
      // Wait a bit and try again
      await new Promise(resolve => setTimeout(resolve, 1000))
    }
    
    // If not in cache or stale, fetch from API
    setIsLoading(true)
    setLastRequestTime(now)
    
    try {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session) return null

      const response = await fetch(`http://localhost:8000/matches/`, {
        headers: {
          'Authorization': `Bearer ${session.access_token}`,
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) throw new Error('Failed to fetch matches')

      const matches = await response.json()
      const teamMatches = matches.filter(match => match.team_id === teamId)
      
      let lastMatchInfo = null
      if (teamMatches.length > 0) {
        // Sort by date and get the most recent
        const sortedMatches = teamMatches.sort((a, b) => 
          new Date(b.played_at) - new Date(a.played_at)
        )
        const lastMatch = sortedMatches[0]
        
        lastMatchInfo = {
          season: lastMatch.season || '2024',
          gameweek: lastMatch.gameweek || 1,
          lastUpdated: new Date().toISOString(),
        }
      } else {
        // No previous matches, use defaults
        lastMatchInfo = {
          season: '2024',
          gameweek: 1,
          lastUpdated: new Date().toISOString(),
        }
      }

      // Update cache with size management
      setLastMatchCache(prev => {
        const newCache = {
          ...prev,
          [teamId]: lastMatchInfo
        }
        
        // Clean up if cache is too large
        if (isCacheTooLarge(newCache)) {
          return cleanupCache(newCache)
        }
        
        return newCache
      })

      // Update cache stats
      setCacheStats(prev => ({
        ...prev,
        misses: prev.misses + 1,
        size: getCacheSize(lastMatchCache)
      }))

      return lastMatchInfo
    } catch (error) {
      console.error('Error fetching last match info:', error)
      // Return cached data if available, otherwise defaults
      return lastMatchCache[teamId] || {
        season: '2024',
        gameweek: 1,
        lastUpdated: new Date().toISOString(),
      }
    } finally {
      setIsLoading(false)
    }
  }

  // Update cache when a new match is logged
  const updateCacheAfterMatch = (teamId, newSeason, newGameweek) => {
    setLastMatchCache(prev => ({
      ...prev,
      [teamId]: {
        season: newSeason,
        gameweek: newGameweek,
        lastUpdated: new Date().toISOString(),
      }
    }))
  }

  // Check if cached data is stale (older than 5 minutes)
  const isStale = (cachedData) => {
    if (!cachedData.lastUpdated) return true
    const fiveMinutesAgo = new Date(Date.now() - 5 * 60 * 1000)
    return new Date(cachedData.lastUpdated) < fiveMinutesAgo
  }

  // Calculate cache size in bytes
  const getCacheSize = (cache) => {
    try {
      return new Blob([JSON.stringify(cache)]).size
    } catch {
      return 0
    }
  }

  // Check if cache is too large (over 2MB)
  const isCacheTooLarge = (cache) => {
    return getCacheSize(cache) > 2 * 1024 * 1024 // 2MB limit
  }

  // Clean up old entries to reduce cache size
  const cleanupCache = (cache) => {
    const entries = Object.entries(cache)
    if (entries.length <= 10) return cache // Keep at least 10 entries
    
    // Sort by last updated and remove oldest entries
    const sortedEntries = entries.sort((a, b) => 
      new Date(b[1].lastUpdated) - new Date(a[1].lastUpdated)
    )
    
    // Keep only the 10 most recent entries
    return Object.fromEntries(sortedEntries.slice(0, 10))
  }

  // Clear cache for a specific team
  const clearTeamCache = (teamId) => {
    setLastMatchCache(prev => {
      const newCache = { ...prev }
      delete newCache[teamId]
      return newCache
    })
  }

  // Clear all cache
  const clearAllCache = () => {
    setLastMatchCache({})
  }

  const value = {
    lastMatchCache,
    isLoading,
    cacheStats,
    getLastMatchInfo,
    updateCacheAfterMatch,
    clearTeamCache,
    clearAllCache,
  }

  return (
    <MatchCacheContext.Provider value={value}>
      {children}
    </MatchCacheContext.Provider>
  )
} 