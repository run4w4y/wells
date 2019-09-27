from flask import Flask, render_template, request
from oil_db import *

app = Flask('oil')
db = MainDB('oil')
app.debug = True


@app.route('/', methods=['GET'])
def index():
    names = list(map(
        lambda x: {
            'name': x.name, 
            'id': x.id, 
            'capacity': x.capacity,
            'oil_height': x.depth - max([i.d_to for i in x.layers]),
            'type': x.well_type.name,
            'layers': list(map(
                lambda y: {
                    'from': y.d_from,
                    'to': y.d_to,
                    'color': y.properties.color,
                    'name': y.properties.name,
                    'trans': y.properties.translation
                }, 
                x.layers
            ))
        }, 
        db.wells
    ))
    return render_template('index.html', names=names)

@app.route('/jquery.js')
def jquery():
    with open('js/jquery.js') as f:
        return f.read()

@app.route('/add', methods=['GET'])
def add():
    return render_template('add.html')

@app.route('/edit/<int:well_id>')
def edit(well_id):
    return render_template('edit.html')


if __name__ == '__main__':
    app.run()
