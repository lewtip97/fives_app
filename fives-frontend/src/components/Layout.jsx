import { supabase } from '../supabaseClient'
import { theme } from '../theme'

function Layout({ user, children, onLogout, breadcrumbs = [] }) {
  return (
    <div style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      height: '100vh', 
      width: '100vw',
      position: 'relative',
    }}>
      {/* Header - Glass morphism */}
      <header style={{
        ...theme.glass.medium,
        padding: '20px 32px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        minHeight: '80px',
        boxShadow: theme.colors.shadowLight,
        position: 'sticky',
        top: 0,
        zIndex: 1000,
        borderBottom: `1px solid ${theme.colors.glassBorder}`,
      }}>
        {/* Breadcrumbs */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <h1 style={{
            fontSize: '26px',
            fontWeight: theme.typography.fontWeights.bold,
            color: theme.colors.textPrimary,
            fontFamily: theme.typography.fontFamily,
            margin: 0,
            letterSpacing: theme.typography.letterSpacing.tight,
            background: 'linear-gradient(135deg, #FFD700 0%, #FFEB3B 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
          }}>
            Fives App
          </h1>
          
          {breadcrumbs.length > 0 && (
            <>
              <span style={{
                color: theme.colors.textMuted,
                fontSize: '16px',
                margin: '0 4px',
                opacity: 0.5,
              }}>
                ›
              </span>
              
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
                {breadcrumbs.map((crumb, index) => (
                  <div key={index} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span style={{
                      color: index === breadcrumbs.length - 1 ? theme.colors.textPrimary : theme.colors.textSecondary,
                      fontSize: '15px',
                      fontWeight: index === breadcrumbs.length - 1 ? theme.typography.fontWeights.semibold : theme.typography.fontWeights.normal,
                      fontFamily: theme.typography.fontFamily,
                      cursor: crumb.onClick ? 'pointer' : 'default',
                      transition: 'all 0.2s ease',
                      padding: '4px 8px',
                      borderRadius: 8,
                    }} 
                    onClick={crumb.onClick}
                    onMouseEnter={crumb.onClick ? (e) => {
                      e.target.style.color = theme.colors.primary;
                      e.target.style.background = 'rgba(255, 215, 0, 0.1)';
                    } : undefined}
                    onMouseLeave={crumb.onClick ? (e) => {
                      e.target.style.color = index === breadcrumbs.length - 1 ? theme.colors.textPrimary : theme.colors.textSecondary;
                      e.target.style.background = 'transparent';
                    } : undefined}
                    >
                      {crumb.label}
                    </span>
                    {index < breadcrumbs.length - 1 && (
                      <span style={{
                        color: theme.colors.textMuted,
                        fontSize: '14px',
                        opacity: 0.5,
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
              fontSize: '13px', 
              color: theme.colors.textMuted,
              fontFamily: theme.typography.fontFamily,
              fontWeight: theme.typography.fontWeights.normal,
              opacity: 0.8,
            }}>
              Signed in as
            </div>
            <div style={{ 
              fontSize: '15px', 
              fontWeight: theme.typography.fontWeights.semibold, 
              color: theme.colors.textPrimary,
              fontFamily: theme.typography.fontFamily,
            }}>
              {user.email}
            </div>
          </div>
          <div
            style={{
              width: '44px',
              height: '44px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #FFD700 0%, #FFEB3B 100%)',
              color: '#000000',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: theme.typography.fontWeights.bold,
              fontSize: '18px',
              fontFamily: theme.typography.fontFamily,
              boxShadow: '0 4px 12px rgba(255, 215, 0, 0.4)',
              border: '2px solid rgba(255, 215, 0, 0.5)',
            }}
          >
            {user.email.charAt(0).toUpperCase()}
          </div>
          <button onClick={onLogout} style={{
            ...theme.styles.button.secondary,
            padding: '10px 20px',
            fontSize: '15px',
            fontFamily: theme.typography.fontFamily,
          }} onMouseEnter={(e) => {
            e.target.style.background = 'rgba(255, 215, 0, 0.2)'
            e.target.style.transform = 'translateY(-1px)'
          }} onMouseLeave={(e) => {
            e.target.style.background = 'rgba(255, 215, 0, 0.1)'
            e.target.style.transform = 'translateY(0)'
          }}>
            Log out
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main style={{ 
        flex: 1, 
        display: 'flex', 
        flexDirection: 'column', 
        overflow: 'hidden',
        position: 'relative',
      }}>
        <div style={{ 
          flex: 1, 
          padding: '32px', 
          overflow: 'auto',
          position: 'relative',
          zIndex: 1,
        }}>
          {children}
        </div>
      </main>
      

    </div>
  )
}

export default Layout 