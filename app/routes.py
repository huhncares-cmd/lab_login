from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
import flask_bcrypt

from app.tools import is_valid_ip_address, jsonify

from app import *

import requests

@app.route('/')
def index():
    if current_user.is_authenticated:
        esps = ESP.query.all()
        program_configs = ProgramConfig.query.filter_by(name=current_user.name).all()
        return render_template('pages/index.html', user=current_user, program_configs=program_configs, esps=esps)
    return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error=""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        user = User.query.filter_by(name=username).first()
        try:
            if user and flask_bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
        except Exception:
            error = "Fehler beim Login."
        error = "Nutzername oder Passwort falsch."
    return render_template('pages/user_mgmt/login.html', error=error)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = ""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        if password != password_confirm:
            error = "Die Passwörter stimmen nicht überein."
        elif password == "" or username == "":
            error = "Die Felder dürfen nicht leer sein."
        elif User.query.filter_by(name=username).first():
            error = "Der Nutzer existiert bereits."
        else:
            user = User(name=username, password=flask_bcrypt.generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
    return render_template('pages/user_mgmt/register.html', error=error)

@app.route('/logout/')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('login'))

@app.route('/program_config/update/')
def update_program_config():
    if current_user.is_authenticated:
        programs = [
            "chrome",
            "firefox",
            "tronxyslicer",
            "pronterface",
            "thonny",
            "vscode"
        ]
        # get all get names
        program_config_name = request.args.getlist('name')
        esp = request.args.get('esp')
        esp = ESP.query.filter_by(name=esp).first()
        if esp == None:
            return {"error": "ESP does not exist."}
        
        for name in program_config_name:
            if name not in programs:
                if name == "":
                    continue
                return {"error": "Invalid program name."}
            
        program_config = ProgramConfig.query.filter_by(name=current_user.name, esp_name=esp.name).first()
        
        if program_config == None:
            program_config = ProgramConfig(name=current_user.name, esp_name=esp.name, configured_programs=','.join(program_config_name))
            db.session.add(program_config)
            db.session.commit()
            return {"success": "Program config created."}
        program_config.configured_programs = ','.join(program_config_name)
        db.session.commit()
        return {"success": "Program config updated."}
    return redirect(url_for('login'))

@app.route('/workspace/start/')
def start_workspace():
    if current_user.is_authenticated:
        esp=request.args.get('esp')
        if esp != None and ESP.query.filter_by(name=esp).first() != None:
            esp = ESP.query.filter_by(name=esp).first()
            programs = ProgramConfig.query.filter_by(name=current_user.name, esp_name=esp.name).first()
            programs = programs.configured_programs.split(',')
            content = jsonify(programs)
            try:
                requests.post(f"http://{esp.ip_address}", timeout=5, json=content)
            except Exception as e:
                db.session.delete(esp)
                program_config = ProgramConfig.query.filter_by(esp_name=esp.name).all()
                for config in program_config:
                    db.session.delete(config)
                db.session.commit()
                return {"error": "ESP not reachable."}
            return {"success": "Workspace started."}
        return {"error": "Missing arguments."}
    return redirect(url_for('login'))

@app.route('/workspace/stop/')
def stop_workspace():
    if current_user.is_authenticated:
        esp = request.args.get('esp')
        if esp != None and ESP.query.filter_by(name=esp).first() != None:
            esp = ESP.query.filter_by(name=esp).first()
            try:
                requests.post(f"http://{esp.ip_address}/stop", timeout=5)
            except Exception as e:
                db.session.delete(esp)
                program_config = ProgramConfig.query.filter_by(esp_name=esp.name).all()
                for config in program_config:
                    db.session.delete(config)
                db.session.commit()
                return {"error": "ESP not reachable."}
            return {"success": "Workspace stopped."}
        return {"error": "Missing arguments."}
    return redirect(url_for('login'))

@app.route('/create_esp/')
def create_esp():
    esp_name = request.args.get('name')
    esp_ip = request.args.get('ip')
    if esp_name == None or esp_ip == None:
        return {"error": "Missing arguments."}
    if not is_valid_ip_address(esp_ip):
        return {"error": "Invalid IP address."}
    if ESP.query.filter_by(name=esp_name).first():
        return {"error": "ESP already exists."}
    if ESP.query.filter_by(ip_address=esp_ip).first():
        return {"error": "IP address already exists."}
    esp = ESP(name=esp_name, ip_address=esp_ip)
    db.session.add(esp)
    db.session.commit()
    return {"success": "ESP created."}

@app.route('/delete_esp/')
def delete_esp():
    esp_name = request.args.get('name')
    if esp_name == None:
        return {"error": "Missing arguments."}
    esp = ESP.query.filter_by(name=esp_name).first()
    if esp == None:
        return {"error": "ESP does not exist."}
    db.session.delete(esp)
    program_config = ProgramConfig.query.filter_by(esp_name=esp_name).all()
    for config in program_config:
        db.session.delete(config)
    db.session.commit()
    return {"success": "ESP deleted."}