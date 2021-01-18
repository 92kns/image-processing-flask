
from flask import Flask, request, render_template, url_for, redirect, flash

from scipy import signal, ndimage
import numpy as np 
import matplotlib.pylab as plt
from pymongo import MongoClient  
import os
import glob

from PIL import Image
import base64
import io




def get_image_metadata(filename):
	# the Image.open method conveniently does not fully load the image into memory
	# thus easy to quickly grab metadata without burden if it was a really big image!
	im = Image.open(filename)
	width, height = im.size
	size = os.stat(filename).st_size //1024 #convert to kb
	file_name = os.path.basename(filename)[:-4] # hardcode -4 to remove .jpg or .png tag
	return {'imagename':file_name,
			'width':width,
			'height':height,
			'size':size}


def get_image_list():
	cwd = os.getcwd()
	im_static = 'static'
	im_path_list = glob.glob(os.path.join(cwd,im_static,'*jpg'))
	return im_path_list

# ------------ db stuff
def get_db():
	# initialize DB

	# client = MongoClient()
	client = MongoClient('mongodb://mongodb:27017/')
	db = client.imagedb
	im_path_list = get_image_list()
	meta_list = []
	for i in im_path_list:
		meta_data_dump = get_image_metadata(i)
		meta_list.append(meta_data_dump)
		db.imagedb.insert_one(meta_data_dump)
	return db, meta_list

db, meta_list = get_db()

# ------------ make app, basic
def create_app():
    app = Flask(__name__)

    return app

app = create_app()

@app.route('/',methods = ["GET","POST"])
def homePage():
	if request.method=="POST":
		max_width = request.form['max_width']
		max_height = request.form['max_height']
		# bits per pixel could be a fun query paramater in the future!
		# min_bits_per_pix = request.form['min_bits_per_pix']

		if max_width == '' or max_height == '':
			return render_template("pleasegoback.html")
		return redirect(url_for('imageBrowser', max_width = max_width, max_height=max_height))
	
	return render_template("piclist.html",data=meta_list)

@app.route('/list/max_width_<int:max_width>_max_height_<int:max_height>',methods = ["GET","POST"])
def imageBrowser(max_width,max_height):


	# query database given max height and width
	dimension_query = { 'height': {  '$lt': max_height }, 'width': {  '$lt': max_width }  }
	queryPics = db.imagedb.find(dimension_query)

	
	#option to refresh page based on new query parameters if another POST instance is received while already done querying
	if request.method=="POST":
		
		max_width = request.form['max_width']
		max_height = request.form['max_height']
		# min_bits_per_pix = request.form['min_bits_per_pix']
		if max_width == '' or max_height == '':
			# flash('BAD')
			return render_template("pleasegoback.html") 
		return redirect(url_for('imageBrowser', max_width = max_width, max_height=max_height))

	return render_template("piclist.html",data=queryPics)

@app.route('/imviewer', methods =["GET","POST"])
def imviewer():
	imagename=request.form['imagename']
	return render_template('viewimage.html', full_file = '/static/'+imagename+'.jpg')


@app.route('/image',methods = ["GET","POST"])
def imageProcessing1():
    #first form page for query parameters before going to main image processing functions
	if request.method=="POST":
		picname = request.form['imagename']
		filtertype=request.form['filtertype']
		filterval=request.form['filterval']
		return redirect(url_for("imageProcessing2", imagename = picname, filtertype = filtertype, filterval= filterval))

	return render_template("processing_form.html", data= meta_list)

@app.route('/image/<string:imagename>/<string:filtertype>/<string:filterval>',methods = ["GET","POST"])
def imageProcessing2(imagename,filtertype,filterval):
	
	#main image processing function

	path2file = os.path.join('./static',imagename+'.jpg')
	im = plt.imread(path2file)
	im.dtype='uint8' #just in case frce 0, 255 channels
	x,y,z = im.shape
	imgray=im.mean(axis=-1,keepdims=1)
	cmap_type = 'bwr'


	filterval = float(filterval)
	if request.method=="GET":
		if filtertype=='grayscale':
            # already computed above
			processed_im = imgray[:,:,0] #im.mean(axis=-1,keepdims=1)
			
			cmap_type = 'gray'

		if filtertype == 'lowpass':
			# use gaussian convolution with a provided standard deviation

		    processed_im = ndimage.gaussian_filter(input=im,sigma=filterval)

		if filtertype == 'dx':
            #gradient in x direction along each x 1D array
		    processed_im = np.zeros(im.shape)
		    for i in list(range(0,y)):
		        processed_im[:,i,0] = np.gradient(imgray[:,i,0],0.1)
		    
		    processed_im = processed_im[:,:,0]
		    

		if filtertype == 'dy':
            #gradient in y dir, along each 1d array
		    processed_im = np.zeros(im.shape)
		    for i in list(range(0,x)):
		        processed_im[i,:,0] = np.gradient(imgray[i,:,0],0.1)

		    processed_im = processed_im[:,:,0]
		   

		if filtertype == 'rotate':
            # rotation in degrees
		    processed_im = ndimage.rotate(im,filterval)
		    processed_im = processed_im[:,:,0]
		  


		# stash image in memory rather than writing to disk
		# use PIL and IO encoding
		proc_im_pil = Image.fromarray(processed_im).convert('RGB')
		data = io.BytesIO()
		proc_im_pil.save(data, "JPEG")
		encoded_img_data = base64.b64encode(data.getvalue())


	## pseudo refresh page - > option to reset results with new query-> then render filter		
	if request.method =="POST":
		picname = request.form['imagename']
		filtertype=request.form['filtertype']
		filterval=request.form['filterval']
		return redirect(url_for("imageProcessing2", imagename = picname, filtertype = filtertype, filterval= filterval))	

	# return full_filename image to server
	return render_template('imageproc.html',  img_data=encoded_img_data.decode('utf-8'),data= meta_list)

# help debug and seperate out specific exceptions
class ImageServerException(Exception):
	pass


if __name__ == '__main__':

	# app.run(debug=True)
	
	app.run(debug=True, host = '0.0.0.0')

