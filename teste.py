from flask import Flask, jsonify, render_template, redirect, request, url_for
import pymysql

# Configuração da conexão com o banco de dados
def connect_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='lipe444555',
        database='restalrante'
    )

app = Flask(__name__, template_folder="../HTML", static_folder="../CSS")
app.config['SECRET_KEY'] = 'CHABLAU'

# Página inicial (mercado)
@app.route("/", methods=['GET'])
def home():
    return render_template('mercado.html')

# Página de login
@app.route("/login", methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form.get('email')
        phone = request.form.get('phone')
        connectionn = connect_db()
        try:
            with connectionn.cursor() as cursors:
                cursors.execute ('select*from clientes where email = %s and Telefone = %s', (email, phone))
                recursos = cursors.fetchone()

            if recursos:
                email_ = recursos[3]
                phone_ = recursos[2]

                if email_  == email and phone_ == phone:
                    return render_template('produtos.html')
        except Exception as error:
            print (error)
        finally:
            connectionn.close()
          # Implementar lógica de login com o banco de dados
          # Redireciona para produtos após login bem-sucedido
    return render_template('login.html')  # Renderiza o formulário de login se for GET


            
# Páginas
@app.route("/produtos", methods=['GET'])
def produtos():
    return render_template('produtos.html')

@app.route("/carrinho", methods= ['GET'])
def carrinho():
    return render_template('carrinho.html')

@app.route("/pagamento", methods= ['GET'])
def pagamento():
    return render_template('pagamento.html')


# Página de registro
@app.route("/registrar", methods=['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return render_template('registro.html')

    elif request.method == 'POST':
        data = request.get_json()
        nome = data.get('name')
        email = data.get('email')
        phone = data.get('phone')

        if not data or not nome or not email or not phone:
            return jsonify({'erro': 'Dados incompletos'}), 400

        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                cursor.execute('call Novos_Dados (%s, %s, %s)', (nome, phone, email))
                connection.commit()

            # Em vez de renderizar produtos.html, enviamos a URL como resposta JSON
            return jsonify({'mensagem': 'Registro realizado com sucesso!', 'redirect_url': '/produtos'})
        except Exception as e:
            return jsonify({'erro': str(e)}), 500
        finally:
            connection.close()





if __name__ == "__main__":
    app.run(debug=True)
