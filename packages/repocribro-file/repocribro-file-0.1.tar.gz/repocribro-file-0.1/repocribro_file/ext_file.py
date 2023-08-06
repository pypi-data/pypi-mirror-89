import base64
import flask
import requests

from repocribro.extending import Extension
from repocribro.extending.helpers import ViewTab, Badge


from repocribro_file.models import FileDescriptor, FileInstance


def get_content(repo, filepath):
    # TODO: use user's token for private repos
    r = requests.get(f'https://api.github.com/repos/{repo.full_name}/contents/{filepath}')
    try:
        r.raise_for_status()
        content = r.json()['content']
        if r.json()['encoding'] == 'base64':
            content = base64.b64decode(content)
        return content
    except Exception:
        return None


def update_repo_file(db, repo, fd):
    fi = db.session.query(FileInstance).filter_by(
        repository_id=repo.id, descriptor_id=fd.id
    ).first()
    content = get_content(repo, fd.filename)
    if content is None:
        return  # failed to get content
    if fi is None:
        fi = FileInstance(content, repo.id, fd.id)
        db.session.add(fi)
    else:
        fi.update(content)
    db.session.commit()


def update_repo_files(db, repo, *args, **kwargs):
    """Process push webhook msg

    .. todo:: deal with limit of commits in webhook msg (20)
    """
    fds = db.session.query(FileDescriptor).all()
    for fd in fds:
        try:
            update_repo_file(db, repo, fd)
        except Exception:
            pass  # TODO: log problems


class FileExtension(Extension):
    #: Name of file extension
    NAME = 'file'
    #: Category of file extension
    CATEGORY = 'basic'
    #: Author of file extension
    AUTHOR = 'Marek Suchánek'
    #: GitHub URL of file extension
    GH_URL = 'https://github.com/MarekSuchanek/repocribro-file'
    #: Priority of file extension
    PRIORITY = 100

    @staticmethod
    def provide_blueprints():
        from .controllers import all_blueprints
        return all_blueprints

    @staticmethod
    def provide_models():
        from repocribro_file.models import all_models
        return all_models

    @staticmethod
    def provide_template_loader():
        from jinja2 import PackageLoader
        return PackageLoader('repocribro_file', 'templates')

    @staticmethod
    def get_gh_webhook_processors():
        """Get all GitHub webhooks processory"""
        return {
            'push': [update_repo_files]
        }

    @staticmethod
    def get_gh_event_processors():
        """Get all GitHub events processors"""
        return {
            'push': [update_repo_files]
        }

    def view_core_repo_detail_tabs(self, repo, tabs_dict):
        tabs_dict['files'] = ViewTab(
            'files', 'Files', 10,
            flask.render_template('core/repo/files_tab.html', repo=repo),
            octicon='file'
        )

    def view_admin_index_tabs(self, tabs_dict):
        """Prepare tabs for index view of admin controller
        :param tabs_dict: Target dictionary for tabs
        :type tabs_dict: dict of str: ``repocribro.extending.helpers.ViewTab``
        """
        fds = self.db.session.query(FileDescriptor).all()

        tabs_dict['files'] = ViewTab(
            'files', 'Files', 0,
            self.app.jinja_env.get_template('admin/tabs/files.html').render(
                filedescriptors=fds
            ),
            octicon='file',
            badge=Badge(len(fds))
        )

    # TODO: search by content of file


def make_extension(*args, **kwargs):
    return FileExtension(*args, **kwargs)
