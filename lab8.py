from flask import Blueprint, render_template, request, redirect, url_for
from db import db
from db.models import users, articles
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user 
from sqlalchemy import or_

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html', login=current_user.login if current_user.is_authenticated else 'anonymous')

@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/register.html', error='Имя пользователя не должно быть пустым')
    if not password_form:
        return render_template('lab8/register.html', error='Пароль не должен быть пустым')
    
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    return redirect('/lab8/')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember') 

    if not login_form or not password_form:
        return render_template('lab8/login.html', error='Заполните все поля')

    user = users.query.filter_by(login=login_form).first()

    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=remember_me == 'on')
        return redirect('/lab8/')
    
    return render_template('lab8/login.html', error='Ошибка входа: логин и/или пароль неверны')

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)

@lab8.route('/lab8/public_articles/')
def public_articles():
    public_list = articles.query.filter_by(is_public=True).all()
    return render_template('lab8/public_articles.html', articles=public_list)

@lab8.route('/lab8/search/', methods=['GET', 'POST'])
def search():
    query = request.form.get('query') if request.method == 'POST' else request.args.get('query')
    results = []
    
    if query:
        query_lower = query.lower()
    
        if current_user.is_authenticated:
            visibility_crit = or_(articles.is_public == True, articles.login_id == current_user.id)
        else:
            visibility_crit = (articles.is_public == True)

        accessible_articles = articles.query.filter(visibility_crit).all()

        results = [
            a for a in accessible_articles 
            if query_lower in a.title.lower() or query_lower in a.article_text.lower()
        ]
        
    return render_template('lab8/search.html', articles=results, query=query)


@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')
    
    title = request.form.get('title')
    text = request.form.get('text')
    is_public = request.form.get('is_public') == 'on'
    
    if not title or not text:
        return render_template('lab8/create_article.html', error='Заполните все поля')
    
    new_article = articles(login_id=current_user.id, title=title, article_text=text, 
                           is_favorite=False, is_public=is_public, likes=0)
    db.session.add(new_article)
    db.session.commit()
    return redirect('/lab8/articles/')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)
    if article.login_id != current_user.id:
        return redirect('/lab8/articles/')

    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)
    
    article.title = request.form.get('title')
    article.article_text = request.form.get('text')
    article.is_public = request.form.get('is_public') == 'on' 
    db.session.commit()
    return redirect('/lab8/articles/')

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)
    if article.login_id == current_user.id:
        db.session.delete(article)
        db.session.commit()
    return redirect('/lab8/articles/')

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')
    