import flask
import flask_login

from repocribro.security import permissions
from repocribro.models import Repository

from repocribro_badges.models import Badge


#: Badges controller blueprint
badges = flask.Blueprint('badges', __name__, url_prefix='/badges')


@badges.route('/<badge_hash>.svg', methods=['GET'])
def show_badge(badge_hash):
    db = flask.current_app.container.get('db')
    badge = db.session.query(Badge).filter_by(hash=badge_hash).first()
    if badge is None:
        badge = Badge('badge', 'not found', 'flat', '#aaaaaa')
    return flask.render_template(f'badges/{badge.style}.svg',
                                 name=badge.name, value=badge.value,
                                 color=badge.colorhex)


@badges.route('/create', methods=['POST'])
@permissions.roles.badger.require(403)
def create_badge():
    badge = Badge(
        flask.request.form.get('name', None),
        flask.request.form.get('value', None),
        flask.request.form.get('style', ''),
        flask.request.form.get('colorhex', ''),
    )
    repo_id = flask.request.form.get('repository_id', -1)
    db = flask.current_app.container.get('db')
    repo = db.session.query(Repository).filter_by(id=repo_id).first()
    if repo is None:
        flask.abort(400)
    login, reponame = repo.full_name.split('/')
    if not badge.is_valid:
        flask.flash('Such badge cannot be created.', 'danger')
    else:
        try:
            random_hash = Badge.generate_random_hash()
            collision = db.session.query(Badge).filter_by(hash=random_hash).first()
            while collision is not None:
                random_hash = Badge.generate_random_hash()
                collision = db.session.query(Badge).filter_by(hash=random_hash).first()
            badge.hash = random_hash
            badge.assigner_id = flask_login.current_user.id
            badge.repository_id = repo_id
            db.session.add(badge)
            db.session.commit()
            flask.flash('Badge created.', 'success')
        except Exception:
            db.session.rollback()
            flask.flash('Error while saving the Badge.', 'danger')
    return flask.redirect(
        flask.url_for('core.repo_detail',
                      login=login, reponame=reponame,
                      tab='badges')
    )


@badges.route('/<badge_hash>/delete', methods=['GET', 'DELETE'])
@permissions.roles.badger.require(403)
def delete_badge(badge_hash):
    db = flask.current_app.container.get('db')

    badge = db.session.query(Badge).filter_by(hash=badge_hash).first()
    if badge is None or badge.repository is None:
        flask.abort(404)

    db.session.delete(badge)
    db.session.commit()
    flask.flash('Badge has been deleted.', 'success')
    login, reponame = badge.repository.full_name.split('/')
    return flask.redirect(
        flask.url_for('core.repo_detail',
                      login=login, reponame=reponame,
                      tab='badges')
    )
