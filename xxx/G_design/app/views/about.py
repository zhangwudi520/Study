from flask import Blueprint, jsonify, redirect, request, abort, render_template, Response, session

ab = Blueprint('ab', __name__)


@ab.route('/about/')
def about():

    return render_template('about.html')
