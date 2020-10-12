from flask import Flask,render_template,url_for,redirect,request,session,jsonify
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Email,DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bootstrap import Bootstrap


app=Flask(__name__)
bootstrap=Bootstrap(app)
ma=Marshmallow(app)

app.config["SECRET_KEY"]="3e8ujdn03ioejfd"
app.config["SQLALCHEMY_DATABASE_URI"]='mysql://root:''@localhost/newdata'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30))
    email=db.Column(db.String(30))

    def __init__(self,name,email):
        self.name=name
        self.email=email

    
class User_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=User

class Adduser(FlaskForm):
    name=StringField("name",validators=[DataRequired()])
    email=StringField("email",validators=[DataRequired(),Email()])
    submit=SubmitField("submit")

@app.route("/")
def home():
    user=User.query.all()
    return render_template("home.html",title="Home",user=user)



@app.route("/adduser",methods=["GET",'POST'])
def adduser():
    form=Adduser()
    if form.validate_on_submit():
        name=form.name.data
        email=form.email.data
        mydata=User(name,email)
        db.session.add(mydata)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("adduser.html",title="Adduser",form=form)




@app.route("/delete/<int:id>",methods=['GET','POST'])
def delete_user(id):
    user=User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/edit/<int:id>",methods=['GET','POST'])
def edit_user(id):
    user=User.query.get(id)
    form=Adduser()
    if form.validate_on_submit():
        user.name=form.name.data
        user.email=form.email.data
        db.session.commit()
        return redirect(url_for('home'))
    if request.method=="GET":
        form.name.data=user.name
        form.email.data=user.email
    return render_template('adduser.html',form=form)


@app.route("/api",methods=['GET','POST'])
def api():
    user=User.query.all()
    user_schema=User_Schema(many=True)
    output=user_schema.dump(user)
    return jsonify(output)





if __name__ == "__main__":
    app.route(debug=True)