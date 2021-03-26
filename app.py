"""

"""

from flask import Flask, render_template, redirect
from forms import GeoForm
from mbta_helper import find_stop_near

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = GeoForm()
    if form.is_submitted():
        return render_template('mbta.html')
    return render_template('index.html', form=form)

@app.route('/mbta')
def mbta():
    return render_template('mbta.html')


if __name__ == "__main__":
    app.run(debug=True)
