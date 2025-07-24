from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import length, EqualTo, Email, DataRequired, ValidationError
from mercado.models import User

class CadastroForm(FlaskForm):
  def validate_usuario(self, check_user):
    user = User.query.filter_by(usuario=check_user.data).first()
    if user:
      raise ValidationError('Usuário já cadastrado. Por favor, escolha outro nome de usuário.')
  def validate_email(self, check_email):
    email = User.query.filter_by(email=check_email.data).first()
    if email:
      raise ValidationError('E-mail já cadastrado. Por favor, escolha outro e-mail.') 
  def validate_senha(self, check_senha):
    if len(check_senha.data) < 6:
      raise ValidationError('A senha deve ter pelo menos 6 caracteres.')
    senha_existente = User.query.filter_by(senha=check_senha.data).first()
    if senha_existente:
      raise ValidationError('Senha já existe! Cadastre outra senha.')
  usuario = StringField(label='Username:', validators=[length(min=2, max=30), DataRequired()])
  email = StringField(label='E-mail:', validators=[Email(message='E-mail inválido'), DataRequired()])
  senha1 = PasswordField(label='Senha:', validators=[length(min=6), DataRequired()])
  senha2 = PasswordField(label='Confirmação de Senha:', validators=[EqualTo('senha1', message='As senhas devem ser iguais'), DataRequired()])
  submit = SubmitField(label='Cadastrar')

class LoginForm(FlaskForm):
    usuario = StringField(label='Usuário:', validators=[DataRequired()])
    senha = PasswordField(label='Senha:', validators=[DataRequired()])
    submit = SubmitField(label='Log In')

class CompraProdutoForm(FlaskForm):
    submit = SubmitField(label= "Comprar Produto!")

class VendaProdutoForm(FlaskForm):
    submit = SubmitField(label= "Vender Produto!")