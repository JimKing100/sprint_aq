# Import Flask package

from decouple import config
from flask import Flask, render_template
from TEST.models import DB, Record
# import requests
import openaq


def create_app():
    # Create Flask web server, makes the application
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    # Routes determine location
    @app.route("/")
    def home():
        DB.drop_all()
        DB.create_all()

        api = openaq.OpenAQ()
        status, body = api.measurements(city='Los Angeles', parameter='pm25')

        for i in range(0, 100):
            date1 = body['results'][i]['date']['utc']
            value1 = body['results'][i]['value']
            db_record = Record(id=i, datetime=date1, value=value1)
            DB.session.add(db_record)

        DB.session.commit()
        records = Record.query.filter(Record.value > 10)
        return render_template('home.html', title=date1, records=records)
    return app
