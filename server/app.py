import os
import json
from flask import Flask, jsonify, request, g, current_app
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from utils import pagination, paginate_data
from xmlrpc.client import ServerProxy

app = Flask(__name__)

CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:qwe```@127.0.0.1/wedata2?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class OfficialAccount(db.Model):
    __tablename__ = 'official_account'
    id = db.Column('id', db.Integer, primary_key=True)
    account_id = db.Column('account_id', db.String(30))
    account_name = db.Column('account_name', db.String(30))
    tag = db.Column('tag', db.String(30))
    biz = db.Column('biz', db.String(20))

    @classmethod
    def list_accounts(cls, q=None):
        qs = cls.query
        if q:
            qs = qs.filter(cls.name.ilike("%{}%".format(q)))
        if hasattr(g, "paginator"):
            g.paginator.count = qs.count()
            qs = qs.limit(g.paginator.limit).offset(g.paginator.offset)
        return qs.all()

    @classmethod
    def get_account_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def partial_update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        db.session.commit()

    @classmethod
    def create(cls, **kwargs):
        coount = cls()
        for k, v in kwargs.items():
            setattr(account, k, v)
        db.session.add(project)
        db.session.commit()
        return project


class OfficialAccountSchema(Schema):
    id = db.Column('id', db.Integer, primary_key=True)
    account_id = fields.String(required=True)
    account_name = fields.String()
    tag = fields.String()
    biz = fields.String()

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column('id', db.Integer, primary_key=True)
    account_id = db.Column('account_id', db.String(30))
    article_title = db.Column('article_title', db.String(200))
    author = db.Column('author', db.String(30))
    page_raw = db.Column('source_content', db.Text)
    # publication_time = db.Column('biz', db.String(20))

    @classmethod
    def list_articles(cls, account_id):
        qs = cls.query
        qs = qs.filter(cls.account_id==account_id)
        if hasattr(g, "paginator"):
            g.paginator.count = qs.count()
            qs = qs.limit(g.paginator.limit).offset(g.paginator.offset)
        return qs.all()

    @classmethod
    def get_detail_page(cls, account_id, title):
        qs = cls.query
        qs = qs.filter(cls.account_id==account_id).filter(cls.article_title==title)
        return qs

class ArticleSchema(Schema):
    id = db.Column('id', db.Integer, primary_key=True)
    account_id = fields.String()
    article_title = fields.String()
    page_raw = fields.String()

@app.route('/v1/accounts')
@pagination
def list_accounts():
    schema = OfficialAccountSchema(only=('account_id', 'account_name', 'tag', 'biz'))
    results = schema.dump(OfficialAccount.list_accounts(q=request.args.get("q")),
                          many=True,
                          ).data
    return jsonify(paginate_data(results))

@app.route('/v1/account/<name>')
@pagination
def list_articles(name):
    schema = ArticleSchema(only=('account_id', 'article_title', 'author'))
    results = schema.dump(Article.list_articles(name),
                        many=True,
                        ).data
    return jsonify(paginate_data(results))

@app.route('/v1/account/<title>')
def get_detail_page(name, title):
    print(name, title)
    schema = ArticleSchema(only('account_id', 'article_title', 'page_raw'))
    results = schema.dump(Article.get_detail_page(title)).data
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7001, debug=True)
