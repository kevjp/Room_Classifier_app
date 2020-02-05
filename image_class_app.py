from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import classify_module
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

UPLOAD_FOLDER = '/Users/kevinryan/Documents/DataScienceMSc/Rightmove/Rightmove/Flask_app/static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# model = '/Users/kevinryan/Documents/DataScienceMSc/Rightmove/Results_google_images_resnet_classifiers/grid_searches/folder_2019-11-15_inception_resnet_alldata/resnet_classifier'
model = './classifier/resnet_classifier'
labelbin = './classifier/binerizer_object'
classify = classify_module.Classify_image(model, labelbin)

graph = tf.get_default_graph()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # print("check",request.form['file'])
        print("check2",request.files)
        # check if the post request has the file part
        if 'image_url' not in request.files:
            flash('No file part')
            return redirect(request.url)
        # file = request.form['file']
        file = request.files['image_url']
        print("check3",file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # print("check1",classify)
            # classify = Classify_image(model, labelbin)
            classify.load_image(full_path)
            global graph
            with graph.as_default():
                labels = classify.classify_image()
            return render_template("output.html", img_url = file.filename, labels = labels)
    else:
        return render_template('image_url_input.html', form=request.form)
    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    #   <input type=file name=file>
    #   <input type=submit value=Upload>
    # </form>
    # '''


# class ReusableForm(Form):

image_url = TextField('Name:', validators=[validators.required()])


# @app.route("/", methods=['GET', 'POST'])
# def classify_im():
#     # form = ReusableForm(request.form)

#     model = '/Users/kevinryan/Documents/DataScienceMSc/Rightmove/Results_google_images_resnet_classifiers/grid_searches/folder_2019-11-15_inception_resnet_alldata/resnet_classifier'
#     labelbin = '/Users/kevinryan/Documents/DataScienceMSc/Rightmove/Results_google_images_resnet_classifiers/grid_searches/folder_2019-11-15_inception_resnet_alldata/binerizer_object'

#     # print(request.form.errors)
#     if request.method == 'POST':
#         image_url=request.form['image_url']
#         print(image_url)
#         print("check",request.form['image_url'])
#         return render_template("output.html", img_url = request.form['image_url'])

#     if request.method == 'GET':
#         # Save the comment here.
#         # classify = Classify_image(model, labelbin, image_url)
#         # classify.load_image()
#         # classify.classify_image()
#         return render_template('image_url_input.html', form=request.form)

#     # else:
#     #     print("nothing entered")
#     #     flash('All the form fields are required. ')
#     #     return render_template('image_url_input.html', form=form)

# @app.route("/output")
# def output():

#     return render_template("output.html", te = request.form['image_url'])





if __name__ == '__main__':
    app.run(host='0.0.0.0', use_reloader=False)
