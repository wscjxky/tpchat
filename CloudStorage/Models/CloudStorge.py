# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import datetime
from sqlalchemy.ext.associationproxy import association_proxy
from enum import IntEnum
import mysql.connector.conversion
from Database import db
from sqlalchemy.dialects.mysql import DOUBLE


class UserRole(db.Model):
    __tablename__ = "userrole"
    Id = db.Column(db.BIGINT, primary_key=True)
    RoleId = db.Column(db.BIGINT, db.ForeignKey('role.Id'))
    UserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))


class VideoObject(db.Model):
    __tablename__ = "video"
    fileID = db.Column(db.BIGINT, primary_key=True)
    fileOriginUrl = db.Column(db.String(255))
    fileTranscodedUrl = db.Column(db.String(255))
    fileThumbUrl = db.Column(db.String(255))
    fileOwnerID = db.Column(db.Integer)
    fileParent = db.Column(db.Integer)
    CreateTime = db.Column(db.TIMESTAMP)
    FileSize = db.Column(db.Integer)
    FileType = db.Column(db.Integer)


userrole = db.Table('userrole', db.Column('Id', db.BIGINT, primary_key=True), extend_existing=True)


class RegisterIdentity(db.Model):
    __tablename__ = "registeridentity"
    Id = db.Column(db.Integer, primary_key=True)
    IdentityCode = db.Column(db.VARCHAR(20))
    CreateTime = db.Column(db.TIMESTAMP)
    Email = db.Column(db.VARCHAR(100))
    def __init__(self, Email): 
        self.Email = Email
        # self.CreateTime = 'current_timestamp()'
        
    def __repr__(self):
        return '<RegisterIdentity %r>' % {'Email': self.Email}


class User(db.Model):
    __tablename__ = "user"
    Id = db.Column(db.Integer, primary_key=True)
    NIPUserId = db.Column(db.BIGINT)
    DomainId = db.Column(db.BIGINT, db.ForeignKey("domain.Id"))
    DomainName = db.Column(db.VARCHAR(100))
    Password = db.Column(db.CHAR(32))
    SessionId = db.Column(db.String(50))
    Email = db.Column(db.String(50))
    NickName = db.Column(db.String(50))
    type = db.Column(db.Integer)
    CreateTime = db.Column(db.TIMESTAMP)
    LeastTime = db.Column(db.DATETIME)
    RealName = db.Column(db.VARCHAR(100))
    Status = db.Column(db.Integer)
    Identity = db.Column(db.VARCHAR(100))
    CellPhone = db.Column(db.VARCHAR(100))
    Level = db.Column(db.INT)
    LastLoginTime = db.Column(db.DATETIME)
    WeiXinOpenId = db.Column(db.VARCHAR(255))
    Roles = db.relationship('Role', secondary=userrole,
                            backref=db.backref('User', lazy='dynamic'))
    DomainPermissionInvalidate = db.Column(db.INTEGER)

    def __init__(self, NIPUserId, Email, NickName):
        self.NIPUserId = NIPUserId
        self.Email = Email
        self.NickName = NickName
        self.DomainPermissionInvalidate = 0
        self.Password = None
        self.Level = 0
        self.WeiXinOpenId = ''

    def __repr__(self):
        return '<User %r>' % {'Id': self.Id, 'Email': self.Email}


class ObjectType(IntEnum):
    Video, Image, Document, Other = range(0, 4)


#注册MySQLConverter
mysql.connector.conversion.MySQLConverter._objecttype_to_mysql = lambda self, x: x.value


class Object(db.Model):
    __tablename__ = "object"
    Id = db.Column(db.Integer, primary_key=True)
    OwnerUserId = db.Column(db.Integer)
    FileId = db.Column(db.Integer, db.ForeignKey("file.Id"))
    CreatorUserId = db.Column(db.Integer)
    _Left_ = db.Column(db.Integer)
    _Right_ = db.Column(db.Integer)
    Name = db.Column(db.String(255))
    Extend = db.Column(db.String(255))
    Remark = db.Column(db.String(255))
    Type = db.Column(db.String(255))
    Status = db.Column(db.Integer)
    ParentId = db.Column(db.Integer, db.ForeignKey("object.Id"))
    Size = db.Column(db.Integer)
    ModifyTime = db.Column(db.TIMESTAMP)
    CreateTime = db.Column(db.TIMESTAMP)
    Description = db.Column(db.String(1000))
    Camera = db.Column(db.String(255))
    Script = db.Column(db.String(255))
    Category_1 = db.Column(db.INT)
    Category_2 = db.Column(db.INT)
    Tag = db.Column(db.VARCHAR(255))
    BShare = db.Column(db.BOOLEAN)
    ReferPrice = db.Column(db.FLOAT)
    BasePrice = db.Column(db.FLOAT)
    SchemePrice = db.Column(db.FLOAT)
    ShotPrice = db.Column(db.FLOAT)
    MusicPrice = db.Column(db.FLOAT)
    ActorPrice = db.Column(db.FLOAT)
    AEPrice = db.Column(db.FLOAT)
    Price = db.Column(db.FLOAT) #竞价金额
    File = db.relationship('File', backref=db.backref('Objects', lazy='dynamic'), lazy='joined')
    Parent = db.relationship('Object', backref=db.backref('Children', lazy='dynamic'), remote_side=[Id], uselist=False)

    def __init__(self, Name, _Left_, _Right_, ParentId, OwnerUserId, CreatorUserId, Size):
        self.Name = Name
        self._Left_ = _Left_
        self._Right_ = _Right_
        self.ParentId = ParentId
        self.CreatorUserId = CreatorUserId
        self.OwnerUserId = OwnerUserId
        self.Size = Size
        self.ReferPrice = 0
        self.BShare = 0
        self.BasePrice = 0
        self.SchemePrice = 0
        self.ShotPrice = 0
        self.MusicPrice = 0
        self.ActorPrice = 0
        self.AEPrice = 0
        self.Price = 0
        # self.CreateTime='current_timestamp()'

    def __repr__(self):
        return '<Object %r>' % {'Name': self.Name}


class File(db.Model):
    __tablename__ = "file"
    Id = db.Column(db.Integer, primary_key=True)
    Size = db.Column(db.Integer)
    MD5 = db.Column(db.String(255))#db.Column(db.BINARY(16))
    RefCount = db.Column(db.Integer)
    DelTime = db.Column(db.TIMESTAMP)  # 删除到RefCount为0时的时间
    Path = db.Column(db.String(255))
    Ext = db.Column(db.String(255))
    Status = db.Column(db.Integer)
    CreateTime = db.Column(db.TIMESTAMP)
    WatermarkFile = db.Column(db.String(255))
    #转码后的视频文件如果有的话
    VideoFile = db.Column(db.String(255))
    #视频文件的FileCode
    FileCode = db.Column(db.String(255))
    HighFrequencyFile = db.Column(db.String(255))
    LowFrequencyFile = db.Column(db.String(255))
    TotalTime = db.Column(db.BIGINT)
    Format = db.Column(db.VARCHAR(255))
    BitRate = db.Column(db.FLOAT)
    RatioWidth = db.Column(db.FLOAT)
    RatioHeight = db.Column(db.FLOAT)

    def __init__(self, Ext, Path, MD5, Size, RefCount, VideoUrl, Filecode):
        self.Ext = Ext
        self.Path = Path
        self.MD5 = MD5
        self.Size = Size
        self.RefCount = RefCount
        #self.CreateTime='current_timestamp()'
        #self.DelTime = 'current_timestamp()'
        #视频url
        self.VideoFile = VideoUrl
        self.FileCode = Filecode
    def __repr__(self):
        return '<File %r>' % {'Id': self.Id, 'MD5': self.MD5}


class DomainStatus(IntEnum):
    init, review, use = range(0, 3)


#注册MySQLConverter
mysql.connector.conversion.MySQLConverter._domainstatus_to_mysql = lambda self, x: x.value


class Domain(db.Model):
    __tablename__ = "domain"
    Id = db.Column(db.Integer, primary_key=True)
    DomainName = db.Column(db.VARCHAR(255))
    OwnerUserId = db.Column(db.Integer, db.ForeignKey('user.Id'))
    ExpireTime = db.Column(db.DateTime)
    CreateTime = db.Column(db.TIMESTAMP)
    Alipay = db.Column(db.VARCHAR(50))
    Status = db.Column(db.INT)
    ShowType = db.Column(db.INT)
    CompanyName = db.Column(db.VARCHAR(255))
    CompanyAddr = db.Column(db.VARCHAR(1024))
    CompanyLicense = db.Column(db.VARCHAR(50))
    CompanyPhone = db.Column(db.VARCHAR(15))
    CompanyCelPhone = db.Column(db.VARCHAR(15))
    CompanyFax = db.Column(db.VARCHAR(20))
    CompanyEmail = db.Column(db.VARCHAR(100))
    CompanyLicAttachment = db.Column(db.VARCHAR(255))
    IsService = db.Column(db.BOOLEAN)
    UsedSize = db.Column(db.BIGINT)
    Intro = db.Column(db.VARCHAR(1024))
    StarLevel = db.Column(db.INT)
    ZoneName = db.Column(db.VARCHAR(255))
    Focus = db.Column(db.INT)
    Level = db.Column(db.INT)
    Work = db.Column(db.INT)
    Trade = db.Column(db.INT)
    Count = db.Column(db.FLOAT)
    DefaultStorageSize = db.Column(db.BIGINT)
    ExtendStorageSize = db.Column(db.BIGINT)
    ESExpireTime = db.Column(db.DATETIME)
    MembershipTax = db.Column(db.BIGINT)
    Price = db.Column(db.FLOAT)
    Portrait = db.Column(db.VARCHAR(255))
    Weight = db.Column(db.FLOAT)
    ZoneBanner = db.Column(db.VARCHAR(255))
    Users = db.relationship('User', backref=db.backref('Domain', lazy='joined', uselist=False), lazy='dynamic',
                            foreign_keys='User.DomainId')


    def __init__(self, DomainName, OwnerUserId):
        self.DomainName = DomainName + '\'s' # + '\'s family'
        self.OwnerUserId = OwnerUserId
        self.IsService = 0
        self.Status = DomainStatus.init
        self.ShowType = 0
        self.CompanyName = DomainName
        self.ExtendStorageSize = 0
        self.ExpireTime = datetime.datetime.now()
        self.ESExpireTime = datetime.datetime.now()
        self.Intro = 'intro'
        self.Portrait = '/image/contacts.png'
        self.Trade = 0
        self.Focus = 0
        self.Price = 0
        self.Weight = 0
        self.Count = 0

    def __repr__(self):
        return '<Domain %r>' % {'Id': self.Id, 'DomainName': self.DomainName}


class Role(db.Model):
    __tablename__ = "role"
    Id = db.Column(db.Integer, primary_key=True)
    DomainId = db.Column(db.Integer, db.ForeignKey("domain.Id"))
    Name = db.Column(db.VARCHAR(255))
    CreatorId = db.Column(db.Integer)
    CreateTime = db.Column(db.TIMESTAMP)
    DomainAdmin = db.Column(db.BOOLEAN)
    Domain = db.relationship('Domain', backref=db.backref('Roles', lazy='dynamic'))

    def __init__(self, Name, DomainId, CreatorId, DomainAdmin):
        self.Name = Name
        self.DomainId = DomainId
        self.CreatorId = CreatorId
        self.DomainAdmin = DomainAdmin
        # self.CreateTime='current_timestamp()'

    def __repr__(self):
        return '<Domain %r>' % {'Id': self.Id, 'DomainId': self.DomainId}


class Right(db.Model):
    __tablename__ = "right"
    Id = db.Column(db.BIGINT, primary_key=True)
    Title = db.Column(db.VARCHAR(255))
    Identity = db.Column(db.VARCHAR(255))
    Description = db.Column(db.VARCHAR(1024))
    ParentId = db.Column(db.BIGINT, db.ForeignKey('right.Id'))
    Level = db.Column(db.INT)
    Leaf = db.Column(db.BOOLEAN)
    CreateTime = db.Column(db.TIMESTAMP)
    def __init__(self):
        self.Level = 0
        #self.CreateTime='current_timestamp()'


class RoleRight(db.Model):
    __tablename__ = "roleright"
    Id = db.Column(db.BIGINT, primary_key=True)
    RightId = db.Column(db.BIGINT, db.ForeignKey('right.Id'))
    RoleId = db.Column(db.BIGINT, db.ForeignKey('role.Id'))
    Checked = db.Column(db.BOOLEAN)

    def __init__(self, rightId, roleId, checked):
        self.RightId = rightId
        self.RoleId = roleId
        self.Checked = checked


class Share(db.Model):
    __tablename__ = "share"
    Id = db.Column(db.Integer, primary_key=True)
    ObjectId = db.Column(db.Integer, db.ForeignKey("object.Id"))
    CreatorUserId = db.Column(db.Integer, db.ForeignKey("user.Id"))
    Name = db.Column(db.VARCHAR(255))
    CreateTime = db.Column(db.TIMESTAMP)
    Users = db.relationship("ShareUser",
                            backref=db.backref("Share", uselist=False), lazy="dynamic",
                            foreign_keys="ShareUser.ShareObjectId")
    CreatorUser = db.relationship("User", backref=db.backref("Shares", lazy="dynamic"), uselist=False,
                                  foreign_keys="Share.CreatorUserId")
    Object = db.relationship("Object", uselist=False, backref=db.backref("Shares"))
    UsersCache = db.relationship("ShareUserCache",
                                 backref=db.backref("Share", uselist=False), lazy="dynamic",
                                 foreign_keys="ShareUserCache.ShareObjectId")

    def __init__(self, Name, CreatorUserId, ObjectId):
        self.Name = Name
        self.CreatorUserId = CreatorUserId
        self.ObjectId = ObjectId
        # self.CreateTime='current_timestamp()'

    def __repr__(self):
        return '<Share %r>' % {'Id': self.Id, 'CreatorUserId': self.CreatorUserId}


class ShareUser(db.Model):
    __tablename__ = "shareuser"
    Id = db.Column(db.Integer, primary_key=True)
    ShareObjectId = db.Column(db.Integer, db.ForeignKey("share.Id"))
    UserId = db.Column(db.Integer, db.ForeignKey("user.Id"))
    UserRead = db.Column(db.BOOLEAN)
    UserWrite = db.Column(db.BOOLEAN)
    UserCreate = db.Column(db.BOOLEAN)
    UserDelete = db.Column(db.BOOLEAN)
    UserDownload = db.Column(db.BOOLEAN)
    CreateTime = db.Column(db.TIMESTAMP)
    User = db.relationship('User', lazy='joined')
    ShareObject = db.relationship('Share', uselist=False, backref=db.backref('ShareUser', lazy='dynamic'))

    def __init__(self, UserId, UserRead, UserWrite, UserCreate, UserDelete, UserDownload):
        self.UserId = UserId
        self.UserRead = UserRead
        self.UserWrite = UserWrite
        self.UserCreate = UserCreate
        self.UserDelete = UserDelete
        self.UserDownload = UserDownload
        # self.CreateTime='current_timestamp()'

    def __repr__(self):
        return '<Domain %r>' % {'Id': self.Id, 'UserId': self.UserId}


class ShareUserCache(db.Model):
    __tablename__ = "shareusercache"
    Id = db.Column(db.Integer, primary_key=True)
    ShareObjectId = db.Column(db.Integer, db.ForeignKey("share.Id"))
    UserId = db.Column(db.Integer, db.ForeignKey("user.Id"))
    UserRead = db.Column(db.BOOLEAN)
    UserWrite = db.Column(db.BOOLEAN)
    UserCreate = db.Column(db.BOOLEAN)
    UserDelete = db.Column(db.BOOLEAN)
    UserDownload = db.Column(db.BOOLEAN)
    CreateTime = db.Column(db.TIMESTAMP)
    User = db.relationship('User', lazy='joined', backref=db.backref('ShareCache', lazy='dynamic'))
    ShareObject = db.relationship('Share', uselist=False, backref=db.backref('ShareUserCache', lazy='dynamic'))

    def __init__(self, UserId, UserRead, UserWrite, UserCreate, UserDelete, UserDownload):
        self.UserId = UserId
        self.UserRead = UserRead
        self.UserWrite = UserWrite
        self.UserCreate = UserCreate
        self.UserDelete = UserDelete
        self.UserDownload = UserDownload
        # self.CreateTime='current_timestamp()'

    def __repr__(self):
        return '<Domain %r>' % {'Id': self.Id, 'UserId': self.UserId}


class GroupUser(db.Model):
    __tablename__ = "groupuser"
    Id = db.Column(db.BIGINT, primary_key=True)
    GroupId = db.Column(db.BIGINT, db.ForeignKey('group.Id'))
    UserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    Group = db.relationship('Group', uselist=False)

    def __init__(self, GroupId, UserId):
        self.GroupId = GroupId
        self.UserId = UserId


groupusers = db.Table('groupuser', db.Column('Id', db.BIGINT, primary_key=True), extend_existing=True)


class Group(db.Model):
    __tablename__ = "group"
    Id = db.Column(db.Integer, primary_key=True)
    GroupName = db.Column(db.String(50))
    ShareObjectId = db.Column(db.Integer, db.ForeignKey("share.Id"))
    GroupRead = db.Column(db.BOOLEAN)
    GroupWrite = db.Column(db.BOOLEAN)
    GroupCreate = db.Column(db.BOOLEAN)
    GroupDelete = db.Column(db.BOOLEAN)
    GroupDownload = db.Column(db.BOOLEAN)
    CreateTime = db.Column(db.TIMESTAMP)
    ShareObject = db.relationship('Share', backref=db.backref('Groups', lazy='dynamic'), lazy='select', uselist=False)
    Users = db.relationship('User', secondary=groupusers, backref=db.backref('Group', uselist=False))
    UsersQuery = db.relationship('User', secondary=groupusers, lazy='dynamic')

    def __init__(self, GroupName, GroupRead, GroupWrite, GroupCreate, GroupDelete, GroupDownload):
        self.GroupName = GroupName
        self.GroupRead = GroupRead
        self.GroupWrite = GroupWrite
        self.GroupCreate = GroupCreate
        self.GroupDelete = GroupDelete
        self.GroupDownload = GroupDownload
        # self.CreateTime='current_timestamp()'
    def __repr__(self):
        return '<Group %r>' % {'Id': self.Id, 'OwnerUserId': self.OwnerUserId}


class FileCache(db.Model):
    __tablename__ = "fileCache"
    Id = db.Column(db.BIGINT, primary_key=True)
    ClientFileName = db.Column(db.String(255))
    ServerFileName = db.Column(db.String(255))
    Size = db.Column(db.BIGINT)
    TotalSize = db.Column(db.BIGINT)
    UserId = db.Column(db.BIGINT)
    FileName = db.Column(db.String(255))

    def __init__(self, ClientFileName, ServerFileName, FileSize, UserId, FileName):
        self.ClientFileName = ClientFileName
        self.ServerFileName = ServerFileName
        self.Size = 0
        self.TotalSize = FileSize
        self.UserId = UserId
        self.FileName = FileName
    def __repr__(self):
        return '<FileCache %r>' % {'Id': self.Id, 'ClientFileName': self.ClientFileName}

class Wall(db.Model):
    __tablename__ = "wall"
    Id = db.Column(db.INT, primary_key=True)
    Fileid = db.Column(db.INT, db.ForeignKey('object.Id'))
    Userid = db.Column(db.INT, db.ForeignKey('user.Id'))
    Filename = db.Column(db.VARCHAR)
    object = db.relationship('Object', lazy='joined')
    user = db.relationship('User', lazy='joined')
    def __init__(self, fileid, userid, name):
        self.Fileid = fileid
        self.Userid = userid
        self.Filename = name
    def __repr__(self):
        return'<Wall %r>' % {'Id': self.Id, 'Fileid': self.Fileid, 'Userid': self.Userid, 'Filename': self.Filename}

class Wallsort(db.Model):
    __tablename__ = "wallsort"
    Id = db.Column(db.INT, primary_key=True)
    Wallid = db.Column(db.INT, db.ForeignKey('wall.Id'))
    Sort = db.Column(db.INT)
    wall = db.relationship('Wall', lazy='joined')
    def __init__(self, wallid, sort):
        self.Wallid = wallid
        self.Sort = sort
    def __repr__(self):
        return'<Wallsort %r>' % {'Wallid': self.Wallid, 'Sort': self.Sort}


class Focus(db.Model):
    __tablename__ = "focus"
    Id = db.Column(db.INT, primary_key=True)
    Form = db.Column(db.INT)
    To = db.Column(db.INT)
    def __init__(self, form, to):
        self.Form = form
        self.To = to
    def __repr__(self):
        return '<Focus %r>' % {'form': self.Form, 'to': self.To}


class CommentVideo(db.Model):
    __tablename__ = "comment_video"
    Id = db.Column(db.INT, primary_key=True)
    ObjectId = db.Column(db.INT)
    UserId = db.Column(db.INT, db.ForeignKey('user.Id'))
    CreateTime = db.Column(db.TIMESTAMP)
    Content = db.Column(db.TEXT)
    User = db.relationship('User', lazy='joined')
    def __init__(self, objid, userid, content):
        self.ObjectId = objid
        self.UserId = userid
        self.Content = content
    def __repr__(self):
        return '<Comment %r>' % {'objid': self.ObjectId, 'userid': self.UserId, 'content': self.Content}


class ManageStorage(db.Model):
    __tablename__ = "manage_storage"
    Id = db.Column(db.INT, primary_key=True)
    PlatformStorage = db.Column(db.FLOAT)
    UserStorage = db.Column(db.FLOAT)
    UsedStorage = db.Column(db.FLOAT)
    UpdateTime = db.Column(db.DATE)

    def __init__(self, platform_s, user_s, used_s):
        self.PlatformStorage = platform_s
        self.UserStorage = user_s
        self.UsedStorage = used_s


class PlatformSetting(db.Model):
    __tablename__ = 'platformSetting'
    Id = db.Column(db.BIGINT, primary_key=True)
    StorageSize = db.Column(db.BIGINT)
    MemberShipTax = db.Column(db.FLOAT)


class ManageUser(db.Model):
    __tablename__ = "manage_user"
    Id = db.Column(db.INT, primary_key=True)
    CustomerCount = db.Column(db.BIGINT)
    ProducerCount = db.Column(db.BIGINT)
    UpdateTime = db.Column(db.DATETIME)

    def __init__(self, cc, pc):
        self.CustomerCount = cc
        self.ProducerCount = pc


class ManageTrade(db.Model):
    __tablename__ = "manage_trade"
    Id = db.Column(db.INT, primary_key=True)
    ExtendStorageAmount = db.Column(db.FLOAT)
    ContractAmount = db.Column(db.FLOAT)
    RechargeAccountAmount = db.Column(db.FLOAT)
    MemberShipTaxAmount = db.Column(db.FLOAT)
    TotalAmount = db.Column(db.FLOAT)
    UpdateTime = db.Column(db.DATETIME)

    def __init__(self, esa, ca, raa, msta, ta):
        self.ExtendStorageAmount = esa
        self.ContractAmount = ca
        self.RechargeAccountAmount = raa
        self.MemberShipTaxAmount = msta
        self.TotalAmount = ta


class StorageShare(db.Model):
    __tablename__ = 'storage_share'
    Id = db.Column(db.BIGINT, primary_key=True)
    ObjectId = db.Column(db.BIGINT, db.ForeignKey('object.Id'))
    DomainId = db.Column(db.BIGINT, db.ForeignKey('domain.Id'))
    DownloadPermission = db.Column(db.BOOLEAN)
    WritePermission = db.Column(db.BOOLEAN)
    ObjectOwnerDomainId = db.Column(db.BIGINT, db.ForeignKey('domain.Id'))
    CreateTime = db.Column(db.DATETIME)
    Domain = db.relation('Domain', lazy='joined', foreign_keys='StorageShare.DomainId')
    OwnerDomain = db.relation('Domain', lazy='joined', foreign_keys='StorageShare.ObjectOwnerDomainId')
    Object = db.relation('Object', lazy='joined', foreign_keys='StorageShare.ObjectId')

    def __init__(self, object_id, domain_id, downloadPermission, writePermission, owner_domain_id):
        self.ObjectId = object_id
        self.DomainId = domain_id
        self.DownloadPermission = downloadPermission
        self.WritePermission = writePermission
        self.ObjectOwnerDomainId = owner_domain_id