from re import A

from wtforms import form

from flask import Flask, render_template,request,redirect,url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms

from models import db, email
from models import Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
csrf=CSRFProtect()

@app.route("/",methods=['GET', 'POST'])
@app.route("/index")
def index():
	create_form=forms.UserForm2(request.form)	
	alumnos = Alumnos.query.all()
	return render_template("index.html",form=create_form, alumno=alumnos)

@app.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
    form = forms.UserForm2(request.form)
    
    if request.method == 'POST':
        if form.validate():
            alum = Alumnos(
                nombre=form.nombre.data,
                apaterno=form.apaterno.data,
				amaterno=request.form.get('amaterno'),
                email=form.email.data
            )
            db.session.add(alum)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            print("ERRORES DETECTADOS:", form.errors)
            
    return render_template("alumnos.html", form=form)

@app.route('/detalles', methods=['GET','POST'])
def detalles():
    create_form=forms.UserForm2(request.form)
    if request.method=='GET':
        id = int(request.args.get("id"))
        #select * from alumnos where id==id
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        id=request.args.get('id')
        nombre=alum1.nombre
        apellidos=alum1.apellidos
        email=alum1.email
        telefono=alum1.telefono
        
    return render_template('detalles.html', id=id,nombre=nombre,apellidos=apellidos,email=email,telefono=telefono,form=create_form)

@app.route("/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm2(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        
        if alum1:
            create_form.id.data = alum1.id
            create_form.nombre.data = alum1.nombre
            create_form.apellidos.data = alum1.apellidos 
            create_form.email.data = alum1.email
            
    if request.method == 'POST':
        id = create_form.id.data
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        
        if alum1:
            alum1.nombre = create_form.nombre.data
            alum1.apellidos = create_form.apellidos.data 
            alum1.email = create_form.email.data
            
            db.session.add(alum1)
            db.session.commit()
            return redirect(url_for('index'))
            
    return render_template("modificar.html", form=create_form)

@app.route("/eliminar", methods=['GET','POST'])
def eliminar():
    create_form=forms.UserForm2(request.form)
    if request.method =='GET':
        id= request.args.get('id')
        alumn1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        if alumn1:
            create_form.id.data=alumn1.id
            create_form.nombre.data=alumn1.nombre
            create_form.apellidos.data=alumn1.apellidos
            create_form.email.data=alumn1.email
            create_form.telefono.data=alumn1.telefono
            return render_template("eliminar.html", form=create_form)
        
    if request.method=='POST':
            id=create_form.id.data
            alumn=db.session.query(Alumnos).filter(Alumnos.id==id).first()
            if alumn:
                db.session.delete(alumn)
                db.session.commit()
            return redirect(url_for('index'))
    return render_template("eliminar.html", form=create_form)

@app.errorhandler(404)
def page_not_fount(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
	#app.run(debug=True)
	with app.app_context():
		db.create_all()
		app.run()
	csrf = CSRFProtect(app)

