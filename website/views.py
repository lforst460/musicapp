from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note, Times
from . import db
import json
from datetime import datetime
import calendar

views = Blueprint('views', __name__)


@views.route('/<id>', methods=['GET', 'POST'])
@login_required
def home(id):
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')


    return render_template('home.html', user=current_user, notes=Note.query.filter(Note.user_id==id))

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


@views.route('/schedule/', methods=['GET', 'POST'])
@login_required
def add_times():
    cal = calendar.Calendar()
    next_month = cal.itermonthdays4(2023, 10)
    times = ['9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM']
    if request.method == 'POST':
        pass

    return render_template('times.html', user=current_user, next_month=next_month, times=times)

@views.route('/add-to-availability', methods=['POST'])
def add_to_availability():
    date_and_time = json.loads(request.data)
    print(date_and_time)
    time = date_and_time['time']
    print(date_and_time)
    date = str(str(date_and_time['month']) + '/' + str(date_and_time['day']) + '/' + str(date_and_time['year']))
    new_time = Times(date=date, time=time, user_id=current_user.id)
    db.session.add(new_time)
    db.session.commit()
    flash('Time added', category='success')
    return jsonify({})

@views.route('/remove-from-availability', methods=['POST']) 
def remove_from_availability():
    time = json.loads(request.data)
    time_to_delete = time['timeId']
    time = Times.query.get(time_to_delete)
    if time:
        if time.user_id == current_user.id:
            db.session.delete(time)
            db.session.commit()
    return jsonify({})

@views.route('/availability/<id>', methods=['GET', 'POST'])
@login_required
def view_availability(id):
    times = Times.query.filter_by(user_id=id) 
    return render_template('available_times.html', user=current_user, times=times)
