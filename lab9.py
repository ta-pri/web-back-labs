from flask import Blueprint, render_template, request, session, jsonify
from flask_login import current_user # Импортируем для проверки авторизации
import random

lab9 = Blueprint('lab9', __name__)

greetings = [
    "Счастья, здоровья и исполнения всех желаний в Новом Году!",
    "Пусть 2026 год принесет только яркие эмоции и море позитива!",
    "Желаю успехов в учебе, легких сессий и крутых проектов!",
    "Пусть каждый день Нового года будет наполнен радостью и смехом!",
    "Желаю найти под елкой именно то, о чем давно мечталось!",
    "Крепкого здоровья, удачи во всех начинаниях и верных друзей!",
    "Пусть в вашем доме всегда царят уют, тепло и взаимопонимание!",
    "Желаю новых свершений, великих побед и финансового благополучия!",
    "Пусть новогодняя ночь превратит вашу жизнь в настоящую сказку!",
    "Желаю неиссякаемого вдохновения и творческих успехов в будущем году!"
]

gifts_data = []
for i in range(10):
    gifts_data.append({
        'id': i,
        'box_img': f'box{i+1}.png',
        'gift_img': f'gift{i+1}.png',
        'greeting': greetings[i],
        'is_empty': False,
        'is_for_auth': i % 2 == 0, 
        'left': random.randint(5, 85),
        'top': random.randint(10, 70)
    })

@lab9.route('/lab9/')
def main():
    unopened = len([g for g in gifts_data if not g['is_empty']])
    return render_template('lab9/index.html', gifts=gifts_data, unopened=unopened)

@lab9.route('/lab9/open_box', methods=['POST'])
def open_box():
    data = request.json
    idx = data.get('box_id')
    gift = gifts_data[idx]

    if gift['is_for_auth'] and not current_user.is_authenticated:
        return jsonify({
            'success': False, 
            'message': 'Этот подарок только для зарегистрированных пользователей! Пожалуйста, войдите в систему.'
        })

    if 'opened_count' not in session:
        session['opened_count'] = 0
        
    if session['opened_count'] >= 3:
        return jsonify({'success': False, 'message': 'Вы уже открыли 3 коробки!'})
        
    if not gift['is_empty']:
        gift['is_empty'] = True
        session['opened_count'] += 1
        return jsonify({
            'success': True,
            'image': f'/static/lab9/{gift["gift_img"]}',
            'text': gift['greeting'],
            'remaining': len([g for g in gifts_data if not g['is_empty']])
        })
    return jsonify({'success': False, 'message': 'Эта коробка уже пуста!'})

@lab9.route('/lab9/reset', methods=['POST'])
def reset_all():
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': 'Только Дед Мороз (авторизованный пользователь) может это делать!'})
    
    for gift in gifts_data:
        gift['is_empty'] = False
    
    session['opened_count'] = 0 
    return jsonify({'success': True})