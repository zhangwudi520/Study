from flask import Blueprint, jsonify, redirect, request, abort, render_template, Response, session

bb = Blueprint('bb', __name__)


@bb.route('/blog/')
def blog():

    return render_template('blog.html')
