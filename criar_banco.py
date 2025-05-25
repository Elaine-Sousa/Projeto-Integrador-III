import sqlite3

# Conectar ao banco (ou criar se não existir)
conn = sqlite3.connect('banco.db')
cursor = conn.cursor()

# Criar a tabela 'devolucoes'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS devolucoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        motivo TEXT NOT NULL,
        imagem TEXT NOT NULL,
        preco REAL,
        quantidade INTEGER NOT NULL
    )
''')
# Criar a tabela 'imagens_devolucoes'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS imagens_devolucoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        devolucao_id INTEGER NOT NULL,
        url_imagem TEXT NOT NULL,
        FOREIGN KEY (devolucao_id) REFERENCES devolucoes(id)
    )
''')

# Criar a tabela 'estoque_fisico'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS estoque_fisico (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        preco REAL,
        status_estoque TEXT NOT NULL
    )
''')

# Criar a tabela 'descarte'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS descarte (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        motivo TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        preco REAL,
        imagem TEXT NOT NULL
    )
''')

# Limpar dados antigos para evitar duplicatas
cursor.execute('DELETE FROM devolucoes')
cursor.execute('DELETE FROM estoque_fisico')
cursor.execute('DELETE FROM imagens_devolucoes')

# Dados para a tabela devolucoes
devolucoes = [
    ("Tênis Esportivo XYZ", "Tamanho incorreto", "imagens/tenis.jpg", None, 2),
    ("Camiseta Algodão Básica", "Produto com defeito", "imagens/camisa.jpg", None, 1),
    ("Calça Jeans Slim", "Não serviu", "imagens/calça.jpg", None, 3),
    ("Jaqueta Corta-Vento", "Cor diferente da esperada", "imagens/JaquetaCorta-Vento.jpg", None, 1),
    ("Meia Esportiva", "Material desconfortável", "imagens/MeiaEsportiva.jpg", None, 5),
    ("Boné Casual", "Produto amassado", "imagens/BoneCasual.jpg", None, 2),
    ("Relógio Digital", "Não funcionou", "imagens/RelogioDigital.jpg", None, 1),
    ("Mochila Escolar", "Zíper com defeito", "imagens/MochilaEscolar.jpg", None, 2),
    ("Óculos de Sol", "Risco na lente", "imagens/oculosdeSol.jpg", None, 1),
    ("Ventilador Portatil", "Desisti da compra", "imagens/ventilado.jpg", None, 1),
    ("Ventilador", "Não liga", "imagens/ventilador.jpg", None, 1),
    ("Tablet", "Risco na lente", "imagens/Tablet.jpg", None, 1),
]

# Inserir devoluções
cursor.executemany('''
    INSERT INTO devolucoes (nome, motivo, imagem, preco, quantidade) VALUES (?, ?, ?, ?, ?)
''', devolucoes)

# Dados para imagens_devolucoes (múltiplas imagens)
imagens_devolucoes = [
    (1, 'imagens/tenis1.png'),
    (1, 'imagens/tenis2.png'),
    (2, 'imagens/camisa1.png'),
    (2, 'imagens/camisa2.png'),
    (3, 'imagens/calça1.png'),
    (3, 'imagens/calça2.png'),
    (4, 'imagens/JaquetaCorta-Vento1.png'),
    (5, 'imagens/MeiaEsportiva.jpg'),
    (6, 'imagens/BoneCasual.jpg'),
    (7, 'imagens/RelogioDigital.jpg'),
    (8, 'imagens/MochilaEscolar.jpg'),
    (9, 'imagens/oculosdeSol.jpg'),
    (10, 'imagens/ventilado.jpg'),
    (11, 'imagens/ventilador.jpg'),
    (12, 'imagens/Tablet.jpg')
]

cursor.executemany('''
    INSERT INTO imagens_devolucoes (devolucao_id, url_imagem) VALUES (?, ?)
''', imagens_devolucoes)

# Dados para estoque_fisico
estoque_fisico = [
    ('Camiseta Básica', 'Roupas', 50, 39.99, 'Em Estoque'),
    ('Calça Jeans', 'Roupas', 30, 89.99, 'Em Estoque'),
    ('Smartphone', 'Eletrônicos', 0, 1499.99, 'Fora de Estoque'),
    ('Fone de Ouvido', 'Eletrônicos', 15, 199.99, 'Em Estoque'),
    ('Relógio de Pulso', 'Acessórios', 8, 250.00, 'Fora de Estoque'),
    ('Jaqueta de Couro', 'Roupas', 25, 349.99, 'Em Estoque'),
    ('Boné New Era', 'Acessórios', 18, 89.90, 'Em Estoque'),
    ('Blusa de Frio', 'Roupas', 40, 129.99, 'Em Estoque'),
    ('Macbook Pro', 'Eletrônicos', 5, 12999.00, 'Em Estoque'),
    ('Xbox Series X', 'Eletrônicos', 20, 4499.99, 'Em Estoque'),
    ('PlayStation 5', 'Eletrônicos', 3, 5299.00, 'Em Estoque'),
    ('Tablet Samsung', 'Eletrônicos', 8, 1199.00, 'Em Estoque'),
    ('Smartwatch', 'Eletrônicos', 10, 799.99, 'Em Estoque'),
    ('Óculos de Sol Ray-Ban', 'Acessórios', 15, 450.00, 'Em Estoque'),
    ('Chinelo Havaianas', 'Roupas', 100, 29.90, 'Em Estoque'),
    ('Caneca Personalizada', 'Acessórios', 50, 29.90, 'Em Estoque'),
    ('Carteira de Couro', 'Acessórios', 25, 99.99, 'Em Estoque'),
    ('Perfume Masculino', 'Cosméticos', 12, 199.00, 'Em Estoque'),
    ('Perfume Feminino', 'Cosméticos', 8, 179.00, 'Em Estoque'),
    ('Shampoo Anticaspa', 'Cosméticos', 100, 19.90, 'Em Estoque'),
    ('Condicionador L\'Oréal', 'Cosméticos', 60, 29.90, 'Em Estoque'),
    ('Sabonete Dove', 'Cosméticos', 150, 8.99, 'Em Estoque'),
    ('Camiseta Estampada', 'Roupas', 70, 59.90, 'Em Estoque'),
    ('Blusa de Manga Longa', 'Roupas', 45, 79.90, 'Em Estoque'),
    ('Vestido Floral', 'Roupas', 30, 99.90, 'Em Estoque'),
    ('Meia Lupo', 'Acessórios', 150, 14.90, 'Em Estoque'),
    ('Óculos de Natação', 'Esportes', 35, 39.90, 'Em Estoque'),
    ('Raquete de Tênis', 'Esportes', 10, 199.00, 'Em Estoque'),
    ('Bolsa de Ginástica', 'Acessórios', 20, 79.90, 'Em Estoque'),
    ('Corda de Pular', 'Esportes', 40, 19.90, 'Em Estoque')
]

cursor.executemany('''
    INSERT INTO estoque_fisico (nome, categoria, quantidade, preco, status_estoque) VALUES (?, ?, ?, ?, ?)
''', estoque_fisico)

# Finalizar
conn.commit()
conn.close()

print("✅ Banco de dados criado e populado com sucesso!")
