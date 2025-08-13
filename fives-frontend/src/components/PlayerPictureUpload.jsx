import React, { useState, useRef } from 'react'
import { theme } from '../theme'
import { playersApi } from '../services/api'

const PlayerPictureUpload = ({ player, onPictureUpdated }) => {
  const [isEditing, setIsEditing] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [dragActive, setDragActive] = useState(false)
  const fileInputRef = useRef(null)

  const handleFileSelect = async (file) => {
    if (!file) return

    // Validate file type
    if (!file.type.startsWith('image/')) {
      setError('Please select an image file (JPEG, PNG, etc.)')
      return
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      setError('File size must be less than 5MB')
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      const result = await playersApi.uploadPlayerPicture(player.id, file)
      setIsEditing(false)
      onPictureUpdated?.(result.profile_picture)
    } catch (err) {
      setError('Failed to upload profile picture')
      console.error('Error uploading profile picture:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0])
    }
  }

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0])
    }
  }

  const handleCancel = () => {
    setIsEditing(false)
    setError(null)
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      {/* Current Picture Display */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: 12,
      }}>
        <div style={{
          width: 60,
          height: 60,
          borderRadius: '50%',
          overflow: 'hidden',
          background: theme.colors.primary,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          fontSize: '20px',
          fontWeight: theme.typography.fontWeights.bold,
        }}>
          {player.profile_picture ? (
            <img 
              src={player.profile_picture} 
              alt={player.name}
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            />
          ) : (
            player.name.charAt(0).toUpperCase()
          )}
        </div>
        
                       <div style={{ flex: 1 }}>
                 <div style={{
                   fontSize: '16px',
                   fontWeight: theme.typography.fontWeights.semibold,
                   color: theme.colors.textPrimary,
                   fontFamily: theme.typography.fontFamily,
                 }}>
                   {player.name}
                 </div>
          <button
            onClick={() => setIsEditing(true)}
            style={{
              background: theme.colors.primary,
              color: 'white',
              border: 'none',
              padding: '8px 16px',
              borderRadius: 6,
              fontSize: '14px',
              cursor: 'pointer',
              fontFamily: theme.typography.fontFamily,
            }}
          >
            {player.profile_picture ? 'Change Picture' : 'Add Picture'}
          </button>
        </div>
      </div>

      {/* Edit Mode - File Upload */}
      {isEditing && (
        <div style={{
          padding: 16,
          background: theme.colors.content,
          borderRadius: 8,
          border: `1px solid ${theme.colors.border}`,
        }}>
          <div style={{ marginBottom: 16 }}>
            <label style={{
              fontSize: '14px',
              fontWeight: theme.typography.fontWeights.semibold,
              color: theme.colors.textPrimary,
              fontFamily: theme.typography.fontFamily,
              marginBottom: 8,
              display: 'block',
            }}>
              Upload Profile Picture:
            </label>
            
            {/* Drag & Drop Zone */}
            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              style={{
                border: `2px dashed ${dragActive ? theme.colors.primary : theme.colors.border}`,
                borderRadius: 8,
                padding: '24px',
                textAlign: 'center',
                cursor: 'pointer',
                background: dragActive ? `${theme.colors.primary}10` : theme.colors.card,
                transition: 'all 0.2s ease',
              }}
            >
              <div style={{
                fontSize: '16px',
                color: theme.colors.textPrimary,
                fontFamily: theme.typography.fontFamily,
                marginBottom: 8,
              }}>
                📸 Click to select or drag & drop
              </div>
              <div style={{
                fontSize: '14px',
                color: theme.colors.textSecondary,
                fontFamily: theme.typography.fontFamily,
              }}>
                Supports JPEG, PNG, GIF (max 5MB)
              </div>
            </div>
            
            {/* Hidden file input */}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileInput}
              style={{ display: 'none' }}
            />
          </div>

          {error && (
            <div style={{
              color: theme.colors.error,
              fontSize: '14px',
              marginBottom: 12,
              fontFamily: theme.typography.fontFamily,
            }}>
              {error}
            </div>
          )}

          <div style={{ display: 'flex', gap: 8 }}>
            <button
              onClick={handleCancel}
              disabled={isLoading}
              style={{
                background: theme.colors.content,
                color: theme.colors.textPrimary,
                border: `1px solid ${theme.colors.border}`,
                padding: '8px 16px',
                borderRadius: 6,
                fontSize: '14px',
                cursor: isLoading ? 'not-allowed' : 'pointer',
                fontFamily: theme.typography.fontFamily,
              }}
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default PlayerPictureUpload 