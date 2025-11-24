# 🚀 Getting Started Guide

Complete step-by-step guide for beginners. Follow these instructions even if you've never used similar projects before!

---

## 📋 Prerequisites (Download Links)

### 1. Python (For Backend)
- **Download:** https://www.python.org/downloads/
- **Installation:** Run the downloaded file, check "Add Python to PATH", click "Install Now"
- **Verify:** Open terminal and type `python --version` (should show Python 3.8+)

### 2. Node.js (For Web App)
- **Download:** https://nodejs.org/
- **Choose LTS version** (long-term support)
- **Installation:** Run the downloaded file, continue with "Next"
- **Verify:** Open terminal and type `node --version`

### 3. Git (You probably already have it, but verify)
- **Verify:** Open terminal and type `git --version`
- **If not:** https://git-scm.com/downloads

---

## 🎯 Option 1: Use Only Backend API

### Step 1: Navigate to Project
```bash
cd C:\Users\user\master-application-agent
```

### Step 2: Go to Backend Folder
```bash
cd backend
```

### Step 3: Install Required Packages
```bash
pip install -r requirements.txt
```

### Step 4: Start Backend
```bash
python app.py
```

**Output:**
```
 * Running on http://127.0.0.1:5000
```

### Step 5: Test It (Open New Terminal)
Open your browser and go to:
```
http://localhost:5000/api/universities
```

You should see the university list! ✅

---

## 🌐 Option 2: Use with Web App (Recommended)

### Step 1: Start Backend
Follow "Option 1" steps above, keep backend running.

### Step 2: Open New Terminal
While backend is running, open a **new terminal window**.

### Step 3: Navigate to Web App Folder
```bash
cd C:\Users\user\master-application-agent\web-app
```

### Step 4: Install Node Packages (First Time Only)
```bash
npm install
```

**Note:** This may take 2-5 minutes, be patient! ☕

### Step 5: Start Web App
```bash
npm run dev
```

**Output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

### Step 6: Open in Browser
Open your browser and go to:
```
http://localhost:5173
```

**The web interface will appear!** 🎉

---

## 📱 Option 3: iOS App (Advanced)

iOS app requires Xcode and Mac. Start with the web app first, you can do iOS later.

---

## 🧪 First Test - University Matching

### In Web App:
1. **Enter GPA** (e.g., 3.5)
2. **Select Language test** (TOEFL or IELTS)
3. **Enter Score** (e.g., 95)
4. **Select Background** (e.g., robotics, engineering)
5. **Enter Work experience** (e.g., 1.5 years)
6. **Click "Find My Match"** button

**Result:** Universities will be sorted as High/Medium/Low match! 🎯

---

## 🛠️ Troubleshooting

### "python: command not found"
- Python is not installed or not added to PATH
- Reinstall Python, make sure to check "Add to PATH"

### "pip: command not found"
- Comes with Python, try `python -m pip install -r requirements.txt`

### "npm: command not found"
- Node.js is not installed
- Reinstall Node.js

### "Port 5000 already in use"
- Backend is already running or another program is using it
- Close that program or use a different port

### "Port 5173 already in use"
- Web app is already running
- Open `http://localhost:5173` in your browser

---

## 📚 Next Steps

1. **Upload CV:** Upload your CV in the web app, get automatic analysis
2. **Premium Features:** Check `backend/premium.py` file
3. **Stripe Integration:** Open Stripe account to monetize
4. **Deploy:** Deploy to platforms like Railway, Vercel

---

## 🆘 Need Help?

- **GitHub Issues:** https://github.com/tekesineren/university-match-ai/issues
- **Read README:** Check `README.md` file for detailed information
- **Backend Code:** Explore `backend/app.py` file

---

**Good luck! 🚀**

