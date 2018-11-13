import base64
import json
from compute import Compute
from flask import (
    Flask,
    request
)

# Create the application instance
app = Flask(__name__, template_folder="templates")

@app.route('/', methods=['POST'])
def pro():
    print('pro...')

    if (os.path.exists('./temp')) :
        shutil.rmtree('./temp')
        os.mkdir('./temp')
    else :
        os.mkdir('./temp')
    if (os.path.exists('./res')) :
        shutil.rmtree('./res')
        os.mkdir('./res')
    else :
        os.mkdir('./res')
    if (os.path.exists('./binary')) :
        shutil.rmtree('./binary')
        os.mkdir('./binary')
    else :
        os.mkdir('./binary')
    if (os.path.exists('./json')) :
        shutil.rmtree('./json')
        os.mkdir('./json')
    else :
        os.mkdir('./json')

    c = Compute()
    # show the post with the given id, the id is an integer
    #return 'Post %s' % base
    data = request.get_json()['img']
    imgdata = base64.b64decode(data)
    filename = './temp/image.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)

    return c.compute()

    # If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True,port=4000)
