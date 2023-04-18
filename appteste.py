from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, marshal
import logging

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, help='Problema na conversão do nome!')
parser.add_argument('email', type=str, help='Problema na conversão do email!')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
                    handlers=[logging.FileHandler("hello_flask.log", mode='w'),
                              logging.StreamHandler()])
stream_handler = [h for h in logging.root.handlers if isinstance(
    h, logging.StreamHandler)][0]
stream_handler.setLevel(logging.INFO)

api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix='/api')

db.init_app(app)

pessoa_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'email': fields.String
}
mensagem_fields = {
  'descricao': fields.String,
  'codigo': fields.String
}

class Mensagem():
  def __init__(self, descricao, codigo):
    self.descricao = descricao
    self.codigo = codigo

class Pessoa(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String, unique=True, nullable=False)
  email = db.Column(db.String)

  def __init__(self, nome, email):
    self.nome = nome
    self.email = email
    
  def __repr__(self):
      return f'<Pessoa {self.nome}, {self.email}>>'

with app.app_context():
  db.create_all()

class PessoaResource(Resource):
  @marshal_with(pessoa_fields)
  def get(self):
    pessoas = Pessoa.query.all()
    return (pessoas, 200)

  @marshal_with(pessoa_fields)  
  def post(self):
    args = parser.parse_args()
    nome = args['nome']
    email = args['email']
    
    pessoa = Pessoa(nome, email)

    db.session.add(pessoa)
    db.session.commit()

    return pessoa, 201

  def put(self, pessoa_id):

    args = parser.parse_args()

    nome = args['nome']
    email = args['email'] 

    pessoa = Pessoa.query.get(pessoa_id)

    if pessoa is not None:

      pessoa.nome = nome
      pessoa.email = email

      db.session.add(pessoa)
      db.session.commit(pessoa)
      return marshal(pessoa, pessoa_fields), 201
    else:
      mensagem = Mensagem('Pessoa não encontrada.', 1)
      return marshal(mensagem, mensagem_fields), 404 

api.add_resource(PessoaResource, '/pessoas', '/pessoas/<int:pessoa_id>')
app.register_blueprint(api_bp)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)