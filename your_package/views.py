from flask import render_template, request, redirect, url_for

from your_package import app
from your_package.models import DataPipeline

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        search = request.form['searchBar']
        # Here you can interact with your model
        data_pipeline = DataPipeline()
        weather_data = data_pipeline.totalProcess(search)
        temperature = weather_data.temp
        return render_template('data.html', temp=temperature) #problem, refer to model