// Apple Glass / Glassmorphism Theme - Dark Mode with Yellow Accent
const theme = {
  colors: {
    // Primary colors - Yellow theme
    primary: '#FFD700', // Gold/Yellow
    primaryHover: '#FFC700',
    primaryLight: '#FFEB3B',
    primaryText: '#000000',
    
    // Background colors - Dark gradients
    background: 'linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%)',
    backgroundAlt: 'linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%)',
    backgroundDark: 'linear-gradient(135deg, #000000 0%, #1a1a2e 100%)',
    
    // Glass morphism elements - Dark mode
    glass: 'rgba(0, 0, 0, 0.3)',
    glassDark: 'rgba(0, 0, 0, 0.4)',
    glassLight: 'rgba(255, 255, 255, 0.05)',
    glassBorder: 'rgba(255, 215, 0, 0.2)',
    
    // Text colors - Light text for dark mode
    textPrimary: '#FFFFFF',
    textSecondary: '#CCCCCC',
    textMuted: '#999999',
    textLight: '#FFFFFF',
    
    // Border colors - Yellow tinted
    border: 'rgba(255, 215, 0, 0.25)',
    borderLight: 'rgba(255, 215, 0, 0.15)',
    borderDark: 'rgba(0, 0, 0, 0.5)',
    
    // Status colors - Yellow theme with variations
    error: '#FF6B6B',
    success: '#4ECDC4',
    warning: '#FFD700',
    info: '#4A90E2',
    
    // Shadows - Dark mode with yellow glow
    shadow: '0 8px 32px 0 rgba(0, 0, 0, 0.5)',
    shadowLight: '0 4px 16px 0 rgba(0, 0, 0, 0.3)',
    shadowHeavy: '0 20px 60px 0 rgba(255, 215, 0, 0.2)',
    shadowInset: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.3)',
    shadowYellow: '0 8px 32px 0 rgba(255, 215, 0, 0.25)',
  },
  
  // Supabase Auth UI theme - Dark mode with yellow
  authTheme: {
    theme: 'ThemeSupa',
    variables: {
      default: {
        colors: {
          brand: '#FFD700',
          brandAccent: '#FFEB3B',
          brandButtonText: '#000000',
          defaultButtonBackground: 'rgba(255, 215, 0, 0.1)',
          defaultButtonBackgroundHover: 'rgba(255, 215, 0, 0.2)',
          defaultButtonBorder: 'rgba(255, 215, 0, 0.3)',
          defaultButtonText: '#FFFFFF',
          dividerBackground: 'rgba(255, 215, 0, 0.2)',
          inputBackground: 'rgba(0, 0, 0, 0.3)',
          inputBorder: 'rgba(255, 215, 0, 0.25)',
          inputBorderHover: 'rgba(255, 215, 0, 0.4)',
          inputBorderFocus: '#FFD700',
          inputText: '#FFFFFF',
          inputLabelText: '#CCCCCC',
          inputPlaceholder: '#999999',
          messageText: '#FFFFFF',
          messageTextDanger: '#FF6B6B',
          anchorTextColor: '#FFD700',
          anchorTextHoverColor: '#FFEB3B',
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
  
  // Common styles - Glass morphism (Dark mode)
  styles: {
    glassCard: {
      background: 'rgba(0, 0, 0, 0.3)',
      backdropFilter: 'blur(20px) saturate(180%)',
      WebkitBackdropFilter: 'blur(20px) saturate(180%)',
      borderRadius: 20,
      border: '1px solid rgba(255, 215, 0, 0.2)',
      boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.5)',
      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    },
    
    glassCardHover: {
      transform: 'translateY(-4px)',
      boxShadow: '0 12px 40px 0 rgba(255, 215, 0, 0.3)',
      background: 'rgba(255, 215, 0, 0.1)',
      border: '1px solid rgba(255, 215, 0, 0.4)',
    },
    
    card: {
      background: 'rgba(0, 0, 0, 0.3)',
      backdropFilter: 'blur(20px) saturate(180%)',
      WebkitBackdropFilter: 'blur(20px) saturate(180%)',
      borderRadius: 20,
      boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.5)',
      border: '1px solid rgba(255, 215, 0, 0.2)',
    },
    
    button: {
      primary: {
        background: 'linear-gradient(135deg, #FFD700 0%, #FFEB3B 100%)',
        color: '#000000',
        border: 'none',
        borderRadius: 12,
        padding: '14px 28px',
        fontWeight: 600,
        cursor: 'pointer',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        boxShadow: '0 4px 16px rgba(255, 215, 0, 0.4)',
      },
      
      secondary: {
        background: 'rgba(255, 215, 0, 0.1)',
        backdropFilter: 'blur(10px)',
        WebkitBackdropFilter: 'blur(10px)',
        color: '#FFFFFF',
        border: '1px solid rgba(255, 215, 0, 0.3)',
        borderRadius: 12,
        padding: '14px 28px',
        fontWeight: 600,
        cursor: 'pointer',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
      },
    },
    
    input: {
      background: 'rgba(0, 0, 0, 0.3)',
      backdropFilter: 'blur(10px)',
      WebkitBackdropFilter: 'blur(10px)',
      border: '1px solid rgba(255, 215, 0, 0.25)',
      borderRadius: 12,
      color: '#FFFFFF',
      padding: '14px 16px',
      fontSize: '16px',
      transition: 'all 0.3s ease',
    },
  },
  
  // Glass effect utilities (Dark mode)
  glass: {
    light: {
      background: 'rgba(0, 0, 0, 0.2)',
      backdropFilter: 'blur(20px) saturate(180%)',
      WebkitBackdropFilter: 'blur(20px) saturate(180%)',
      border: '1px solid rgba(255, 215, 0, 0.15)',
    },
    medium: {
      background: 'rgba(0, 0, 0, 0.35)',
      backdropFilter: 'blur(25px) saturate(180%)',
      WebkitBackdropFilter: 'blur(25px) saturate(180%)',
      border: '1px solid rgba(255, 215, 0, 0.25)',
    },
    heavy: {
      background: 'rgba(0, 0, 0, 0.5)',
      backdropFilter: 'blur(30px) saturate(180%)',
      WebkitBackdropFilter: 'blur(30px) saturate(180%)',
      border: '1px solid rgba(255, 215, 0, 0.35)',
    },
  },
}

export { theme } 