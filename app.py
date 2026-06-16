from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import init_db, Provider, Resource, Tool, Education, FAQ, AdminUser
import json
import markdown

app = Flask(__name__)
app.config.from_object(Config)

@app.template_filter('markdown')
def markdown_filter(text):
    return markdown.markdown(text, extensions=['fenced_code', 'codehilite', 'tables', 'nl2br'])

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Silakan login terlebih dahulu.'


class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    conn = AdminUser.get_db()
    row = conn.execute('SELECT * FROM admin_users WHERE id=?', (user_id,)).fetchone()
    conn.close()
    if row:
        return User(row['id'], row['username'])
    return None


# ──────────────────────────────────────────
# CONTEXT PROCESSORS
# ──────────────────────────────────────────
@app.context_processor
def inject_stats():
    return {
        'total_providers': Provider.count(),
        'total_resources': Resource.count(),
        'total_tools': Tool.count(),
        'total_education': Education.count(),
    }


# ──────────────────────────────────────────
# PUBLIC ROUTES
# ──────────────────────────────────────────
@app.route('/')
def index():
    providers = Provider.get_all()
    resources = Resource.get_all()
    tools = Tool.get_all()
    articles = Education.get_published()
    return render_template('index.html',
                           providers=providers,
                           resources=resources,
                           tools=tools,
                           articles=articles,
                           provider_count=len(providers),
                           resource_count=len(resources),
                           tool_count=len(tools),
                           edu_count=len(articles))


@app.route('/providers')
def providers():
    all_providers = Provider.get_all()
    return render_template('providers.html', providers=all_providers)


@app.route('/providers/<slug>')
def provider_detail(slug):
    provider = Provider.get_by_slug(slug)
    if not provider:
        return render_template('404.html'), 404
    return render_template('provider_detail.html', provider=provider)


@app.route('/resources')
def resources():
    all_resources = Resource.get_all()
    categories = {
        'vps': [r for r in all_resources if r['category'] == 'vps'],
        'api': [r for r in all_resources if r['category'] == 'api'],
        'gpu': [r for r in all_resources if r['category'] == 'gpu'],
        'tools': [r for r in all_resources if r['category'] == 'tools'],
    }
    return render_template('resources.html', resources=all_resources, categories=categories)


@app.route('/tools')
def tools():
    all_tools = Tool.get_all()
    categories = {
        'coding': [t for t in all_tools if t['category'] == 'coding'],
        'image': [t for t in all_tools if t['category'] == 'image'],
        'writing': [t for t in all_tools if t['category'] == 'writing'],
        'chat': [t for t in all_tools if t['category'] == 'chat'],
    }
    return render_template('tools.html', tools=all_tools, categories=categories)


@app.route('/education')
def education():
    articles = Education.get_published()
    return render_template('education.html', articles=articles)


@app.route('/education/<slug>')
def education_detail(slug):
    article = Education.get_by_slug(slug)
    if not article:
        return render_template('404.html'), 404
    return render_template('education_detail.html', article=article)


@app.route('/faq')
def faq():
    faqs = FAQ.get_all()
    return render_template('faq.html', faqs=faqs)


@app.route('/search')
def search():
    q = request.args.get('q', '').strip()
    if not q:
        return redirect(url_for('index'))

    results = {
        'providers': Provider.search(q),
        'resources': Resource.search(q),
        'tools': Tool.search(q),
        'education': Education.search(q),
    }
    total = sum(len(v) for v in results.values())
    return render_template('search.html', query=q, results=results, total=total)


# ──────────────────────────────────────────
# ADMIN ROUTES
# ──────────────────────────────────────────
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        user = AdminUser.get_by_username(username)

        if user and check_password_hash(user['password_hash'], password):
            login_user(User(user['id'], user['username']))
            return redirect(url_for('admin_dashboard'))
        flash('Username atau password salah.', 'error')

    return render_template('admin/login.html')


@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))


@app.route('/admin')
@login_required
def admin_dashboard():
    return render_template('admin/dashboard.html',
                           providers_count=Provider.count(),
                           resources_count=Resource.count(),
                           tools_count=Tool.count(),
                           education_count=Education.count(),
                           faq_count=FAQ.count())


# ── ADMIN: PROVIDERS ──
@app.route('/admin/providers')
@login_required
def admin_providers():
    all_providers = Provider.get_all(active_only=False)
    return render_template('admin/providers.html', providers=all_providers)


@app.route('/admin/providers/add', methods=['GET', 'POST'])
@login_required
def admin_providers_add():
    if request.method == 'POST':
        data = request.form.to_dict()
        data['is_active'] = 1 if 'is_active' in request.form else 0
        data['sort_order'] = int(data.get('sort_order', 0))
        Provider.create(data)
        flash('Provider berhasil ditambahkan!', 'success')
        return redirect(url_for('admin_providers'))
    return render_template('admin/provider_form.html', provider=None)


@app.route('/admin/providers/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def admin_providers_edit(item_id):
    provider = Provider.get_by_id(item_id)
    if not provider:
        return redirect(url_for('admin_providers'))

    if request.method == 'POST':
        data = request.form.to_dict()
        data['is_active'] = 1 if 'is_active' in request.form else 0
        data['sort_order'] = int(data.get('sort_order', 0))
        Provider.update(item_id, data)
        flash('Provider berhasil diupdate!', 'success')
        return redirect(url_for('admin_providers'))
    return render_template('admin/provider_form.html', provider=provider)


@app.route('/admin/providers/delete/<int:item_id>', methods=['POST'])
@login_required
def admin_providers_delete(item_id):
    Provider.delete(item_id)
    flash('Provider berhasil dihapus!', 'success')
    return redirect(url_for('admin_providers'))


# ── ADMIN: RESOURCES ──
@app.route('/admin/resources')
@login_required
def admin_resources():
    all_resources = Resource.get_all(active_only=False)
    return render_template('admin/resources.html', resources=all_resources)


@app.route('/admin/resources/add', methods=['GET', 'POST'])
@login_required
def admin_resources_add():
    if request.method == 'POST':
        data = request.form.to_dict()
        data['is_active'] = 1 if 'is_active' in request.form else 0
        data['sort_order'] = int(data.get('sort_order', 0))
        Resource.create(data)
        flash('Resource berhasil ditambahkan!', 'success')
        return redirect(url_for('admin_resources'))
    return render_template('admin/resource_form.html', resource=None)


@app.route('/admin/resources/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def admin_resources_edit(item_id):
    resource = Resource.get_by_id(item_id)
    if not resource:
        return redirect(url_for('admin_resources'))

    if request.method == 'POST':
        data = request.form.to_dict()
        data['is_active'] = 1 if 'is_active' in request.form else 0
        data['sort_order'] = int(data.get('sort_order', 0))
        Resource.update(item_id, data)
        flash('Resource berhasil diupdate!', 'success')
        return redirect(url_for('admin_resources'))
    return render_template('admin/resource_form.html', resource=resource)


@app.route('/admin/resources/delete/<int:item_id>', methods=['POST'])
@login_required
def admin_resources_delete(item_id):
    Resource.delete(item_id)
    flash('Resource berhasil dihapus!', 'success')
    return redirect(url_for('admin_resources'))


# ── ADMIN: TOOLS ──
@app.route('/admin/tools')
@login_required
def admin_tools():
    all_tools = Tool.get_all(active_only=False)
    return render_template('admin/tools.html', tools=all_tools)


@app.route('/admin/tools/add', methods=['GET', 'POST'])
@login_required
def admin_tools_add():
    if request.method == 'POST':
        data = request.form.to_dict()
        data['is_active'] = 1 if 'is_active' in request.form else 0
        data['sort_order'] = int(data.get('sort_order', 0))
        data['rating'] = float(data.get('rating', 0))
        Tool.create(data)
        flash('Tool berhasil ditambahkan!', 'success')
        return redirect(url_for('admin_tools'))
    return render_template('admin/tool_form.html', tool=None)


@app.route('/admin/tools/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def admin_tools_edit(item_id):
    tool = Tool.get_by_id(item_id)
    if not tool:
        return redirect(url_for('admin_tools'))

    if request.method == 'POST':
        data = request.form.to_dict()
        data['is_active'] = 1 if 'is_active' in request.form else 0
        data['sort_order'] = int(data.get('sort_order', 0))
        data['rating'] = float(data.get('rating', 0))
        Tool.update(item_id, data)
        flash('Tool berhasil diupdate!', 'success')
        return redirect(url_for('admin_tools'))
    return render_template('admin/tool_form.html', tool=tool)


@app.route('/admin/tools/delete/<int:item_id>', methods=['POST'])
@login_required
def admin_tools_delete(item_id):
    Tool.delete(item_id)
    flash('Tool berhasil dihapus!', 'success')
    return redirect(url_for('admin_tools'))


# ── ADMIN: EDUCATION ──
@app.route('/admin/education')
@login_required
def admin_education():
    all_education = Education.get_all(active_only=False)
    return render_template('admin/education.html', articles=all_education)


@app.route('/admin/education/add', methods=['GET', 'POST'])
@login_required
def admin_education_add():
    if request.method == 'POST':
        data = request.form.to_dict()
        data['is_published'] = 1 if 'is_published' in request.form else 0
        Education.create(data)
        flash('Artikel berhasil ditambahkan!', 'success')
        return redirect(url_for('admin_education'))
    return render_template('admin/education_form.html', article=None)


@app.route('/admin/education/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def admin_education_edit(item_id):
    article = Education.get_by_id(item_id)
    if not article:
        return redirect(url_for('admin_education'))

    if request.method == 'POST':
        data = request.form.to_dict()
        data['is_published'] = 1 if 'is_published' in request.form else 0
        Education.update(item_id, data)
        flash('Artikel berhasil diupdate!', 'success')
        return redirect(url_for('admin_education'))
    return render_template('admin/education_form.html', article=article)


@app.route('/admin/education/delete/<int:item_id>', methods=['POST'])
@login_required
def admin_education_delete(item_id):
    Education.delete(item_id)
    flash('Artikel berhasil dihapus!', 'success')
    return redirect(url_for('admin_education'))


# ── ADMIN: FAQ ──
@app.route('/admin/faq')
@login_required
def admin_faq():
    all_faq = FAQ.get_all(active_only=False)
    return render_template('admin/faq.html', faqs=all_faq)


@app.route('/admin/faq/add', methods=['GET', 'POST'])
@login_required
def admin_faq_add():
    if request.method == 'POST':
        data = request.form.to_dict()
        data['is_active'] = 1 if 'is_active' in request.form else 0
        data['sort_order'] = int(data.get('sort_order', 0))
        FAQ.create(data)
        flash('FAQ berhasil ditambahkan!', 'success')
        return redirect(url_for('admin_faq'))
    return render_template('admin/faq_form.html', faq=None)


@app.route('/admin/faq/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def admin_faq_edit(item_id):
    faq = FAQ.get_by_id(item_id)
    if not faq:
        return redirect(url_for('admin_faq'))

    if request.method == 'POST':
        data = request.form.to_dict()
        data['is_active'] = 1 if 'is_active' in request.form else 0
        data['sort_order'] = int(data.get('sort_order', 0))
        FAQ.update(item_id, data)
        flash('FAQ berhasil diupdate!', 'success')
        return redirect(url_for('admin_faq'))
    return render_template('admin/faq_form.html', faq=faq)


@app.route('/admin/faq/delete/<int:item_id>', methods=['POST'])
@login_required
def admin_faq_delete(item_id):
    FAQ.delete(item_id)
    flash('FAQ berhasil dihapus!', 'success')
    return redirect(url_for('admin_faq'))


# ──────────────────────────────────────────
# API ENDPOINTS
# ──────────────────────────────────────────
@app.route('/api/stats')
def api_stats():
    return jsonify({
        'providers': Provider.count(),
        'resources': Resource.count(),
        'tools': Tool.count(),
        'education': Education.count(),
    })


# ──────────────────────────────────────────
# ERROR HANDLERS
# ──────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


# ──────────────────────────────────────────
# STARTUP
# ──────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    # Create default admin if not exists
    if not AdminUser.get_by_username(Config.ADMIN_USERNAME):
        AdminUser.create(Config.ADMIN_USERNAME, generate_password_hash(Config.ADMIN_PASSWORD))
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
