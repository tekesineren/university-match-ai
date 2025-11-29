# University Match AI - Replit Setup

## Overview
University Match AI is an AI-powered university matching system for Master's degree applications. The platform analyzes academic profiles, CVs, and motivation letters to provide personalized university recommendations.

**Current Version**: 1.3
**Last Updated**: November 29, 2024

## Project Structure

### Backend (Python Flask)
- **Location**: `backend/`
- **Port**: 5001 (localhost only)
- **Main File**: `app.py`
- **Dependencies**: Flask, Flask-CORS, PyPDF2, python-docx, pandas, numpy, stripe
- **Purpose**: REST API for university matching algorithm, CV parsing, and premium features

### Frontend (React + Vite)
- **Location**: `web-app/`
- **Port**: 5000 (0.0.0.0)
- **Build Tool**: Vite
- **Dependencies**: React 18.2.0, Axios, Capacitor (for mobile)
- **Purpose**: Web interface for user input and results display

### Other Components
- `ios-app/`: Swift iOS app (optional)
- `ios-app-expo/`: React Native Expo app (optional)
- `examples/`: Sample data and profiles

## Architecture

### Development Environment (Replit)
1. **Frontend**: Runs on `0.0.0.0:5000` (accessible via webview)
   - Configured in `web-app/vite.config.js` with `allowedHosts: true` to support Replit's proxy
   - Proxies API requests to backend via `/api` route

2. **Backend**: Runs on `127.0.0.1:5001` (internal only)
   - Handles API requests from frontend
   - Provides endpoints for matching, CV parsing, and premium features

### Workflow
The "Start Application" workflow runs both backend and frontend:
```bash
cd backend && python app.py & cd web-app && npm run dev
```

## Recent Changes (November 29, 2024)

### Replit Environment Setup
1. **Port Configuration**:
   - Changed frontend from port 3000 to 5000 (Replit requirement)
   - Changed backend from port 5000 to 5001 (to avoid conflict)
   - Updated Vite proxy to target `http://localhost:5001`

2. **Host Configuration**:
   - Frontend: `0.0.0.0` with `allowedHosts: true` (for Replit proxy)
   - Backend: `127.0.0.1` (localhost only, for internal API calls)

3. **Dependencies Installed**:
   - Python 3.11 with all backend requirements
   - Node.js 20 with all frontend dependencies

4. **Workflow Setup**:
   - Created single workflow that runs both backend and frontend
   - Configured webview output on port 5000

5. **Deployment Configuration**:
   - Set up autoscale deployment target
   - Configured build and run commands

## Key Features

### Core Functionality
- Smart university matching based on GPA, language scores, background, and experience
- CV parsing (PDF, DOCX) with automatic data extraction
- Motivation letter analysis
- Results categorized by match level (High/Medium/Low)
- Multi-language support (EN, TR, ES, DE, FR)

### Premium Features
- Rate limiting and user tiers
- Stripe payment integration
- API key management
- Enhanced features for premium users

## API Endpoints

- `GET /` - API information
- `GET /api/health` - Health check
- `POST /api/match` - University matching algorithm
- `POST /api/parse-cv` - CV parsing
- `GET /api/universities` - List all universities
- `POST /api/feedback` - Submit user feedback
- Premium endpoints: `/api/premium/*`, `/api/checkout`, `/api/webhook`

## Environment Variables

No environment variables are currently required for basic functionality. Premium features (Stripe) require:
- `STRIPE_SECRET_KEY` (for payment processing)
- `STRIPE_WEBHOOK_SECRET` (for webhook verification)

## Development Notes

### Testing
- Backend API testing must go through frontend/Vite proxy: `curl http://localhost:5000/api/health`
- Direct backend access (dev only): `curl http://localhost:5001/api/health`
- Frontend accessible at: Replit webview preview

### Important
- The backend listens only on localhost (127.0.0.1:5001) in development
- API requests from browser must go through the Vite proxy on port 5000
- In deployment (when PORT env var is set), backend automatically binds to 0.0.0.0

### Known Issues
- LSP shows import errors in `backend/app.py` - these are false positives (packages are installed)
- Missing `email_service.py` - imported but file doesn't exist (non-critical)

### File Structure Conventions
- Backend: Standard Flask application structure
- Frontend: React component-based architecture
- Separate directories for different platforms (web, iOS, Expo)

## User Preferences
None documented yet.

## Next Steps
- Monitor application performance in Replit environment
- Test CV upload and parsing functionality
- Test university matching algorithm
- Verify premium features work correctly
