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
      color: theme.colors.primary, // Yellow/Gold
    },
    {
      title: "Log Match Result",
      description: "Record game scores, player performances, and track stats",
      action: () => onNavigate('log-match'),
      color: '#FFB800', // Darker yellow
    },
    {
      title: "View Statistics",
      description: "Analyze team performance, player stats, and trends",
      action: () => onNavigate('stats'),
      color: theme.colors.warning, // Gold
    },
    {
      title: "Match Forecaster",
      description: "Predict match outcomes and player performance",
      action: () => onNavigate('match-forecaster'),
      color: '#FFE135', // Bright yellow
    },
  ])

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', animation: 'fadeIn 0.6s ease-out' }}>
      {/* Hero Section */}
      <div style={{
        textAlign: 'center',
        padding: '40px 20px',
        marginBottom: 48,
      }}>
        <h1 style={{
          fontSize: '56px',
          fontWeight: theme.typography.fontWeights.bold,
          fontFamily: theme.typography.fontFamily,
          letterSpacing: theme.typography.letterSpacing.tight,
          marginBottom: 20,
          background: 'linear-gradient(135deg, #FFD700 0%, #FFEB3B 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
        }}>
          Welcome to Fives App
        </h1>
        <p style={{
          fontSize: '22px',
          color: theme.colors.textPrimary,
          fontFamily: theme.typography.fontFamily,
          fontWeight: theme.typography.fontWeights.normal,
          maxWidth: 700,
          margin: '0 auto',
          lineHeight: 1.6,
          opacity: 0.9,
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
              ...theme.styles.glassCard,
              padding: 32,
              cursor: 'pointer',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-8px) scale(1.02)'
              e.currentTarget.style.boxShadow = theme.colors.shadowHeavy
              e.currentTarget.style.background = 'rgba(255, 215, 0, 0.15)'
              e.currentTarget.style.border = '1px solid rgba(255, 215, 0, 0.4)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0) scale(1)'
              e.currentTarget.style.boxShadow = theme.colors.shadow
              e.currentTarget.style.background = 'rgba(0, 0, 0, 0.3)'
              e.currentTarget.style.border = '1px solid rgba(255, 215, 0, 0.2)'
            }}
          >
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              textAlign: 'center',
            }}>
              {/* Simple Icon */}
              <div style={{
                width: 72,
                height: 72,
                borderRadius: '50%',
                background: `linear-gradient(135deg, ${action.color} 0%, ${action.color}dd 100%)`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: 24,
                boxShadow: `0 8px 24px ${action.color}40`,
                border: '2px solid rgba(255, 215, 0, 0.4)',
                fontSize: '32px',
                fontWeight: 'bold',
                color: '#000000',
              }}>
                {action.title === "Manage Teams" && '⚙'}
                {action.title === "Log Match Result" && '●'}
                {action.title === "View Statistics" && '■'}
                {action.title === "Match Forecaster" && '◆'}
              </div>
              
              <h3 style={{
                fontSize: '22px',
                fontWeight: theme.typography.fontWeights.bold,
                color: theme.colors.textPrimary,
                fontFamily: theme.typography.fontFamily,
                marginBottom: 12,
              }}>
                {action.title}
              </h3>
              <p style={{
                fontSize: '15px',
                color: theme.colors.textSecondary,
                fontFamily: theme.typography.fontFamily,
                lineHeight: 1.6,
                opacity: 0.9,
              }}>
                {action.description}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Activity Section */}
      <div style={{
        ...theme.styles.glassCard,
        padding: 40,
        marginBottom: 32,
      }}>
        <h2 style={{
          fontSize: '32px',
          fontWeight: theme.typography.fontWeights.bold,
          color: theme.colors.textPrimary,
          fontFamily: theme.typography.fontFamily,
          marginBottom: 28,
          background: 'linear-gradient(135deg, #FFD700 0%, #FFEB3B 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
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
                ...theme.glass.light,
                padding: 20,
                borderRadius: 16,
                transition: 'all 0.3s ease',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'rgba(255, 215, 0, 0.1)'
                e.currentTarget.style.transform = 'translateX(4px)'
                e.currentTarget.style.border = '1px solid rgba(255, 215, 0, 0.3)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'rgba(0, 0, 0, 0.2)'
                e.currentTarget.style.transform = 'translateX(0)'
                e.currentTarget.style.border = '1px solid rgba(255, 215, 0, 0.15)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <div style={{
                    width: 48,
                    height: 48,
                    background: `linear-gradient(135deg, ${getActivityColor(activity.type, activity.color)} 0%, ${getActivityColor(activity.type, activity.color)}dd 100%)`,
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontSize: '20px',
                    fontWeight: theme.typography.fontWeights.bold,
                    boxShadow: `0 4px 12px ${getActivityColor(activity.type, activity.color)}40`,
                    border: '2px solid rgba(255, 255, 255, 0.3)',
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