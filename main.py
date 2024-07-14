from flask import Flask, render_template, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from utils import *
import re
import obfuscation_detection as od

vba_codes = []
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Analyze File")

@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        #return "File Has been uploaded"
        return redirect(url_for('analyze', filename=filename))
    return render_template('index.html', form=form)

@app.route('/analyze')
def analyze():
    try:
        filename = request.args.get('filename', None)
        global vba_codes
        vba_codes=get_vbaCode(filename)
        if len(vba_codes)==0:
            return render_template('error.html', filename=filename)
        return render_template('analyze.html', filename=filename)
    except Exception as e:
        return render_template('error.html', message="An error occurred: " + str(e))

@app.route('/analyze/flow')
def flow():
    filename = request.args.get('filename', None)
    filename = request.args.get('filename', None)
    prompt1 = """Analyze the provided VBA macro code to outline its data flow. Describe the sequence of operations executed by the macro, including how data is manipulated or processed at each step. 
    Give it in concise paragraphs and not as points"""

    prompt2 ="""Analyze the provided VBA macro code to outline its process flow. Describe the sequence of operations executed by the macro, including how data is manipulated or processed at each step.
    Give it in concise paragraphs and not as points"""
    recommendations_dataFlow= []
    recommendations_processFlow= []
    for vbc in vba_codes:
        points_list = re.split(r'\n', generate_content(vbc, prompt1))
        points = [point.strip() for point in points_list if point.strip()]
        recommendations_dataFlow.append(points)

        points_list = re.split(r'\n', generate_content(vbc, prompt2))
        points = [point.strip() for point in points_list if point.strip()]
        recommendations_processFlow.append(points)
    print(recommendations_dataFlow)
    print(recommendations_processFlow)
    return render_template('content.html', filename=filename, dataFlow=recommendations_dataFlow, processFlow=recommendations_processFlow)
    #return render_template('analyze.html', filename=filename)


@app.route('/analyze/dataflowDiagram')
def dataflowDiagram():
    filename = request.args.get('filename', None)
    prompt = """Analyze the following Excel VBA macros code and generate a data flow diagram.
                The each point content generated should be very small and concise with no subpoints"""

    for vbc in vba_codes:
        diagram = generate_content(vbc, prompt)
        drawDiagram(diagram)

    return render_template('content.html', filename=filename, processDiagram = True)
    #return render_template('analyze.html', filename=filename)

@app.route('/analyze/processflowDiagram')
def processflowDiagram():
    filename = request.args.get('filename', None)
    prompt = """Analyze the following Excel VBA macros code and generate a process flow diagram.
                The each point content generated should be very small and concise with no subpoints"""

    for vbc in vba_codes:
        diagram = generate_content(vbc, prompt)
        drawDiagram(diagram)

    return render_template('content.html', filename=filename, processDiagram = True)
    #return render_template('analyze.html', filename=filename)

@app.route('/analyze/logic')
def logic():
    filename = request.args.get('filename', None)
    prompt = "Analyze the following VBA code from an Excel macro and generate a concise explanation of its logic in a single paragraph without bullet points"
    recommendations= []
    for vbc in vba_codes:
        recommendations.append(generate_content(vbc, prompt))
    print(recommendations)
    return render_template('content.html', filename=filename, logic=recommendations)
    return render_template('analyze.html', filename=filename)

@app.route('/analyze/listmacro')
def listmacro():
    
    filename = request.args.get('filename', None)    
    print(vba_codes)
    return render_template('content.html', filename=filename, vbaCodes=vba_codes)

@app.route('/analyze/efficiency')
def efficiency():
    filename = request.args.get('filename', None)
    prompt = """Analyze the structure and performance of the given VBA macro.
                Provide insights on its quality and efficiency, potential inefficiencies, redundant code, optimization opportunities.
                Give it in concise paragraphs and not as points"""
    recommendations= []
    for vbc in vba_codes:
        recommendations.append(generate_content(vbc, prompt))
    print(recommendations)
    return render_template('content.html', filename=filename, efficiencyData=recommendations)

@app.route('/analyze/errordetection')
def errordetection():
    filename = request.args.get('filename', None)
    prompt = """Analyze the following VBA code from an Excel macro and generate a concise explanation of the errors present in the macro code.
    Give it in concise paragraphs and not as points"""
    recommendations= []
    for vbc in vba_codes:
        points_list = re.split(r'\n', generate_content(vbc, prompt))
        points = [point.strip() for point in points_list if point.strip()]
        recommendations.append(points)
    print(recommendations)
    return render_template('content.html', filename=filename, errors=recommendations)

@app.route('/analyze/conversion')
def conversion():
    filename = request.args.get('filename', None)
    target_language = 'Python'
    prompt = "Rewrite the provided VBA macro in {target_language} while preserving its functionality and logic.Recommend suitable constructs, syntax adaptations, and best practices for the chosen language."
    recommendations= []
    for vbc in vba_codes:
        text = generate_content(vbc, prompt)
        code = code = "\n".join(re.findall(r'```(.*?)```', text, re.DOTALL))
        recommendations.append(code)
    print(code)
    return render_template('content.html', filename=filename, conversionData=recommendations)

@app.route('/analyze/security')
def security():
    filename = request.args.get('filename', None) 
    vba_suspicious_keywords = []
    vba_suspicious_patterns = []
    oc = od.ObfuscationClassifier(od.PlatformType.ALL)
    classifications = oc(vba_codes)
    print(classifications)
    for vbc in vba_codes:
        susKey = get_suspicious_keywords(vbc)
        if len(susKey)==0:
            vba_suspicious_keywords.append(['No suspecious Key words found in the macro'])
        else:
            vba_suspicious_keywords.append(susKey)

        susPattern = get_suspicious_patterns(vbc)
        if len(susPattern)==0:
            vba_suspicious_patterns.append(['No suspecious Key words found in the macro'])
        else:
            vba_suspicious_patterns.append(susPattern)
    print(vba_suspicious_keywords)
    print(vba_suspicious_patterns)

    return render_template('content.html', filename=filename, suspiciousKeywords=vba_suspicious_keywords, suspiciousPatterns=vba_suspicious_patterns)

@app.route('/analyze/NLPexplain')
def nlp():
    filename = request.args.get('filename', None)
    prompt = "Convert the following VBA code into a natural language explanation in a layman view in concise paragrphs"
    recommendations= []
    for vbc in vba_codes:
        recommendations.append(generate_content(vbc, prompt))
    print(recommendations)
    return render_template('content.html', filename=filename, nlpContent=recommendations)

if __name__== "__main__":
    app.run(debug=True)