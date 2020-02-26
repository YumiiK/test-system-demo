from flask import Flask, json, request, session, render_template, redirect, flash, jsonify, make_response
#from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey

app = Flask(__name__)
app.secret_key = "SECRET"

#debug = DebugToolbarExtension(app)

trial = Survey( "Trial",
    "In this section, we have prepared several questions to familiarize you with them. After you choose the "
    "answer, the correct answer will appear.",
    []
    )


train_files= ["02_T2_M_100","03_T2_L_1k","04_T2_H_300"]

with open('task2.json',mode='r') as f:
    data = json.load(f)
    all_t2 = data["T2"]
    for i in train_files:
        for j in range(len(all_t2)):
            if all_t2[j]["index"]==i:
                print(all_t2[j]["index"])
                img_filename= "/static/img/"+ i + ".png"
                ques = Question(all_t2[j]["question"],[all_t2[j]["A"],all_t2[j]["B"],all_t2[j]["C"]],all_t2[j]["Answer"],img_filename)
                trial.questions.append(ques)
                continue




test = Survey(
    "Test",
    "In this section, you have 45 questions to answer. After every 15 questions, you can take a rest, then continue. "
    "Begin the formal test now!",
    []
)



surveys = {
    "trial": trial,
    "test": test,
}

# def return_img_stream(img_local_path):
#   """
#   工具函数:
#   获取本地图片流
#   :param img_local_path:文件单张图片的本地绝对路径
#   :return: 图片流
#   """
#   import base64
#   img_stream = ''
#   with open(img_local_path, 'r') as img_f:
#     img_stream = img_f.read()
    
#     img_stream = base64.b64encode(img_stream)
#   return img_stream


@app.route('/')
def home():
    surveys_taken = json.loads(request.cookies.get("surveys_taken", '{}'))
    current_user_surveys = surveys.copy()
    for survey in surveys_taken:
        current_user_surveys.pop(survey, None)
    return render_template('home.html', surveys=current_user_surveys)


@app.route('/start-survey/<string:survey_picked>', methods=["POST", "GET"])
def start_survey(survey_picked=None):
    # store survey picked in session
    # survey_picked = request.form.get("survey")
    # survey_picked = "trial"
    session['survey_name'] = survey_picked
    session[survey_picked] = [()]*len(surveys[survey_picked].questions)
    return render_template('start-survey.html', name=survey_picked, title=surveys[survey_picked].title, instructions=surveys[survey_picked].instructions)


@app.route('/trial/<int:question_num>', methods=["POST","GET"])
def trial(question_num):
    survey_picked = session['survey_name']
    if question_num != 0:
        selection = request.form.get("selection")
        comments = request.form.get("comments", "N/A")
        answer = (selection, comments)
        print(answer)
        answers = session[survey_picked]
        answers[question_num-1] = answer
        session[survey_picked] = answers
    if question_num >= len(surveys[survey_picked].questions):
        for i in range(len(surveys[survey_picked].questions)):
            question = surveys[survey_picked].questions[i].question
            answer = session[survey_picked][i][0]
            comment = session[survey_picked][i][1]
            # TURN INTO DICT FIRST
            flash(question, 'question')
            flash(answer, 'answer')
            flash(comment, 'comment')
        return redirect('/start-survey/test')
    


    return render_template('trial.html', next_id=question_num + 1, question=surveys[survey_picked].questions[question_num].question, choices=surveys[survey_picked].questions[question_num].choices,scatterimg = surveys[survey_picked].questions[question_num].image,  textbox=surveys[survey_picked].questions[question_num].allow_text)


@app.route('/test/<int:question_num>', methods=["POST"])
def question(question_num):
    survey_picked = session['survey_name']
    if question_num != 0:
        selection = request.form.get("selection")
        comments = request.form.get("comments", "N/A")
        answer = (selection, comments)
        print(answer)
        answers = session[survey_picked]
        answers[question_num-1] = answer
        session[survey_picked] = answers
    if question_num >= len(surveys[survey_picked].questions):
        for i in range(len(surveys[survey_picked].questions)):
            question = surveys[survey_picked].questions[i].question
            answer = session[survey_picked][i][0]
            comment = session[survey_picked][i][1]
            # TURN INTO DICT FIRST
            flash(question, 'question')
            flash(answer, 'answer')
            flash(comment, 'comment')
        return redirect('/thanks')

    return render_template('question.html', next_id=question_num + 1, question=surveys[survey_picked].questions[question_num].question, choices=surveys[survey_picked].questions[question_num].choices, textbox=surveys[survey_picked].questions[question_num].allow_text)


@app.route('/thanks')
def thanks():

    # Setting cookie that user has taken survey
    survey_picked = session['survey_name']
    surveys_taken = json.loads(request.cookies.get("surveys_taken", '{}'))
    surveys_taken[survey_picked] = 0
    html = render_template('thanks.html')
    resp = make_response(html)
    resp.set_cookie('surveys_taken', json.dumps(surveys_taken))

    return resp
