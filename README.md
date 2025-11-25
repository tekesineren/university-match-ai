# University Match AI 🎓✨

> **AI-Powered University Matching System** for Master's Degree Applications

**Version 1.3** - Portfolio Modal & Enhanced LinkedIn Sharing  
Built collaboratively with [Cursor AI](https://cursor.sh)

---

## 📋 Table of Contents

1. [Introduction](#-introduction)
2. [Technology Stack](#-technology-stack)
3. [Project Structure](#-project-structure)
4. [Quick Start](#-quick-start)
5. [Detailed Setup](#-detailed-setup-guide)
6. [API Documentation](#-api-documentation)
7. [Platform-Specific Notes](#-platform-specific-notes)
8. [Troubleshooting & FAQ](#-troubleshooting--faq)
9. [Features](#-features)

---

## 🎯 Introduction

**University Match AI** helps prospective Master's students find their perfect-fit universities through intelligent matching algorithms. The platform analyzes academic profiles, CVs, and motivation letters to provide personalized university recommendations.

### What This Application Does

- 🔍 **Smart Matching**: Scores 20+ top universities based on GPA, language scores, background, and experience
- 📄 **CV Analysis**: Automatically extracts and analyzes information from PDF and DOCX CV files
- ✍️ **Application Support**: Evaluates motivation letters against key criteria
- 🎯 **Categorized Results**: Universities sorted into High/Medium/Low match categories
- 📱 **Multi-Platform**: Web app, iOS-ready, and API-first architecture

### Why Use This Tool?

Finding the right Master's program is overwhelming. With hundreds of universities worldwide, each with different requirements, students struggle to identify where they belong. University Match AI solves this by providing:

- **Instant Matching**: Get personalized recommendations in seconds
- **Objective Scoring**: Algorithm-based evaluation removes bias
- **Comprehensive Database**: 20+ top universities with detailed requirements
- **Application Portfolio**: Export results as PDF for your application portfolio

---

## 🛠️ Technology Stack

### Backend (Python)
- **Flask 3.0.0**: Web framework for REST API
- **Flask-CORS 4.0.0**: Cross-origin resource sharing
- **PyPDF2 3.0.1**: PDF parsing for CV extraction
- **python-docx 1.1.0**: DOCX parsing for CV extraction
- **pandas 2.1.3**: Data processing and analysis
- **numpy 1.26.2**: Numerical computations
- **Stripe 7.0.0**: Payment processing (premium features)

### Frontend (React)
- **React 18.2.0**: UI library
- **Vite 5.0.8**: Build tool and development server
- **Axios 1.6.2**: HTTP client for API communication

### Mobile & Development
- **Capacitor 6.0.0**: Web-to-native bridge for iOS/Android apps
- **Node.js 16+**: Runtime for frontend development

---

## 📁 Project Structure

Understanding the project structure helps you navigate and modify the codebase:

```
university-match-ai/
│
├── backend/                          # Python Flask Backend (API Server)
│   ├── app.py                       # ⭐ Main API server & matching algorithm
│   ├── premium.py                   # Premium features & rate limiting
│   ├── stripe_integration.py        # Payment processing integration
│   ├── email_service.py             # Email service for feedback
│   ├── requirements.txt             # Python dependencies (install with pip)
│   ├── CHECK_BACKEND.py             # Backend setup verification script
│   └── users.json                   # User data (auto-generated)
│
├── web-app/                         # React Frontend (Web Interface)
│   ├── src/                         # Source code
│   │   ├── components/              # React components (UI elements)
│   │   │   ├── InputForm.jsx       # User input form
│   │   │   ├── ResultsView.jsx     # Results display
│   │   │   ├── CVUpload.jsx        # CV upload component
│   │   │   └── ...                 # Other components
│   │   ├── utils/                  # Utility functions
│   │   │   ├── cvParser.js         # CV parsing utilities
│   │   │   └── i18n.js             # Internationalization
│   │   ├── App.jsx                 # ⭐ Main application component
│   │   └── main.jsx                # Entry point
│   ├── public/                     # Static files (images, icons, HTML)
│   ├── package.json                # Node.js dependencies (install with npm)
│   ├── vite.config.js              # ⭐ Vite configuration (ports, proxy)
│   ├── CHECK_SETUP.js              # Frontend setup verification script
│   └── capacitor.config.json       # Mobile app configuration
│
├── ios-app/                        # Swift iOS App (Optional)
│   └── *.swift files               # SwiftUI components
│
├── examples/                       # Sample data & examples
│   └── sample_profile.json         # Example user profile
│
├── README.md                       # This file! 📖
├── SETUP_GUIDE.md                  # ⭐ Complete setup guide (Windows & macOS)
├── HATA_COZUM_REHBERI.md          # Error resolution guide (Turkish)
└── TROUBLESHOOTING.md             # General troubleshooting guide
```

### Key Files Explained

| File | Purpose | When to Modify |
|------|---------|----------------|
| **`backend/app.py`** | Main backend server. Handles API requests, matching algorithm, CV parsing. **Must run for app to work.** | Add new API endpoints, modify matching algorithm |
| **`backend/requirements.txt`** | Python dependencies list | Add new Python packages |
| **`web-app/package.json`** | Node.js dependencies list | Add new npm packages |
| **`web-app/src/App.jsx`** | Main React component - what users see | Modify UI structure, add features |
| **`web-app/vite.config.js`** | Development server configuration (ports, proxy) | Change ports, modify API proxy settings |
| **`web-app/src/components/InputForm.jsx`** | User input form component | Modify form fields, validation |
| **`web-app/src/components/ResultsView.jsx`** | Results display component | Modify how results are shown |

---

## 🚀 Quick Start

For detailed setup instructions, see **[SETUP_GUIDE.md](SETUP_GUIDE.md)** (complete guide for Windows & macOS).

### Prerequisites

Install these before starting:

- **Python 3.8+** - [Download](https://www.python.org/downloads/) (Check "Add Python to PATH" on Windows)
- **Node.js 16+** - [Download](https://nodejs.org/) (Choose LTS version)
- **Git** - [Download](https://git-scm.com/downloads) (usually pre-installed)

**Verify installations**:
```bash
python --version   # or python3 on macOS
node --version
git --version
```

### Installation Steps

#### 1. Clone the Repository

```bash
git clone https://github.com/tekesineren/university-match-ai.git
cd university-match-ai
```

**⚠️ Important**: Folder name is `university-match-ai` (NOT `university-match-ai-main`)

#### 2. Setup Backend (Terminal 1)

```bash
cd backend
pip install -r requirements.txt   # Windows
pip3 install -r requirements.txt  # macOS (use pip3)
python app.py                     # Windows
python3 app.py                    # macOS (use python3)
```

✅ Backend runs on `http://localhost:5000`  
**Keep this terminal open!**

#### 3. Setup Frontend (Terminal 2 - NEW WINDOW)

Open a **new terminal window**:

```bash
cd university-match-ai/web-app
npm install
npm run dev
```

✅ Frontend runs on `http://localhost:5173`

#### 4. Open in Browser

Open your browser and go to: **http://localhost:5173**

---

## 📖 Detailed Setup Guide

For comprehensive setup instructions with troubleshooting, see:

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete step-by-step guide (Windows & macOS)
  - Prerequisites with download links
  - Detailed installation steps
  - Platform-specific notes
  - Common errors and solutions
  - Verification checklist

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Quick start guide for beginners

---

## 📡 API Documentation

The backend provides a REST API with the following endpoints:

### Root Endpoint

**GET /** - API information
```bash
curl http://localhost:5000/
```

**Response**:
```json
{
  "name": "University Match AI API",
  "version": "1.0",
  "status": "running",
  "endpoints": {...}
}
```

### Health Check

**GET /api/health** - Check if API is running
```bash
curl http://localhost:5000/api/health
```

**Response**:
```json
{
  "status": "ok",
  "message": "API is running"
}
```

### Match Universities

**POST /api/match** - Match universities based on profile

**Request**:
```json
{
  "gpa": 3.5,
  "language_test_type": "toefl",
  "language_test_score": 95,
  "background": ["robotics", "engineering"],
  "work_experience": 1.5,
  "research_experience": 0,
  "publications": 0,
  "recommendation_letters": 2
}
```

**Response**:
```json
{
  "success": true,
  "results": {
    "high_match": [...],
    "medium_match": [...],
    "low_match": [...],
    "extra_options": [...]
  }
}
```

### Parse CV

**POST /api/parse-cv** - Extract information from CV

**Request**: `multipart/form-data` with `file` field (PDF or DOCX)

**Response**:
```json
{
  "success": true,
  "data": {
    "gpa": 3.8,
    "work_experience": 2.0,
    ...
  }
}
```

### Get Universities

**GET /api/universities** - Get list of all universities

**Response**:
```json
{
  "universities": [...]
}
```

### Submit Feedback

**POST /api/feedback** - Submit user feedback

**Request**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "message": "Great app!"
}
```

---

## 🖥️ Platform-Specific Notes

### Windows 10/11

- **Terminal**: Use **PowerShell** (recommended) or Command Prompt
- **Python**: Use `python` (not `python3`)
- **Path Format**: `C:\Users\YourName\Documents\...`

**Example**:
```powershell
cd C:\Users\YourName\Desktop
git clone https://github.com/tekesineren/university-match-ai.git
cd university-match-ai\backend
python app.py
```

### macOS (All Versions)

- **Terminal**: Use **Terminal.app** (built-in)
- **Python**: Always use `python3` (not `python`)
- **pip**: Always use `pip3` (not `pip`)
- **Home Directory**: Use `~` (shortcut for `/Users/YourName`)

**Example**:
```bash
cd ~/Desktop
git clone https://github.com/tekesineren/university-match-ai.git
cd university-match-ai/backend
python3 app.py
```

**Permission Issues**: If you get permission errors with `pip3`, use:
```bash
pip3 install --user -r requirements.txt
```

---

## 🆘 Troubleshooting & FAQ

### Quick Fixes

**Frontend Setup Check**:
```bash
cd web-app
npm run check-setup
```

**Backend Setup Check**:
```bash
cd backend
python CHECK_BACKEND.py   # Windows
python3 CHECK_BACKEND.py  # macOS
```

**Fix Frontend Issues**:
```bash
cd web-app
npm run fix-setup
```

### Common Errors

#### ❌ "cd: no such file or directory: university-match-ai-main"

**Problem**: Wrong folder name.

**Solution**: The correct folder name is `university-match-ai` (without `-main`).
```bash
cd university-match-ai   # Correct
# NOT: cd university-match-ai-main
```

**How to find the correct folder**:
```bash
# List current directory
ls       # macOS
dir      # Windows

# Look for "university-match-ai" folder
```

---

#### ❌ Backend Returns 404 on Root URL (`/`)

**Problem**: Accessing `http://localhost:5000/` returns 404.

**Solution**: This is now fixed! The backend has a root route that shows API information.

If you still see 404:
- Make sure backend is running: `python app.py` (or `python3`)
- Check backend terminal for errors
- Test health endpoint: `http://localhost:5000/api/health`

---

#### ❌ "Bad HTTP/0.9 request type" or SSL/TLS Error

**Problem**: Frontend trying HTTPS, backend only supports HTTP.

**Solution**:
1. Always use `http://127.0.0.1:5173` (NOT `https://`)
2. Verify `web-app/vite.config.js` has `secure: false` in proxy settings
3. See [HATA_COZUM_REHBERI.md](HATA_COZUM_REHBERI.md) for detailed fix

---

#### ❌ "Port 5000 already in use" (Backend)

**Problem**: Another application is using port 5000.

**Solution (Windows)**:
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Solution (macOS)**:
```bash
kill -9 $(lsof -ti:5000)
```

---

#### ❌ "python: command not found" (macOS)

**Problem**: macOS uses `python3`, not `python`.

**Solution**: Always use `python3` on macOS:
```bash
python3 app.py
pip3 install -r requirements.txt
```

---

#### ❌ Frontend Can't Connect to Backend

**Checklist**:
- [ ] Is backend running? (Check Terminal 1)
- [ ] Is backend on `http://127.0.0.1:5000`?
- [ ] Is frontend using `http://127.0.0.1:5173`? (NOT `https://`)
- [ ] Test backend: `curl http://localhost:5000/api/health`

---

### More Help

1. **Complete Setup Guide**: [SETUP_GUIDE.md](SETUP_GUIDE.md) - Comprehensive guide with all errors
2. **Error Resolution**: [HATA_COZUM_REHBERI.md](HATA_COZUM_REHBERI.md) - Detailed error fixes (Turkish)
3. **General Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues

---

## ✨ Features

### Core Features

- 🔍 **Smart University Matching**: Advanced scoring algorithm based on GPA, language scores, background, experience, and more
- 📄 **CV Parsing**: Automatically extracts information from PDF and DOCX CV files
- ✍️ **Motivation Letter Analysis**: Evaluates motivation letters against key criteria
- 🎯 **Categorized Results**: Universities sorted into High/Medium/Low match categories
- 📱 **Multi-Platform**: Web app, iOS-ready (Capacitor), and API-first architecture

### Additional Features

- 🌐 **Multi-Language Support**: 5 main languages (EN, TR, ES, DE, FR) with auto-detection
- 📊 **Application Portfolio**: Export results as PDF with LinkedIn sharing
- 💬 **Feedback System**: Submit feedback directly from the app
- 📝 **Release Notes**: View version history and updates
- ⚙️ **Settings**: Customize language and preferences

---

## 📊 Matching Algorithm

The matching algorithm scores universities on a 0-110 scale using weighted criteria:

- **GPA (30 points)**: Academic performance evaluation
- **Language Score (20 points)**: TOEFL/IELTS proficiency
- **Background Match (15 points)**: Field alignment
- **Research Experience (10 points)**: Research background
- **Work Experience (8 points)**: Professional experience
- **Publications (5 points)**: Research publications
- **Recommendation Letters (5 points)**: Reference quality
- **University Ranking (4 points)**: Undergraduate institution
- **GRE/GMAT (3 points)**: Standardized test scores
- **Bonus Points (up to 10)**: Projects, competitions, etc.

---

## 🎯 Use Cases

1. **Prospective Students**: Find the best-fit universities for Master's applications
2. **Academic Counselors**: Quickly assess student profiles and suggest universities
3. **Institutions**: Understand applicant matching criteria and improve outreach
4. **Educational Platforms**: Integrate matching capabilities into existing services

---

## 🛠️ Development

### Running Tests

```bash
cd backend
python test_api.py        # Windows
python3 test_api.py       # macOS
```

### Adding Universities

Edit `backend/app.py` and add to the `UNIVERSITIES` list. Each university entry should include:
- Name and program
- Country
- Minimum GPA requirements
- Language score requirements
- Required background fields

---

## 📝 Examples

See `examples/sample_profile.json` for a sample user profile and expected results.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built to help students navigate the complex world of graduate school applications. This project aims to make higher education more accessible by providing intelligent matching tools.

### Built with [Cursor AI](https://cursor.sh) ✨

This entire project was developed collaboratively with **Cursor AI** - an exceptional AI coding assistant that truly understands context and helps bring ideas to life.

---

## 📅 Version History

**Current Version: 1.3** - Portfolio Modal & Enhanced LinkedIn Sharing

See [RELEASE_NOTES.md](RELEASE_NOTES.md) for detailed changelog.

**Previous Versions**:
- **1.1** - Enhanced Form Validation & User Experience
- **1.0** - Initial Release

---

## 📈 Application Strategy: Why Multiple Applications Matter

Research consistently shows that **applying to multiple universities significantly increases your chances of admission**. Graduate school admissions are inherently uncertain, and each university evaluates candidates differently.

**Recommended Approach**:
- **Minimum**: 5-6 applications (balanced portfolio)
- **Optimal**: 8-12 applications (well-distributed across match levels)
- **Maximum**: 12-15 applications (diminishing returns after this point)

**Important**: Quality matters more than quantity. Each application should be tailored to the specific program and demonstrate genuine interest.

### How This Tool Helps

University Match AI helps you build your application portfolio by:
1. **Identifying Multiple Options**: Find 20+ universities matching your profile
2. **Categorizing by Match Level**: Understand which are reach, match, or safety schools
3. **Strategic Planning**: Build a balanced list across different match categories
4. **Efficiency**: Quickly identify programs you might not have considered

---

**Note**: This tool is for informational purposes only. Always verify requirements directly with universities. Results are based on algorithmic matching and should be used as a starting point for your research. Admission decisions are made by universities and are subject to their individual policies and evaluation criteria.

---

**Last Updated**: November 2024
