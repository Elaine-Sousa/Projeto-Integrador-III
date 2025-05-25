import os
from flask import Flask, flash, jsonify, redirect, render_template, g, request, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'uma_chave_secreta_qualquer'

DATABASE = 'banco.db'

# Função para obter conexão com o banco SQLite
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Fecha conexão com o banco no fim da requisição
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# -------- FUNÇÃO PARA BUSCAR IMAGENS DE DEVOLUÇÃO --------
def buscar_imagens_por_id(id_devolucao):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT url_imagem FROM imagens_devolucoes WHERE devolucao_id = ?", (id_devolucao,))
    resultados = cursor.fetchall()
    conn.close()
    return [row['url_imagem'] for row in resultados]

@app.route('/imagens_devolucao/<int:id>')
def imagens_devolucao(id):
    imagens = buscar_imagens_por_id(id)
    return jsonify({"imagens": imagens})

# -------- ROTAS HTML --------

@app.route('/')
def home():
    return render_template('home.html', logo='imagens/logoPI.png')

@app.route('/reclamacoes')
def reclamacoes():
    db = get_db()
    cursor = db.execute("SELECT motivo, COUNT(*) FROM devolucoes GROUP BY motivo")
    resultados = cursor.fetchall()
    labels = [linha[0] for linha in resultados]
    valores = [linha[1] for linha in resultados]
    return render_template("reclamacoes.html", labels=labels, valores=valores)

@app.route('/estoqueFisico')
def estoque_fisico():
    db = get_db()
    produtos = db.execute('SELECT nome, categoria, quantidade, preco, status_estoque FROM estoque_fisico').fetchall()
    return render_template('estoqueFisico.html', produtos=produtos)

@app.route('/descarte')
def descarte():
    conn = get_db()
    itens_descarte = conn.execute('SELECT * FROM descarte').fetchall()
    return render_template('descarte.html', itens=itens_descarte, logo='imagens/logoPI.png')

@app.route('/estoquedevolucao')
def estoque_devolucao():
    conn = get_db()
    devolucoes = conn.execute('SELECT * FROM devolucoes').fetchall()
    lista_devolucoes = []
    for d in devolucoes:
        item = dict(d)
        if item['preco'] is None:
            item['preco'] = 0.0
        lista_devolucoes.append(item)
    return render_template('estoqueDevolucao.html', devolucoes=lista_devolucoes)

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', logo='imagens/logoPI.png')

@app.route('/login')
def login():
    return render_template('login.html', logo='imagens/logoPI.png')

@app.route('/acesso', methods=['GET', 'POST'])
def acesso():
    if request.method == 'POST':
        dados = request.get_json()
        matricula = dados.get('matricula')
        email = dados.get('email')
        senha = dados.get('senha')
    return render_template('acesso.html')

# -------- INSERÇÃO DE IMAGENS NO BANCO --------

def criar_tabela_imagens_devolucoes():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS imagens_devolucoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            devolucao_id INTEGER NOT NULL,
            url_imagem TEXT NOT NULL,
            FOREIGN KEY (devolucao_id) REFERENCES devolucoes(id)
        )
    ''')
    db.commit()

def inserir_imagens_se_necessario():
    db = get_db()
    imagens_por_devolucao = {
        1:  ['tenis1.png', 'tenis2.png'],
        2:  ['camisa1.png', 'camisa2.png' ],
        3:  ['calça1.png', 'calça2.png'],
        4:  ['JaquetaCorta-Vento1.png'],
        5:  ['MeiaEsportiva.jpg'],
        6:  ['BoneCasual.jpg'],
        7:  ['RelogioDigital.jpg'],
        8:  ['MochilaEscolar.jpg'],
        9:  ['oculosdeSol.jpg'],
        10: ['ventilado.jpg'], 
        11: ['ventilador.jpg'],
        12: ['Tablet.jpg'],
    }
    cursor = db.execute('SELECT COUNT(*) FROM imagens_devolucoes')
    if cursor.fetchone()[0] > 0:
        return
    for devolucao_id, imagens in imagens_por_devolucao.items():
        for img in imagens:
            url = f'imagens/{img}'
            db.execute(
                'INSERT INTO imagens_devolucoes (devolucao_id, url_imagem) VALUES (?, ?)',
                (devolucao_id, url)
            )
    db.commit()

# -------- MOVIMENTAÇÃO DE ITENS --------

@app.route('/mover_estoque_fisico', methods=['POST'])
def mover_para_estoque_fisico():
    db = get_db()
    data = request.get_json()
    item_id = data.get('id')

    if not item_id:
        return jsonify({'error': 'ID não informado'}), 400

    item = db.execute("SELECT * FROM devolucoes WHERE id = ?", (item_id,)).fetchone()
    if item:
        db.execute('''
            INSERT INTO estoque_fisico (nome, categoria, quantidade, preco, status_estoque)
            VALUES (?, ?, ?, ?, ?)
        ''', (item['nome'], 'Categoria Desconhecida', item['quantidade'], item['preco'], 'Em Estoque'))

        db.execute("DELETE FROM devolucoes WHERE id = ?", (item_id,))
        db.commit()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'error': 'Item não encontrado'}), 404

@app.route('/mover_para_descarte/<int:id>', methods=['POST'])
def mover_para_descarte(id):
    try:
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()

        cursor.execute("SELECT nome, motivo, quantidade, preco, imagem FROM devolucoes WHERE id = ?", (id,))
        item = cursor.fetchone()

        if not item:
            print(f'Item com id {id} não encontrado')
            return {'error': 'Item não encontrado'}, 404

        nome, motivo, quantidade, preco, imagem = item

        cursor.execute("""
            INSERT INTO descarte (nome, motivo, quantidade, preco, imagem)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, motivo, quantidade, preco, imagem))

        cursor.execute("DELETE FROM devolucoes WHERE id = ?", (id,))
        conn.commit()

        print(f'Item com id {id} movido para descarte com sucesso')
        return {'message': 'Item movido para descarte com sucesso'}, 200

    except Exception as e:
        print(f'Erro no mover_para_descarte: {e}')
        return {'error': str(e)}, 500

    finally:
        conn.close()

# -------- ERRO 404 --------

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

# -------- MAIN --------

if __name__ == '__main__':
    app.run(debug=True)
