from flask import Flask, request, jsonify
from module import analyze_resume, extract_text_from_file
import tempfile
import os
import spacy

try:
    nlp = spacy.load("en_core_web_md")
except:
    import spacy.cli
    spacy.cli.download("en_core_web_md")
    nlp = spacy.load("en_core_web_md")


app = Flask(__name__)

@app.route('/analyze-resume', methods=['POST'])
def analyze_resume_endpoint():
    try:
        resume_file = request.files['resume']
        job_description = request.form['job_description']
        job_role = request.form['job_role']

        _, ext = os.path.splitext(resume_file.filename)
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as temp:
            resume_file.save(temp.name)
            resume_content = extract_text_from_file(temp.name, ext)
            os.unlink(temp.name)

        report, df = analyze_resume(resume_content, job_description, job_role)
        return jsonify({
            "success": True,
            "report": report,
            "scores": df.to_dict('records')
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return "Resume Scoring API is Live!"

if __name__ == '__main__':
    app.run()
