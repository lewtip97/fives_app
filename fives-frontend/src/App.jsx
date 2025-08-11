import { useEffect, useState } from 'react'
import { Auth } from '@supabase/auth-ui-react'
import { ThemeSupa } from '@supabase/auth-ui-shared'
import { supabase } from './supabaseClient'
import Layout from './components/Layout'
import Teams from './pages/Teams'
import TeamOverview from './pages/TeamOverview'
import Landing from './pages/Landing'
import LogMatch from './pages/LogMatch'
import Stats from './pages/Stats'
import { MatchCacheProvider } from './contexts/MatchCacheContext'
import { theme } from './theme'
import './App.css'

function App() {
  const [user, setUser] = useState(null)
  const [currentPage, setCurrentPage] = useState('landing')
  const [selectedTeamId, setSelectedTeamId] = useState(null)

  const getBreadcrumbs = () => {
    switch (currentPage) {
      case 'landing':
        return [
          { label: 'Dashboard' }
        ]
      case 'teams':
        return [
          { label: 'Dashboard', onClick: () => setCurrentPage('landing') },
          { label: 'Teams' }
        ]
      case 'team-overview':
        return [
          { label: 'Dashboard', onClick: () => setCurrentPage('landing') },
          { label: 'Teams', onClick: () => setCurrentPage('teams') },
          { label: 'Team Details' }
        ]
      case 'log-match':
        return [
          { label: 'Dashboard', onClick: () => setCurrentPage('landing') },
          { label: 'Log Match' }
        ]
      case 'players':
        return [
          { label: 'Dashboard', onClick: () => setCurrentPage('landing') },
          { label: 'Players' }
        ]
      case 'stats':
        return [
          { label: 'Dashboard', onClick: () => setCurrentPage('landing') },
          { label: 'Stats' }
        ]
      default:
        return [
          { label: 'Dashboard' }
        ]
    }
  }

  useEffect(() => {
    // Check for an existing session on mount
    supabase.auth.getUser().then(({ data }) => {
      setUser(data.user)
    })

    // Listen for auth state changes
    const { data: listener } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
    })

    // Cleanup the listener on unmount
    return () => {
      listener.subscription.unsubscribe()
    }
  }, [])

  const handleViewTeam = (teamId) => {
    setSelectedTeamId(teamId)
    setCurrentPage('team-overview')
  }

  const handleBackToTeams = () => {
    setSelectedTeamId(null)
    setCurrentPage('teams')
  }

  const handleNavigate = (page) => {
    setCurrentPage(page)
    if (page !== 'team-overview') {
      setSelectedTeamId(null)
    }
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'landing':
        return <Landing user={user} onNavigate={handleNavigate} />
      case 'teams':
        return <Teams user={user} onViewTeam={handleViewTeam} />
      case 'team-overview':
        return <TeamOverview user={user} teamId={selectedTeamId} onBack={handleBackToTeams} />
      case 'log-match':
        return <LogMatch user={user} onBack={() => handleNavigate('landing')} />
      case 'players':
        return (
          <div style={{ textAlign: 'center', padding: 40 }}>
            <h2 style={{ color: theme.colors.primary }}>Players Page</h2>
            <p style={{ color: theme.colors.textSecondary }}>Coming soon...</p>
          </div>
        )
      case 'stats':
        return <Stats user={user} />
      default:
        return <Landing user={user} onNavigate={handleNavigate} />
    }
  }

  if (!user) {
    // Not logged in: show Auth UI
    return (
      <div
        style={{
          minHeight: '100vh',
          background: theme.colors.background,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '20px',
        }}
      >
        <div
          style={{
            ...theme.styles.card,
            padding: 40,
            maxWidth: 400,
            width: '100%',
          }}
        >
          <h2 style={{ 
            textAlign: 'center', 
            marginBottom: 24, 
            color: theme.colors.primary,
            fontFamily: theme.typography.fontFamily,
            fontWeight: theme.typography.fontWeights.bold,
            letterSpacing: theme.typography.letterSpacing.tight,
          }}>
            Fives App Login
          </h2>
          <Auth 
            supabaseClient={supabase} 
            appearance={theme.authTheme} 
          />
        </div>
      </div>
    )
  }

  // Logged in: show user info
    return (
    <MatchCacheProvider>
      <Layout
        user={user}
        onLogout={async () => {
          await supabase.auth.signOut()
          setUser(null)
        }}
        breadcrumbs={getBreadcrumbs()}
      >
        {renderPage()}
      </Layout>
    </MatchCacheProvider>
  )
}

export default App
