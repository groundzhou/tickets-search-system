import click
import psycopg2
from psycopg2.extras import RealDictCursor
from flask.cli import with_appcontext
from flask import g, current_app


def get_db():
    """
    获取数据库连接
    """
    if 'db' not in g:
        g.db = psycopg2.connect(
            dbname=current_app.config['DB_NAME'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            host=current_app.config['DB_HOST'],
            port=current_app.config['DB_PORT'],
            cursor_factory=RealDictCursor
        )

    return g.db


def close_db(e=None):
    """
    关闭数据库
    """
    db = g.pop('db', None)

    if db:
        db.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db = get_db()
    with db.cursor() as cur:
        with current_app.open_resource('schema.sql') as f:
            cur.execute(f.read().decode('utf8'))
    db.commit()
    click.echo('Initialized the database.')


@click.command('drop-db')
@with_appcontext
def drop_db_command():
    """Clear all tables."""
    db = get_db()
    with db.cursor() as cur:
        cur.execute('DROP TABLE IF EXISTS test;')
    db.commit()
    click.echo('Drop all tables.')


@click.command('insert-data')
def insert_data_command():
    """插入数据"""
    from app.data import insert_data
    insert_data()
    click.echo('Insert data into db.')


def init_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(drop_db_command)
    app.cli.add_command(insert_data_command)
    app.teardown_appcontext(close_db)
