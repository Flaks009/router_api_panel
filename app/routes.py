import os
from app import app
from flask import render_template, redirect
from app.router_control import reboot

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reboot', methods=['POST'])
def reboot_button():
    reboot()
    return render_template('reboot.html')

