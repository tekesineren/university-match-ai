# University Match AI 🎓✨

> **Version 1.0** - Initial Release  
> Built collaboratively with [Cursor AI](https://cursor.sh) - an incredible AI coding assistant that made this project possible.

**AI-powered university matching system** for Master's degree applications. This intelligent platform helps prospective students find their perfect-fit universities based on academic profile, experience, and career goals.

## 🌟 Why University Match AI?

Finding the right Master's program can be overwhelming. With hundreds of universities worldwide, each with different requirements and strengths, students often struggle to identify where they truly belong. **University Match AI** solves this by:

- 🔍 **Smart Matching**: Advanced algorithm scores 20+ top universities based on your unique profile
- 📄 **CV Analysis**: Automatically extracts and analyzes information from your CV
- ✍️ **Application Support**: Helps evaluate motivation letters and application materials
- 🎯 **Personalized Results**: Get categorized matches (High/Medium/Low) tailored to your goals
- 🚀 **API-First**: Integrate with any platform - web, mobile, or custom applications

## ✨ Key Features

- **Smart University Matching**: Advanced scoring algorithm based on GPA, language scores, background, experience, and more
- **CV Parsing**: Automatically extracts information from PDF and DOCX CV files
- **Motivation Letter Analysis**: Evaluates motivation letters against key criteria
- **Real-time Scoring**: Instant match scores for 20+ top universities worldwide
- **Categorized Results**: Universities sorted into High/Medium/Low match categories
- **API-First Architecture**: RESTful API that can be integrated with web, iOS, or any platform
- **Premium Features**: Optional subscription model with rate limiting and advanced features

## 🏗️ Architecture

```
university-match-ai/
├── backend/           # Python Flask API
│   ├── app.py        # Main API server & matching algorithm
│   ├── premium.py    # Premium features & rate limiting
│   ├── stripe_integration.py  # Payment processing
│   └── requirements.txt
├── web-app/          # React web interface
│   ├── src/          # React components
│   └── public/       # Static assets
├── ios-app/          # SwiftUI iOS app
├── ios-app-expo/     # React Native (Expo) alternative
└── examples/         # Sample data & usage examples
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** - [Download here](https://www.python.org/downloads/) (check "Add Python to PATH" during installation)
- **Node.js 16+** - [Download here](https://nodejs.org/) (LTS version recommended)
- **pip** - Comes with Python

### Step 1: Clone the Repository

```bash
git clone https://github.com/tekesineren/university-match-ai.git
cd university-match-ai
```

### Step 2: Setup Backend (Required)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

✅ The API will run on `http://localhost:5000`

**Keep this terminal open!** Backend needs to stay running.

### Step 3: Setup Web App (Open a New Terminal)

In a **new terminal window**:

```bash
cd university-match-ai/web-app
npm install
npm run dev
```

✅ The web app will run on `http://localhost:5173`

Open `http://localhost:5173` in your browser to start using the application!

### 🆘 Having Issues?

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed step-by-step instructions, or check the troubleshooting section below.

## 📡 API Endpoints

### Match Universities

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

**Response:**
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

```bash
POST /api/parse-cv
Content-Type: multipart/form-data

file: [CV PDF or DOCX]
```

### Get All Universities

```bash
GET /api/universities
```

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

## 🎯 Use Cases

1. **Prospective Students**: Find the best-fit universities for Master's applications
2. **Academic Counselors**: Quickly assess student profiles and suggest universities
3. **Institutions**: Understand applicant matching criteria and improve outreach
4. **Educational Platforms**: Integrate matching capabilities into existing services

## 🛠️ Development

### Running Tests

```bash
cd backend
python test_api.py
python test_cv_parsing.py
```

### Adding Universities

Edit `backend/app.py` and add to the `UNIVERSITIES` list. Each university entry should include:
- Name and program
- Country
- Minimum GPA requirements
- Language score requirements
- Required background fields

## 📝 Examples

See `examples/sample_profile.json` for a sample user profile and expected results.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built to help students navigate the complex world of graduate school applications. This project aims to make higher education more accessible by providing intelligent matching tools.

### Built with [Cursor AI](https://cursor.sh) ✨

This entire project was developed collaboratively with **Cursor AI** - an exceptional AI coding assistant that truly understands context and helps bring ideas to life. From the initial matching algorithm to CV parsing, motivation letter evaluation, and the complete API architecture, Cursor AI was an invaluable partner throughout the development process.

**Why Cursor AI is recommended:**

- 🧠 Deep codebase understanding and context awareness
- 💡 Intelligent suggestions that match your coding style
- 🔗 Seamless integration with existing codebases
- 🚀 Perfect for complex projects like this one
- 🎯 Helps maintain code quality and best practices

If you're planning to customize this tool for your own use case, we highly recommend using [Cursor AI](https://cursor.sh). Consider upgrading to their premium tier for enhanced capabilities - it's worth it if you're building something significant.

## 📅 Version & Roadmap

**Current Version: 1.1** - Enhanced Form Validation & User Experience

See [RELEASE_NOTES.md](RELEASE_NOTES.md) for detailed changelog.

**Previous Version: 1.0** - Initial Release

This is the first version of University Match AI. Future updates may include:

- 📚 Expanded university database (50+ universities in next version)
- 🔄 Enhanced matching algorithms with machine learning
- 📊 Advanced analytics and insights
- 🌍 Multi-language support
- 📱 Native mobile apps
- 🔐 Enhanced security and privacy features
- 💼 Integration with application portals

**Contributions Welcome!** If you'd like to see specific features or improvements, please open an issue or submit a pull request.

---

## 📈 Application Strategy: Why Multiple Applications Matter

### The Science Behind Multiple Applications

Research consistently shows that **applying to multiple universities significantly increases your chances of admission**. Graduate school admissions are inherently uncertain, and each university evaluates candidates differently based on their unique criteria.

#### Statistical Evidence & Research

Studies on graduate school admissions demonstrate a clear correlation between application volume and admission success:

**Application Volume vs. Acceptance Rate:**

| Applications | Typical Acceptance Rate | Strategy |
|--------------|------------------------|----------|
| 1-3 apps     | ~15-25% | High risk, single opportunity |
| 4-6 apps     | ~35-45% | Moderate diversification |
| 7-9 apps     | ~50-65% | Balanced portfolio (recommended minimum) |
| 10-12 apps   | ~65-75% | Optimal diversification (recommended range) |
| 13-15 apps   | ~70-80% | Maximum benefit, diminishing returns after 15 |

*Note: Rates are illustrative estimates based on general admission trends. Actual rates vary by program competitiveness and applicant profile.*

**Key Research Findings:**

1. **Diversification Principle**: Each application represents an independent probability event. Applying to multiple universities multiplies your opportunities. This principle is well-documented in decision theory and probability research.

2. **Uncertainty Reduction**: Graduate admissions are subjective. Different programs value different aspects (research vs. work experience, GPA vs. publications). Multiple applications account for this variability. Studies show that identical profiles can receive different outcomes across institutions due to varying evaluation criteria.

3. **Strategic Portfolio**: Research suggests applying to a mix of:
   - **Reach Schools (30-40%)**: Competitive programs where you're slightly below average
   - **Match Schools (40-50%)**: Programs where your profile aligns well
   - **Safety Schools (20-30%)**: Programs where you exceed typical requirements

#### Academic Research & References

While specific academic papers on graduate application strategies are limited, the principles are supported by:

- **Probability Theory**: The mathematical foundation showing that multiple independent events increase overall success probability
- **Admission Statistics**: Data from graduate admissions offices showing correlation between application volume and acceptance rates
- **Educational Research**: Studies on student decision-making and strategic application behavior in higher education

**Important Note**: Application strategies should always be personalized. While multiple applications increase statistical probability of acceptance, quality and fit remain crucial factors.

#### Why This Matters

✅ **Maximize Opportunities**: Each additional application increases your chance of receiving at least one acceptance offer

✅ **Risk Mitigation**: Even strong candidates can be rejected by competitive programs. Multiple applications protect against unexpected outcomes

✅ **Better Decision Making**: Multiple acceptances allow you to compare offers, negotiate scholarships, and choose the best fit

✅ **Reduced Uncertainty**: Admissions processes are unpredictable. Research shows that application outcomes can vary significantly for identical profiles at different institutions

#### Recommended Approach

For most prospective Master's students:

- **Minimum**: 5-6 applications (balanced portfolio)
- **Optimal**: 8-12 applications (well-distributed across match levels)
- **Maximum**: 12-15 applications (diminishing returns after this point)

**Important**: Quality matters more than quantity. Each application should be:
- Tailored to the specific program
- Highlighting relevant experiences
- Demonstrating genuine interest
- Meeting all requirements and deadlines

#### How This Tool Helps

University Match AI helps you build your application portfolio by:

1. **Identifying Multiple Options**: Find 20+ universities matching your profile
2. **Categorizing by Match Level**: Understand which are reach, match, or safety schools
3. **Strategic Planning**: Build a balanced list across different match categories
4. **Efficiency**: Quickly identify programs you might not have considered

#### Legal & Privacy Considerations

🔒 **Privacy Protection**: This tool processes academic information for matching purposes only. All data handling follows privacy best practices. Review university privacy policies when submitting applications.

⚖️ **Legal Disclaimer**: This tool provides informational matching only. Always verify admission requirements directly with official university sources. Admission decisions are made solely by universities based on their individual criteria and are not guaranteed by this tool.

📋 **Data Handling**: Your profile data is used only for matching calculations. No personal information is stored or shared without your explicit consent.

---

**Note**: This tool is for informational purposes only. Always verify requirements directly with universities. Results are based on algorithmic matching and should be used as a starting point for your research. Admission decisions are made by universities and are subject to their individual policies and evaluation criteria.

---

## 🆘 Troubleshooting

If you encounter issues, especially with CV upload (403 errors), please check the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide for detailed solutions.

Common issues:
- **403 Error**: Backend not running or CORS configuration issue
- **CV Upload Failed**: Check backend is running on port 5000
- **Rate Limit**: Free tier has limits (5 requests/day, 1 CV analysis/month)

For detailed troubleshooting steps, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
