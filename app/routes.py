from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_file, flash
from .models import File, User
from . import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, UploadForm
from werkzeug.utils import secure_filename
import os, binascii, io
from .crypto import encrypt_file_bytes, decrypt_file_bytes

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    files = File.query.order_by(File.uploaded_at.desc()).all()
    return render_template('index.html', files=files)

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = request.files['file']
        filename = secure_filename(f.filename)
        data = f.read()
        ciphertext, nonce, tag, filekey_enc_hex, wrap_nonce_hex, wrap_tag_hex = encrypt_file_bytes(data)
        stored_name = binascii.hexlify(os.urandom(12)).decode() + '.enc'
        stored_path = os.path.join(current_app.config['STORAGE_DIR'], stored_name)
        with open(stored_path, 'wb') as out:
            out.write(ciphertext)
        new = File(original_filename=filename, stored_filename=stored_name, filekey_enc='|'.join([filekey_enc_hex, wrap_nonce_hex, wrap_tag_hex]), nonce_hex=binascii.hexlify(nonce).decode(), tag_hex=binascii.hexlify(tag).decode(), mimetype=f.mimetype, filesize=len(data))
        db.session.add(new)
        db.session.commit()
        flash('Uploaded successfully', 'success')
        return redirect(url_for('main.index'))
    return render_template('upload.html', form=form)

@main.route('/download/<int:file_id>')
@login_required
def download(file_id):
    f = File.query.get_or_404(file_id)
    stored_path = os.path.join(current_app.config['STORAGE_DIR'], f.stored_filename)
    if not os.path.exists(stored_path):
        flash('File missing', 'danger')
        return redirect(url_for('main.index'))
    with open(stored_path, 'rb') as inp:
        ciphertext = inp.read()
    nonce = binascii.unhexlify(f.nonce_hex)
    tag = binascii.unhexlify(f.tag_hex)
    filekey_enc_hex, wrap_nonce_hex, wrap_tag_hex = f.filekey_enc.split('|')
    try:
        plaintext = decrypt_file_bytes(ciphertext, nonce, tag, filekey_enc_hex, wrap_nonce_hex, wrap_tag_hex)
    except Exception as e:
        flash('Decryption failed: ' + str(e), 'danger')
        return redirect(url_for('main.index'))
    return send_file(io.BytesIO(plaintext), download_name=f.original_filename, mimetype=f.mimetype)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
