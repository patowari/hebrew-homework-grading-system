# AI Homework Grading System for Handwritten Hebrew Math
# Requirements: pip install google-generativeai streamlit PyPDF2 Pillow python-docx pdf2image

import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import base64
from PIL import Image
import docx
import json
import datetime
import os
from pdf2image import convert_from_bytes
import tempfile

class HomeworkGradingSystem:
    def __init__(self, api_key):
        """Initialize the grading system with Gemini API"""
        genai.configure(api_key=api_key)
        
        # Try different model names in order of preference
        model_names = [
            'gemini-2.0-flash-exp',
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-pro'
        ]
        
        self.model = None
        self.vision_model = None
        
        for model_name in model_names:
            try:
                self.model = genai.GenerativeModel(model_name)
                self.vision_model = genai.GenerativeModel(model_name)
                self.model_name = model_name
                # Test the model with a simple request
                test_response = self.model.generate_content("Test")
                break
            except Exception as e:
                continue
        
        if not self.model:
            raise Exception("No compatible Gemini model found. Please check your API key and available models.")
        
        self.reference_content = ""
        self.reference_images = []
        self.reference_type = "none"
    
    def list_available_models(self):
        """List available models for debugging"""
        try:
            models = list(genai.list_models())
            return [model.name for model in models if 'generateContent' in model.supported_generation_methods]
        except Exception as e:
            return f"Error listing models: {str(e)}"
        
    def extract_pdf_content(self, pdf_file):
        """Extract content from PDF - handles both text and handwritten PDFs"""
        try:
            # First try text extraction
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                text += page_text + "\n"
            
            # If we got meaningful text (more than just whitespace/minimal characters)
            if len(text.strip()) > 50:
                return {"type": "text", "content": text}
            
            # If minimal text, treat as handwritten PDF - convert to images
            pdf_file.seek(0)  # Reset file pointer
            pdf_bytes = pdf_file.read()
            
            # Convert PDF pages to images
            images = convert_from_bytes(pdf_bytes, dpi=200)
            
            return {"type": "images", "content": images}
            
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
            return {"type": "error", "content": str(e)}
    
    def extract_pdf_text(self, pdf_file):
        """Legacy method - kept for compatibility"""
        result = self.extract_pdf_content(pdf_file)
        if result["type"] == "text":
            return result["content"]
        elif result["type"] == "images":
            return f"[Handwritten PDF with {len(result['content'])} pages detected]"
        else:
            return ""
    
    def extract_docx_text(self, docx_file):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(docx_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading DOCX: {str(e)}")
            return ""
    
    def process_image(self, image_file):
        """Process image file for text extraction"""
        try:
            image = Image.open(image_file)
            return image
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            return None
    
    def load_reference_material(self, reference_file):
        """Load the reference Hebrew math PDF (handwritten or text)"""
        if reference_file is not None:
            result = self.extract_pdf_content(reference_file)
            
            if result["type"] == "text":
                self.reference_content = result["content"]
                self.reference_type = "text"
                return True
            elif result["type"] == "images":
                self.reference_images = result["content"]
                self.reference_type = "images"
                # Create a summary of the reference material from images
                self.reference_content = f"מידע ההפניה מבוסס על {len(result['content'])} עמודים של מתמטיקה בכתב יד בעברית"
                return True
            else:
                return False
        return False
    
    def analyze_homework_text(self, homework_text, student_name="Anonymous"):
        """Analyze homework text and provide scoring"""
        if not self.reference_content:
            return {"error": "Reference material not loaded"}
        
        prompt = f"""
        אתה מורה מתמטיקה מומחה הבודק שיעורי בית בעברית. 
        
        חומר ייחוס (תוכן מתמטיקה בעברית):
        {self.reference_content[:4000]}
        
        שיעורי בית של התלמיד:
        שם התלמיד: {student_name}
        תוכן: {homework_text}
        
        אנא נתח את שיעורי הבית האלה וספק:
        1. ציון כללי מתוך 100
        2. משוב מפורט לכל בעיה/קטע
        3. תחומים שבהם התלמיד הצטיין
        4. תחומים הזקוקים לשיפור
        5. הצעות ספציפיות להבנה טובה יותר
        
        השב בפורמט JSON הבא:
        {{
            "score": <מספר בין 0-100>,
            "detailed_feedback": [
                {{"problem": "תיאור הבעיה", "score": <0-10>, "feedback": "משוב מפורט"}},
            ],
            "strengths": ["רשימת חוזקות"],
            "improvements": ["רשימת תחומים לשיפור"],
            "suggestions": ["הצעות לימוד ספציפיות"],
            "overall_comment": "הערה כללית מעודדת"
        }}
        
        היה הוגן, בונה ומעודד במשוב שלך. קח בחשבון:
        - דיוק מתמטי
        - גישה לפתרון בעיות
        - הצגת עבודה/שלבים
        - הבנה של מושגים
        - בהירות הצגה
        
        אם יש בעיות בעברית, אתה יכול להשיב גם באנגלית.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Try to parse JSON response
            try:
                # Clean the response text to extract JSON
                response_text = response.text.strip()
                if response_text.startswith('```json'):
                    response_text = response_text[7:-3].strip()
                elif response_text.startswith('```'):
                    response_text = response_text[3:-3].strip()
                
                result = json.loads(response_text)
                result["timestamp"] = datetime.datetime.now().isoformat()
                result["student_name"] = student_name
                return result
            except json.JSONDecodeError:
                # If JSON parsing fails, return structured response
                return {
                    "score": self._extract_score_from_text(response.text),
                    "raw_feedback": response.text,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "student_name": student_name,
                    "note": "Response parsed from natural language"
                }
        except Exception as e:
            return {"error": f"Error analyzing homework: {str(e)}"}
    
    def analyze_homework_with_reference_images(self, homework_content, student_name="Anonymous"):
        """Analyze homework using reference images (for handwritten reference materials)"""
        
        # Create a comprehensive prompt for handwritten reference comparison
        prompt = f"""
        אתה מורה מתמטיקה מומחה הבודק שיעורי בית בעברית.
        
        יש לך חומר ייחוס של מתמטיקה בכתב יד בעברית (תמונות).
        
        שיעורי בית של התלמיד:
        שם התלמיד: {student_name}
        תוכן: {homework_content}
        
        בהתבסס על חומר הייחוס המתמטי שתראה, אנא נתח את שיעורי הבית וספק:
        
        1. ציון כללי מתוך 100
        2. השוואה לחומר הייחוס
        3. נכונות הפתרונות
        4. איכות הסבר והצגה
        5. הבנת המושגים
        
        השב בפורמט הבא:
        ציון: [מספר]/100
        
        השוואה לחומר הייחוס:
        [כיצד התשובות משתוות לחומר הלימוד]
        
        ניתוח פתרונות:
        [ניתוח מפורט של כל פתרון]
        
        חוזקות:
        [מה התלמיד עשה טוב]
        
        שיפורים נדרשים:
        [מה צריך לשפר]
        
        המלצות:
        [המלצות ללימוד נוסף]
        
        הערה כללית:
        [הערה מעודדת ובונה]
        """
        
        try:
            # Include reference images in the analysis
            content_list = [prompt]
            
            # Add up to 3 reference images to avoid token limits
            for i, ref_image in enumerate(self.reference_images[:3]):
                content_list.append(ref_image)
            
            # Add homework content based on type
            if isinstance(homework_content, str):
                content_list.append(f"תוכן שיעורי הבית: {homework_content}")
            elif hasattr(homework_content, 'mode'):  # PIL Image
                content_list.append(homework_content)
            
            response = self.vision_model.generate_content(content_list)
            
            # Extract score from response
            score = self._extract_score_from_text(response.text)
            
            return {
                "score": score,
                "feedback": response.text,
                "timestamp": datetime.datetime.now().isoformat(),
                "student_name": student_name,
                "analysis_type": "handwritten_reference_comparison"
            }
            
        except Exception as e:
            return {"error": f"Error analyzing with reference images: {str(e)}"}
    
    def analyze_homework_image(self, image, student_name="Anonymous"):
        """Analyze homework from image"""
        if not self.reference_content:
            return {"error": "Reference material not loaded"}
        
        prompt = f"""
        אתה מורה מתמטיקה מומחה הבודק שיעורי בית בעברית מהתמונה הזו.
        
        חומר ייחוס (תוכן מתמטיקה בעברית):
        {self.reference_content[:3000]}
        
        תלמיד: {student_name}
        
        אנא נתח את שיעורי הבית המוצגים בתמונה הזו וספק:
        1. ציון כללי מתוך 100
        2. אילו בעיות/תרגילים אתה יכול לזהות
        3. הערכה של הפתרונות המוצגים
        4. משוב על דיוק מתמטי
        5. הצעות לשיפור
        
        התמקד ב:
        - נכונות הפתרונות המתמטיים
        - בהירות העבודה המוצגת
        - גישה לפתרון בעיות
        - הבנה שהודגמה
        
        ספק משוב מעודד ובונה בעברית או באנגלית.
        
        השב בפורמט הבא:
        ציון: [מספר]/100
        
        הערכה:
        [הערכה מפורטת]
        
        משוב:
        [משוב ספציפי]
        
        הצעות לשיפור:
        [הצעות קונקרטיות]
        """
        
        try:
            response = self.vision_model.generate_content([prompt, image])
            
            # Extract score from response
            score = self._extract_score_from_text(response.text)
            
            return {
                "score": score,
                "feedback": response.text,
                "timestamp": datetime.datetime.now().isoformat(),
                "student_name": student_name,
                "type": "image_analysis"
            }
        except Exception as e:
            return {"error": f"Error analyzing image: {str(e)}"}

def main():
    st.set_page_config(
        page_title="AI Homework Grading System",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("🎓 AI Homework Grading System")
    st.markdown("### Upload homework to get instant AI-powered grading and feedback")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input("Enter Gemini API Key:", type="password")
        
        if not api_key:
            st.warning("Please enter your Gemini API key to continue")
            st.stop()
        
        # Initialize grading system
        try:
            grader = HomeworkGradingSystem(api_key)
            st.success(f"✅ Connected successfully! Using model: {grader.model_name}")
        except Exception as e:
            st.error(f"❌ Failed to initialize: {str(e)}")
            
            # Show available models for debugging
            if st.button("🔍 Check Available Models"):
                try:
                    models = list(genai.list_models())
                    available_models = [model.name for model in models if 'generateContent' in model.supported_generation_methods]
                    st.write("Available models:")
                    for model in available_models:
                        st.write(f"- {model}")
                except Exception as model_error:
                    st.error(f"Error checking models: {str(model_error)}")
            st.stop()
        
        st.header("📖 Reference Material")
        reference_file = st.file_uploader(
            "Upload Hebrew Math PDF (Reference):",
            type=['pdf'],
            help="Upload the math reference material in Hebrew"
        )
        
        if reference_file:
            if grader.load_reference_material(reference_file):
                st.success("✅ Reference material loaded successfully!")
            else:
                st.error("❌ Failed to load reference material")
    
    # Main content area
    if not grader.reference_content:
        st.warning("⚠️ Please upload the reference material first")
        st.stop()
    
    # Student information
    col1, col2 = st.columns([2, 1])
    with col1:
        student_name = st.text_input("Student Name:", placeholder="Enter student name")
    with col2:
        assignment_type = st.selectbox("Assignment Type:", ["Homework", "Quiz", "Test", "Practice"])
    
    # File upload options
    st.header("📄 Upload Homework")
    upload_method = st.radio(
        "Choose upload method:",
        ["Text File", "Image", "Direct Text Input"]
    )
    
    homework_content = None
    
    if upload_method == "Text File":
        uploaded_file = st.file_uploader(
            "Choose homework file:",
            type=['pdf', 'docx', 'txt'],
            help="Upload PDF, DOCX, or TXT file"
        )
        
        if uploaded_file:
            file_type = uploaded_file.type
            if 'pdf' in file_type:
                homework_content = grader.extract_pdf_text(uploaded_file)
            elif 'word' in file_type or 'document' in file_type:
                homework_content = grader.extract_docx_text(uploaded_file)
            else:  # txt file
                homework_content = str(uploaded_file.read(), "utf-8")
    
    elif upload_method == "Image":
        uploaded_image = st.file_uploader(
            "Choose homework image:",
            type=['png', 'jpg', 'jpeg'],
            help="Upload clear image of homework"
        )
        
        if uploaded_image:
            image = grader.process_image(uploaded_image)
            if image:
                st.image(image, caption="Uploaded Homework", use_column_width=True)
                homework_content = image
    
    else:  # Direct text input
        homework_content = st.text_area(
            "Enter homework content:",
            height=300,
            placeholder="Type or paste the homework content here..."
        )
    
    # Grading button
    if st.button("🎯 Grade Homework", type="primary"):
        if not homework_content:
            st.error("Please provide homework content to grade")
        elif not student_name:
            st.error("Please enter student name")
        else:
            with st.spinner("🤖 AI is grading the homework..."):
                # Analyze based on content type
                if upload_method == "Image":
                    result = grader.analyze_homework_image(homework_content, student_name)
                else:
                    result = grader.analyze_homework_text(homework_content, student_name)
                
                # Display results
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    # Score display
                    score = result.get('score', 0)
                    col1, col2, col3 = st.columns([1, 2, 1])
                    
                    with col2:
                        st.metric(
                            label="📊 Final Score",
                            value=f"{score}/100",
                            delta=f"{score-75} from average" if score != 75 else None
                        )
                        
                        # Score color coding
                        if score >= 90:
                            st.success("🌟 Excellent work!")
                        elif score >= 80:
                            st.success("👍 Good job!")
                        elif score >= 70:
                            st.warning("📈 Room for improvement")
                        else:
                            st.error("📚 Needs more practice")
                    
                    # Detailed feedback
                    if 'detailed_feedback' in result:
                        st.header("📝 Detailed Feedback")
                        for feedback in result['detailed_feedback']:
                            with st.expander(f"Problem: {feedback['problem']}"):
                                st.write(f"**Score:** {feedback['score']}/10")
                                st.write(f"**Feedback:** {feedback['feedback']}")
                    
                    # Strengths and improvements
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if 'strengths' in result and result['strengths']:
                            st.success("💪 Strengths")
                            for strength in result['strengths']:
                                st.write(f"• {strength}")
                    
                    with col2:
                        if 'improvements' in result and result['improvements']:
                            st.warning("🎯 Areas to Improve")
                            for improvement in result['improvements']:
                                st.write(f"• {improvement}")
                    
                    # Suggestions
                    if 'suggestions' in result and result['suggestions']:
                        st.info("💡 Learning Suggestions")
                        for suggestion in result['suggestions']:
                            st.write(f"• {suggestion}")
                    
                    # Overall comment
                    if 'overall_comment' in result:
                        st.success("🎉 Teacher's Comment")
                        st.write(result['overall_comment'])
                    
                    # Raw feedback for images or parsing errors
                    if 'raw_feedback' in result:
                        with st.expander("📋 Full AI Response"):
                            st.write(result['raw_feedback'])
                    
                    # Save results option
                    st.header("💾 Save Results")
                    if st.button("Download Grade Report"):
                        report = f"""
HOMEWORK GRADE REPORT
====================
Student: {student_name}
Assignment: {assignment_type}
Date: {result.get('timestamp', 'N/A')}
Score: {score}/100

{result.get('raw_feedback', 'Detailed feedback available above')}
                        """
                        st.download_button(
                            label="📥 Download Report",
                            data=report,
                            file_name=f"{student_name}_grade_report.txt",
                            mime="text/plain"
                        )

if __name__ == "__main__":
    main()
