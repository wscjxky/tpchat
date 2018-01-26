# -*- coding: utf-8 -*-
from Database import db

class IndexBanner(db.Model):
    __tablename__ = "indexbanner"
    Id = db.Column(db.Integer, primary_key=True)
    Banner = db.Column(db.VARCHAR(255))
    Path = db.Column(db.VARCHAR(255))
    ActivityPage = db.Column(db.VARCHAR(255))

    def __init__(self, banner, path, page):
        self.Banner = banner
        self.Path = path
        self.ActivityPage = page

    def __repr__(self):
        return '<Index %r>' % {'Id': self.Id, 'Banner': self.Banner, 'ActivityPage': self.ActivityPage}


class ChannelSetting(db.Model):
    __tablename__ = "setting_channel"
    Id = db.Column(db.BIGINT, primary_key=True)
    CategoryId = db.Column(db.BIGINT)
    Position = db.Column(db.INT)
    Name = db.Column(db.VARCHAR(100))
    ParentId = db.Column(db.BIGINT)
    BackupName = db.Column(db.VARCHAR(100))

    def __init__(self, cid, position, name, parentId):
        self.CategoryId = cid
        self.Position = position
        self.Name = name
        self.ParentId = parentId
        self.BackupName = name


class ClassicalSetting(db.Model):
    __tablename__ = "setting_classical"
    ZoneItemId = db.Column(db.BIGINT, db.ForeignKey('zone_item.Id'), primary_key=True)
    Position = db.Column(db.INT)
    ZoneItem = db.relation('ZoneItem', foreign_keys='ClassicalSetting.ZoneItemId')

    def __init__(self, zid, position):
        self.ZoneItemId = zid
        self.Position = position


class ProducerSetting(db.Model):
    __tablename__ = "setting_producer"
    DomainId = db.Column(db.BIGINT, db.ForeignKey('domain.Id'), primary_key=True)
    Position = db.Column(db.INT)
    Domain = db.relation('Domain', foreign_keys='ProducerSetting.DomainId')

    def __init__(self, did, position):
        self.DomainId = did
        self.Position = position

class Settings(db.Model):
    __tablename__ = "settings"
    Item = db.Column(db.VARCHAR(255), primary_key=True)
    Value = db.Column(db.VARCHAR(255))

    def __init__(self, item, value):
        self.Item = item
        self.Value = value

