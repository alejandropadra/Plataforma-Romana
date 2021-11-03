from flask import jsonify
import control_db

def response(data):
	return jsonify(
		{
			'success': True,
			'data' : data
		}
	), 200

def bad_request():
	return jsonify(
		{
			'success': False,
			'data':{},
			'messages':'Bad request',
			'code': 400
		}
	), 400