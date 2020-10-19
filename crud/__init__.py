# -*- coding: utf-8 -*-
from flask import Flask, render_template, request,redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sitemap.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255), nullable = False)
    url = db.Column(db.String(255), unique = True, nullable = True)
    depth = db.Column(db.Integer, nullable = False)
    sortseq = db.Column(db.Integer, unique = True, nullable = False)
    describe = db.Column(db.String(255), unique = True, nullable = True)

    def __init__(self, title,url,depth,sortseq,describe):
        self.title = title
        self.url = url
        self.depth = depth
        self.sortseq = sortseq
        self.describe = describe

@app.route("/")
def index():
    all_data = User.query.order_by(User.id.desc()).all() # selelct * from sitmemap
    return render_template("index.html",sitemap = all_data)

@app.route("/insert",methods=['POST'])
def insertUser():
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        depth = request.form['depth']
        sortseq = request.form['sortseq']
        describe = request.form['describe']
        
        inputUser = User(title,url,depth,sortseq,describe) 
        db.session.add(inputUser)
        db.session.commit()

        flash(u"직원이 성공적으로 등록되었습니다.","success") # 한글은 앞에 u넣기

        return redirect(url_for('index'))
        
@app.route('/update', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        inputUser = User.query.get(request.form.get('id'))
        inputUser.title = request.form['title']
        inputUser.url = request.form['url']
        inputUser.depth = request.form['depth']
        inputUser.sortseq = request.form['sortseq']
        inputUser.describe = request.form['describe']

        db.session.commit()

        flash(u"직원이 성공적으로 수정되었습니다.","success")
        flash(u"수고하셨습니다.","success")

        return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['GET','POST'])
def delete(id):
    deleteUser = User.query.get(id)
    db.session.delete(deleteUser)
    db.session.commit()
    flash(u"직원이 성공적으로 삭제되었습니다.","success")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()