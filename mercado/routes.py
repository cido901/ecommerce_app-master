from mercado import app
from flask import render_template, redirect, url_for, flash, request
from mercado.models import Item, User
from mercado.forms import CadastroForm, LoginForm, CompraProdutoForm, VendaProdutoForm
from mercado import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def page_home():
    # Renderiza o template com o formulário        
    return render_template("home.html")


@app.route('/produtos', methods=['GET', 'POST'])
@login_required
def page_produtos():
    compra_form = CompraProdutoForm()
    venda_form = VendaProdutoForm()
    if request.method == 'POST':
        # Processa a compra de um produto
        compra_produto = request.form.get('compra_produto')
        produto_obj = Item.query.filter_by(nome=compra_produto).first()
        if produto_obj:
            if current_user.compra_disponivel(produto_obj):
                produto_obj.compra(current_user)
                flash(f'Produto {produto_obj.nome} comprado com sucesso!', category='success')
            else:
                flash(f'Saldo insuficiente para comprar este produto {produto_obj.nome}.', category="danger")
    # Processa a venda de um produto
        venda_produto = request.form.get('venda_produto')
        produto_obj_venda = Item.query.filter_by(nome=venda_produto).first()
        if produto_obj_venda:
            if current_user.venda_disponivel(produto_obj_venda):
                produto_obj_venda.vender(current_user)
                flash(f'Produto {produto_obj_venda.nome} vendido com sucesso!', category='success')
            else:
                flash(f'Você não é o dono deste produto {produto_obj_venda.nome}.', category="danger")
        return redirect(url_for('page_produtos'))
    if request.method == 'GET':
        itens = Item.query.filter_by(dono=None)
        dono_itens = Item.query.filter_by(dono=current_user.id)
        return render_template("produtos.html", itens=itens, compra_form=compra_form, dono_itens=dono_itens, venda_form=venda_form)

@app.route('/cadastro', methods=['GET', 'POST'])
def page_cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        usuario = User(
            usuario = form.usuario.data,
            email = form.email.data,
            senha_hash = form.senha1.data
        )
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('page_produtos'))
    if form.errors != {}:
        for error in form.errors.values():
            flash(f'Erro no formulário: {error}')
    # Renderiza o template com o formulário        
    return render_template("cadastro.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def page_login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario_logado = User.query.filter_by(usuario=form.usuario.data).first()
        if usuario_logado and usuario_logado.converte_senha(senha_texto_claro=form.senha.data):
            login_user(usuario_logado)
            flash(f'Login realizado com sucesso para {usuario_logado.usuario}!', category='success') 
            return redirect(url_for('page_produtos'))
        else:
            flash('Usuário ou senha inválidos.')
    if form.errors != {}:
        for error in form.errors.values():
            flash(f'Erro no formulário: {error}')
    # Renderiza o template com o formulário        
    return render_template("login.html", form=form)

@app.route('/logout')
def page_logout():
    logout_user()
    flash('Logout realizado com sucesso!', category='info')
    return redirect(url_for('page_home'))

