// Theme configuration for consistent black and yellow styling
export const theme = {
  colors: {
    // Primary colors
    primary: '#FFD700', // Golden yellow
    primaryHover: '#FFED4E', // Lighter yellow for hover
    primaryText: '#000000', // Black text on yellow
    
    // Background colors
    background: 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)',
    sidebar: '#000000',
    header: '#1a1a1a',
    content: '#2d2d2d',
    card: '#1a1a1a',
    
    // Text colors
    textPrimary: '#ffffff',
    textSecondary: '#cccccc',
    textMuted: '#888888',
    
    // Border colors
    border: '#333333',
    borderLight: '#555555',
    
    // Status colors
    error: '#ff6b6b',
    success: '#51cf66',
    warning: '#ffd43b',
    
    // Shadow
    shadow: '0 4px 24px rgba(0,0,0,0.3)',
    shadowLight: '0 1px 3px rgba(0,0,0,0.3)',
  },
  
  // Supabase Auth UI theme
  authTheme: {
    theme: 'ThemeSupa',
    variables: {
      default: {
        colors: {
          brand: '#FFD700',
          brandAccent: '#FFED4E',
          brandButtonText: '#000000',
          defaultButtonBackground: '#333333',
          defaultButtonBackgroundHover: '#444444',
          defaultButtonBorder: '#555555',
          defaultButtonText: '#ffffff',
          dividerBackground: '#333333',
          inputBackground: '#2d2d2d',
          inputBorder: '#555555',
          inputBorderHover: '#FFD700',
          inputBorderFocus: '#FFD700',
          inputText: '#ffffff',
          inputLabelText: '#cccccc',
          inputPlaceholder: '#888888',
          messageText: '#ffffff',
          messageTextDanger: '#ff6b6b',
          anchorTextColor: '#FFD700',
          anchorTextHoverColor: '#FFED4E',
        },
        space: {
          inputPadding: '12px',
          buttonPadding: '12px',
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
          borderRadiusButton: '8px',
          buttonBorderRadius: '8px',
          inputBorderRadius: '8px',
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
  
  // Common styles
  styles: {
    card: {
      background: '#1a1a1a',
      borderRadius: 16,
      boxShadow: '0 4px 24px rgba(0,0,0,0.3)',
      border: '1px solid #333',
    },
    
    button: {
      primary: {
        background: '#FFD700',
        color: '#000000',
        border: 'none',
        borderRadius: 8,
        padding: '12px 24px',
        fontWeight: 'bold',
        cursor: 'pointer',
        transition: 'all 0.2s',
      },
      
      secondary: {
        background: '#333333',
        color: '#ffffff',
        border: '1px solid #555555',
        borderRadius: 8,
        padding: '12px 24px',
        fontWeight: 'bold',
        cursor: 'pointer',
        transition: 'all 0.2s',
      },
    },
    
    input: {
      background: '#2d2d2d',
      border: '1px solid #555555',
      borderRadius: 8,
      color: '#ffffff',
      padding: '12px',
      fontSize: '16px',
    },
  },
}

export default theme 