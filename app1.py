from flask import Flask, json, request, session, render_template, redirect, flash, jsonify, make_response
from surveys import Question, Survey, satisfaction_survey, surveys

import json


app = Flask(__name__)


@app.route('/trial')
def train_get_task_img():
    train_files= ["02_T2_M_100","03_T2_L_1k","04_T2_H_300"]
    trail_que=[]
    trail_A=[]
    trail_B=[]
    trail_C=[]
    trail_ans=[]
    trail_img_urls = []
    for k in range(len(train_files)):
        trail_img_urls.append("img/"+train_files[k]+".png")

    trail_img_urls.append("img/"+train_files)
    with open('task2.json',mode='r') as f:
        data = json.load(f)
        all_t2 = data["T2"]
        for i in range(len(train_files)):
            for j in range(len(all_t2)):
                if all_t2[j]["index"]==train_files[i]:
                    trail_que.append(all_t2[j]["question"])
                    trail_A.append(all_t2[j]["A"])
                    trail_B.append(all_t2[j]["B"])
                    trail_C.append(all_t2[j]["C"])
                    trail_ans.append(all_t2[j]["Answer"])
    
    
    #将选中的训练题目及对应散点图传到trail.html,其中题干、选项A、选项B、选项C、答案、图片url分别存入数组
    return render_template('trail.html', Question = trail_que, OptionA = trail_A, OptionB = trail_B, OptionB = trail_C,Answer = trail_ans,ImageUrl = trail_img_urls)







if __name__ == "__main__":
    app1.run(debug=True)