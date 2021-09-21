from api.views import user_blueprint,post_blueprint
from api.models import app

app.register_blueprint(user_blueprint)
app.register_blueprint(post_blueprint)

if __name__=='__main__':
    app.run(debug=True)