from api.controllers import login,users,post,author,address
from api.models.users_models import app

app.register_blueprint(login.login_blueprint)
app.register_blueprint(users.user_blueprint)
app.register_blueprint(post.post_blueprint)
app.register_blueprint(author.author_blueprint)
app.register_blueprint(address.address_blueprint)


if __name__=='__main__':
    app.run(debug=True)