# Update Notification System

## Overview

The Update Notification System automatically checks for new releases and prompts users to update the application. Users can update immediately or schedule the update for later.

## Features

### 🔔 Update Notification
- Automatically detects new versions
- Shows a beautiful, user-friendly notification modal
- Displays current version → new version comparison
- Minimal user interaction required

### ⏰ Scheduled Updates
Users can schedule updates for:
- **15 minutes later** - Quick delay for active work
- **60 minutes later** - Delay until break time
- **Never** - Dismiss this update (until next major version)
- **Custom** - Choose exact date, hour, and minute

### 🎨 Design
- Modern, clean UI matching the application theme
- Smooth animations and transitions
- Responsive design for all screen sizes
- Non-intrusive overlay design

## How It Works

### Version Checking
1. On app load, checks `/version.json` for latest version
2. Compares with stored version in `localStorage`
3. If newer version found, shows notification

### Scheduled Updates
- Scheduled time is stored in `localStorage` as ISO string
- App checks every minute if scheduled time has arrived
- When time arrives, update notification is shown

### User Preferences
- Dismissed updates stored with expiration time
- Scheduled updates stored with exact timestamp
- Preferences persist across sessions

## Implementation Details

### Components

#### `UpdateNotification.jsx`
- Main notification component
- Handles version checking
- Manages notification display logic

#### `UpdateSchedule.jsx`
- Schedule selection interface
- Custom date/time picker
- Handles scheduling logic

### Files

- `web-app/public/version.json` - Version information file
- `web-app/src/components/UpdateNotification.jsx` - Notification component
- `web-app/src/components/UpdateSchedule.jsx` - Schedule component
- `web-app/src/components/UpdateNotification.css` - Notification styles
- `web-app/src/components/UpdateSchedule.css` - Schedule styles

### localStorage Keys

- `app_version` - Current installed version
- `update_dismissed_until` - Dismissal expiration timestamp
- `scheduled_update` - Scheduled update timestamp

## Usage

### For Developers

To trigger an update notification:
1. Update version in `web-app/public/version.json`
2. Update `CURRENT_VERSION` constant in `UpdateNotification.jsx`
3. Deploy the new version
4. Users will see notification on next app load

### For Users

1. **Update Now**: Click "Şimdi Güncelle" to update immediately
2. **Schedule Later**: Click "Sonra Güncelle" to choose when to update
3. **Dismiss**: Click X button to dismiss for 24 hours

## Future Enhancements

- Backend API endpoint for version checking
- Release notes display in notification
- Progressive update system
- Update progress indicator
- Offline update detection

