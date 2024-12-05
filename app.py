from flask import Flask, render_template

from database import database

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)


@app.route("/")
def view_dashboard_page():
    return render_template("dashboard.jinja")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)

