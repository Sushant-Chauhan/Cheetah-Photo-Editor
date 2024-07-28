# pip install flask opencv-python
import os, cv2
from flask import Flask,render_template, request, redirect, url_for,flash, session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "23#$rt54%%nfvdi*7&&jnsf"

@app.route('/')
def home():
    # return render_template("index.html")
    message = session.pop('message', None)
    image_url = session.pop('image_url', None)
    return render_template("index.html", message=message, image_url=image_url)

@app.route('/create')
def create():
    return render_template("create.html")

@app.route('/guide')
def guide():
    return render_template("guide.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

# Processing of - Operation on Image
def processImage(filename, operation):
    print(f"The Filename is = {filename} & Operation is {operation}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
            newFilename = f"static/{filename}" 
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        
        case "cwebp": 
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        
        case "cjpg":
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        
        case "cpng":
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
    
# Form Submit
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS   #checking 2 conditions- filename contains . and file is from allowed extensions

@app.route('/editing', methods = ['GET','POST'])
def edit():
    if request.method=='POST':
        # return "This is a POST request" 
        operation = request.form.get('operation')
        file      = request.files['file']
        
        # File Validation -  check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "Errorr"   #redirect(request.url)
      
        # No File Submitted - If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if operation == 'Choose an Operation':
            flash("Choose an Operation")
            return redirect(request.url)
        
        # File Submitted - Now do processing ...
        if file and operation!='Choose an Operation' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"Your image has been processed and is available <a href='/{new}'>here</a>")
            return render_template("index.html") #redirect(url_for('download_file', name=filename))
    return render_template("index.html") 


app.run(debug=True, port=5001)