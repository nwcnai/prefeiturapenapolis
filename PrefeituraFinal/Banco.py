import sqlite3

conexao = sqlite3.connect('banco.db')
cursor = conexao.cursor()
cursor.execute(
    'CREATE TABLE IF NOT EXISTS CamisasCAP('
    'id INTEGER PRIMARY KEY,'
    'Foto BLOB NOT NULL,'
    'NomeCamisa TEXT NOT NULL,'
    'AnoPublicacao TEXT NOT NULL,'
    'Preco TEXT NOT NULL,'
    'FreteGratis TEXT NOT NULL)'
)