import { supabase } from '../supabaseClient'
import { theme } from '../theme'

const navBtnStyle = {
  width: '100%',
  padding: '12px 0',
  background: 'none',
  color: '#fff',
  border: 'none',
  borderRadius: 0,
  textAlign: 'left',
  fontSize: 16,
  fontWeight: 500,
  cursor: 'pointer',
  marginBottom: 8,
  paddingLeft: 32,
  transition: 'background 0.2s',
  fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
  letterSpacing: '-0.025em',
}

const navBtnHoverStyle = {
  ...navBtnStyle,
  background: 'rgba(255, 255, 0, 0.1)',
}

function Layout({ user, children, onLogout, currentPage, onPageChange }) {
  return (
    <div style={{ display: 'flex', height: '100vh', width: '100vw', background: theme.colors.background }}>
      {/* Sidebar */}
      <aside
        style={{
          width: 220,
          background: theme.colors.sidebar,
          color: '#fff',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          padding: '32px 0',
          boxShadow: theme.colors.shadowLight,
          borderRight: `1px solid ${theme.colors.border}`,
        }}
      >
        <div style={{ 
          fontWeight: theme.typography.fontWeights.extrabold, 
          fontSize: 28, 
          marginBottom: 40, 
          letterSpacing: theme.typography.letterSpacing.wide, 
          color: theme.colors.primary,
          fontFamily: theme.typography.fontFamily,
        }}>
          Fives App
        </div>
        <nav style={{ width: '100%' }}>
          <ul style={{ listStyle: 'none', padding: 0, width: '100%' }}>
            <li>
              <button 
                style={{
                  ...navBtnStyle,
                  background: currentPage === 'teams' ? 'rgba(255, 215, 0, 0.2)' : 'none',
                  color: currentPage === 'teams' ? theme.colors.primary : '#fff',
                }}
                onMouseEnter={(e) => {
                  if (currentPage !== 'teams') {
                    e.target.style.background = 'rgba(255, 215, 0, 0.1)'
                  }
                }}
                onMouseLeave={(e) => {
                  if (currentPage !== 'teams') {
                    e.target.style.background = 'none'
                  }
                }}
                onClick={() => onPageChange('teams')}
              >
                Teams
              </button>
            </li>
            <li>
              <button 
                style={{
                  ...navBtnStyle,
                  background: currentPage === 'players' ? 'rgba(255, 215, 0, 0.2)' : 'none',
                  color: currentPage === 'players' ? theme.colors.primary : '#fff',
                }}
                onMouseEnter={(e) => {
                  if (currentPage !== 'players') {
                    e.target.style.background = 'rgba(255, 215, 0, 0.1)'
                  }
                }}
                onMouseLeave={(e) => {
                  if (currentPage !== 'players') {
                    e.target.style.background = 'none'
                  }
                }}
                onClick={() => onPageChange('players')}
              >
                Players
              </button>
            </li>
            <li>
              <button 
                style={{
                  ...navBtnStyle,
                  background: currentPage === 'stats' ? 'rgba(255, 215, 0, 0.2)' : 'none',
                  color: currentPage === 'stats' ? theme.colors.primary : '#fff',
                }}
                onMouseEnter={(e) => {
                  if (currentPage !== 'stats') {
                    e.target.style.background = 'rgba(255, 215, 0, 0.1)'
                  }
                }}
                onMouseLeave={(e) => {
                  if (currentPage !== 'stats') {
                    e.target.style.background = 'none'
                  }
                }}
                onClick={() => onPageChange('stats')}
              >
                Stats
              </button>
            </li>
          </ul>
        </nav>
        <div style={{ flex: 1 }} />
        <button
          style={{
            width: '80%',
            padding: '10px 0',
            background: theme.colors.primary,
            color: theme.colors.primaryText,
            border: 'none',
            borderRadius: 8,
            cursor: 'pointer',
            fontWeight: theme.typography.fontWeights.semibold,
            fontSize: 16,
            marginBottom: 16,
            transition: 'all 0.2s',
            fontFamily: theme.typography.fontFamily,
            letterSpacing: theme.typography.letterSpacing.tight,
          }}
          onMouseEnter={(e) => e.target.style.background = theme.colors.primaryHover}
          onMouseLeave={(e) => e.target.style.background = theme.colors.primary}
          onClick={onLogout}
        >
          Log out
        </button>
      </aside>

      {/* Main content */}
      <main style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        {/* Header */}
        <header
          style={{
            background: theme.colors.header,
            borderBottom: `1px solid ${theme.colors.border}`,
            padding: '16px 32px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            boxShadow: theme.colors.shadowLight,
          }}
        >
          <div>
            <h1 style={{ 
              fontSize: '24px', 
              fontWeight: theme.typography.fontWeights.bold, 
              color: theme.colors.primary, 
              margin: 0,
              fontFamily: theme.typography.fontFamily,
              letterSpacing: theme.typography.letterSpacing.tight,
            }}>
              {currentPage === 'teams' ? 'Teams' : 
               currentPage === 'players' ? 'Players' : 
               currentPage === 'stats' ? 'Stats' : 'Dashboard'}
            </h1>
            <p style={{ 
              fontSize: '14px', 
              color: theme.colors.textSecondary, 
              margin: '4px 0 0 0',
              fontFamily: theme.typography.fontFamily,
              fontWeight: theme.typography.fontWeights.normal,
            }}>
              Welcome back, {user.email}
            </p>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ textAlign: 'right' }}>
              <div style={{ 
                fontSize: '14px', 
                color: theme.colors.textSecondary,
                fontFamily: theme.typography.fontFamily,
                fontWeight: theme.typography.fontWeights.normal,
              }}>Account</div>
              <div style={{ 
                fontSize: '16px', 
                fontWeight: theme.typography.fontWeights.semibold, 
                color: theme.colors.textPrimary,
                fontFamily: theme.typography.fontFamily,
              }}>
                {user.email}
              </div>
            </div>
            <div
              style={{
                width: '40px',
                height: '40px',
                borderRadius: '50%',
                background: theme.colors.primary,
                color: theme.colors.primaryText,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: theme.typography.fontWeights.bold,
                fontSize: '16px',
                fontFamily: theme.typography.fontFamily,
              }}
            >
              {user.email.charAt(0).toUpperCase()}
            </div>
          </div>
        </header>

        {/* Content Area */}
        <div style={{ flex: 1, padding: '32px', overflow: 'auto', background: theme.colors.content }}>
          {children}
        </div>
      </main>
    </div>
  )
}

export default Layout 