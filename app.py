from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/submit_form_route', methods=['POST'])
def submit_form_route():
    if request.method == 'POST':
        # Process the form data here
        # For example, you can access the form data using request.form
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
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
    
    return jsonify({'status': 'error', 'message': 'This route only accepts POST request for form submission.'}), 405

if __name__ == '__main__':
    app.run(debug=True)
