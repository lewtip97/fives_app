// Apple Glass / Glassmorphism Theme
const theme = {
  colors: {
    // Primary colors - Modern, soft blues/purples
    primary: '#007AFF', // Apple blue
    primaryHover: '#0051D5',
    primaryLight: '#5AC8FA',
    primaryText: '#FFFFFF',
    
    // Background colors - Soft gradients
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
    backgroundAlt: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    backgroundDark: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
    
    // Glass morphism elements
    glass: 'rgba(255, 255, 255, 0.1)',
    glassDark: 'rgba(0, 0, 0, 0.2)',
    glassLight: 'rgba(255, 255, 255, 0.2)',
    glassBorder: 'rgba(255, 255, 255, 0.18)',
    
    // Text colors - High contrast for readability
    textPrimary: '#1d1d1f',
    textSecondary: '#6e6e73',
    textMuted: '#86868b',
    textLight: '#ffffff',
    
    // Border colors - Subtle and elegant
    border: 'rgba(255, 255, 255, 0.18)',
    borderLight: 'rgba(255, 255, 255, 0.1)',
    borderDark: 'rgba(0, 0, 0, 0.1)',
    
    // Status colors - Apple-inspired
    error: '#FF3B30',
    success: '#34C759',
    warning: '#FF9500',
    info: '#5AC8FA',
    
    // Shadows - Soft, layered
    shadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
    shadowLight: '0 4px 16px 0 rgba(31, 38, 135, 0.2)',
    shadowHeavy: '0 20px 60px 0 rgba(31, 38, 135, 0.5)',
    shadowInset: 'inset 0 2px 4px 0 rgba(255, 255, 255, 0.1)',
  },
  
  // Supabase Auth UI theme - Glass style
  authTheme: {
    theme: 'ThemeSupa',
    variables: {
      default: {
        colors: {
          brand: '#007AFF',
          brandAccent: '#5AC8FA',
          brandButtonText: '#FFFFFF',
          defaultButtonBackground: 'rgba(255, 255, 255, 0.1)',
          defaultButtonBackgroundHover: 'rgba(255, 255, 255, 0.2)',
          defaultButtonBorder: 'rgba(255, 255, 255, 0.18)',
          defaultButtonText: '#1d1d1f',
          dividerBackground: 'rgba(255, 255, 255, 0.1)',
          inputBackground: 'rgba(255, 255, 255, 0.1)',
          inputBorder: 'rgba(255, 255, 255, 0.18)',
          inputBorderHover: 'rgba(255, 255, 255, 0.3)',
          inputBorderFocus: '#007AFF',
          inputText: '#1d1d1f',
          inputLabelText: '#6e6e73',
          inputPlaceholder: '#86868b',
          messageText: '#1d1d1f',
          messageTextDanger: '#FF3B30',
          anchorTextColor: '#007AFF',
          anchorTextHoverColor: '#5AC8FA',
        },
        space: {
          inputPadding: '14px',
          buttonPadding: '14px 24px',
        },
        fontSizes: {
          baseButtonSize: '16px',
          baseInputSize: '16px',
        },
        borderWidths: {
          buttonBorderWidth: '1px',
          inputBorderWidth: '1px',
        },
        radii: {
          borderRadiusButton: '12px',
          buttonBorderRadius: '12px',
          inputBorderRadius: '12px',
        },
      },
    },
  },
  
  // Typography
  typography: {
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    fontWeights: {
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
      extrabold: 800,
    },
    letterSpacing: {
      tight: '-0.025em',
      normal: '0em',
      wide: '0.025em',
    },
    lineHeights: {
      tight: 1.2,
      normal: 1.5,
      relaxed: 1.75,
    },
  },
  
  // Common styles - Glass morphism
  styles: {
    glassCard: {
      background: 'rgba(255, 255, 255, 0.1)',
      backdropFilter: 'blur(20px) saturate(180%)',
      WebkitBackdropFilter: 'blur(20px) saturate(180%)',
      borderRadius: 20,
      border: '1px solid rgba(255, 255, 255, 0.18)',
      boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    },
    
    glassCardHover: {
      transform: 'translateY(-4px)',
      boxShadow: '0 12px 40px 0 rgba(31, 38, 135, 0.5)',
      background: 'rgba(255, 255, 255, 0.15)',
    },
    
    card: {
      background: 'rgba(255, 255, 255, 0.1)',
      backdropFilter: 'blur(20px) saturate(180%)',
      WebkitBackdropFilter: 'blur(20px) saturate(180%)',
      borderRadius: 20,
      boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
      border: '1px solid rgba(255, 255, 255, 0.18)',
    },
    
    button: {
      primary: {
        background: 'linear-gradient(135deg, #007AFF 0%, #5AC8FA 100%)',
        color: '#FFFFFF',
        border: 'none',
        borderRadius: 12,
        padding: '14px 28px',
        fontWeight: 600,
        cursor: 'pointer',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        boxShadow: '0 4px 16px rgba(0, 122, 255, 0.3)',
      },
      
      secondary: {
        background: 'rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(10px)',
        WebkitBackdropFilter: 'blur(10px)',
        color: '#1d1d1f',
        border: '1px solid rgba(255, 255, 255, 0.18)',
        borderRadius: 12,
        padding: '14px 28px',
        fontWeight: 600,
        cursor: 'pointer',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
      },
    },
    
    input: {
      background: 'rgba(255, 255, 255, 0.1)',
      backdropFilter: 'blur(10px)',
      WebkitBackdropFilter: 'blur(10px)',
      border: '1px solid rgba(255, 255, 255, 0.18)',
      borderRadius: 12,
      color: '#1d1d1f',
      padding: '14px 16px',
      fontSize: '16px',
      transition: 'all 0.3s ease',
    },
  },
  
  // Glass effect utilities
  glass: {
    light: {
      background: 'rgba(255, 255, 255, 0.1)',
      backdropFilter: 'blur(20px) saturate(180%)',
      WebkitBackdropFilter: 'blur(20px) saturate(180%)',
      border: '1px solid rgba(255, 255, 255, 0.18)',
    },
    medium: {
      background: 'rgba(255, 255, 255, 0.15)',
      backdropFilter: 'blur(25px) saturate(180%)',
      WebkitBackdropFilter: 'blur(25px) saturate(180%)',
      border: '1px solid rgba(255, 255, 255, 0.25)',
    },
    heavy: {
      background: 'rgba(255, 255, 255, 0.2)',
      backdropFilter: 'blur(30px) saturate(180%)',
      WebkitBackdropFilter: 'blur(30px) saturate(180%)',
      border: '1px solid rgba(255, 255, 255, 0.3)',
    },
  },
}

export { theme } 