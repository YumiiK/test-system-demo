import os
import pickle
import zipfile

from flask import Flask, json, request, session, render_template, redirect, flash, jsonify, make_response, g, \
    send_from_directory
# from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, ResultList
import random

app = Flask(__name__)
app.secret_key = "SECRET"

# debug = DebugToolbarExtension(app)

trial = Survey("Training",
               "In the training section, you will have 9 questions to answer. Each question will be presented "
               "together with a chart. You must choose the best answer from the three choices marked A), B) and C) by "
               "clicking the choice. After you make the choice, the right answer will be highlighted in green with a "
               "check mark next to it. If you choose the wrong answer, it will be highlighted in red with a cross "
               "next to it. Then you need to click NEXT button to move on to the next question. Through this part you "
               "can get familiar with the tasks. If you are not confident enough, you can repeat the training part by "
               "clicking RETRY button.",
               []
               )

train_files = ["02_T2_M_100", "03_T2_L_1k", "04_T2_H_300"]  # 不能和test重复  用额外数据集

with open('task2.json', mode='r') as f:
    data = json.load(f)
    all_t2 = data["T2"]
    # all_t3 = data["T3"]
    # all_t1 = data["T1"]
    for i in train_files:
        for j in range(len(all_t2)):
            if all_t2[j]["index"] == i:
                print(all_t2[j]["index"])
                img_filename = "/static/img/" + i + ".png"
                ques = Question(all_t2[j]["index"], all_t2[j]["question"],
                                [all_t2[j]["A"], all_t2[j]["B"], all_t2[j]["C"]],
                                all_t2[j]["Answer"], img_filename)
                trial.questions.append(ques)
                continue
ch_que1 = []
ch_que2 = []
ch_que3 = []
ch_que4 = []
ch_que5 = []
ch_que6 = []
ch_que7 = []
ch_que8 = []
ch_que9 = []
ch_all = [ch_que1, ch_que2, ch_que3, ch_que4, ch_que5, ch_que6, ch_que7, ch_que8, ch_que9]

test = Survey(
    "Test",
    "In this section, you have 45 questions to answer. After every 15 questions, you can take a rest, then continue. "
    "Begin the formal test now!",
    []
)

dataset_num = ["02", "03", "04", "05", "06", "16", "17", "20", "23", "24", "25", "26", "28", "29", "30"]
pick_num = [0, 1, 2, 3, 4, 5, 6, 7, 8]


def re_init():
    for r in range(len(ch_all)):
        ch_all[r] = []

    for n in dataset_num:
        random.shuffle(pick_num)
        for i in range(len(all_t2)):
            test_img_filename = "/static/img/" + all_t2[i]["index"] + ".png"
            ch = Question(all_t2[i]["index"], all_t2[i]["question"], [all_t2[i]["A"], all_t2[i]["B"], all_t2[i]["C"]],
                          all_t2[i]["Answer"],
                          test_img_filename)
            if all_t2[i]["index"][0:2] == n and all_t2[i]["index"][6:7] == "M" and all_t2[i]["index"][8:10] == "1k":
                ch_all[pick_num[0]].append(ch)
            if all_t2[i]["index"][0:2] == n and all_t2[i]["index"][6:7] == "L" and all_t2[i]["index"][8:10] == "10":
                ch_all[pick_num[1]].append(ch)
            if all_t2[i]["index"][0:2] == n and all_t2[i]["index"][6:7] == "H" and all_t2[i]["index"][8:10] == "30":
                ch_all[pick_num[2]].append(ch)
            if all_t2[i]["index"][0:2] == n and all_t2[i]["index"][6:7] == "L" and all_t2[i]["index"][8:10] == "30":
                ch_all[pick_num[3]].append(ch)
            if all_t2[i]["index"][0:2] == n and all_t2[i]["index"][6:7] == "H" and all_t2[i]["index"][8:10] == "1k":
                ch_all[pick_num[4]].append(ch)
            if all_t2[i]["index"][0:2] == n and all_t2[i]["index"][6:7] == "M" and all_t2[i]["index"][8:10] == "10":
                ch_all[pick_num[5]].append(ch)
            if all_t2[i]["index"][0:2] == n and all_t2[i]["index"][6:7] == "H" and all_t2[i]["index"][8:10] == "10":
                ch_all[pick_num[6]].append(ch)
            if all_t2[i]["index"][0:2] == n and all_t2[i]["index"][6:7] == "M" and all_t2[i]["index"][8:10] == "30":
                ch_all[pick_num[7]].append(ch)
            if all_t2[i]["index"][0:2] == n and all_t2[i]["index"][6:7] == "L" and all_t2[i]["index"][8:10] == "1k":
                ch_all[pick_num[8]].append(ch)
    for r in range(len(ch_all)):
        random.shuffle(ch_all[r])

        #### 加 T1 和 T3


surveys = {
    "trial": trial,
    "test": test
}

Test_No = 0

@app.route('/')
def home():
    global Test_No 
    tester_no = Test_No 
    Test_No = Test_No + 1
    surveys_taken = json.loads(request.cookies.get("surveys_taken", '{}'))
    current_user_surveys = surveys.copy()
    for survey in surveys_taken:
        current_user_surveys.pop(survey, None)
    return render_template('home.html', testNO = tester_no,surveys=current_user_surveys)





@app.route('/start-survey/<string:survey_picked>/<int:tester_no>', methods=["POST", "GET"])
def start_survey(tester_no, survey_picked=None):
    # store survey picked in session
    session['survey_name'] = survey_picked

    session[survey_picked] = [()] * 45

    if survey_picked=="trial":
        tester_age = request.form.get("age")
        tester_sex = request.form.get("sex")
        tester_edu = request.form.get("education")
        tester_exp1_1 = request.form.get("visual-exp-month")
        tester_exp1_2 = request.form.get("visual-exp-year")
        tester_exp2_1 = request.form.get("data-ana-exp-month")
        tester_exp2_2 = request.form.get("data-ana-exp-year")

        tester_expa = int(tester_exp1_2)+int(tester_exp1_1)/12.0
        tester_expb = int(tester_exp2_2)+int(tester_exp2_1)/12.0
        
        tester_exp1 = str(tester_expa)
        tester_exp2 = str(tester_expb)

    
        result_file = open('result/result_%s.json' % tester_no, 'w+', encoding="utf-8")
        result_file.write("{\n\"No.\":\"%s\"," % tester_no)
        result_file.write("\"Age\":\"%s\",\n\"Sex\":\"%s\",\n\"Education\":\"%s\",\n\"Vis-Exp\":\"%s\",\n\"Data-Exp\":\"%s\","
                          %(tester_age,tester_sex,tester_edu,tester_exp1,tester_exp2))
        result_file.close()
        

    return render_template('start-survey.html', name=survey_picked, tester=tester_no,
                           title=surveys[survey_picked].title,
                           instructions=surveys[survey_picked].instructions)


@app.route('/trial/<int:tester_no>/<int:question_num>', methods=["POST", "GET"])
def trial(tester_no,question_num):
    survey_picked = session['survey_name']
    survey_picked = 'trial'  # 强改呃呃呃 防止并行时另一个用户已经进入test，导致本用户无法进入trial
    if question_num != 0:
        selection = request.form.get("radio")
        comments = request.form.get("comments", "N/A")
        answer = (selection, comments)
        print(answer)
        answers = session[survey_picked]
        answers[question_num - 1] = answer
        session[survey_picked] = answers
    if question_num >= len(surveys[survey_picked].questions):
        # print(survey_picked)
        # print(len(surveys[survey_picked].questions))
        for i in range(len(surveys[survey_picked].questions)):
            question = surveys[survey_picked].questions[i].question
            answer = session[survey_picked][i][0]
            comment = session[survey_picked][i][1]
            # TURN INTO DICT FIRST
            flash(question, 'question')
            flash(answer, 'answer')
            flash(comment, 'comment')
        test_tester_no = str(tester_no)
        return redirect('/start-survey/test/%s'%test_tester_no)

    return render_template('trial.html', next_id=question_num + 1,tester = tester_no,
                           question=surveys[survey_picked].questions[question_num].question,
                           choices=surveys[survey_picked].questions[question_num].choices,
                           answer=surveys[survey_picked].questions[question_num].answer,
                           scatterimg=surveys[survey_picked].questions[question_num].image,
                           textbox=surveys[survey_picked].questions[question_num].allow_text)


set1 = 1
set2 = 0


@app.route('/test/<int:tester_No>/<int:test_num>/<int:question_num_>', methods=["POST"])
def question(tester_No, test_num, question_num_):
    global set1  # 控制9套题的初始化

    if set1 == 1:
        re_init()
        set1 = 0
    if question_num_ == 0 and test_num == 0:
        print("again!!!!!")

        a_questions = []
        a_questions = []
        a_questions = []
        # for xx in range(0,15):
        #     own_questions.append(single_ques)
        a_questions = ch_all[(tester_No % 3) * 3]
        b_questions = ch_all[(tester_No % 3) * 3 + 1]
        c_questions = ch_all[(tester_No % 3) * 3 + 2]
        a_questions = pickle.dumps(a_questions)
        b_questions = pickle.dumps(b_questions)
        c_questions = pickle.dumps(c_questions)
        with open("store/TT_%s_%s" % (tester_No, "0"), "ab") as fw:
            fw.write(a_questions)
        with open("store/TT_%s_%s" % (tester_No, "1"), "ab") as fw:
            fw.write(b_questions)
        with open("store/TT_%s_%s" % (tester_No, "2"), "ab") as fw:
            fw.write(c_questions)

    if tester_No % 3 == 2 and test_num == 0 and question_num_ == 0:
        set1 = 1

    global Test_No

    fr = open("store/TT_%s_%s" % (tester_No, test_num), "rb")
    while 1:
        try:
            obj = pickle.load(fr)
        except:
            break
    fr.close()
    own_questions = obj

    if test_num == 0 and question_num_ == 0:
        result_file = open('result/result_%s.json' % tester_No, 'a+', encoding="utf-8")
        result_file.write("\n\"QA\":[")
        result_file.close()

    survey_picked = session['survey_name']
    if question_num_ != 0:
        selection = request.form.get("radio")
        comments = request.form.get("comments", "N/A")
        time_interval = request.form.get("timer")
        print("The interval is :")
        print(time_interval)

        browser_size = request.form.get("browser")


        answer = (selection, comments)
        print(answer)
        answers = session[survey_picked]
        answers[question_num_ - 1] = answer
        session[survey_picked] = answers
        if selection[0:1] == 'A':
            trans_answer = "1"
        if selection[0:1] == 'B':
            trans_answer = "2"
        if selection[0:1] == 'C':
            trans_answer = "3"
        if_right = "n"
        if trans_answer == own_questions[question_num_ - 1].answer:
            if_right = "y"
        if question_num_ <= 14 or test_num < 2:
            # this_result.set_no.append(test_num + 1)
            # this_result.t_no.append(question_num_)
            # this_result.ans_time.append(time_interval)
            # this_result.c_a.append(test.questions[question_num_ - 1].answer)
            # this_result.p_a.append(trans_answer)
            # this_result.t_index.append(test.questions[question_num_ - 1].qindex)
            # this_result.ifright.append(if_right)
            print("***********************************")
            result_file = open('result/result_%s.json' % tester_No, 'a+', encoding="utf-8")
            result_file.write(
                "{\"Set_No\":\"%s\",\"T_No\":\"%s\",\"time\":\"%s\",\"index\":\"%s\",\"CorrectA\":\"%s\",\"PersonA\":\"%s\",\"correctness\":\"%s\"},\n" % (
                    test_num + 1, question_num_, time_interval, own_questions[question_num_ - 1].qindex,
                    own_questions[question_num_ - 1].answer, trans_answer, if_right))
            result_file.close()

        if question_num_ == 15 and test_num == 2:
            # this_result.set_no.append(test_num + 1)
            # this_result.t_no.append(question_num_)
            # this_result.ans_time.append(time_interval)
            # this_result.c_a.append(test.questions[question_num_ - 1].answer)
            # this_result.p_a.append(trans_answer)
            # this_result.t_index.append(test.questions[question_num_ - 1].qindex)
            # this_result.ifright.append(if_right)

            result_file = open('result/result_%s.json' % tester_No, 'a+', encoding="utf-8")
            result_file.write(
                "{\"Set_No\":\"%s\",\"T_No\":\"%s\",\"time\":\"%s\",\"index\":\"%s\",\"CorrectA\":\"%s\",\"PersonA\":\"%s\",\"correctness\":\"%s\"}],\n\"browser\":\"%s\"}" % (
                    test_num + 1, question_num_, time_interval, own_questions[question_num_ - 1].qindex,
                    own_questions[question_num_ - 1].answer, trans_answer, if_right,browser_size))
            result_file.close()

            # result_file = open('result/result_%s.json' % tester_No, 'a+', encoding="utf-8")
            # for cc in range(44):
            #     result_file.write(
            #     "{\"Set_No\":\"%s\",\"T_No\":\"%s\",\"time\":\"%s\",\"index\":\"%s\",\"CorrectA\":\"%s\",\"PersonA\":\"%s\",\"correctness\":\"%s\"},\n" % (
            #         this_result.set_no[cc], this_result.t_no[cc], this_result.ans_time[cc], this_result.t_index[cc],
            #         this_result.c_a[cc], this_result.p_a[cc], this_result.ifright[cc]))
            # result_file.write(
            #     "{\"Set_No\":\"%s\",\"T_No\":\"%s\",\"time\":\"%s\",\"index\":\"%s\",\"CorrectA\":\"%s\",\"PersonA\":\"%s\",\"correctness\":\"%s\"}]}" % (
            #         this_result.set_no[44], this_result.t_no[44], this_result.ans_time[44], this_result.t_index[44],
            #         this_result.c_a[44], this_result.p_a[44], this_result.ifright[44]))
            # result_file.close()

    if question_num_ >= len(own_questions):
        # for i in range(len(surveys[survey_picked].questions)):
        #     question = surveys[survey_picked].questions[i].question
        #     answer = session[survey_picked][i][0]
        #     comment = session[survey_picked][i][1]
        #     # TURN INTO DICT FIRST
        #     flash(question, 'question')
        #     flash(answer, 'answer')
        #     flash(comment, 'comment')

        if test_num >= 2:
            return redirect('/thanks')
        else:
            return render_template('break.html', test_id=test_num + 1, tester=tester_No)

    return render_template('question.html', tester=tester_No, next_id=question_num_ + 1, test_id=test_num,
                           question=own_questions[question_num_].question,
                           choices=own_questions[question_num_].choices,
                           answer=own_questions[question_num_].answer,
                           scatterimg=own_questions[question_num_].image,
                           textbox=own_questions[question_num_].allow_text)


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


@app.route("/download")
def index():
    result = []
    directory = os.getcwd()  # 假设在当前目录
    for parent, dirnames, filenames in os.walk(directory + '/result'):
        for filename in filenames:
            if filename.endswith(".json") and filename != 'task2.json':
                result.append(filename)
    return render_template('download.html', filenames=result)


@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.getcwd()  # 假设在当前目录
    return send_from_directory(directory + '/result', filename, as_attachment=True)


@app.route("/download-all")
def download_all():
    z = zipfile.ZipFile('zip/result.zip', 'w')
    directory = os.getcwd()  # 假设在当前目录
    for parent, dirnames, filenames in os.walk(directory + '/result'):
        for filename in filenames:
            # if filename.endswith(".json") and filename != 'task2.json':
            z.write(filename)
    z.close()
    return send_from_directory(directory + '/zip', 'result.zip', as_attachment=True)


@app.route("/download/delete-all")
def delete_all():
    directory = os.getcwd()  # 假设在当前目录
    for parent, dirnames, filenames in os.walk(directory + '/result'):
        for filename in filenames:
            os.remove(directory + '/result/' + filename)
    return render_template('download.html')


if __name__ == "__main__":
    app.run(debug=True)
