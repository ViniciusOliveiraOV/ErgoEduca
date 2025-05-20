from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback_development_secret_key')

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'ergoeduca.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ... (resto dos seus imports e configurações, como Flask-Mail, se estiver usando) ...
# app.secret_key = ... (se estiver usando flash messages)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')


class Cadastro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Cadastro {self.name} - {self.email} - {self.phone}>'


@app.route('/submit_form_route', methods=['POST'])
def submit_form_route():
    if request.method == 'POST':
        # Process the form data here
        # For example, you can access the form data using request.form
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        if not name or not email:
            return jsonify({'status': 'error', 'message': 'Nome e Email são obrigatórios.'}), 400
        # Verificar se o email já existe (se o campo email for unique=True)
        if Cadastro.query.filter_by(email=email).first():
            return jsonify({'status': 'error', 'message': 'Este email já foi cadastrado.'}), 409 # 409 Conflict

        try:
            novo_cadastro = Cadastro(name=name, email=email, phone=phone)
            db.session.add(novo_cadastro)
            db.session.commit()

            print(f"Formulário Recebido: {request.form}")
            print(f"  Nome: {name}")
            print(f"  Email: {email}")
            print(f"  Telefone: {phone}")

            '''response_data = {
                'status': 'success',
                'message': 'Form submitted successfully!',
                'submitted_name': name,
                'submitted_email': email,
                'submitted_phone': phone
            }'''

            return jsonify({'status': 'success', 'message': 'Dados recebidos com sucesso!'}), 200
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar no banco de dados: {e}")
            return jsonify({'status': 'error', 'message': 'Erro ao processar o formulário.'}), 500
    
    return jsonify({'status': 'error', 'message': 'This route only accepts POST request for form submission.'}), 405



if __name__ == '__main__':
    #with app.app_context():
    #    db.create_all()
    app.run(host='0.0.0.0', port=8080, debug=True)
