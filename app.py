from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, UserMixin, SQLAlchemyAdapter, login_required

from flask import *
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import flask_wtf as wtf
from functools import wraps
from werkzeug.security import generate_password_hash
from flask_admin.contrib.fileadmin import FileAdmin
from os.path import dirname, join
from flask_user import login_required , UserManager , UserMixin, SQLAlchemyAdapter
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database9.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'randomstring'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['CSRF_ENABLED'] = True
app.config['USER_ENABLE_EMAIL'] = False

from flask_admin.contrib.fileadmin import FileAdmin
from os.path import dirname, join

db = SQLAlchemy(app)

admin=Admin(app)
login_manager = LoginManager(app)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    active = db.Column(db.Boolean(), nullable=False, server_default='0')


db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)




class Producto(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    material = db.Column(db.String)
    materialForro = db.Column(db.String)
    materialPlantilla = db.Column(db.String)
    materialPlataforma = db.Column(db.String)

    habilitado=db.Column(db.Boolean)
    precio = db.Column(db.Float)
    tallas=db.relationship("TallasxProducto", backref='producto')
    image = db.Column(db.String, nullable=True)
    def lista(self):
        u=self.query.filter_by(habilitado=1)
        lista=[[x.id,x.name,x.material,x.materialForro,x.precio,x.image,x.materialPlantilla,x.materialPlataforma] for x in u]
        return lista


    def __repr__(self):
        return self.name


class Tallas(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    clase_id= db.Column(db.Integer, db.ForeignKey('producto.id'))
    tamano = db.Column(db.Integer)
    Productos = db.relationship("TallasxProducto", backref='tallas')

    def __repr__(self):
        return str(self.tamano)
class TallasxProducto(db.Model):
    id_Talla=db.Column("id_Talla",db.Integer,db.ForeignKey("tallas.id"), primary_key=True)
    id_Producto=db.Column("id_Producto", db.Integer, db.ForeignKey("producto.id"), primary_key=True)
    activado=db.Column("activo",db.Boolean)
    stock = db.Column(db.Integer)

class UserView(ModelView):
    column_exclude_list = []
    column_display_pk = True
    can_create = True
    can_edit = True
    can_delete = False
    can_export = True
    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password, method='sha256')



    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return '<h1>You are not logged in!</h1>'
class ProductoView(ModelView):
    column_exclude_list = ['descripcion']
    column_display_pk = True
    can_create = True
    can_edit = True
    can_delete = False
    can_export = True


    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return '<h1>You are not logged in!</h1>'
class TallasView(ModelView):
    column_exclude_list = []
    column_display_pk = True
    can_create = True
    can_edit = True
    can_delete = False
    can_export = True


    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return '<h1>You are not logged in!</h1>'
class TallasxProductoView(ModelView):
    column_exclude_list = []
    column_display_pk = True
    can_create = True
    can_edit = True
    can_delete = False
    can_export = True



    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return '<h1>You are not logged in!</h1>'



@app.route('/')
def index():

    productos=Producto().lista()
    print(productos)
    return render_template('/inicio.html',products=productos,ubicacion='home')

@app.route('/producto=<producto>')
def producto(producto):
    a=TallasxProducto.query.filter_by(id_Producto=producto).all()
    b=[[x.stock,Tallas.query.filter_by(id=x.id_Talla).one()] for x in a]
    productos=Producto.query.filter_by(id=producto).one()
    pro=Producto.query.filter_by(id=producto).one()
    lista=[productos,b,pro.material,pro.precio,pro.image,pro.materialForro,pro.materialPlantilla,pro.materialPlataforma]
    return render_template('/producto.html',producto=lista)

admin.add_view(ProductoView(Producto,db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(TallasxProductoView(TallasxProducto, db.session))
admin.add_view(TallasView(Tallas, db.session))
path = join(dirname(__file__), 'static')
class FileView(FileAdmin):




    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return '<h1>You are not logged in!</h1>'
admin.add_view(FileView(path, '/static/', name='Uploads'))


if __name__ ==  '__main__':
    db.create_all()
    app.run(debug=True,port=1009)