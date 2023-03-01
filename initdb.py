from flaskr import create_app
from flaskr.models import db

app = create_app()

with app.app_context():
    db.create_all()
    # @app.route('/')
    # def index():
    #     return render_template('index.html', data=Composer.query.all())
    

