from flask import Blueprint, render_template, url_for, request, redirect, flash, current_app
from app.extensions import db
from app.forms import NewFood, Date
from app.models import Food, Log

bp = Blueprint("bp", __name__)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    form = Date()

    if request.method == 'POST' and form.validate_on_submit():
        check = Log.query.filter_by(date=form.date.data).first()
        if not check:
            new_date = Log(date=form.date.data)
            db.session.add(new_date)
            db.session.commit()
            return redirect(url_for('bp.view', log_id=new_date.id))
        else:
            return redirect(url_for('bp.view', log_id=check.id))
        

    if Log.query.filter_by().count() > 0:
        logs = Log.query.order_by(Log.date.desc()).all()

        log_dates = []
        
        for log in logs:
            proteins = 0
            carbs = 0
            fats = 0
            calories = 0

            for food in log.foods:
                proteins += food.proteins
                carbs += food.carbs
                fats += food.fats
                calories += food.calories

            log_dates.append({
                'log_date' : log,
                'proteins' : proteins,
                'carbs' : carbs,
                'fats' : fats,
                'calories' : calories
            })

        return render_template('index.html', form=form, dates_exist=True, log_dates=log_dates)
    else:
        return render_template('index.html', form=form, dates_exist=False)


@bp.route('/view/<log_id>', methods=['GET','POST'])
def view(log_id):
    log = Log.query.get(log_id)

    if not log:
        return redirect(url_for('bp.index'))
    
    if request.method == 'GET':

        totals = {
            'protein' : 0,
            'carbs' : 0,
            'fat' : 0,
            'calories' : 0
        }

        foods = Food.query.all()

        for food in log.foods:
            totals['protein'] += food.proteins
            totals['carbs'] += food.carbs
            totals['fat'] += food.fats
            totals['calories'] += food.calories
        
        return render_template('view.html', foods=foods, log=log, totals=totals)
    

@bp.route('/add', methods=['GET', 'POST'])
def add():
    form = NewFood()

    if request.method == 'POST' and form.validate_on_submit():
        new_food = Food(name=form.food_name.data, proteins=form.proteins.data, 
                        carbs=form.carbs.data, fats=form.fats.data)
        db.session.add(new_food)
        db.session.commit()
        return redirect(url_for('bp.add'))
        
    if Food.query.filter_by().count() > 0:
        food = Food.query.all()
        return render_template('add.html', food_exists=True, form=form, food=food)
    else:
        return render_template('add.html', food_exists=False, form=form)


@bp.route('/edit_food/<food_id>', methods=['GET', 'POST'])
def edit_food(food_id):
    form = NewFood()
    food = Food.query.get(food_id)

    if not food:
        return redirect(url_for('bp.add'))

    if request.method == 'GET':
        data = food.name, food.proteins, food.carbs, food.fats
        return render_template('edit_food.html',form=form, data=data)

    if form.validate_on_submit():
        food.name = form.food_name.data
        food.proteins = form.proteins.data
        food.carbs = form.carbs.data
        food.fats = form.fats.data
        db.session.commit()
        return redirect(url_for('bp.add'))


@bp.route('/remove_food/<food_id>')
def remove_food(food_id):
    food = Food.query.get(food_id)

    if not food:
        return redirect(url_for('bp.add'))
    
    try:
        db.session.delete(food)
    except Exception as e:
        print('Something happened with db session/connection...')
        print(e)
        db.session.rollback()
    else:
        db.session.commit()

    return redirect(url_for('bp.add'))


@bp.route('/add_food_to_log/<log_id>', methods=['POST'])
def add_food_to_log(log_id):
    log = Log.query.get(log_id)

    if not log:
        return redirect(url_for('bp.index'))

    selected_food = request.form.get('food-select')

    food = Food.query.get(selected_food)

    log.foods.append(food)
    db.session.commit()

    return redirect(url_for('bp.view', log_id=log_id))


@bp.route('/remove_food_from_log/<log_id>/<food_id>')
def remove_food_from_log(log_id, food_id):
    log = Log.query.get(log_id)
    food = Food.query.get(food_id)

    if not log:
        redirect(url_for('bp.index'))

    if not food:
        redirect(url_for('bp.view', log_id=log_id))

    log.foods.remove(food)
    db.session.commit()

    return redirect(url_for('bp.view', log_id=log_id))


@bp.route('/delete_log/<log_id>')
def delete_log(log_id):
    log = Log.query.get(log_id)

    if not log:
        return redirect(url_for('bp.index'))

    db.session.delete(log)
    db.session.commit()

    return redirect(url_for('bp.index'))