# -*- coding: utf-8 -*-
__author__ = 'admin'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
import datetime
import hashlib
from flask import Flask, Blueprint, render_template, abort, request, flash, redirect, url_for
from sqlalchemy import and_, or_
from jinja2 import TemplateNotFound



park = Blueprint('park', __name__, template_folder='templates', static_folder='static')

@park.route('/park')
def ParkIndex():
    return render_template('park/parkindex.html')

#@park.route('/parkserve')
#def ParkServe():
#    return render_template('park/parkserve.html')

@park.route('/parkserve_capital')
def ParkServe_Capital():
    return render_template('park/parkserve_capital.html',name='parkserve_capital')

@park.route('/parkserve_goverappro')
def ParkServe_goverappro():
    return render_template('park/parkserve_goverappro.html',name='parkserve_goverappro')

@park.route('/parkserve_hr')
def ParkServe_hr():
    return render_template('park/parkserve_hr.html',name='parkserve_hr')

@park.route('/parkserve_ipr')
def ParkServe_ipr():
    return render_template('park/parkserve_ipr.html',name='parkserve_ipr')
@park.route('/parkserve_law')
def ParkServe_law():
    return render_template('park/parkserve_law.html',name='parkserve_law')

@park.route('/parkserve_reg')
def ParkServe_reg():
    return render_template('park/parkserve_reg.html',name='parkserve_reg')

@park.route('/parkserve_tax')
def ParkServe_tex():
    return render_template('park/parkserve_tax.html',name='parkserve_tax')



