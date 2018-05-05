from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from utils import Serializer
from parser import get_sel, get_params

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://appfollow:appfollow@localhost/appfollow'
db = SQLAlchemy(app)


# Implementing DB Model for storing permissions
class Permissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.String(100), unique=True, nullable=False)
    permission = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return '<Permissions for App: {}>'.format(self.app_id)


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/parser', methods=['POST'])
def parser():
    if request.method == 'POST':
        url = request.form['url']
        # TODO: implement url validation
        params = get_params(url)
        app_id = params['id'][0]
        try:
            ln = params['hl'][0]
        except KeyError:
            print('No language specified in url')
            ln = 'en'

        print(ln)
        # TODO: Check language
        permission = Permissions.query.filter_by(app_id=app_id).first()
        if permission:
            output = Serializer.deserialize(permission.permission)
            return jsonify({'permissions': output})

        res = get_sel(app_id, ln)
        new_permission = Permissions(app_id=app_id, permission=Serializer.serialize(res))
        db.session.add(new_permission)
        db.session.commit()
        return jsonify({'permissions': res})


if __name__ == '__main__':
    app.run(debug=True)
