import flask

from repocribro_badges.models import Badge as RepoBadge

from repocribro.extending import Extension
from repocribro.extending.helpers import ViewTab, Badge
from repocribro.models import Role


class RepocribroBadges(Extension):
    #: Name of pages extension
    NAME = 'badges'
    #: Category of pages extension
    CATEGORY = 'basic'
    #: Author of pages extension
    AUTHOR = 'Marek Suchánek'
    #: GitHub URL of pages extension
    GH_URL = 'https://github.com/MarekSuchanek/repocribro-badges'
    #: Priority of pages extension
    PRIORITY = 10

    @staticmethod
    def provide_roles():
        return {
            'admin': Role('badger',
                          'badge:*',
                          'Badge assigner/moderator'),
        }

    @staticmethod
    def provide_models():
        return [RepoBadge]

    @staticmethod
    def provide_template_loader():
        from jinja2 import PackageLoader
        return PackageLoader('repocribro_badges', 'templates')

    @staticmethod
    def provide_blueprints():
        from repocribro_badges.controllers import all_blueprints
        return all_blueprints

    def view_core_repo_detail_tabs(self, repo, tabs_dict):
        tabs_dict['badges'] = ViewTab(
            'badges', 'Badges', 10,
            flask.render_template('core/repo/badges_tab.html', repo=repo, styles=RepoBadge.styles),
            octicon='verified', badge=Badge(len(repo.badges))
        )


def make_extension(*args, **kwargs):
    return RepocribroBadges(*args, **kwargs)
