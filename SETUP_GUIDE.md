# 🚀 Complete Setup Guide - University Match AI

> **Platform-Independent Installation Guide**  
> This guide works for **Windows 10/11** and **macOS** (all versions)

---

## 📋 Table of Contents

1. [Introduction](#-introduction)
2. [What You Need](#-what-you-need-prerequisites)
3. [Technology Stack](#-technology-stack)
4. [Project Structure](#-project-structure)
5. [Installation Steps](#-installation-steps)
6. [Running the Application](#-running-the-application)
7. [Troubleshooting & FAQ](#-troubleshooting--faq)
8. [Platform-Specific Notes](#-platform-specific-notes)

---

## 🎯 Introduction

**University Match AI** is an AI-powered platform that helps prospective Master's students find their perfect-fit universities. It uses an intelligent matching algorithm to score and categorize universities based on your academic profile.

### What This Application Does

- 🔍 **Smart Matching**: Scores 20+ top universities based on your profile
- 📄 **CV Analysis**: Automatically extracts information from PDF/DOCX CVs
- ✍️ **Application Support**: Evaluates motivation letters and materials
- 🎯 **Categorized Results**: High/Medium/Low match categories
- 🌐 **Web Interface**: Beautiful, responsive React web application
- 📱 **Mobile Ready**: Can be converted to iOS/Android apps

---

## 📦 What You Need (Prerequisites)

Before starting, make sure you have these installed:

### Required Software

#### 1. **Python 3.8+** (For Backend)
- **Download**: https://www.python.org/downloads/
- **Installation**:
  - Windows: Check "Add Python to PATH" during installation
  - macOS: Python comes pre-installed, but verify version with `python3 --version`
- **Verify**: Open terminal and type:
  ```bash
  python --version   # Windows
  python3 --version  # macOS (use python3)
  ```
- **Expected Output**: `Python 3.8.x` or higher

#### 2. **Node.js 16+** (For Web App)
- **Download**: https://nodejs.org/ (Choose **LTS version**)
- **Installation**: Run the installer, click "Next" until finished
- **Verify**: Open terminal and type:
  ```bash
  node --version
  npm --version
  ```
- **Expected Output**: `v18.x.x` or higher for Node.js, `9.x.x` or higher for npm

#### 3. **Git** (To Clone Repository)
- **Windows**: Usually comes with Git for Windows
- **macOS**: Usually pre-installed, verify with `git --version`
- **Download**: https://git-scm.com/downloads (if not installed)
- **Verify**: 
  ```bash
  git --version
  ```

#### 4. **pip** (Python Package Manager)
- **Windows**: Comes with Python installation
- **macOS**: Usually pre-installed
- **Verify**: 
  ```bash
  pip --version   # Windows
  pip3 --version  # macOS
  ```

---

## 🛠️ Technology Stack

This project uses the following technologies:

### Backend (Python)
- **Flask 3.0.0**: Web framework for API
- **Flask-CORS 4.0.0**: Cross-origin resource sharing
- **PyPDF2 3.0.1**: PDF parsing for CV extraction
- **python-docx 1.1.0**: DOCX parsing for CV extraction
- **pandas 2.1.3**: Data processing
- **numpy 1.26.2**: Numerical computations

### Frontend (React)
- **React 18.2.0**: UI library
- **Vite 5.0.8**: Build tool and dev server
- **Axios 1.6.2**: HTTP client for API calls

### Development Tools
- **Capacitor 6.0.0**: For converting web app to mobile apps
- **Node.js**: Runtime for frontend development

---

## 📁 Project Structure

Understanding the project structure helps you navigate the codebase:

```
university-match-ai/
│
├── backend/                    # Python Flask Backend
│   ├── app.py                 # Main API server (this is the brain!)
│   ├── premium.py             # Premium features & rate limiting
│   ├── stripe_integration.py  # Payment processing
│   ├── email_service.py       # Email service for feedback
│   ├── requirements.txt       # Python dependencies (install these)
│   ├── CHECK_BACKEND.py       # Setup verification script
│   └── users.json             # User data (auto-created)
│
├── web-app/                   # React Frontend
│   ├── src/                   # Source code
│   │   ├── components/        # React components (UI elements)
│   │   ├── utils/            # Utility functions (CV parser, i18n)
│   │   ├── App.jsx           # Main application component
│   │   └── main.jsx          # Entry point
│   ├── public/               # Static files (images, icons)
│   ├── package.json          # Node.js dependencies (install these)
│   ├── vite.config.js        # Vite configuration
│   ├── CHECK_SETUP.js        # Setup verification script
│   └── capacitor.config.json # Mobile app configuration
│
├── ios-app/                  # Swift iOS app (optional)
│   └── *.swift files         # SwiftUI components
│
├── examples/                 # Sample data
│   └── sample_profile.json   # Example user profile
│
├── README.md                 # Main documentation
├── SETUP_GUIDE.md           # This file! 📖
└── HATA_COZUM_REHBERI.md    # Error resolution guide (Turkish)

```

### Key Files Explained

- **`backend/app.py`**: The main backend server. Handles all API requests, matching algorithm, CV parsing. **This must run for the app to work.**
- **`backend/requirements.txt`**: List of Python packages needed. Install with `pip install -r requirements.txt`
- **`web-app/package.json`**: List of Node.js packages needed. Install with `npm install`
- **`web-app/src/App.jsx`**: Main React component - this is what users see in the browser
- **`web-app/vite.config.js`**: Configuration for the development server (ports, proxy settings)

---

## 📥 Installation Steps

### Step 1: Clone the Repository

Open your terminal (PowerShell on Windows, Terminal on macOS) and run:

```bash
git clone https://github.com/tekesineren/university-match-ai.git
```

**⚠️ Important**: The folder will be named `university-match-ai` (NOT `university-match-ai-main`)

**Navigate into the project**:
```bash
cd university-match-ai
```

**Verify you're in the right place** (you should see folders like `backend`, `web-app`):
```bash
# Windows (PowerShell)
dir

# macOS (Terminal)
ls
```

**❌ Common Error**: `cd: no such file or directory: university-match-ai-main`

**✅ Solution**: The correct folder name is `university-match-ai` (without `-main`). Use:
```bash
cd university-match-ai
```

---

### Step 2: Setup Backend (Python)

#### 2.1 Navigate to Backend Folder

```bash
cd backend
```

#### 2.2 Install Python Dependencies

```bash
# Windows
pip install -r requirements.txt

# macOS (use pip3)
pip3 install -r requirements.txt
```

**⏱️ This takes 1-3 minutes.** You'll see packages downloading.

**✅ Success looks like**:
```
Successfully installed flask-3.0.0 flask-cors-4.0.0 ...
```

**❌ Common Errors**:
- **"pip: command not found"** (macOS): Use `pip3` instead of `pip`
- **"Permission denied"** (macOS): Use `pip3 install --user -r requirements.txt`
- **"No module named pip"**: Reinstall Python and check "Add to PATH"

#### 2.3 Verify Backend Setup (Optional but Recommended)

```bash
# Windows
python CHECK_BACKEND.py

# macOS
python3 CHECK_BACKEND.py
```

This checks if all dependencies are installed correctly.

---

### Step 3: Setup Web App (Node.js)

#### 3.1 Open a NEW Terminal Window

**⚠️ Keep the backend terminal open!** Open a **new terminal window** for the frontend.

#### 3.2 Navigate to Web App Folder

From the project root (`university-match-ai`):

```bash
cd web-app
```

#### 3.3 Install Node.js Dependencies

```bash
npm install
```

**⏱️ This takes 2-5 minutes.** You'll see many packages downloading.

**✅ Success looks like**:
```
added 185 packages, and audited 186 packages in 5s
```

**❌ Common Errors**:
- **"npm: command not found"**: Install Node.js from https://nodejs.org/
- **"Unexpected end of file in JSON"**: Run `npm cache clean --force && npm install`
- **Network errors**: Check your internet connection, try again

#### 3.4 Verify Frontend Setup (Optional but Recommended)

```bash
npm run check-setup
```

This verifies your setup is correct.

---

## 🚀 Running the Application

### Important: You Need TWO Terminal Windows

The application consists of two parts that must run simultaneously:
1. **Backend** (Python Flask API) - Port 5000
2. **Frontend** (React Web App) - Port 5173

---

### Terminal 1: Start Backend

```bash
# Navigate to backend folder (if not already there)
cd backend

# Windows
python app.py

# macOS
python3 app.py
```

**✅ Success output**:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

**⚠️ Keep this terminal open!** The backend must stay running.

**❌ Common Errors**:
- **"Port 5000 already in use"**: Another process is using port 5000. Kill it or change the port in `app.py`.
- **"Module not found"**: Run `pip install -r requirements.txt` again
- **404 errors on `/`**: This is normal! The backend only has `/api/*` routes. Access `/api/health` to test.

---

### Terminal 2: Start Frontend

**Open a NEW terminal window** and run:

```bash
# Navigate to web-app folder
cd university-match-ai/web-app

# Start development server
npm run dev
```

**✅ Success output**:
```
  VITE v5.x.x  ready in 14158 ms

  ➜  Local:   http://127.0.0.1:5173/
  ➜  Network: use --host to expose
```

**⚠️ Keep this terminal open too!**

---

### Step 4: Open in Browser

Open your web browser and go to:

```
http://127.0.0.1:5173
```

or

```
http://localhost:5173
```

**✅ You should see the University Match AI homepage!**

---

## 🆘 Troubleshooting & FAQ

### ❌ Error: "cd: no such file or directory"

**Problem**: You're trying to access a folder that doesn't exist.

**Solutions**:

1. **Check current directory**:
   ```bash
   # Windows (PowerShell)
   pwd
   
   # macOS (Terminal)
   pwd
   ```

2. **List files to see what's available**:
   ```bash
   # Windows
   dir
   
   # macOS
   ls
   ```

3. **Find where you cloned the project**:
   ```bash
   # Windows - common locations:
   cd C:\Users\YourUsername\Desktop
   cd C:\Users\YourUsername\Documents
   
   # macOS - common locations:
   cd ~/Desktop
   cd ~/Documents
   ```

4. **If you don't see `university-match-ai` folder**:
   - You might not have cloned it yet. Run: `git clone https://github.com/tekesineren/university-match-ai.git`
   - The folder name is `university-match-ai` (NOT `university-match-ai-main`)

---

### ❌ Error: Backend Returns 404 on Root URL

**Problem**: Accessing `http://localhost:5000/` returns 404.

**Explanation**: This is **NORMAL**! The backend is an API-only server. It doesn't have a root route (`/`).

**✅ Correct URLs to test backend**:
- Health check: `http://localhost:5000/api/health`
- Get universities: `http://localhost:5000/api/universities`

**The web app** (`http://localhost:5173`) is what you should use - it talks to the backend automatically.

---

### ❌ Error: "Bad HTTP/0.9 request type" or SSL/TLS Error

**Problem**: Frontend trying to use HTTPS, backend only supports HTTP.

**Solution**: 
1. Always use `http://127.0.0.1:5173` (NOT `https://`)
2. Check `web-app/vite.config.js` has `secure: false` in proxy settings
3. See [HATA_COZUM_REHBERI.md](HATA_COZUM_REHBERI.md) for detailed fix

---

### ❌ Error: "Unexpected end of file in JSON" (package.json)

**Problem**: `package.json` is corrupted or empty.

**Solution**:
```bash
cd web-app
npm run fix-setup
```

Or manually restore from Git:
```bash
cd web-app
git checkout package.json
npm install
```

---

### ❌ Error: "Port 5000 already in use" (Backend)

**Problem**: Another application is using port 5000.

**Solution (Windows)**:
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with the number you found)
taskkill /PID <PID> /F
```

**Solution (macOS)**:
```bash
# Find process using port 5000
lsof -ti:5000

# Kill the process
kill -9 $(lsof -ti:5000)
```

**Alternative**: Change the port in `backend/app.py` (line ~1206).

---

### ❌ Error: "Port 5173 already in use" (Frontend)

**Solution (Windows)**:
```powershell
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

**Solution (macOS)**:
```bash
kill -9 $(lsof -ti:5173)
```

**Alternative**: Vite will automatically use the next available port (5174, 5175, etc.)

---

### ❌ Error: "Module not found" or "Cannot find module"

**Problem**: Dependencies not installed.

**Solution**:
```bash
# Backend
cd backend
pip install -r requirements.txt  # Windows
pip3 install -r requirements.txt # macOS

# Frontend
cd web-app
npm install
```

---

### ❌ Error: Frontend can't connect to backend (Network Error)

**Problem**: Backend not running or wrong URL.

**Checklist**:
1. ✅ Is backend running? (Check Terminal 1)
2. ✅ Is backend on `http://127.0.0.1:5000`? (Check Terminal 1 output)
3. ✅ Is frontend using `http://127.0.0.1:5173`? (NOT `https://`)
4. ✅ Check `web-app/vite.config.js` proxy settings point to `http://localhost:5000`

**Test backend directly**:
```bash
# Windows (PowerShell)
curl http://localhost:5000/api/health

# macOS
curl http://localhost:5000/api/health
```

**Expected output**: `{"status":"ok"}`

---

### ❌ Error: "python: command not found" (macOS)

**Problem**: macOS uses `python3`, not `python`.

**Solution**: Always use `python3` instead of `python` on macOS:
```bash
python3 app.py
pip3 install -r requirements.txt
```

---

### ❌ Error: "npm: command not found"

**Problem**: Node.js not installed.

**Solution**: 
1. Download Node.js from https://nodejs.org/ (LTS version)
2. Install it
3. **Restart your terminal** (important!)
4. Verify: `node --version`

---

### ❌ Error: "pip: command not found" (macOS)

**Problem**: macOS may not have `pip` in PATH.

**Solution**: Use `pip3`:
```bash
pip3 install -r requirements.txt
```

Or install pip:
```bash
python3 -m ensurepip --upgrade
```

---

## 🖥️ Platform-Specific Notes

### Windows 10/11

1. **Terminal**: Use **PowerShell** (recommended) or **Command Prompt**
2. **Python**: Use `python` (not `python3`)
3. **Path Separator**: Use backslashes `\` or forward slashes `/` (both work)
4. **File Paths**: Full paths like `C:\Users\YourName\Documents\...`

**Example Windows commands**:
```powershell
cd C:\Users\YourName\Desktop
git clone https://github.com/tekesineren/university-match-ai.git
cd university-match-ai\backend
python app.py
```

---

### macOS (All Versions)

1. **Terminal**: Use **Terminal.app** (built-in) or **iTerm2**
2. **Python**: Always use `python3` (not `python`)
3. **pip**: Always use `pip3` (not `pip`)
4. **Path Separator**: Use forward slashes `/`
5. **Home Directory**: Use `~` (shortcut for `/Users/YourName`)

**Example macOS commands**:
```bash
cd ~/Desktop
git clone https://github.com/tekesineren/university-match-ai.git
cd university-match-ai/backend
python3 app.py
```

**macOS Permission Issues**:
If you get permission errors with `pip3`, use:
```bash
pip3 install --user -r requirements.txt
```

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Python installed and working (`python --version` or `python3 --version`)
- [ ] Node.js installed and working (`node --version`)
- [ ] Git installed and working (`git --version`)
- [ ] Project cloned successfully
- [ ] Backend dependencies installed (`cd backend && pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`cd web-app && npm install`)
- [ ] Backend runs without errors (`python app.py` or `python3 app.py`)
- [ ] Frontend runs without errors (`npm run dev`)
- [ ] Browser can access `http://localhost:5173`
- [ ] Backend health check works: `http://localhost:5000/api/health`

---

## 📚 Additional Resources

- **Main README**: [README.md](README.md) - Project overview and features
- **Error Resolution Guide**: [HATA_COZUM_REHBERI.md](HATA_COZUM_REHBERI.md) - Detailed error fixes (Turkish)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - General troubleshooting
- **Getting Started**: [GETTING_STARTED.md](GETTING_STARTED.md) - Quick start guide

---

## 🎉 Success!

If you've completed all steps and can access `http://localhost:5173`, you're ready to use University Match AI!

**Next Steps**:
1. Fill out your academic profile
2. Upload your CV (optional)
3. Get matched with universities!
4. Explore the categorized results

---

## 💬 Need Help?

If you're still having issues:

1. Read this guide completely
2. Check [HATA_COZUM_REHBERI.md](HATA_COZUM_REHBERI.md) for specific errors
3. Run the verification scripts:
   - Backend: `python CHECK_BACKEND.py` (or `python3`)
   - Frontend: `npm run check-setup`
4. Check that both backend and frontend are running in separate terminals

---

**Last Updated**: November 2024  
**Tested On**: Windows 10/11, macOS 11+ (Big Sur and later)

