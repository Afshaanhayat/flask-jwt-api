from flask import *  
app = Flask(__name__)  
 
@app.route('/tay', methods=["GET", "POST"])  
def upload():  
    return render_template("/file_upload_form.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':

        if request.files:
        	image = request.files['file']
        	image.save(image.filename)
        return render_template("success.html", name = image.filename)  
  
if __name__ == '__main__':  
    app.run(debug = True)