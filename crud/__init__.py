# -*- coding: utf-8 -*-
from flask import Flask, render_template, request,redirect, url_for, flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import json
app = Flask(__name__)
app.secret_key = "Secret Key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sitemap.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

class sitemap(db.Model):
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    title = db.Column(db.String(255), nullable = False)
    url = db.Column(db.String(255), unique = True, nullable = True)
    depth = db.Column(db.Integer, nullable = False)
    pid = db.Column(db.Integer, nullable = False)
    sortseq = db.Column(db.Integer, unique = True, nullable = False)
    describe = db.Column(db.String(255), unique = True, nullable = True)

    def __init__(self, title,url,depth,pid,sortseq,describe):
        self.title = title
        self.url = url
        self.depth = depth
        self.pid = pid
        self.sortseq = sortseq
        self.describe = describe

@app.route("/")
def index():
    all_data = sitemap.query.order_by(sitemap.id.desc()).all() # selelct * from sitmemap
    return render_template("sitemap_list.html",sitemap = all_data)

@app.route("/admin")
def admin():
    all_data = sitemap.query.order_by(sitemap.id.desc()).all() # selelct * from sitmemap
    return render_template("admin.html",sitemap = all_data)

@app.route("/search",methods=['POST','GET'])
def search():
    searchtxt = request.form['search_text']
    # searchtxt = '메인 화면'
    search_txt1=searchtxt.split()[0]
    search_txt2=searchtxt.split()[1]
    search_txt1_db=db.session.query(sitemap).filter(sitemap.title.contains(search_txt1)).all()
    searcht_txt2_db=db.session.query(sitemap).filter(sitemap.title.contains(search_txt2)).all()
    # exam =db.session.query(sitemap).filter(and_(sitemap.title=='searchtxt1',sitemap.title=='searchtxt2')).all()

    c=[]
    # for i in searchtxt3 :
    #     a.append({'title' : i.title, 'id' : i.id})
    
    # for j in searchtxt4:
    #     b.append({'title' : j.title, 'id' : j.id})

    # exam =db.session.query(sitemap).filter(and_(sitemap.title==a.title,sitemap.title==b.title)).all()
    # for k in exam:
    #     c.append({'title' : k.title, 'id' : k.id})

    for i in search_txt1_db : #9
        for j in searcht_txt2_db :#5
            exam =db.session.query(sitemap).filter(and_(sitemap.id==i.id , sitemap.id==j.id)).all()
            for k in exam:
                c.append({'title' : k.title, 'id' : k.id})



             
    # exam =db.session.query(sitemap).filter(and_(sitemap.title==a,sitemap.title==b)).all()
    # for i in exam:
    #     a.append({'title' : i.title, 'id' : i.id})
    # c=[]
    # exam=[]
    # for i in searchtxt :
    #     b=db.session.query(sitemap).filter(sitemap.title.contains(i)).all()
    #     for j in b:
    #         c.append({'title' : j.title, 'id' : j.id})
    # for k in searchtxt1:
    #     d=db.session.query(sitemap).filter(sitemap.title.contains(i)).all()
    #     for o in d:
    #         e.append({'title' : o.title, 'id' : o.id})
    # exam = sitemap.query.filter(and_(sitemap.title=='c',sitemap.title=='e')).all()
    
    
    json_list = json.dumps(c,ensure_ascii=False)

    # searchtxt = '메인 화면'
    # searchtxt=searchtxt.split() #지오유 그룹웨어 > [지오유,그룹웨어]
    # find = []
    # for txt in searchtxt :
    #     search_db = sitemap.query.filter(sitemap.title.contains(txt)).all()
    #     for result in search_db :
    #         find.append({'title' : result.title , 'id' : result.id})
    # search_result = json.dumps(find,ensure_ascii=False) #한글 깨짐 방지          

    # a=''
    # for txt in searchtxt :
    #     a += "sitemap.title=='"+txt+"',"
    # b=a.rstrip(',')
    # exam = sitemap.query.filter(and_(b)).all()
    # for text in exam :
    #     find.append({'title' : text.title , 'id' : text.id})
    # search_result = json.dumps(find,ensure_ascii=False) #한글 깨짐 방지
    return json_list

@app.route("/insert",methods=['POST'])
def insertUser():
    if request.method == 'POST':
        title = request.form[u'title']
        url = request.form['url']
        depth = request.form['depth']
        pid = request.form['pid']
        sortseq = request.form['sortseq']
        describe = request.form['describe']
        
        inputUser = sitemap(title,url,depth,pid,sortseq,describe) 
        db.session.add(inputUser)
        db.session.commit()

        flash(u"db가 성공적으로 등록되었습니다.","success")

        return redirect(url_for('admin'))   
     
@app.route('/click',methods=['GET','POST'])
def click():
    value = request.form['pid']
    # value = 19
    li = db.session.query(sitemap).filter_by(pid=value).order_by(sitemap.sortseq).all()
    a=[]
    for i in li :
        a.append({'title' : i.title, 'id' : i.id})
    
    json_list = json.dumps(a,ensure_ascii=False) #한글 깨짐 방지
    return json_list

@app.route('/urlclick',methods=['GET','POST'])
def urlclick():
    uid = request.form['urlid']
    # uid = 1
    url = db.session.query(sitemap).filter_by(id = uid).one()
    a={'url' : url.url}
    json_url = json.dumps(a)
    return json_url

@app.route('/desclick',methods=['GET','POST'])
def desclick():
    desid = request.form['desid']
    # desid = 1
    des = db.session.query(sitemap).filter_by(id = desid).one()
    a={'title' : des.title , 'describe' : des.describe}
    json_des = json.dumps(a,ensure_ascii=False)
    return json_des
    
@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        inputUser = sitemap.query.get(request.form.get('id'))
        inputUser.title = request.form[u'title']
        inputUser.url = request.form['url']
        inputUser.depth = request.form['depth']
        inputUser.pid = request.form['pid']
        inputUser.sortseq = request.form['sortseq']
        inputUser.describe = request.form['describe']

        db.session.commit()

        flash(u"db가 성공적으로 수정되었습니다.","success")
        flash(u"수고하셨습니다.","success")

        return redirect(url_for('admin'))

@app.route('/delete/<id>', methods=['GET','POST'])
def delete(id):
    deleteUser = sitemap.query.get(id)
    db.session.delete(deleteUser)
    db.session.commit()
    flash(u"db가 성공적으로 삭제되었습니다.","success")
    return redirect(url_for('admin'))
