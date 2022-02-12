import os
import urllib.parse

import flask
import flask_login

from . import auth, db, forms, models, repo

PAGE_SIZE = 10


app = flask.Flask("supreme_umbrella")
db.init_app(app)
auth.login_manager.init_app(app)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "OK"}


@app.get("/")
def main() -> str:
    page = max(1, int(flask.request.args.get("p", 1)))
    offset = (page - 1) * PAGE_SIZE
    users = repo.UserRepo.get_all(limit=PAGE_SIZE, offset=offset)
    return flask.render_template("main.html", users=users, page=page, title="Main Page")


@app.route("/login", methods=["GET", "POST"])
def login() -> str | flask.Response:
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = repo.UserRepo.get_by_email(form.email.data)
        if user is not None:
            if auth.verify_hash(form.password.data, user.password_hash):
                next = flask.request.args.get("next")
                if urllib.parse.urlparse(next).netloc:
                    flask.abort(400)
                flask_login.login_user(user)
                return flask.redirect(next or flask.url_for("main"))
        flask.flash("User or password is invalid.")

    return flask.render_template("form.html", form=form, title="Login")


@app.route("/register", methods=["GET", "POST"])
def register() -> str | flask.Response:
    form = forms.RegisterForm()
    if form.validate_on_submit():
        data = form.data.copy()
        data.pop("csrf_token")
        data.pop("password_again")
        password = data.pop("password")
        password_hash = auth.create_hash(password)
        data["password_hash"] = password_hash
        user = models.User(**data, id=None)
        try:
            repo.UserRepo.add(user)
        except repo.IntegrityError:
            flask.flash("User already exists.")
        else:
            flask_login.login_user(user)
            flask.flash("Congratulations on registration!")
            return flask.redirect(flask.url_for("main"))

    return flask.render_template("form.html", form=form, title="Register")


@app.get("/logout")
def logout() -> flask.Response:
    flask_login.logout_user()
    return flask.redirect(flask.url_for("main"))


@app.get("/profile/<slug>/<int:id>")
def profile(slug: str, id: int) -> str:
    user = repo.UserRepo.get_by_id(id)
    if user is None:
        flask.abort(404)

    return flask.render_template("profile.html", user=user)


@app.route("/edit", methods=["GET", "POST"])
@flask_login.login_required
def edit() -> str | flask.Response:
    form = forms.ProfileForm(obj=flask_login.current_user)
    if form.validate_on_submit():
        form.populate_obj(flask_login.current_user)
        repo.UserRepo.save(flask_login.current_user)
        return flask.redirect(flask.url_for("main"))

    return flask.render_template("form.html", form=form, title="Edit")


@app.route("/search", methods=["GET", "POST"])
def search() -> str:
    form = forms.SearchForm()
    if form.validate_on_submit():
        users = repo.UserRepo.search(
            first=form.first_name.data,
            last=form.last_name.data,
        )
        return flask.render_template("main.html", users=users, title="Search Results")

    return flask.render_template("form.html", form=form, title="Search")
