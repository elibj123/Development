from flask import Flask, jsonify

app = Flask(__name__)

zayanim = [
		{
			'id':1,
			'name':u'Eli Baranskiy',
			'zayan':u'zayan'
		},
		{
			'id':2,
			'name':u'Jacob Roginsky',
			'zayan':u'zayan'
		},
		{
			'id':3,
			'name':u'Arthur Azrieli',
			'zayan':u'zayan'
		}
			];
@app.route('/zayanim',methods=['GET'])
def get_zayanim():
	return jsonify({'zayanim':zayanim});

if __name__ == '__main__':
    app.run(debug=True)