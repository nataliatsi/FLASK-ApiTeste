from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

app = Flask(__name__)
api = Api(app)

engine = create_engine('sqlite:///pessoas.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Pessoa(Base):
    __tablename__ = 'pessoas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    email = Column(String(50))

Base.metadata.create_all(engine)

class PessoaAPI(Resource):
    def get(self, pessoa_id=None):
        if pessoa_id is None:
            session = Session()
            pessoas = session.query(Pessoa).all()
            session.close()
            return [{'id': p.id, 'nome': p.nome, 'email': p.email} for p in pessoas]
        else:
            session = Session()
            pessoa = session.query(Pessoa).filter_by(id=pessoa_id).first()
            session.close()
            return {'id': pessoa.id, 'nome': pessoa.nome, 'email': pessoa.email}

    def post(self):
        session = Session()
        pessoa = Pessoa(nome=request.json['nome'], email=request.json['email'])
        session.add(pessoa)
        session.commit()
        session.close()
        return {'id': pessoa.id, 'nome': pessoa.nome, 'email': pessoa.email}

    def put(self, pessoa_id):
        session = Session()
        pessoa = session.query(Pessoa).filter_by(id=pessoa_id).first()
        pessoa.nome = request.json['nome']
        pessoa.email = request.json['email']
        session.commit()
        session.close()
        return {'id': pessoa.id, 'nome': pessoa.nome, 'email': pessoa.email}

    def delete(self, pessoa_id):
        session = Session()
        pessoa = session.query(Pessoa).filter_by(id=pessoa_id).first()
        session.delete(pessoa)
        session.commit()
        session.close()
        return {'message': 'Pessoa deletada com sucesso.'}

api.add_resource(PessoaAPI, '/pessoas', '/pessoas/<int:pessoa_id>')

if __name__ == '__main__':
    app.run(debug=True)
