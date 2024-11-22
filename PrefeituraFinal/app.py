from flask import Flask, render_template, request, g, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = 'ChaveSecretaPrefeitura'

def ligar_banco():
    banco = g._database = sqlite3.connect('banco.db')
    return banco

# ⬇️ ROTAS INICIAIS ⬇️ ------------------------------------------------------------------------------------------------#
@app.route('/')
def inicio():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT id, Imagem, Titulo, Descricao, Autor, DataPublicacao FROM Noticias')
    Noticias = cursor.fetchall()
    return render_template('inicio.html', titulo='Prefeitura Penápolis', Noticias=Noticias)

@app.route('/administracao')
def administracao():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT id, Foto, Nome, Partido, Funcao, Email FROM Politicos')
    Politicos = cursor.fetchall()

    cursor.execute('SELECT id, Foto, Nome, Funcao FROM Prefeitos')
    Prefeitos = cursor.fetchall()
    return render_template('administracao.html', titulo='Administração de Penápolis', Politicos=Politicos, Prefeitos=Prefeitos)

@app.route('/planejamento')
def planejamento():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT id, Foto, Titulo, Descricao FROM Planejamentos')
    Planejamentos = cursor.fetchall()
    return render_template('planejamento.html', titulo='Obras de Penápolis', Planejamentos=Planejamentos)

@app.route('/contato')
def contato():
    return render_template('contato.html', titulo='Contatos da Prefeitura')

@app.route('/penapolenseshop')
def penapolenseshop():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT id, Foto, NomeCamisa, AnoPublicacao, Preco, FreteGratis FROM CamisasCAP')
    Camisas = cursor.fetchall()
    return render_template('penapolenseshop.html', titulo='Penapolense Shopping', Camisas=Camisas)

# ⬇️ ROTAS PARA EDIÇÃO ⬇️ ---------------------------------------------------------------------------------------------#
@app.route('/editaradministracao')
def editaradministracao():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT id, Foto, Nome, Partido, Funcao, Email FROM Politicos')
    Politicos = cursor.fetchall()

    cursor.execute('SELECT id, Foto, Nome, Funcao FROM Prefeitos')
    Prefeitos = cursor.fetchall()

    return render_template('visualizaradministracao.html', titulo='Visualizar Administração', Politicos=Politicos, Prefeitos=Prefeitos)

@app.route('/editarPolitico/<int:id>', methods=['GET', 'POST'])
def editarPolitico(id):
    banco = ligar_banco()
    cursor = banco.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        partido = request.form['partido']
        funcao = request.form['funcao']
        nova_imagem = request.files.get('nova_imagem')

        if nova_imagem:
            foto_blob = nova_imagem.read()
            cursor.execute('UPDATE Politicos SET Foto = ?, Nome = ?, Partido = ?, Funcao = ? WHERE id = ?',
                           (foto_blob, nome, partido, funcao, id))
        else:
            cursor.execute('UPDATE Politicos SET Nome = ?, Partido = ?, Funcao = ? WHERE id = ?',
                           (nome, partido, funcao, id))

        banco.commit()
        return redirect('/editaradministracao')

    cursor.execute('SELECT id, Nome, Partido, Funcao FROM Politicos WHERE id = ?', (id,))
    politico = cursor.fetchone()
    return render_template('editarpolitico.html', politico=politico)

@app.route('/editarPrefeito/<int:id>', methods=['GET', 'POST'])
def editarPrefeito(id):
    banco = ligar_banco()
    cursor = banco.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        funcao = request.form['funcao']
        nova_imagem = request.files.get('nova_imagem')

        if nova_imagem:
            foto_blob = nova_imagem.read()
            cursor.execute('UPDATE Prefeitos SET Foto = ?, Nome = ?, Funcao = ? WHERE id = ?',
                           (foto_blob, nome, funcao, id))
        else:
            cursor.execute('UPDATE Prefeitos SET Nome = ?, Funcao = ? WHERE id = ?',
                           (nome, funcao, id))

        banco.commit()
        return redirect('/editaradministracao')

    cursor.execute('SELECT id, Nome, Funcao FROM Prefeitos WHERE id = ?', (id,))
    prefeito = cursor.fetchone()
    return render_template('editarprefeito.html', prefeito=prefeito)

@app.route('/editarPlanejamento/<int:id>', methods=['GET', 'POST'])
def editarPlanejamento(id):
    banco = ligar_banco()
    cursor = banco.cursor()

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        nova_imagem = request.files.get('nova_imagem')

        if nova_imagem:
            foto_blob = nova_imagem.read()
            cursor.execute('UPDATE Planejamentos SET Foto = ?, Titulo = ?, Descricao = ? WHERE id = ?',
                           (foto_blob, titulo, descricao, id))
        else:
            cursor.execute('UPDATE Planejamentos SET Titulo = ?, Descricao = ? WHERE id = ?',
                           (titulo, descricao ,id))

        banco.commit()
        return redirect('/visualizarplanejamento')

    cursor.execute('SELECT id, Foto, Titulo, Descricao FROM Planejamentos WHERE id = ?', (id,))
    planejamento = cursor.fetchone()
    return render_template('editarplanejamento.html', planejamento=planejamento)

@app.route('/editarNoticia/<int:id>', methods=['GET', 'POST'])
def editarNoticia(id):
    banco = ligar_banco()
    cursor = banco.cursor()

    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        autor = request.form['autor']
        datapublicacao = request.form['datapublicacao']
        nova_imagem = request.files.get('nova_imagem')

        if nova_imagem:
            foto_blob = nova_imagem.read()
            cursor.execute('UPDATE Noticias SET Imagem = ?, Titulo = ?, Descricao = ?, Autor = ?, DataPublicacao = ? WHERE id = ?',
                           (foto_blob, titulo, descricao, autor, datapublicacao, id))
        else:
            cursor.execute('UPDATE Noticias SET Titulo = ?, Descricao = ?, Autor = ?, DataPublicacao = ? WHERE id = ?',
                           (titulo, descricao, autor, datapublicacao,id))

        banco.commit()
        return redirect('/visualizarnoticia')

    cursor.execute('SELECT id, Imagem, Titulo, Descricao, Autor, DataPublicacao FROM Noticias WHERE id = ?', (id,))
    noticia = cursor.fetchone()
    return render_template('editarnoticia.html', noticia=noticia)

@app.route('/editarFuncionario/<int:id>', methods=['GET', 'POST'])
def editarFuncionario(id):
    banco = ligar_banco()
    cursor = banco.cursor()

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        nome = request.form['nome']

        cursor.execute('UPDATE Funcionarios SET Email, Senha, Nome = ? WHERE id = ?',
                        (email,senha,nome, id))

        banco.commit()
        return redirect('/visualizarfuncionario')

    cursor.execute('SELECT id, Email, Senha, Nome FROM Funcionarios WHERE id = ?', (id,))
    funcionario = cursor.fetchone()
    return render_template('editarfuncionario.html', funcionario=funcionario)

@app.route('/editarCamisasCAP/<int:id>', methods=['GET', 'POST'])
def editarCamisasCAP(id):
    banco = ligar_banco()
    cursor = banco.cursor()

    if request.method == 'POST':
        foto = request.files['foto']
        foto_blob = foto.read()
        nomecamisa = request.form['nomecamisa']
        anopublicacao = request.form['anopublicacao']
        preco = request.form['preco']
        fretegratis = request.form['fretegratis']

        cursor.execute(
            'UPDATE CamisasCAP SET Foto = ?, NomeCamisa = ?, AnoPublicacao = ?, Preco = ?, FreteGratis = ? WHERE id = ?',
            (foto_blob, nomecamisa, anopublicacao, preco, fretegratis, id))

        banco.commit()
        return redirect('/visualizarcamisacap')

    cursor.execute('SELECT id, Foto, NomeCamisa, AnoPublicacao, Preco, FreteGratis FROM CamisasCAP WHERE id = ?', (id,))
    camisa = cursor.fetchone()
    return render_template('editarcamisacap.html', camisa=camisa)

# ⬇️ ROTAS PARA CADASTRO ⬇️ -------------------------------------------------------------------------------------------#
@app.route('/cadpolitico')
def cadpolitico():
    return render_template('cadpolitico.html', titulo='Cadastro de Políticos')

@app.route('/cadpoliticoform', methods=['GET', 'POST'])
def cadpoliticoform():
    if request.method == 'POST':
        nome = request.form['nome']
        partido = request.form['partido']
        funcao = request.form['funcao']
        email = request.form['email']
        foto = request.files['foto']
        foto_blob = foto.read()

        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute('INSERT INTO Politicos (nome, partido, funcao, email, foto) VALUES (?, ?, ?, ?, ?)', (nome, partido, funcao, email, foto_blob))
        banco.commit()
        return redirect('/homefuncionario')
    return render_template('cadpolitico.html', titulo='Cadastro de Políticos')

@app.route('/cadfuncionario')
def cadfuncionario():
    return render_template('cadfuncionario.html', titulo='Cadastro de Funcionários')

@app.route('/cadfuncionarioform', methods=['GET', 'POST'])
def cadfuncionarioform():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        nome = request.form['nome']

        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute('INSERT INTO Funcionarios (email, senha, nome) VALUES (?, ?, ?)', (email, senha, nome))
        banco.commit()
        return redirect('/homefuncionario')
    return render_template('cadfuncionario.html', titulo='Cadastro de Funcionários')

@app.route('/cadnoticia')
def cadnoticia():
    return render_template('cadnoticia.html', titulo='Cadastro de Notícias')

@app.route('/cadnoticiaform', methods=['GET', 'POST'])
def cadnoticiaform():
    if request.method == 'POST':
        imagem = request.files['imagem']
        foto_blob = imagem.read()
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        autor = request.form['autor']
        datapublicacao = request.form['datapublicacao']

        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute('INSERT INTO Noticias (Imagem, Titulo, Descricao, Autor, DataPublicacao) VALUES (?, ?, ?, ?, ?)', (foto_blob, titulo, descricao, autor, datapublicacao))
        banco.commit()
        return redirect('/homefuncionario')
    return render_template('cadnoticia.html', titulo='Cadastro de Notícias')

@app.route('/cadplanejamento')
def cadplanejamento():
    return render_template('cadplanejamento.html', titulo='Cadastro de planejamentos')

@app.route('/cadplanejamentoform', methods=['GET', 'POST'])
def cadplanejamentoform():
    if request.method == 'POST':
        imagem = request.files['imagem']
        foto_blob = imagem.read()
        titulo = request.form['titulo']
        descricao = request.form['descricao']

        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute('INSERT INTO Planejamentos (Foto, Titulo, Descricao) VALUES (?, ?, ?)', (foto_blob, titulo, descricao))
        banco.commit()
        return redirect('/homefuncionario')
    return render_template('cadplanejamento.html', titulo='Cadastro de planejamentos')

@app.route('/cadcamisacap')
def cadcamisacap():
    return render_template('cadcamisacap.html', titulo='Cadastro de Camisas')

@app.route('/cadcamisacapform', methods=['GET', 'POST'])
def cadcamisacapform():
    if request.method == 'POST':
        foto = request.files['foto']
        foto_blob = foto.read()
        nomecamisa = request.form['nomecamisa']
        anopublicacao = request.form['anopublicacao']
        preco = request.form['preco']
        fretegratis = request.form['fretegratis']

        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute('INSERT INTO CamisasCAP (Foto, NomeCamisa, AnoPublicacao, Preco, FreteGratis) VALUES (?, ?, ?, ?, ?)', (foto_blob, nomecamisa, anopublicacao, preco, fretegratis))
        banco.commit()
        return redirect('/homefuncionario')
    return render_template('cadcamisacap.html', titulo='Cadastro de Camisas')

# ⬇️ ROTAS PARA EXCLUIR ⬇️ --------------------------------------------------------------------------------------------#
@app.route('/excluirpolitico/<int:id>', methods=['GET'])
def excluirpolitico(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('DELETE FROM Politicos WHERE id = ?', (id,))
    banco.commit()
    return redirect('/editaradministracao')

@app.route('/excluirplanejamento/<int:id>', methods=['GET'])
def excluirplanejamento(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('DELETE FROM Planejamentos WHERE id = ?', (id,))
    banco.commit()
    return redirect('/visualizarplanejamento')

@app.route('/excluirfuncionario/<int:id>', methods=['GET'])
def excluirfuncionario(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('DELETE FROM Funcionarios WHERE id = ?', (id,))
    banco.commit()
    return redirect('/visualizarfuncionario')

@app.route('/excluirnoticia/<int:id>', methods=['GET'])
def excluirnoticia(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('DELETE FROM Noticias WHERE id = ?', (id,))
    banco.commit()
    return redirect('/visualizarnoticia')

@app.route('/excluircamisasCAP/<int:id>', methods=['GET'])
def excluircamisasCAP(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('DELETE FROM CamisasCAP WHERE id = ?', (id,))
    banco.commit()
    return redirect('/visualizarcamisacap')

# ⬇️ ROTAS PARA VISUALIZAR ⬇️ -----------------------------------------------------------------------------------------#
@app.route('/visualizarnoticia')
def visualizarnoticia():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT id, Imagem, Titulo, Descricao, Autor, DataPublicacao FROM Noticias')
    Noticias = cursor.fetchall()
    return render_template('visualizarnoticia.html', titulo='Notícias de Penápolis', Noticias=Noticias)

@app.route('/visualizarplanejamento')
def visualizarplanejamento():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT id, Foto, Titulo, Descricao FROM Planejamentos')
    Planejamentos = cursor.fetchall()

    return render_template('visualizarplanejamento.html', titulo='Obras de Penápolis', Planejamentos=Planejamentos)

@app.route('/visualizarfuncionario')
def visualizarfuncionario():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT id, Email, Senha, Nome FROM Funcionarios')
    Funcionarios = cursor.fetchall()

    return render_template('visualizarfuncionario.html', titulo='Visualizar funcionários', Funcionarios=Funcionarios)

@app.route('/visualizarcamisacap')
def visualizarcamisacap():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT id, Foto, NomeCamisa, AnoPublicacao, Preco, FreteGratis FROM CamisasCAP')
    Camisas = cursor.fetchall()
    return render_template('visualizarcamisacap.html', titulo='Camisas - CAP', Camisas=Camisas)

# ⬇️ ROTAS PARA LOGIN ⬇️ ----------------------------------------------------------------------------------------------#
@app.route('/login')
def login():
    return render_template('login.html', titulo='Autenticação da Prefeitura')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = request.form['email']
    senha = request.form['senha']

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT Senha, Nome FROM Funcionarios WHERE Email = ?;', (usuario,))
    person = cursor.fetchone()

    if person and person[0] == senha:
        session['usuario'] = usuario
        session['nome'] = person[1]
        return redirect('/homefuncionario')
    else:
        return render_template('Login.html', MensagemError='Usuário ou senha incorretos, tente novamente!')

@app.route('/homefuncionario')
def homefuncionario():
    return render_template('homefuncionario.html', titulo='Servidor Público - Home')

# ⬇️ ROTAS IMAGEM FETCHONE ⬇️ -----------------------------------------------------------------------------------------#
@app.route('/imagemFETCHONEAPP/<int:id>')
def imagem_fetchoneapp(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT Imagem FROM Noticias WHERE id = ?', (id,))
    imagem = cursor.fetchone()

    if imagem:
        return imagem[0], 200, {'Content-Type': 'image/jpeg'}
    else:
        return "Imagem não encontrada", 404

@app.route('/imagemFETCHONEPREFEITOS/<int:id>')
def imagem_fetchoneprefeitos(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT Foto FROM Prefeitos WHERE id = ?', (id,))
    imagem = cursor.fetchone()
    if imagem:
        return imagem[0], 200, {'Content-Type': 'image/jpeg'}
    else:
        return "Imagem não encontrada", 404

@app.route('/imagemFETCHONEVEREADOR/<int:id>')
def imagem_fetchonevereador(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT Foto FROM Politicos WHERE id = ?', (id,))
    imagem = cursor.fetchone()
    if imagem:
        return imagem[0], 200, {'Content-Type': 'image/jpeg'}
    else:
        return "Imagem não encontrada", 404

@app.route('/imagemFETCHONEPLANEJAMENTO/<int:id>')
def imagem_fetchoneplanejamento(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT Foto FROM Planejamentos WHERE id = ?', (id,))
    imagem = cursor.fetchone()

    if imagem:
        return imagem[0], 200, {'Content-Type': 'image/jpeg'}
    else:
        return "Imagem não encontrada", 404

@app.route('/imagemFETCHONECAMISACAP/<int:id>')
def imagem_fetchonecamisacap(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT Foto FROM CamisasCAP WHERE id = ?', (id,))
    imagem = cursor.fetchone()

    if imagem:
        return imagem[0], 200, {'Content-Type': 'image/jpeg'}
    else:
        return "Imagem não encontrada", 404

# ⬇️ OUTRAS ROTAS ⬇️ --------------------------------------------------------------------------------------------------#
@app.route('/saibamais/<int:id>')
def saibamais(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT Titulo, Descricao, Autor, DataPublicacao, Imagem, id FROM Noticias WHERE id = ?', (id,))
    noticia = cursor.fetchone()

    print(noticia)

    if noticia:
        return render_template('saibamais.html', titulo=noticia[0], noticia=noticia)
    else:
        return "Notícia não encontrada", 404

if __name__ == '__main__':
    app.run()
