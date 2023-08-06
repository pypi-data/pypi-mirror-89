import flask

from repocribro.security import permissions

from repocribro_file.models import FileDescriptor


#: Files admin controller blueprint
admin_files = flask.Blueprint('admin-files', __name__, url_prefix='/admin-files')


@admin_files.route('/<int:fd_id>', methods=['GET'])
@permissions.roles.admin.require(404)
def show_file(fd_id):
    db = flask.current_app.container.get('db')
    fd = db.session.query(FileDescriptor).filter_by(id=fd_id).first()
    if fd is None:
        flask.abort(404)
    return flask.render_template('admin/file.html', fd=fd)


@admin_files.route('/create', methods=['GET'])
@permissions.roles.admin.require(404)
def create_file():
    fd = FileDescriptor(
        flask.request.args.get('filename', ''),
        flask.request.args.get('description', ''),
        flask.request.args.get('filetype', FileDescriptor.filetypes[0]),
    )
    return flask.render_template('admin/forms/file.html', fd=fd,
                                 filetypes=FileDescriptor.filetypes, form_method='POST',
                                 form_title='Create new file descriptor',
                                 form_action=flask.url_for('admin-files.create_file'))


@admin_files.route('/create', methods=['POST'])
@permissions.roles.admin.require(404)
def create_file_post():
    fd = FileDescriptor(
        flask.request.form.get('filename', ''),
        flask.request.form.get('description', ''),
        flask.request.form.get('filetype', ''),
    )

    db = flask.current_app.container.get('db')
    try:
        assert isinstance(fd.filename, str) and len(fd.filename) > 0
        db.session.add(fd)
        db.session.commit()
    except Exception:
        flask.flash('Couldn\'t create such file descriptor', 'danger')
        db.session.rollback()
        return flask.redirect(
            flask.url_for('admin-files.create_file', filetype=fd.filetype,
                          filename=fd.filename, description=fd.description)
        )

    flask.flash('File descriptor created', 'success')
    return flask.redirect(flask.url_for('admin.index', tab='files'))


@admin_files.route('/<int:fd_id>/edit', methods=['GET'])
@permissions.roles.admin.require(404)
def edit_file(fd_id):
    db = flask.current_app.container.get('db')
    fd = db.session.query(FileDescriptor).filter_by(id=fd_id).first()
    if fd is None:
        flask.abort(404)
    return flask.render_template('admin/forms/file.html', fd=fd,
                                 filetypes=FileDescriptor.filetypes, form_method='POST',
                                 form_title='Edit file descriptor',
                                 form_action=flask.url_for('admin-files.edit_file', fd_id=fd.id))


@admin_files.route('/<int:fd_id>/edit', methods=['PUT', 'POST'])
@permissions.roles.admin.require(404)
def edit_file_put(fd_id):
    db = flask.current_app.container.get('db')
    fd = db.session.query(FileDescriptor).filter_by(id=fd_id).first()
    if fd is None:
        flask.abort(404)
    fd.filename = flask.request.form.get('filename', None)
    fd.description = flask.request.form.get('description', '')
    fd.filetype = flask.request.form.get('filetype', FileDescriptor.filetypes[0])
    try:
        db.session.commit()
    except Exception:
        flask.flash('Couldn\'t edit file descriptor', 'danger')
        db.session.rollback()
        return flask.redirect(
            flask.url_for('admin-files.edit_file', fd_id=fd.id,
                          filetype=fd.filetype, filename=fd.filename,
                          description=fd.description)
        )
    return flask.redirect(flask.url_for('admin.index', tab='files'))


@admin_files.route('/<int:fd_id>/delete')
@permissions.roles.admin.require(404)
def delete_file(fd_id):
    db = flask.current_app.container.get('db')
    fd = db.session.query(FileDescriptor).filter_by(id=fd_id).first()
    if fd is None:
        flask.abort(404)

    db.session.delete(fd)
    db.session.commit()
    flask.flash(f'File descriptor {fd.filename} has been deleted', 'success')
    return flask.redirect(flask.url_for('admin.index', tab='files'))
