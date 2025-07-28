import { useEffect, useState } from 'react'
import { Auth } from '@supabase/auth-ui-react'
import { ThemeSupa } from '@supabase/auth-ui-shared'
import { supabase } from './supabaseClient'
import Layout from './components/Layout'
import Teams from './pages/Teams'
import { theme } from './theme'
import './App.css'

function App() {
  const [user, setUser] = useState(null)
  const [currentPage, setCurrentPage] = useState('teams')

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

  const renderPage = () => {
    switch (currentPage) {
      case 'teams':
        return <Teams user={user} />
      case 'players':
        return (
          <div style={{ textAlign: 'center', padding: 40 }}>
            <h2 style={{ color: theme.colors.primary }}>Players Page</h2>
            <p style={{ color: theme.colors.textSecondary }}>Coming soon...</p>
          </div>
        )
      case 'stats':
        return (
          <div style={{ textAlign: 'center', padding: 40 }}>
            <h2 style={{ color: theme.colors.primary }}>Stats Page</h2>
            <p style={{ color: theme.colors.textSecondary }}>Coming soon...</p>
          </div>
        )
      default:
        return <Teams user={user} />
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
    <Layout 
      user={user} 
      onLogout={async () => {
        await supabase.auth.signOut()
        setUser(null)
      }}
      currentPage={currentPage}
      onPageChange={setCurrentPage}
    >
      {renderPage()}
    </Layout>
  )
}

export default App
