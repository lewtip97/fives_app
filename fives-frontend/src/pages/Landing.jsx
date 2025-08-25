import { useState, useEffect } from 'react'
import { theme } from '../theme'
import { statsApi } from '../services/api'

function Landing({ user, onNavigate }) {
  const [activities, setActivities] = useState([])
  const [loadingActivities, setLoadingActivities] = useState(true)
  
  useEffect(() => {
    const fetchActivities = async () => {
      try {
        setLoadingActivities(true)
        const activitiesData = await statsApi.getRecentActivities()
        setActivities(activitiesData)
      } catch (error) {
        console.error('Error fetching activities:', error)
        // Fallback to empty activities array
        setActivities([])
      } finally {
        setLoadingActivities(false)
      }
    }

    if (user) {
      fetchActivities()
    } else {
      // No user, skipping activities fetch
    }
  }, [user])

  const getActivityColor = (activityType, activityColor) => {
    switch (activityType) {
      case 'match':
        return theme.colors.primary
      case 'milestone':
        return theme.colors.success
      case 'team_change':
        return theme.colors.info || '#6366f1'
      default:
        return theme.colors.textSecondary
    }
  }

  const [quickActions] = useState([
    {
      title: "Manage Teams",
      description: "Create teams, add players, and organize your squad",
      action: () => onNavigate('teams'),
      color: theme.colors.primary,
    },
    {
      title: "Log Match Result",
      description: "Record game scores, player performances, and track stats",
      action: () => onNavigate('log-match'),
      color: theme.colors.error,
    },
    {
      title: "View Statistics",
      description: "Analyze team performance, player stats, and trends",
      action: () => onNavigate('stats'),
      color: theme.colors.warning,
    },
    {
      title: "Match Forecaster",
      description: "Predict match outcomes and player performance",
      action: () => onNavigate('match-forecaster'),
      color: theme.colors.info || '#6366f1',
    },
  ])

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto' }}>
      {/* Hero Section */}
      <div style={{
        textAlign: 'center',
        padding: '60px 20px',
        marginBottom: 48,
      }}>
        <h1 style={{
          fontSize: '48px',
          fontWeight: theme.typography.fontWeights.bold,
          color: theme.colors.primary,
          fontFamily: theme.typography.fontFamily,
          letterSpacing: theme.typography.letterSpacing.tight,
          marginBottom: 16,
          textShadow: '0 4px 8px rgba(0,0,0,0.1)',
        }}>
          Welcome to Fives App
        </h1>
        <p style={{
          fontSize: '20px',
          color: theme.colors.textSecondary,
          fontFamily: theme.typography.fontFamily,
          fontWeight: theme.typography.fontWeights.normal,
          maxWidth: 600,
          margin: '0 auto',
          lineHeight: 1.6,
        }}>
          The ultimate platform for managing your 5-a-side football team, tracking performance, and analyzing stats.
        </p>
      </div>

      {/* Quick Actions Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
        gap: 24,
        marginBottom: 48,
        maxWidth: 1200,
        margin: '0 auto 48px auto',
      }}>
        {quickActions.map((action, index) => (
          <div
            key={index}
            onClick={action.action}
            style={{
              background: theme.colors.card,
              padding: 32,
              borderRadius: 16,
              border: `1px solid ${theme.colors.border}`,
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              boxShadow: theme.colors.shadowLight,
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-4px)'
              e.currentTarget.style.boxShadow = theme.colors.shadow
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)'
              e.currentTarget.style.boxShadow = theme.colors.shadowLight
            }}
          >
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              textAlign: 'center',
            }}>
              {/* Logo */}
              <div style={{
                width: 64,
                height: 64,
                borderRadius: '50%',
                background: action.color,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: 20,
                boxShadow: theme.colors.shadowLight,
              }}>
                {action.title === "Manage Teams" && (
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                    <circle cx="9" cy="7" r="4"/>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                  </svg>
                )}
                {action.title === "Log Match Result" && (
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
                    <line x1="9" y1="9" x2="9.01" y2="9"/>
                    <line x1="15" y1="9" x2="15.01" y2="9"/>
                  </svg>
                )}
                {action.title === "View Statistics" && (
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                    <path d="M18 20V10"/>
                    <path d="M12 20V4"/>
                    <path d="M6 20v-6"/>
                  </svg>
                )}
                {action.title === "Match Forecaster" && (
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 17v.01"/>
                  </svg>
                )}
              </div>
              
                            <h3 style={{
                fontSize: '24px',
                fontWeight: theme.typography.fontWeights.bold,
                color: theme.colors.textPrimary,
                fontFamily: theme.typography.fontFamily,
                marginBottom: 12,
              }}>
                {action.title}
              </h3>
              <p style={{
                fontSize: '16px',
                color: theme.colors.textSecondary,
                fontFamily: theme.typography.fontFamily,
                lineHeight: 1.5,
              }}>
                {action.description}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Activity Section */}
      <div style={{
        ...theme.styles.card,
        padding: 32,
        marginBottom: 32,
      }}>
        <h2 style={{
          fontSize: '28px',
          fontWeight: theme.typography.fontWeights.bold,
          color: theme.colors.textPrimary,
          fontFamily: theme.typography.fontFamily,
          marginBottom: 24,
        }}>
          Recent Activity
        </h2>
        
        <div style={{
          display: 'grid',
          gap: 16,
        }}>
          {loadingActivities ? (
            <div style={{
              padding: 40,
              textAlign: 'center',
              color: theme.colors.textSecondary,
              fontFamily: theme.typography.fontFamily,
            }}>
              Loading recent activities...
            </div>
          ) : activities.length > 0 ? (
            activities.map((activity) => (
              <div key={activity.id} style={{
                padding: 20,
                background: theme.colors.content,
                borderRadius: 8,
                border: `1px solid ${theme.colors.border}`,
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <div style={{
                    width: 40,
                    height: 40,
                    background: getActivityColor(activity.type, activity.color),
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontSize: '18px',
                    fontWeight: theme.typography.fontWeights.bold,
                  }}>
                    {activity.icon}
                  </div>
                  <div style={{ flex: 1 }}>
                    <h4 style={{
                      fontSize: '16px',
                      fontWeight: theme.typography.fontWeights.semibold,
                      color: theme.colors.textPrimary,
                      fontFamily: theme.typography.fontFamily,
                      margin: '0 0 4px 0',
                    }}>
                      {activity.title}
                    </h4>
                    <p style={{
                      fontSize: '14px',
                      color: theme.colors.textSecondary,
                      fontFamily: theme.typography.fontFamily,
                      margin: '0 0 2px 0',
                    }}>
                      {activity.description}
                    </p>
                    {activity.details && (
                      <p style={{
                        fontSize: '12px',
                        color: theme.colors.textMuted,
                        fontFamily: theme.typography.fontFamily,
                        margin: 0,
                        fontStyle: 'italic',
                      }}>
                        {activity.details}
                      </p>
                    )}
                  </div>
                  <div style={{
                    fontSize: '12px',
                    color: theme.colors.textMuted,
                    fontFamily: theme.typography.fontFamily,
                  }}>
                    {activity.timestamp ? 
                      new Date(activity.timestamp).toLocaleDateString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      }) : 
                      'Unknown time'
                    }
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div style={{
              padding: 40,
              textAlign: 'center',
              color: theme.colors.textSecondary,
              fontFamily: theme.typography.fontFamily,
            }}>
              No recent activity yet. Start by logging a match or adding players to your team!
            </div>
          )}
        </div>
      </div>


    </div>
  )
}

export default Landing 