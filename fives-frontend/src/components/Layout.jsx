import { supabase } from '../supabaseClient'
import { theme } from '../theme'

function Layout({ user, children, onLogout, breadcrumbs = [] }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw', background: theme.colors.background }}>
      {/* Header */}
      <header style={{
        background: theme.colors.header,
        borderBottom: `1px solid ${theme.colors.border}`,
        padding: '16px 32px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        minHeight: '80px',
        boxShadow: theme.colors.shadowLight,
      }}>
        {/* Breadcrumbs */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <h1 style={{
            fontSize: '24px',
            fontWeight: theme.typography.fontWeights.bold,
            color: theme.colors.primary,
            fontFamily: theme.typography.fontFamily,
            margin: 0,
            letterSpacing: theme.typography.letterSpacing.tight,
          }}>
            Fives App
          </h1>
          
          {breadcrumbs.length > 0 && (
            <>
              <span style={{
                color: theme.colors.textMuted,
                fontSize: '18px',
                margin: '0 8px',
              }}>
                ›
              </span>
              
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
                {breadcrumbs.map((crumb, index) => (
                  <div key={index} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span style={{
                      color: index === breadcrumbs.length - 1 ? theme.colors.textPrimary : theme.colors.textSecondary,
                      fontSize: '16px',
                      fontWeight: index === breadcrumbs.length - 1 ? theme.typography.fontWeights.semibold : theme.typography.fontWeights.normal,
                      fontFamily: theme.typography.fontFamily,
                      cursor: crumb.onClick ? 'pointer' : 'default',
                      transition: 'color 0.2s ease',
                    }} 
                    onClick={crumb.onClick}
                    onMouseEnter={crumb.onClick ? (e) => e.target.style.color = theme.colors.primary : undefined}
                    onMouseLeave={crumb.onClick ? (e) => e.target.style.color = index === breadcrumbs.length - 1 ? theme.colors.textPrimary : theme.colors.textSecondary : undefined}
                    >
                      {crumb.label}
                    </span>
                    {index < breadcrumbs.length - 1 && (
                      <span style={{
                        color: theme.colors.textMuted,
                        fontSize: '14px',
                      }}>
                        ›
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </>
          )}
        </div>

        {/* User Info */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <div style={{ textAlign: 'right' }}>
            <div style={{ 
              fontSize: '14px', 
              color: theme.colors.textSecondary,
              fontFamily: theme.typography.fontFamily,
              fontWeight: theme.typography.fontWeights.normal,
            }}>
              Account
            </div>
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
          <button onClick={onLogout} style={{
            background: 'none',
            border: `1px solid ${theme.colors.border}`,
            color: theme.colors.textSecondary,
            padding: '8px 16px',
            borderRadius: 6,
            cursor: 'pointer',
            fontSize: '14px',
            fontFamily: theme.typography.fontFamily,
            transition: 'all 0.2s ease',
          }} onMouseEnter={(e) => {
            e.target.style.background = theme.colors.border
            e.target.style.color = theme.colors.textPrimary
          }} onMouseLeave={(e) => {
            e.target.style.background = 'none'
            e.target.style.color = theme.colors.textSecondary
          }}>
            Log out
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <div style={{ flex: 1, padding: '32px', overflow: 'auto', background: theme.colors.content }}>
          {children}
        </div>
      </main>
      

    </div>
  )
}

export default Layout 