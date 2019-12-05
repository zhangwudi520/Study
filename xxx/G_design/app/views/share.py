from flask import Blueprint, jsonify, redirect, request, abort, render_template, Response, session

sb = Blueprint('sb', __name__)


@sb.route('/share/')
def share():

    return render_template('share.html')
