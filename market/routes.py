from market import app
from flask import render_template, redirect , url_for , flash, request
from market.models import Item , User
from market import db
from market.forms import Register_form, Login_form, PurchaseItem_Form, SellItem_Form
from flask_login import login_user,logout_user,login_required, current_user

@app.route('/home')
@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/market',methods=['GET','POST'])
@login_required
def market_page():
    purchaseForm=PurchaseItem_Form()
    sellForm= SellItem_Form()
    if request.method == "POST":
        purchasedItem=request.form.get('purchasedItem')
        p_item = Item.query.filter_by(name=purchasedItem).first()
        if p_item:
            if current_user.can_purchase(p_item):
                p_item.buy(current_user)
                flash("Congratulations on your purchase!",category="success")
            else:
                flash("Unfortunatesly you dont have sufficient balance",category="danger")
        s_item_name=request.form.get('soldItem')
        s_item= Item.query.filter_by(name=s_item_name).first()
        if s_item:
            if current_user.can_sell(s_item):
                s_item.sell(current_user)
                flash("Congratulations on your sale!",category="success")
            else:
                flash("Unfortunatesly you dont own the item!",category="danger")
        return redirect(url_for('market_page'))
    
    if request.method == "GET":        
        items = Item.query.filter_by(owner=None) 
        owned_items=Item.query.filter_by(owner=current_user.id)
        return render_template('market.html',items=items,purchaseForm=purchaseForm, owned_items=owned_items, sellForm=sellForm)

@app.route('/register',methods = ['GET','POST'])
def register_page():
    form = Register_form()

    if form.validate_on_submit():
        created_user = User(userName=form.userName.data, email_address=form.email_address.data, password=form.password1.data)
        db.session.add(created_user)
        db.session.commit()
        login_user(created_user)
        flash(f'Account created suucessfully! You are logged in as: {created_user.userName}',category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:  
        for err_msg in form.errors.values():
            flash(f'There was an error: {err_msg}', category = 'danger')

    return render_template('register.html',form=form)

@app.route('/login', methods=['GET','POST'])
def login_page():
    form=Login_form()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(userName=form.userName.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data): 
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.userName}',category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and Password do not match any existing user! Try again',category='danger')
    return render_template('login.html',form=form)

@app.route('/logout')
def logout_page( ):
    logout_user()
    flash("You are logged out!",category='info')
    return redirect(url_for('home_page'))

