from flask import Flask, json, request, session, render_template, redirect, flash, jsonify, make_response
#from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey
import random

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
    # all_t3 = data["T3"]
    # all_t1 = data["T1"]
    for i in train_files:
        for j in range(len(all_t2)):
            if all_t2[j]["index"]==i:
                print(all_t2[j]["index"])
                img_filename= "/static/img/"+ i + ".png"
                ques = Question(all_t2[j]["question"],[all_t2[j]["A"],all_t2[j]["B"],all_t2[j]["C"]],all_t2[j]["Answer"],img_filename)
                trial.questions.append(ques)
                continue





test= Survey(
    "Test",
    "In this section, you have 45 questions to answer. After every 15 questions, you can take a rest, then continue. "
    "Begin the formal test now!",
    []
)

ch_que1 = []
ch_que2 = []
ch_que3 = []
ch_que4 = []
ch_que5 = []
ch_que6 = []
ch_que7 = []
ch_que8 = []
ch_que9 = []

ch_all = []

ch_all.append(ch_que1)
ch_all.append(ch_que2)
ch_all.append(ch_que3)
ch_all.append(ch_que4)
ch_all.append(ch_que5)
ch_all.append(ch_que6)
ch_all.append(ch_que7)
ch_all.append(ch_que8)
ch_all.append(ch_que9)

dataset_num = ["02","03","04","05","06","16","17","20","23","24","25","26","28","29","30"]
pick_num = [0,1,2,3,4,5,6,7,8]


def re_init():
    print("####")
    for n in dataset_num:
        random.shuffle(pick_num)
        for i in range(len(all_t2)):
            test_img_filename = "/static/img/"+ all_t2[i]["index"] + ".png"
            ch = Question(all_t2[i]["question"],[all_t2[i]["A"],all_t2[i]["B"],all_t2[i]["C"]],all_t2[i]["Answer"],test_img_filename)
            if all_t2[i]["index"][0:2]==n and all_t2[i]["index"][6:7]=="M"and all_t2[i]["index"][8:10]=="1k":
                ch_all[pick_num[0]].append(ch)
            if all_t2[i]["index"][0:2]==n and all_t2[i]["index"][6:7]=="L"and all_t2[i]["index"][8:10]=="10":
                ch_all[pick_num[1]].append(ch)
            if all_t2[i]["index"][0:2]==n and all_t2[i]["index"][6:7]=="H"and all_t2[i]["index"][8:10]=="30":
                ch_all[pick_num[2]].append(ch)
            if all_t2[i]["index"][0:2]==n and all_t2[i]["index"][6:7]=="L"and all_t2[i]["index"][8:10]=="30":
                ch_all[pick_num[3]].append(ch)
            if all_t2[i]["index"][0:2]==n and all_t2[i]["index"][6:7]=="H"and all_t2[i]["index"][8:10]=="1k":
                ch_all[pick_num[4]].append(ch)
            if all_t2[i]["index"][0:2]==n and all_t2[i]["index"][6:7]=="M"and all_t2[i]["index"][8:10]=="10":
                ch_all[pick_num[5]].append(ch)
            if all_t2[i]["index"][0:2]==n and all_t2[i]["index"][6:7]=="H"and all_t2[i]["index"][8:10]=="10":
                ch_all[pick_num[6]].append(ch)
            if all_t2[i]["index"][0:2]==n and all_t2[i]["index"][6:7]=="M"and all_t2[i]["index"][8:10]=="30":
                ch_all[pick_num[7]].append(ch)
            if all_t2[i]["index"][0:2]==n and all_t2[i]["index"][6:7]=="L"and all_t2[i]["index"][8:10]=="1k":
                ch_all[pick_num[8]].append(ch) 
    for r in range(len(ch_all)):
        random.shuffle(ch_all[r])
        
        
        
        
        
        #### 加 T1 和 T3

    
       



surveys = {
    "trial": trial,
    "test": test
}



set1 = 0
set2 = 0

def assign_test(user_num):
    test.questions = ch_all[user_num]






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
    print("&&&&&&&&&&&&&&&&&&&&&")
    if question_num != 0:
        selection = request.form.get("selection")
        comments = request.form.get("comments", "N/A")
        answer = (selection, comments)
        print(answer)
        answers = session[survey_picked]
        answers[question_num-1] = answer
        session[survey_picked] = answers
    if question_num >= len(surveys[survey_picked].questions):
        # for i in range(len(surveys[survey_picked].questions)):
        #     question = surveys[survey_picked].questions[i].question
        #     answer = session[survey_picked][i][0]
        #     comment = session[survey_picked][i][1]
        #     # TURN INTO DICT FIRST
        #     flash(question, 'question')
        #     flash(answer, 'answer')
        #     flash(comment, 'comment')
        return redirect('/start-survey/test')
    


    return render_template('trial.html', next_id=question_num + 1, question=surveys[survey_picked].questions[question_num].question, choices=surveys[survey_picked].questions[question_num].choices,answer = surveys[survey_picked].questions[question_num].answer, scatterimg = surveys[survey_picked].questions[question_num].image,  textbox=surveys[survey_picked].questions[question_num].allow_text)


@app.route('/test/<int:question_num_>', methods=["POST"])
def question(question_num_):
    global set1
    global set2
    if set1==0:
        re_init()
    assign_test(set1)
    set2 = set2 + 1
    if set2==16:
        set2=0
        set1 = set1 + 1
    if  set1 == 9:
        set1 = 0
    

    survey_picked = session['survey_name']
    if question_num_ != 0 and set2 !=0:
        selection = request.form.get("selection")
        comments = request.form.get("comments", "N/A")
        answer = (selection, comments)
        print(answer)
        # print("$$$$")
        # print(question_num-1)
        answers = session[survey_picked]
        
        answers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        # print(answers)
        answers[question_num_-1] = answer
        session[survey_picked] = answers
    if question_num_ >= len(surveys[survey_picked].questions) or set2 == 0:
        # for i in range(len(surveys[survey_picked].questions)):
        #     question = surveys[survey_picked].questions[i].question
        #     answer = session[survey_picked][i][0]
        #     comment = session[survey_picked][i][1]
        #     # TURN INTO DICT FIRST
        #     flash(question, 'question')
        #     flash(answer, 'answer')
        #     flash(comment, 'comment')
        return redirect('/thanks')

    return render_template('question.html', next_id=question_num_ + 1, question=surveys[survey_picked].questions[question_num_].question, choices=surveys[survey_picked].questions[question_num_].choices,answer = surveys[survey_picked].questions[question_num_].answer, scatterimg = surveys[survey_picked].questions[question_num_].image,  textbox=surveys[survey_picked].questions[question_num_].allow_text)


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
