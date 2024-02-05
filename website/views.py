from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Event
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash("Note is too short!", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category="success")

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})

@views.route('/my-events', methods=["GET"])
@login_required
def my_events():
    return render_template("my-events.html", user=current_user)

@views.route('/calendar', methods=['GET'])
@login_required
def calendar():
    data = Event.query.all()
    #remove current user after fixing code in calendar.html
    return render_template("calendar.html", user=current_user, data=data)

@views.route('/submitevent', methods=["GET", "POST"])
@login_required
def submission():
    if request.method == 'POST':
        name = request.form.get('name')
        event_date = request.form.get('event_date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        description = request.form.get('description')

        # implement some restrictions here with if statements to restrict data types
        new_event = Event(name=name, event_date=event_date, start_time=start_time, end_time=end_time, description=description, user_id=current_user.id)
        db.session.add(new_event)
        db.session.commit()
        flash("Event Added!", category="success!")

    return render_template("submitevent.html", user=current_user)
