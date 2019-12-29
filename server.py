from flask import Flask, jsonify, request
from custom_code import image_converter
import pickle
#from extract import image
import os
import base64
app = Flask(__name__)

app.config['SECRET_KEY'] = '7eaa32bfa81cf2b06a62f030764f238d'

@app.route('/', methods=['GET','POST'])
def index():
	print(request.method)
	file = request.files['file']
	x = request.get_data()
	print(x)
	file.save('test.jpg')
	image = open('test.jpg', 'rb')
	image_read = image.read()
	image_data = base64.encodebytes(image_read)
	print(image_data)
	#image_data = request_data.split(';base64,')
	image_array, err_msg = image_converter.convert_image(image_data)
	if err_msg == None :
		model_file = f"cnn_model.pkl"
		saved_classifier_model = pickle.load(open(model_file,'rb'))
		prediction = saved_classifier_model.predict(image_array) 
		label_binarizer = pickle.load(open(f"label_transform.pkl",'rb'))
	
	return jsonify({
		'status code': 200,
		'message': 'ok',
		'body': {
			"error" : "0",
			"data" : f"{label_binarizer.inverse_transform(prediction)[0]}"
		}
	})


app.run(host="127.0.0.1",port=5000,threaded=False)