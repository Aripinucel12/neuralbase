import sqlite3
from datetime import datetime
from config import Config


def get_db():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.executescript('''
        CREATE TABLE IF NOT EXISTS providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            logo_url TEXT DEFAULT '',
            description TEXT DEFAULT '',
            pricing_in TEXT DEFAULT '',
            pricing_out TEXT DEFAULT '',
            context_window TEXT DEFAULT '',
            strengths TEXT DEFAULT '',
            weaknesses TEXT DEFAULT '',
            free_tier TEXT DEFAULT '',
            website_url TEXT DEFAULT '',
            is_active INTEGER DEFAULT 1,
            sort_order INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL DEFAULT 'api',
            description TEXT DEFAULT '',
            url TEXT DEFAULT '',
            logo_url TEXT DEFAULT '',
            free_details TEXT DEFAULT '',
            is_active INTEGER DEFAULT 1,
            sort_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL DEFAULT 'chat',
            description TEXT DEFAULT '',
            url TEXT DEFAULT '',
            logo_url TEXT DEFAULT '',
            pricing TEXT DEFAULT '',
            rating REAL DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            sort_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS education (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            category TEXT DEFAULT 'general',
            content TEXT DEFAULT '',
            thumbnail_url TEXT DEFAULT '',
            is_published INTEGER DEFAULT 1,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS faq (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            sort_order INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
    ''')

    conn.commit()
    conn.close()


class BaseModel:
    table = ''

    @classmethod
    def get_db(cls):
        return get_db()

    @classmethod
    def get_all(cls, active_only=True):
        conn = get_db()
        where = 'WHERE is_active=1' if active_only else ''
        rows = conn.execute(f'SELECT * FROM {cls.table} {where} ORDER BY sort_order, id').fetchall()
        conn.close()
        return rows

    @classmethod
    def get_by_id(cls, item_id):
        conn = get_db()
        row = conn.execute(f'SELECT * FROM {cls.table} WHERE id=?', (item_id,)).fetchone()
        conn.close()
        return row

    @classmethod
    def get_by_slug(cls, slug):
        conn = get_db()
        row = conn.execute(f'SELECT * FROM {cls.table} WHERE slug=?', (slug,)).fetchone()
        conn.close()
        return row

    @classmethod
    def count(cls):
        conn = get_db()
        count = conn.execute(f'SELECT COUNT(*) FROM {cls.table}').fetchone()[0]
        conn.close()
        return count

    @classmethod
    def delete(cls, item_id):
        conn = get_db()
        conn.execute(f'DELETE FROM {cls.table} WHERE id=?', (item_id,))
        conn.commit()
        conn.close()


class Provider(BaseModel):
    table = 'providers'

    @classmethod
    def create(cls, data):
        conn = get_db()
        conn.execute('''
            INSERT INTO providers (name, slug, logo_url, description, pricing_in, pricing_out,
                context_window, strengths, weaknesses, free_tier, website_url, is_active, sort_order, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['slug'], data.get('logo_url', ''), data.get('description', ''),
              data.get('pricing_in', ''), data.get('pricing_out', ''), data.get('context_window', ''),
              data.get('strengths', ''), data.get('weaknesses', ''), data.get('free_tier', ''),
              data.get('website_url', ''), data.get('is_active', 1), data.get('sort_order', 0),
              data.get('last_updated', datetime.now().strftime('%Y-%m-%d'))))
        conn.commit()
        conn.close()

    @classmethod
    def update(cls, item_id, data):
        conn = get_db()
        conn.execute('''
            UPDATE providers SET name=?, slug=?, logo_url=?, description=?, pricing_in=?, pricing_out=?,
                context_window=?, strengths=?, weaknesses=?, free_tier=?, website_url=?, is_active=?,
                sort_order=?, last_updated=?
            WHERE id=?
        ''', (data['name'], data['slug'], data.get('logo_url', ''), data.get('description', ''),
              data.get('pricing_in', ''), data.get('pricing_out', ''), data.get('context_window', ''),
              data.get('strengths', ''), data.get('weaknesses', ''), data.get('free_tier', ''),
              data.get('website_url', ''), data.get('is_active', 1), data.get('sort_order', 0),
              data.get('last_updated', datetime.now().strftime('%Y-%m-%d')), item_id))
        conn.commit()
        conn.close()

    @classmethod
    def search(cls, query):
        conn = get_db()
        rows = conn.execute(
            f"SELECT * FROM {cls.table} WHERE is_active=1 AND (name LIKE ? OR description LIKE ?) ORDER BY sort_order",
            (f'%{query}%', f'%{query}%')
        ).fetchall()
        conn.close()
        return rows


class Resource(BaseModel):
    table = 'resources'

    @classmethod
    def create(cls, data):
        conn = get_db()
        conn.execute('''
            INSERT INTO resources (name, slug, category, description, url, logo_url, free_details, is_active, sort_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['slug'], data.get('category', 'api'), data.get('description', ''),
              data.get('url', ''), data.get('logo_url', ''), data.get('free_details', ''),
              data.get('is_active', 1), data.get('sort_order', 0)))
        conn.commit()
        conn.close()

    @classmethod
    def update(cls, item_id, data):
        conn = get_db()
        conn.execute('''
            UPDATE resources SET name=?, slug=?, category=?, description=?, url=?, logo_url=?,
                free_details=?, is_active=?, sort_order=?
            WHERE id=?
        ''', (data['name'], data['slug'], data.get('category', 'api'), data.get('description', ''),
              data.get('url', ''), data.get('logo_url', ''), data.get('free_details', ''),
              data.get('is_active', 1), data.get('sort_order', 0), item_id))
        conn.commit()
        conn.close()

    @classmethod
    def get_by_category(cls, category):
        conn = get_db()
        rows = conn.execute(
            f"SELECT * FROM {cls.table} WHERE is_active=1 AND category=? ORDER BY sort_order", (category,)
        ).fetchall()
        conn.close()
        return rows

    @classmethod
    def search(cls, query):
        conn = get_db()
        rows = conn.execute(
            f"SELECT * FROM {cls.table} WHERE is_active=1 AND (name LIKE ? OR description LIKE ?)",
            (f'%{query}%', f'%{query}%')
        ).fetchall()
        conn.close()
        return rows


class Tool(BaseModel):
    table = 'tools'

    @classmethod
    def create(cls, data):
        conn = get_db()
        conn.execute('''
            INSERT INTO tools (name, slug, category, description, url, logo_url, pricing, rating, is_active, sort_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['slug'], data.get('category', 'chat'), data.get('description', ''),
              data.get('url', ''), data.get('logo_url', ''), data.get('pricing', ''),
              data.get('rating', 0), data.get('is_active', 1), data.get('sort_order', 0)))
        conn.commit()
        conn.close()

    @classmethod
    def update(cls, item_id, data):
        conn = get_db()
        conn.execute('''
            UPDATE tools SET name=?, slug=?, category=?, description=?, url=?, logo_url=?,
                pricing=?, rating=?, is_active=?, sort_order=?
            WHERE id=?
        ''', (data['name'], data['slug'], data.get('category', 'chat'), data.get('description', ''),
              data.get('url', ''), data.get('logo_url', ''), data.get('pricing', ''),
              data.get('rating', 0), data.get('is_active', 1), data.get('sort_order', 0), item_id))
        conn.commit()
        conn.close()

    @classmethod
    def get_by_category(cls, category):
        conn = get_db()
        rows = conn.execute(
            f"SELECT * FROM {cls.table} WHERE is_active=1 AND category=? ORDER BY sort_order", (category,)
        ).fetchall()
        conn.close()
        return rows

    @classmethod
    def search(cls, query):
        conn = get_db()
        rows = conn.execute(
            f"SELECT * FROM {cls.table} WHERE is_active=1 AND (name LIKE ? OR description LIKE ?)",
            (f'%{query}%', f'%{query}%')
        ).fetchall()
        conn.close()
        return rows


class Education(BaseModel):
    table = 'education'

    @classmethod
    def create(cls, data):
        conn = get_db()
        conn.execute('''
            INSERT INTO education (title, slug, category, content, thumbnail_url, is_published, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['title'], data['slug'], data.get('category', 'general'), data.get('content', ''),
              data.get('thumbnail_url', ''), data.get('is_published', 1),
              data.get('last_updated', datetime.now().strftime('%Y-%m-%d'))))
        conn.commit()
        conn.close()

    @classmethod
    def update(cls, item_id, data):
        conn = get_db()
        conn.execute('''
            UPDATE education SET title=?, slug=?, category=?, content=?, thumbnail_url=?, is_published=?,
                last_updated=?
            WHERE id=?
        ''', (data['title'], data['slug'], data.get('category', 'general'), data.get('content', ''),
              data.get('thumbnail_url', ''), data.get('is_published', 1),
              data.get('last_updated', datetime.now().strftime('%Y-%m-%d')), item_id))
        conn.commit()
        conn.close()

    @classmethod
    def get_published(cls):
        conn = get_db()
        rows = conn.execute(
            f"SELECT * FROM {cls.table} WHERE is_published=1 ORDER BY created_at DESC"
        ).fetchall()
        conn.close()
        return rows

    @classmethod
    def search(cls, query):
        conn = get_db()
        rows = conn.execute(
            f"SELECT * FROM {cls.table} WHERE is_published=1 AND (title LIKE ? OR content LIKE ?)",
            (f'%{query}%', f'%{query}%')
        ).fetchall()
        conn.close()
        return rows


class FAQ(BaseModel):
    table = 'faq'

    @classmethod
    def create(cls, data):
        conn = get_db()
        conn.execute('''
            INSERT INTO faq (question, answer, sort_order, is_active, last_updated)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['question'], data['answer'], data.get('sort_order', 0), data.get('is_active', 1),
              data.get('last_updated', datetime.now().strftime('%Y-%m-%d'))))
        conn.commit()
        conn.close()

    @classmethod
    def update(cls, item_id, data):
        conn = get_db()
        conn.execute('''
            UPDATE faq SET question=?, answer=?, sort_order=?, is_active=?, last_updated=?
            WHERE id=?
        ''', (data['question'], data['answer'], data.get('sort_order', 0), data.get('is_active', 1),
              data.get('last_updated', datetime.now().strftime('%Y-%m-%d')), item_id))
        conn.commit()
        conn.close()

    @classmethod
    def search(cls, query):
        conn = get_db()
        rows = conn.execute(
            f"SELECT * FROM {cls.table} WHERE is_active=1 AND (question LIKE ? OR answer LIKE ?)",
            (f'%{query}%', f'%{query}%')
        ).fetchall()
        conn.close()
        return rows


class AdminUser(BaseModel):
    table = 'admin_users'

    @classmethod
    def get_by_username(cls, username):
        conn = get_db()
        row = conn.execute(f'SELECT * FROM {cls.table} WHERE username=?', (username,)).fetchone()
        conn.close()
        return row

    @classmethod
    def create(cls, username, password_hash):
        conn = get_db()
        conn.execute(
            'INSERT INTO admin_users (username, password_hash) VALUES (?, ?)',
            (username, password_hash)
        )
        conn.commit()
        conn.close()
