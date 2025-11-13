from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'sistema_farmacia'
app.secret_key = 'abcd1234'

# Configurações de upload
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

mysql = MySQL(app)

# Criar pasta de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_carrinho():
    if 'carrinho' not in session:
        session['carrinho'] = []

def calcular_total_carrinho():
    total = 0
    for item in session['carrinho']:
        total += item['preco'] * item['quantidade']
    return total

def is_admin():
    return session.get('loggedin') and session.get('tipo') == 'admin'

@app.route("/")
def home():
    search = request.args.get('search', '')
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if search:
        cursor.execute("""
            SELECT p.*, e.quantidade 
            FROM produtos p 
            LEFT JOIN estoque e ON p.id = e.produto_id 
            WHERE p.nome LIKE %s OR p.marca LIKE %s
        """, (f'%{search}%', f'%{search}%'))
    else:
        cursor.execute("""
            SELECT p.*, e.quantidade 
            FROM produtos p 
            LEFT JOIN estoque e ON p.id = e.produto_id
        """)
    
    produtos = cursor.fetchall()
    cursor.close()
    
    init_carrinho()
    return render_template("home.html", produtos=produtos, search=search)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM clientes WHERE email = %s", (email,))
        cliente = cursor.fetchone()
        cursor.close()

        if cliente and cliente['senha'] == senha:
            session['loggedin'] = True
            session['id'] = cliente['id']
            session['nome'] = cliente['nome']
            session['email'] = cliente['email']
            session['tipo'] = cliente.get('tipo', 'cliente')
            init_carrinho()
            
            if session['tipo'] == 'admin':
                flash(f"👋 Bem-vindo, Admin {cliente['nome']}!", "success")
            else:
                flash(f"✅ Bem-vindo, {cliente['nome']}!", "success")
                
            return redirect(url_for('home'))
        else:
            flash("❌ Email ou senha incorretos!", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("🔒 Você saiu da sua conta.", "info")
    return redirect(url_for('home'))

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        cpf = request.form["cpf"]
        telefone = request.form.get("telefone", "")
        data_nascimento = request.form.get("data_nascimento", "")

        if len(senha) < 6:
            flash("❌ A senha deve ter pelo menos 6 caracteres!", "danger")
            return render_template("cadastro.html")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        try:
            cursor.execute("SELECT id FROM clientes WHERE email = %s OR cpf = %s", (email, cpf))
            if cursor.fetchone():
                flash("❌ Email ou CPF já cadastrado!", "danger")
            else:
                cursor.execute("""
                    INSERT INTO clientes (nome, email, senha, cpf, telefone, data_nascimento) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (nome, email, senha, cpf, telefone, data_nascimento))
                
                mysql.connection.commit()
                flash("✅ Cadastro realizado com sucesso! Faça login.", "success")
                return redirect(url_for('login'))
                
        except Exception as e:
            mysql.connection.rollback()
            flash(f"❌ Erro no cadastro: {str(e)}", "danger")
        finally:
            cursor.close()

    return render_template("cadastro.html")

@app.route("/detalhe-produto/<int:id>")
def detalhe_produto(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT p.*, e.quantidade 
        FROM produtos p 
        LEFT JOIN estoque e ON p.id = e.produto_id 
        WHERE p.id = %s
    """, (id,))
    produto = cursor.fetchone()
    cursor.close()
    
    if not produto:
        flash("❌ Produto não encontrado!", "danger")
        return redirect(url_for('home'))
    
    return render_template("detalhe_produto.html", produto=produto)

@app.route("/carrinho")
def carrinho():
    if 'loggedin' not in session:
        flash("⚠️ Por favor, faça login para acessar o carrinho.", "warning")
        return redirect(url_for('login'))
    
    init_carrinho()
    total = calcular_total_carrinho()
    return render_template("carrinho.html", carrinho=session['carrinho'], total=total)

@app.route("/adicionar-carrinho/<int:produto_id>")
def adicionar_carrinho(produto_id):
    if 'loggedin' not in session:
        return jsonify({'success': False, 'message': 'Faça login primeiro'})
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM produtos WHERE id = %s", (produto_id,))
    produto = cursor.fetchone()
    cursor.close()
    
    if not produto:
        return jsonify({'success': False, 'message': 'Produto não encontrado'})
    
    init_carrinho()
    
    for item in session['carrinho']:
        if item['id'] == produto_id:
            item['quantidade'] += 1
            session.modified = True
            return jsonify({
                'success': True, 
                'message': 'Quantidade atualizada', 
                'carrinho_count': len(session['carrinho'])
            })
    
    novo_item = {
        'id': produto['id'],
        'nome': produto['nome'],
        'marca': produto['marca'],
        'preco': float(produto['preco_venda']),
        'quantidade': 1,
        'imagem': produto.get('imagem', 'default.jpg')
    }
    
    session['carrinho'].append(novo_item)
    session.modified = True
    
    return jsonify({
        'success': True, 
        'message': 'Produto adicionado ao carrinho', 
        'carrinho_count': len(session['carrinho'])
    })

@app.route("/remover-carrinho/<int:produto_id>")
def remover_carrinho(produto_id):
    if 'loggedin' not in session:
        return jsonify({'success': False, 'message': 'Faça login primeiro'})
    
    init_carrinho()
    
    for i, item in enumerate(session['carrinho']):
        if item['id'] == produto_id:
            session['carrinho'].pop(i)
            session.modified = True
            return jsonify({
                'success': True, 
                'message': 'Produto removido', 
                'carrinho_count': len(session['carrinho'])
            })
    
    return jsonify({'success': False, 'message': 'Produto não encontrado no carrinho'})

@app.route("/atualizar-quantidade", methods=["POST"])
def atualizar_quantidade():
    if 'loggedin' not in session:
        return jsonify({'success': False, 'message': 'Faça login primeiro'})
    
    data = request.get_json()
    produto_id = data.get('produto_id')
    nova_quantidade = data.get('quantidade')
    
    if not produto_id or not nova_quantidade:
        return jsonify({'success': False, 'message': 'Dados inválidos'})
    
    init_carrinho()
    
    for item in session['carrinho']:
        if item['id'] == int(produto_id):
            item['quantidade'] = int(nova_quantidade)
            session.modified = True
            return jsonify({
                'success': True, 
                'total_item': item['preco'] * item['quantidade'],
                'total_carrinho': calcular_total_carrinho()
            })
    
    return jsonify({'success': False, 'message': 'Produto não encontrado'})

@app.route("/finalizar-pedido", methods=["POST"])
def finalizar_pedido():
    if 'loggedin' not in session:
        return jsonify({'success': False, 'message': 'Faça login primeiro'})
    
    init_carrinho()
    
    if not session['carrinho']:
        return jsonify({'success': False, 'message': 'Carrinho vazio'})
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        cursor.execute("SELECT id FROM clientes WHERE id = %s", (session['id'],))
        if not cursor.fetchone():
            session.clear()
            return jsonify({'success': False, 'message': 'Cliente não encontrado. Faça login novamente.'})
        
        cursor.execute("SELECT * FROM enderecos WHERE cliente_id = %s LIMIT 1", (session['id'],))
        endereco = cursor.fetchone()
        
        if not endereco:
            total = calcular_total_carrinho()
            cursor.execute("INSERT INTO pedidos (cliente_id, total, status) VALUES (%s, %s, 'pendente')", (session['id'], total))
            pedido_id = cursor.lastrowid
            
            for item in session['carrinho']:
                cursor.execute("INSERT INTO pedido_itens (pedido_id, produto_id, quantidade, preco_unitario) VALUES (%s, %s, %s, %s)", (pedido_id, item['id'], item['quantidade'], item['preco']))
            
            mysql.connection.commit()
            
            return jsonify({
                'success': True, 
                'message': 'Precisamos do seu endereço para entrega',
                'pedido_id': pedido_id,
                'needs_address': True
            })
        
        total = calcular_total_carrinho()
        cursor.execute("INSERT INTO pedidos (cliente_id, endereco_entrega_id, total, status) VALUES (%s, %s, %s, 'pendente')", (session['id'], endereco['id'], total))
        pedido_id = cursor.lastrowid
        
        for item in session['carrinho']:
            cursor.execute("INSERT INTO pedido_itens (pedido_id, produto_id, quantidade, preco_unitario) VALUES (%s, %s, %s, %s)", (pedido_id, item['id'], item['quantidade'], item['preco']))
            cursor.execute("UPDATE estoque SET quantidade = quantidade - %s WHERE produto_id = %s", (item['quantidade'], item['id']))
        
        session['carrinho'] = []
        session.modified = True
        mysql.connection.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Pedido realizado com sucesso!',
            'pedido_id': pedido_id,
            'needs_address': False
        })
        
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'success': False, 'message': f'Erro ao finalizar pedido: {str(e)}'})
    finally:
        cursor.close()

@app.route("/meus-pedidos")
def meus_pedidos():
    if 'loggedin' not in session:
        flash("⚠️ Por favor, faça login para ver seus pedidos.", "warning")
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT p.*, e.logradouro, e.cidade, e.estado 
        FROM pedidos p 
        LEFT JOIN enderecos e ON p.endereco_entrega_id = e.id
        WHERE p.cliente_id = %s 
        ORDER BY p.data_pedido DESC
    """, (session['id'],))
    pedidos = cursor.fetchall()
    cursor.close()
    
    return render_template("meus_pedidos.html", pedidos=pedidos)

@app.route("/pagamento/<int:pedido_id>")
def pagamento(pedido_id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM pedidos WHERE id = %s AND cliente_id = %s", (pedido_id, session['id']))
    pedido = cursor.fetchone()
    cursor.close()
    
    if not pedido:
        flash("❌ Pedido não encontrado!", "danger")
        return redirect(url_for('meus_pedidos'))
    
    return render_template("pagamento.html", pedido=pedido)

@app.route("/confirmar-pagamento/<int:pedido_id>", methods=["POST"])
def confirmar_pagamento(pedido_id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("UPDATE pedidos SET status = 'pago' WHERE id = %s AND cliente_id = %s", (pedido_id, session['id']))
        mysql.connection.commit()
        flash("✅ Pagamento confirmado! Seu pedido está sendo processado.", "success")
    except Exception as e:
        mysql.connection.rollback()
        flash(f"❌ Erro ao confirmar pagamento: {str(e)}", "danger")
    finally:
        cursor.close()
    
    return redirect(url_for('meus_pedidos'))

@app.route("/salvar-endereco-pagamento", methods=["POST"])
def salvar_endereco_pagamento():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    pedido_id = request.form.get('pedido_id')
    cep = request.form.get('cep')
    logradouro = request.form.get('logradouro')
    numero = request.form.get('numero')
    complemento = request.form.get('complemento', '')
    bairro = request.form.get('bairro')
    cidade = request.form.get('cidade')
    estado = request.form.get('estado')
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        cursor.execute("INSERT INTO enderecos (cliente_id, cep, logradouro, numero, complemento, bairro, cidade, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (session['id'], cep, logradouro, numero, complemento, bairro, cidade, estado))
        endereco_id = cursor.lastrowid
        
        cursor.execute("UPDATE pedidos SET endereco_entrega_id = %s, status = 'pendente' WHERE id = %s AND cliente_id = %s", (endereco_id, pedido_id, session['id']))
        
        cursor.execute("SELECT * FROM pedido_itens WHERE pedido_id = %s", (pedido_id,))
        itens = cursor.fetchall()
        
        for item in itens:
            cursor.execute("UPDATE estoque SET quantidade = quantidade - %s WHERE produto_id = %s", (item['quantidade'], item['produto_id']))
        
        session['carrinho'] = []
        session.modified = True
        mysql.connection.commit()
        
        flash("✅ Endereço salvo com sucesso! Redirecionando para pagamento.", "success")
        return redirect(url_for('pagamento', pedido_id=pedido_id))
        
    except Exception as e:
        mysql.connection.rollback()
        flash(f"❌ Erro ao salvar endereço: {str(e)}", "danger")
        return redirect(url_for('endereco_pagamento', pedido_id=pedido_id))
    finally:
        cursor.close()

@app.route("/endereco-pagamento/<int:pedido_id>")
def endereco_pagamento(pedido_id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    return render_template("endereco.html", pedido_id=pedido_id)

# ========== ROTAS ADMIN ==========

@app.route("/admin/adicionar-produto", methods=["GET", "POST"])
def adicionar_produto():
    if not is_admin():
        flash("⛔ Acesso restrito para administradores!", "danger")
        return redirect(url_for('home'))
    
    if request.method == "POST":
        nome = request.form["nome"]
        marca = request.form["marca"]
        descricao = request.form["descricao"]
        preco_venda = request.form["preco_venda"]
        quantidade = request.form["quantidade"]
        
        imagem = 'default.jpg'
        if 'imagem' in request.files:
            file = request.files['imagem']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                filename = timestamp + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                imagem = filename
        
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("INSERT INTO produtos (nome, marca, descricao, preco_venda, imagem) VALUES (%s, %s, %s, %s, %s)", (nome, marca, descricao, preco_venda, imagem))
            produto_id = cursor.lastrowid
            cursor.execute("INSERT INTO estoque (produto_id, quantidade) VALUES (%s, %s)", (produto_id, quantidade))
            mysql.connection.commit()
            flash("✅ Produto adicionado com sucesso!", "success")
            return redirect(url_for('home'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f"❌ Erro ao adicionar produto: {str(e)}", "danger")
        finally:
            cursor.close()
    
    return render_template("adicionar_produto.html")

@app.route("/admin/editar-produto/<int:id>", methods=["GET", "POST"])
def editar_produto(id):
    if not is_admin():
        flash("⛔ Acesso restrito para administradores!", "danger")
        return redirect(url_for('home'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == "POST":
        nome = request.form["nome"]
        marca = request.form["marca"]
        descricao = request.form["descricao"]
        preco_venda = request.form["preco_venda"]
        quantidade = request.form["quantidade"]
        
        nova_imagem = None
        if 'imagem' in request.files:
            file = request.files['imagem']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                filename = timestamp + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                nova_imagem = filename
        
        try:
            if nova_imagem:
                cursor.execute("UPDATE produtos SET nome=%s, marca=%s, descricao=%s, preco_venda=%s, imagem=%s WHERE id=%s", (nome, marca, descricao, preco_venda, nova_imagem, id))
            else:
                cursor.execute("UPDATE produtos SET nome=%s, marca=%s, descricao=%s, preco_venda=%s WHERE id=%s", (nome, marca, descricao, preco_venda, id))
            
            cursor.execute("UPDATE estoque SET quantidade=%s WHERE produto_id=%s", (quantidade, id))
            mysql.connection.commit()
            flash("✅ Produto atualizado com sucesso!", "success")
            return redirect(url_for('detalhe_produto', id=id))
        except Exception as e:
            mysql.connection.rollback()
            flash(f"❌ Erro ao atualizar produto: {str(e)}", "danger")
    
    cursor.execute("SELECT p.*, e.quantidade FROM produtos p LEFT JOIN estoque e ON p.id = e.produto_id WHERE p.id = %s", (id,))
    produto = cursor.fetchone()
    cursor.close()
    
    return render_template("editar_produto.html", produto=produto)

if __name__ == "__main__":
    app.run(debug=True)