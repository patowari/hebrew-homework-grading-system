# 🎓 AI Homework Grading System for Hebrew Mathematics

An intelligent homework grading system that uses Google's Gemini AI to automatically grade Hebrew mathematics homework. The system supports both handwritten and typed content, making it perfect for teachers who want to provide instant, detailed feedback to students.

## ✨ Features

### 📚 **Multi-Format Support**
- **Handwritten PDFs**: Automatically converts handwritten math PDFs to images for AI analysis
- **Text-based PDFs**: Extracts and analyzes text content
- **Word Documents**: Supports DOCX files
- **Images**: JPG, PNG formats for handwritten homework photos
- **Direct Text Input**: Type or paste homework directly

### 🔍 **Advanced AI Analysis**
- **Hebrew Language Support**: Native Hebrew prompts and feedback
- **Visual Recognition**: Reads handwritten mathematical expressions
- **Reference Comparison**: Compares homework against teacher's reference materials
- **Intelligent Scoring**: Provides scores out of 100 with detailed breakdown

### 📊 **Comprehensive Feedback**
- **Overall Score**: Clear numerical grade with visual indicators
- **Problem-by-Problem Analysis**: Detailed feedback for each section
- **Strengths & Improvements**: Highlights what students did well and areas to improve
- **Learning Suggestions**: Specific recommendations for better understanding
- **Encouraging Comments**: Motivational feedback in Hebrew

### 🌐 **User-Friendly Interface**
- **Web-based**: Easy-to-use Streamlit interface
- **Real-time Processing**: Instant AI analysis and feedback
- **Preview Images**: Shows uploaded content before analysis
- **Download Reports**: Export grade reports as text files

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/))

### Step 1: Clone or Download
```bash
git clone <repository-url>
cd homework-grading-system
```

### Step 2: Install Python Dependencies
```bash
pip install streamlit google-generativeai PyPDF2 Pillow python-docx pdf2image
```

### Step 3: Install System Dependencies

**macOS:**
```bash
brew install poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**Windows:**
1. Download [poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
2. Extract and add to PATH

**Alternative using conda:**
```bash
conda install poppler
```

## 🚀 Quick Start

### 1. Get Your Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/)
2. Create a new API key
3. Keep it secure - you'll need it to run the application

### 2. Run the Application
```bash
streamlit run homework_grading_system.py
```

### 3. Setup in Browser
1. Open the URL shown in terminal (usually `http://localhost:8501`)
2. Enter your Gemini API key in the sidebar
3. Upload your Hebrew math reference material (PDF)
4. Start grading homework!

## 📖 Usage Guide

### Setting Up Reference Material
1. **Upload Reference PDF**: Click "Upload Hebrew Math PDF (Reference)" in the sidebar
2. **Automatic Detection**: System automatically detects if your PDF is handwritten or text-based
3. **Preview**: See a preview of your reference material
4. **Ready to Grade**: Once loaded, you can start grading student homework

### Grading Student Homework

#### Method 1: File Upload
1. Select "Text File" upload method
2. Upload PDF, DOCX, or TXT file
3. For handwritten PDFs, the system will show a preview
4. Enter student name and click "Grade Homework"

#### Method 2: Image Upload
1. Select "Image" upload method
2. Upload clear photo of handwritten homework
3. System will analyze the image directly

#### Method 3: Direct Input
1. Select "Direct Text Input"
2. Type or paste homework content
3. Best for typed or transcribed homework

### Understanding Results

**Score Display:**
- 🌟 90-100: Excellent work!
- 👍 80-89: Good job!
- 📈 70-79: Room for improvement
- 📚 Below 70: Needs more practice

**Detailed Feedback Sections:**
- **Problem Analysis**: Score and feedback for each problem
- **Strengths**: What the student did well
- **Areas to Improve**: Specific areas needing work
- **Learning Suggestions**: Recommendations for improvement
- **Teacher's Comment**: Encouraging overall feedback

## 🔧 Configuration

### Supported File Formats
- **PDFs**: Both text-based and handwritten
- **Images**: PNG, JPG, JPEG
- **Documents**: DOCX, TXT
- **Languages**: Hebrew (primary), English (fallback)

### AI Models Used
The system automatically tries these Gemini models in order:
1. `gemini-2.0-flash-exp` (latest experimental)
2. `gemini-1.5-flash` (fast and efficient)
3. `gemini-1.5-pro` (most capable)
4. `gemini-pro` (fallback)

## 🛟 Troubleshooting

### Common Issues

**"Command not found: streamlit"**
```bash
pip install streamlit
# or
python3 -m pip install streamlit
```

**"Model not found" error**
- Check your Gemini API key is valid
- Use the "Check Available Models" button in the app
- Some models may not be available in all regions

**PDF processing issues**
- Ensure poppler is installed correctly
- For handwritten PDFs, make sure images are clear and high contrast
- Try converting PDF to images manually if needed

**Hebrew text display problems**
- Ensure your browser supports Hebrew fonts
- Some terminals may not display Hebrew correctly (this doesn't affect the AI analysis)

### Performance Tips

**For Better Results:**
- Use high-resolution images (200+ DPI)
- Ensure handwriting is clear and legible
- Keep reference materials focused and relevant
- Provide complete problem solutions in homework

**For Faster Processing:**
- Limit PDF pages to essential content
- Use smaller image file sizes when possible
- Process one homework at a time for best results

## 📝 Example Workflow

1. **Teacher Setup:**
   - Upload handwritten Hebrew math answer key (PDF)
   - System converts to images and prepares for comparison

2. **Student Submission:**
   - Student uploads handwritten homework (PDF or image)
   - System analyzes against teacher's reference

3. **AI Analysis:**
   - Compares student work to reference material
   - Evaluates mathematical accuracy and approach
   - Generates Hebrew feedback

4. **Results:**
   - Student receives score out of 100
   - Detailed feedback in Hebrew
   - Specific suggestions for improvement
   - Downloadable grade report

## 🔒 Privacy & Security

- **API Key**: Your Gemini API key is only stored locally during the session
- **File Processing**: All files are processed locally and sent to Google's AI services
- **No Data Storage**: The application doesn't store homework or grades permanently
- **Secure**: Uses official Google Gemini API with standard security practices

## 🤝 Contributing

This system can be extended with additional features:

- **Database Integration**: Store grades and track student progress
- **Batch Processing**: Grade multiple homework files at once
- **LMS Integration**: Connect with learning management systems
- **Multi-language Support**: Extend to other languages
- **Advanced Analytics**: Generate class performance reports

## 📄 License

This project is open source. Please ensure you comply with Google's Gemini AI usage policies when using this system.

## 🆘 Support

### Getting Help
1. **Check this README** for common solutions
2. **Use the "Check Available Models" button** to debug API issues
3. **Verify your setup** using the troubleshooting section

### System Requirements
- **Python**: 3.8+
- **RAM**: 4GB minimum (8GB recommended for large PDFs)
- **Internet**: Required for Gemini API calls
- **Browser**: Modern browser with JavaScript enabled

### API Costs
- This system uses Google's Gemini API
- Check [Google AI pricing](https://ai.google.dev/pricing) for current rates
- Costs depend on content length and number of requests

---

## 🎯 Perfect For:
- **Hebrew Math Teachers** looking to automate grading
- **Schools** wanting to provide instant feedback
- **Tutoring Services** needing efficient assessment tools
- **Educational Technology** integration projects

**Start grading smarter, not harder! 🚀**
