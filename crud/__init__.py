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
    all_data = sitemap.query.filter(sitemap.depth==1).order_by(sitemap.id.desc()).all()
    return render_template("sitemap_list.html",sitemap = all_data)

@app.route("/admin")
def admin():
    all_data = sitemap.query.order_by(sitemap.id.desc()).all() # selelct * from sitmemap
    return render_template("admin.html",sitemap = all_data)
@app.route("/search",methods=['POST','GET'])
def search():
    searchtxt = request.form['txtsearch']
    # searchtxt = '메인화면'
    list_txt=searchtxt.split()
    id_number=[]
    if searchtxt=='':
        search_db = sitemap.query.filter(sitemap.depth==1).order_by(sitemap.id.desc()).all()
        return render_template("sitemap_list.html",sitemap = search_db)
    elif len(list_txt) == 1:
        search_db = sitemap.query.filter(sitemap.title.contains(searchtxt)).order_by(sitemap.id.desc()).all()
        for number in search_db :
            id_number.append(number.pid)
        search_up_db =sitemap.query.filter(sitemap.id.in_(id_number))
        return render_template("sitemap_list.html",sitemap = search_db,upgrade_sitemap=search_up_db)
    elif len(list_txt) > 1:
        search_db = sitemap.query.filter(and_(sitemap.title.contains(list_txt[0]),sitemap.title.contains(list_txt[1]))).all()
        for number in search_db :
            id_number.append(number.pid)
        search_up_db =sitemap.query.filter(sitemap.id.in_(id_number))
        return render_template("sitemap_list.html",sitemap = search_db,upgrade_sitemap=search_up_db)

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
    li = db.session.query(sitemap).filter_by(pid=value).order_by(sitemap.sortseq).all()
    a=[]
    for i in li :
        a.append({'title' : i.title, 'id' : i.id})
    json_list = json.dumps(a,ensure_ascii=False) #한글 깨짐 방지
    return json_list

@app.route('/urlclick',methods=['GET','POST'])
def urlclick():
    uid = request.form['urlid']
    url = db.session.query(sitemap).filter_by(id = uid).one()
    a={'url' : url.url}
    json_url = json.dumps(a)
    return json_url

@app.route('/desclick',methods=['GET','POST'])
def desclick():
    desid = request.form['desid']
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