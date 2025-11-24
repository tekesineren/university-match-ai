# Master Application Agent 🎓

> **Version 1.0** - Initial Release  
> Built collaboratively with [Cursor AI](https://cursor.sh) - an incredible AI coding assistant that made this project possible.

AI-powered university matching system for Master's degree applications. This tool helps prospective students find the best-fit universities based on their academic profile, experience, and goals.

**🎯 Real Success Story:** This tool was developed during my actual Master's application process and proved incredibly valuable. I successfully used it to complete applications for top universities including KTH Royal Institute of Technology. I highly recommend this approach - you can upgrade to Cursor's premium features if needed, and work with their AI assistant (similar to the one that helped build this) to customize it for your own journey.

**📅 Roadmap:** This is the initial version. Future updates will include more universities, enhanced matching algorithms, and additional features based on user feedback.

## ✨ Features

- **Smart University Matching**: Advanced algorithm that scores universities based on GPA, language scores, background, experience, and more
- **CV Parsing**: Automatically extracts information from PDF and DOCX CV files
- **Motivation Letter Analysis**: Evaluates motivation letters for key criteria
- **Real-time Scoring**: Instant match scores for 50+ universities worldwide
- **Categorized Results**: Universities sorted into High/Medium/Low match categories
- **API-First Architecture**: RESTful API that can be integrated with web, iOS, or any platform

## 🏗️ Architecture

```
master-application-agent/
├── backend/           # Python Flask API
│   ├── app.py        # Main API server & matching algorithm
│   ├── premium.py    # Premium features & rate limiting
│   └── requirements.txt
├── web-app/          # React web interface
├── ios-app/          # SwiftUI iOS app
├── ios-app-expo/     # React Native (Expo) alternative
└── examples/         # Sample data & usage examples
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+ (for web app)
- pip

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The API will run on `http://localhost:5000`

### API Endpoints

#### Match Universities
```bash
POST /api/match
Content-Type: application/json

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

Response:
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

#### Parse CV
```bash
POST /api/parse-cv
Content-Type: multipart/form-data

file: [CV PDF or DOCX]
```

#### Get All Universities
```bash
GET /api/universities
```

## 📊 Matching Algorithm

The matching algorithm scores universities on a 0-110 scale:

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

## 🎯 Use Cases

1. **Prospective Students**: Find the best-fit universities for Master's applications
2. **Counselors**: Quickly assess student profiles and suggest universities
3. **Institutions**: Understand applicant matching criteria

## 🛠️ Development

### Running Tests

```bash
cd backend
python test_api.py
python test_cv_parsing.py
```

### Adding Universities

Edit `backend/app.py` and add to the `UNIVERSITIES` list.

## 📝 Example

See `examples/sample_profile.json` for a sample user profile and expected results.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built to help students navigate the complex world of graduate school applications.

### Built with [Cursor AI](https://cursor.sh) ✨

This entire project was developed collaboratively with **Cursor AI** - an exceptional AI coding assistant that truly understands context and helps bring ideas to life. From the initial matching algorithm to CV parsing, motivation letter evaluation, and the complete API architecture, Cursor AI was an invaluable partner in this development process.

**Why I recommend Cursor:**
- Deep codebase understanding and context awareness
- Intelligent suggestions that match your coding style
- Seamless integration with existing codebases
- Perfect for complex projects like this one

If you're planning to customize this tool for your own use case, I highly recommend using Cursor. You might want to consider upgrading to their premium tier for enhanced capabilities - it's worth it if you're building something significant.

**My Journey:**
This tool was developed during my real Master's application process. Working with Cursor AI, I was able to:
- Parse my transcript and extract course information
- Generate optimized motivation letters
- Match my profile with suitable universities
- Complete application forms with AI-assisted guidance
- Successfully apply to programs like KTH's Systems, Control and Robotics

The same AI assistant that helped build this tool can help you customize it for your own journey. Consider upgrading to Cursor's premium features if you're serious about your applications - it was a game-changer for me.

---

## 📅 Version & Updates

**Current Version: 1.0** - Initial Release

This is the first version of the Master Application Agent. Future updates may include:
- Expanded university database
- Enhanced matching algorithms
- Additional evaluation criteria
- Web interface improvements
- Mobile app enhancements

**Contribute:** If you'd like to see specific features or improvements, please open an issue or submit a pull request!

---

**Note**: This tool is for informational purposes only. Always verify requirements directly with universities.