from flask import jsonify, request, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user
from app import db
from app.blueprints.api import bp as api
from .auth import basic_auth, token_auth
from app.blueprints.api.models import Tracker
from urllib.request import urlopen
import json


@api.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})


@api.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return jsonify({'message': "User's token has been revoked"}), 204


@api.route('/tracker')
def tracker():
    context = {
        'tracker': Tracker.query.order_by(Tracker.date_created.desc()).all()
    }
    return render_template('tracker.html', **context)


@api.route('/add_tracker', methods=['POST'])
def add_tracker():
    status = request.form.get('tracker_status').lower()
    
    response = urlopen(f'https://api.coinstats.app/public/v1/coins/{status}?currency=us')
    
    data = json.loads(response.read())['coin']

    if status:
        c = Tracker(id=data['id'], name=data['name'], symbol=data['symbol'], rank=data['rank'], price=data['price'], volume=data['volume'], marketCap=data['marketCap'], availableSupply=data['availableSupply'], totalSupply=data['totalSupply'], priceChange1h=data['priceChange1h'], priceChange1d=data['priceChange1d'], priceChange1w=data['priceChange1w'], owner=current_user.get_id())
        db.session.add(c)
        db.session.commit()
        flash('You have successfully added a new cryptocurrency.', 'success')
    else:
        flash('You cannot post nothing', 'warning')
    return redirect(url_for('api.tracker'))