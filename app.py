from flask import Flask, render_template
from src.controllers.presentation_controller import PresentationController

app = Flask(__name__)
presentation_controller = PresentationController()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    return presentation_controller.generate_presentation()

@app.route('/download/<filename>')
def download(filename):
    return presentation_controller.download_presentation(filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 