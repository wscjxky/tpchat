# -*- coding: utf-8 -*-
from Database import db
from enum import IntEnum
import mysql.connector.conversion
import datetime


class RequirementStatus(IntEnum):
    Null, Created, Published, Contracting, PayDeposit, Reviewing, PayAll, Retainage, Last = range(0, 9)
    First = Contracting
    ContractingNext = PayDeposit
    PayDepositNext = Reviewing
    ReviewNext = PayAll
    PayAllNext = Retainage
    RetainageNext = Last


# 注册MySQLConverter
mysql.connector.conversion.MySQLConverter._requirementstatus_to_mysql = lambda self, x: x.value


class Requirement(db.Model):
    __tablename__ = "requirement"
    Id = db.Column(db.BIGINT, primary_key=True)
    PublisherId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    ServiceUserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    Title = db.Column(db.VARCHAR(255))
    Detail = db.Column(db.TEXT)
    Amount = db.Column(db.FLOAT)
    Status = db.Column(db.INT, db.ForeignKey('segment.Id'))
    CreateTime = db.Column(db.TIMESTAMP)
    Publisher = db.relation('User', backref=db.backref('Requirements', lazy='dynamic'),
                            foreign_keys='Requirement.PublisherId', lazy='joined')
    Deadline = db.Column(db.VARCHAR(20))
    Type = db.Column(db.VARCHAR(20))
    Long = db.Column(db.VARCHAR(100))
    Format = db.Column(db.VARCHAR(100))
    Voice = db.Column(db.VARCHAR(2048))
    Gbm = db.Column(db.VARCHAR(2048))
    Place = db.Column(db.VARCHAR(20))
    Refer = db.Column(db.VARCHAR(100))
    ReferName = db.Column(db.VARCHAR(100))
    Symbol = db.Column(db.VARCHAR(20))
    Subtitle = db.Column(db.VARCHAR(2048))
    Category_1 = db.Column(db.INT)
    Category_2 = db.Column(db.INT)
    Scheme = db.Column(db.TEXT)
    ContractId = db.Column(db.INT)
    DepositPercent = db.Column(db.FLOAT)
    Star = db.Column(db.INT)
    Comment = db.Column(db.VARCHAR(255))
    Remark = db.Column(db.TEXT)
    ApplyStatus = db.Column(db.INT)
    ServiceUser = db.relation('User', foreign_keys='Requirement.ServiceUserId', lazy='joined')
    CurSegment = db.relation('Segment', lazy='joined')

    def __init__(self):
        self.DepositPercent = 50.0
        self.ApplyStatus = 0


class RequirementSegment(db.Model):
    __tablename__ = 'requirement_segment'
    Id = db.Column(db.BIGINT, primary_key=True)
    RequirementId = db.Column(db.BIGINT, db.ForeignKey('requirement.Id'))
    SegmentId = db.Column(db.INT, db.ForeignKey('segment.Id'))
    Segment = db.relation('Segment', lazy='joined')
    Requirement = db.relation('Requirement', backref=db.backref('Segments', lazy='joined'), lazy='joined')

    def __init__(self, req_id, seg_id):
        self.RequirementId = req_id
        self.SegmentId = seg_id


class Segment(db.Model):
    __tablename__ = 'segment'
    Id = db.Column(db.BIGINT, primary_key=True)
    Name = db.Column(db.VARCHAR(20))
    Identity = db.Column(db.VARCHAR(20))

    def __init__(self, req_id, seg_id):
        self.RequirementId = req_id
        self.SegmentId = seg_id


class RequirementAttachment(db.Model):
    __tablename__ = "requirementattachment"
    Id = db.Column(db.BIGINT, primary_key=True)
    RequirementId = db.Column(db.BIGINT, db.ForeignKey('requirement.Id'))
    OperateUserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    ObjectId = db.Column(db.BIGINT, db.ForeignKey('object.Id'))
    CreateTime = db.Column(db.TIMESTAMP)
    Description = db.Column(db.VARCHAR(255))
    Requirement = db.relation('Requirement', backref=db.backref('RequirementAttachment', lazy='dynamic'))
    Object = db.relation('Object', lazy='joined')
    OperateUser = db.relation('User', lazy='joined')


class FollowerAttachment(db.Model):
    __tablename__ = 'followerattachment'
    Id = db.Column(db.BIGINT, primary_key=True)
    FollowerId = db.Column(db.BIGINT, db.ForeignKey('requirement_follower.Id'))
    ObjectId = db.Column(db.BIGINT, db.ForeignKey('object.Id'))
    CreateTime = db.Column(db.TIMESTAMP)
    Follower = db.relation('RequirementFollower', backref=db.backref('FollowerAttachment', lazy='joined'))
    Object = db.relation('Object', lazy='joined')

    def __init__(self, follower_id, object_id):
        self.FollowerId = follower_id
        self.ObjectId = object_id
        self.CreateTime = datetime.datetime.now()


class RequirementReplyStatus(IntEnum):
    NewPublished, Contracting, RequirementComplete, Last = range(0, 4)
    First = NewPublished
    NewPublishedNext = Contracting
    ContractingNext = RequirementComplete
    RequirementCompleteNext = Last

#注册MySQLConverter
mysql.connector.conversion.MySQLConverter._requirementreplystatus_to_mysql = lambda self, x: x.value


class RequirementReply(db.Model):
    __tablename__ = "requirementreply"
    Id = db.Column(db.BIGINT, primary_key=True)
    RequirementId = db.Column(db.BIGINT, db.ForeignKey('requirement.Id'))
    PublisherId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    Reply = db.Column(db.Text)
    Status = db.Column(db.BIGINT)
    CreateTime = db.Column(db.TIMESTAMP)
    ReplyGroup = db.Column(db.BIGINT)
    Requirement = db.relation('Requirement', backref=db.backref('RequirementReply', lazy='dynamic'))
    Publisher = db.relation('User', backref=db.backref('RequirementReply', lazy='dynamic'))


class RequirementReplyGroup(db.Model):
    __tablename__ = "requirement_reply_group"
    Id = db.Column(db.BIGINT, primary_key=True)
    RequirementId = db.Column(db.BIGINT, db.ForeignKey('requirement.Id'))
    ServiceDomainId = db.Column(db.BIGINT)
    FollowerId = db.Column(db.BIGINT)  # 方案Id

    def __init__(self, requirementId, serviceDomainId, followerId):
        self.RequirementId = requirementId
        self.ServiceDomainId = serviceDomainId
        self.FollowerId = followerId


class RequirementFollower(db.Model):
    __tablename__ = 'requirement_follower'
    Id = db.Column(db.BIGINT, primary_key=True)
    RequirementId = db.Column(db.BIGINT, db.ForeignKey('requirement.Id'))
    FollowerProducerId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    Scheme = db.Column(db.TEXT)
    Script = db.Column(db.TEXT)
    CreateTime = db.Column(db.TIMESTAMP)
    FollowerDomainId = db.Column(db.BIGINT)
    IsDeny = db.Column(db.BOOLEAN)
    Long = db.Column(db.VARCHAR(100))
    Format = db.Column(db.VARCHAR(100))
    Subtitle = db.Column(db.VARCHAR(2048))
    Voice = db.Column(db.VARCHAR(2048))
    Gbm = db.Column(db.VARCHAR(2048))
    Amount = db.Column(db.FLOAT)
    DepositPercent = db.Column(db.FLOAT)
    Remark = db.Column(db.TEXT)
    Status = db.Column(db.INT)  # 是否申请方案确认，0为未申请，1为申请中
    BasePrice = db.Column(db.FLOAT)
    SchemePrice = db.Column(db.FLOAT)
    ShotPrice = db.Column(db.FLOAT)
    ActorPrice = db.Column(db.FLOAT)
    MusicPrice = db.Column(db.FLOAT)
    AEPrice = db.Column(db.FLOAT)
    Follower = db.relation('User', foreign_keys='RequirementFollower.FollowerProducerId', lazy='joined')
    Requirement = db.relation('Requirement', backref=db.backref('RequirementFollower', lazy='joined'))

    def __init__(self, req_id, followerproducer_id, domain_id):
        self.RequirementId = req_id
        self.FollowerProducerId = followerproducer_id
        self.FollowerDomainId = domain_id
        self.IsDeny = 0
        self.Long = ''
        self.Format = ''
        self.Subtitle = ''
        self.Voice = ''
        self.Gbm = ''
        self.Amount = 0
        self.Script = ''
        self.Remark = ''
        self.DepositPercent = 50
        self.Status = 0
        self.BasePrice = 0
        self.SchemePrice = 0
        self.ShotPrice = 0
        self.ActorPrice = 0
        self.MusicPrice = 0
        self.AEPrice = 0


class ContractStatus(IntEnum):
    Draft, Publish, Established, PayDeposit, Reviewed, PayAll, Retainage, Finish = range(0, 8)
    First = PayDeposit
    PayDepositNext = Reviewed
    ReviewNext = PayAll
    PayAllNext = Retainage
    RetainageNext = Finish

#注册MySQLConverter
mysql.connector.conversion.MySQLConverter._contractstatus_to_mysql = lambda self, x: x.value


class Contract(db.Model):
    __tablename__ = "contract"
    Id = db.Column(db.BIGINT, primary_key=True)
    RequirementId = db.Column(db.BIGINT, db.ForeignKey('requirement.Id'))
    Version = db.Column(db.BIGINT)
    Title = db.Column(db.VARCHAR(255))
    Detail = db.Column(db.TEXT)
    ServiceUserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    CustomerUserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    Status = db.Column(db.BIGINT)
    Amount = db.Column(db.FLOAT)
    CreateTime = db.Column(db.TIMESTAMP)
    PayState = db.Column(db.INTEGER)
    Scheme = db.Column(db.TEXT)
    Script = db.Column(db.TEXT)
    DepositPercent = db.Column(db.FLOAT)
    Procedure = db.Column(db.VARCHAR(20))   # active, applyAbort, abort
    Requirement = db.relation('Requirement', backref=db.backref('Contract', lazy='joined'),
                              foreign_keys='Contract.RequirementId', lazy='joined')
    ServiceUser = db.relation('User',  backref=db.backref('AsServiceContract', lazy='dynamic'),
                                foreign_keys='Contract.ServiceUserId', lazy='joined')
    CustomerUser = db.relation('User', backref=db.backref('AsCustomerContract', lazy='dynamic'),
                               foreign_keys='Contract.CustomerUserId', lazy='joined')
    # ContractSegmentDynamic = db.relation('ContractSegment', lazy='dynamic')

    def __init__(self):
        self.DepositPercent = 50.0
        self.Procedure = 'active'


class ContractAbortRecord(db.Model):
    __tablename__ = 'contract_abort_record'
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'), primary_key=True)
    ApplyRemark = db.Column(db.VARCHAR(255))
    ConfirmRemark = db.Column(db.VARCHAR(255))
    ApplyUserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    ApplyTime = db.Column(db.DATETIME)
    ConfirmTime = db.Column(db.DATETIME)
    ApplyDomainId = db.Column(db.BIGINT)
    Status = db.Column(db.VARCHAR(20))
    ApplyUser = db.relation('User', lazy='joined', foreign_keys='ContractAbortRecord.ApplyUserId')
    Contract = db.relation('Contract', lazy='joined', foreign_keys='ContractAbortRecord.ContractId')

    def __init__(self, cid, apply_remark, apply_userid, apply_domainid, apply_time):
        self.ContractId = cid
        self.ApplyRemark = apply_remark
        self.ApplyUserId = apply_userid
        self.ApplyDomainId = apply_domainid
        self.ApplyTime = apply_time
        self.Status = 'apply'


class ContractSegmentStatus(IntEnum):
    Init, Applied, Confirmed, Returned = range(0, 4)


#注册MySQLConverter
mysql.connector.conversion.MySQLConverter._contractsegmentstatus_to_mysql = lambda self, x: x.value


class ContractSegmentType(IntEnum):
    Apply, Establish, Start, Reviewed, Complete, End = range(0, 6)

#注册MySQLConverter
mysql.connector.conversion.MySQLConverter._contractsegmenttype_to_mysql = lambda self, x: x.value


class ContractSegment(db.Model):
    __tablename__ = "contractsegment"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'))
    Segment = db.Column(db.BIGINT)
    Deadline = db.Column(db.DATETIME)
    Remark = db.Column(db.VARCHAR(2000))
    ApplyUserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    ApplyTime = db.Column(db.DATETIME)
    ApplyRemark = db.Column(db.VARCHAR(2000))
    ConfirmUserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    ConfirmTime = db.Column(db.DATETIME)
    ConfirmRemark = db.Column(db.VARCHAR(2000))
    Status = db.Column(db.BIGINT)
    CreateTime = db.Column(db.TIMESTAMP)
    ServiceResponser = db.Column(db.BIGINT)
    CustomerResponser = db.Column(db.BIGINT)
    # Contract = db.relation('Contract', backref=db.backref('ContractSegment',order_by='ContractSegment.Segment,ContractSegment.Id', lazy='joined'))
    ApplyUser = db.relation('User', foreign_keys='ContractSegment.ApplyUserId', lazy='joined')
    ConfirmUser = db.relation('User', foreign_keys='ContractSegment.ConfirmUserId', lazy='joined')


class ContractAttachmentType(IntEnum):
    Exchange, Clip, CutVideo, RenderVideo, SoundVideo, FinalVideo, End = range(0, 7)

#注册MySQLConverter
mysql.connector.conversion.MySQLConverter._contractattachmenttype_to_mysql = lambda self, x: x.value


class ContractAttachment(db.Model):
    __tablename__ = "contractattachment"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'))
    ProviderUserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    ObjectId = db.Column(db.BIGINT, db.ForeignKey('object.Id'))
    CreateTime = db.Column(db.TIMESTAMP)
    Type = db.Column(db.INT)
    Status = db.Column(db.INT)
    Contract = db.relation('Contract', backref=db.backref('ContractAttachment', lazy='dynamic'))
    ProviderUser = db.relation('User', backref=db.backref('ContractAttachment', lazy='dynamic'))
    Object = db.relation('Object', lazy='joined')

class AttachmentProtect(db.Model):
    __tablename__ = "attachment_protect"
    Id = db.Column(db.BIGINT, primary_key=True)
    ObjectId = db.Column(db.INT)
    ContractId = db.Column(db.INT)
    Deadline = db.Column(db.DATETIME)

    def __init__(self, objectid, contractid, deadline):
        self.ObjectId = objectid
        self.ContractId = contractid
        self.Deadline = deadline

class ContractLogActionType(IntEnum):
    Reply, Apply, Deny, Cancel, Accept, Edit = range(0, 6)

#注册MySQLConverter
mysql.connector.conversion.MySQLConverter._contractlogactiontype_to_mysql = lambda self, x: x.value


class ContractEventLog(db.Model):
    __tablename__ = "contracteventlog"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'))
    UserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    Action = db.Column(db.BIGINT)
    Segment = db.Column(db.BIGINT)
    Detail = db.Column(db.TEXT)
    CreateTime = db.Column(db.TIMESTAMP)
    Contract = db.relation('Contract', backref=db.backref('ContractEventLog', lazy='dynamic'))
    User = db.relation('User', backref=db.backref('ContractEventLog', lazy='dynamic'))

    def __init__(self, con_id, user_id, action, segment, detail):
        self.ContractId = con_id
        self.UserId = user_id
        self.Action = action
        self.Segment = segment
        self.Detail = detail


class ContractReply(db.Model):
    __tablename__ = "contractreply"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'))
    PublisherId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    Reply = db.Column(db.Text)
    Status = db.Column(db.BIGINT)
    CreateTime = db.Column(db.TIMESTAMP)
    DestUserId = db.Column(db.BIGINT)
    Contract = db.relation('Contract')
    Publisher = db.relation('User')


class ContractUserGroup(db.Model):
    __tablename__ = "contractusergroup"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'))
    UserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    DomainId = db.Column(db.BIGINT)
    CreateTime = db.Column(db.TIMESTAMP)
    Description = db.Column(db.VARCHAR(255))
    User = db.relation('User', lazy='joined')

    def __init__(self, con_id, user_id, domain_id, description):
        self.ContractId = con_id
        self.UserId = user_id
        self.DomainId = domain_id
        self.Description = description


class ContractHistory(db.Model):
    __tablename__ = "contracthistory"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'))
    Version = db.Column(db.BIGINT)
    RejectReason = db.Column(db.VARCHAR(1024))
    RejectTime = db.Column(db.DATETIME)
    ApplyRemark = db.Column(db.VARCHAR(1024))
    ApplyTime = db.Column(db.DATETIME)
    CreateTime = db.Column(db.TIMESTAMP)
    Detail = db.Column(db.TEXT)
    ModifyPerson = db.Column(db.VARCHAR(255))
    Scheme = db.Column(db.TEXT)
    Script = db.Column(db.TEXT)
    DepositPercent = db.Column(db.FLOAT)
    Contract = db.relation('Contract', backref=db.backref('ContractHistory', lazy='dynamic'))


class Project(db.Model):
    __tablename__ = "project"
    Id = db.Column(db.BIGINT, primary_key=True)
    PrincipalUserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'))
    RequirementId = db.Column(db.BIGINT, db.ForeignKey('requirement.Id'))
    Title = db.Column(db.VARCHAR(255))
    Detail = db.Column(db.TEXT)
    CreateTime = db.Column(db.TIMESTAMP)
    # Contract = db.relation('Contract', lazy="joined", backref=db.backref('Project', lazy='dynamic'))
    # PrincipalUser = db.relation('User', lazy="joined", backref=db.backref('Project', lazy='dynamic'))
    # Requirement = db.relation('Requirement', lazy="joined", backref=db.backref('Project', lazy='dynamic'))
    # ProjectSegmentDynamic = db.relation('ProjectSegment', lazy='dynamic')

class ProjectSegmentStatus(IntEnum):
    Init, Applied, Confirmed, Returned = range(0, 4)


#注册MySQLConverter
mysql.connector.conversion.MySQLConverter._projectsegmentstatus_to_mysql = lambda self, x: x.value


class ProjectSegmentType(IntEnum):
    Edit, Reviewed = range(0, 2)

#注册MySQLConverter
mysql.connector.conversion.MySQLConverter._projectsegmenttype_to_mysql = lambda self, x: x.value


class ProjectSegment(db.Model):
    __tablename__ = "projectsegment"
    Id = db.Column(db.BIGINT, primary_key=True)
    ProjectId = db.Column(db.BIGINT, db.ForeignKey('project.Id'))
    ContractSegmentId = db.Column(db.BIGINT, db.ForeignKey('contractsegment.Id'))
    PrincipalUserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    Segment = db.Column(db.BIGINT)
    Deadline = db.Column(db.DATETIME)
    Remark = db.Column(db.VARCHAR(2000))
    ApplyUserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    ApplyTime = db.Column(db.DATETIME)
    ApplyRemark = db.Column(db.VARCHAR(2000))
    ConfirmUserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    ConfirmTime = db.Column(db.DATETIME)
    ConfirmRemark = db.Column(db.VARCHAR(2000))
    Status = db.Column(db.BIGINT)
    CreateTime = db.Column(db.TIMESTAMP)
    ContractSegment = db.relation('ContractSegment',  backref=db.backref('ProjectSegment', lazy='dynamic'))
    Project = db.relation('Project', backref=db.backref('ProjectSegment',lazy='joined'))
    ApplyUser = db.relation('User', foreign_keys='ProjectSegment.ApplyUserId',lazy='joined')
    ConfirmUser = db.relation('User', foreign_keys='ProjectSegment.ConfirmUserId',lazy='joined')


class ProjectEventLog(db.Model):
    __tablename__ = "projecteventlog"
    Id = db.Column(db.BIGINT, primary_key=True)
    ProjectId = db.Column(db.BIGINT, db.ForeignKey('project.Id'))
    UserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    Action = db.Column(db.BIGINT)
    Segment = db.Column(db.BIGINT)
    Detail = db.Column(db.TEXT)
    CreateTime = db.Column(db.TIMESTAMP)
    Project = db.relation('Project', backref=db.backref('ProjectEventLog', lazy='dynamic'))
    ApplyUser = db.relation('User', backref=db.backref('ProjectEventLog', lazy='dynamic'))


class SchemeHistory(db.Model):
    __tablename__ = "schemehistory"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'))
    Version = db.Column(db.BIGINT)
    RejectReason = db.Column(db.VARCHAR(1024))
    RejectTime = db.Column(db.DATETIME)
    ApplyRemark = db.Column(db.VARCHAR(1024))
    ApplyTime = db.Column(db.DATETIME)
    CreateTime = db.Column(db.TIMESTAMP)
    Detail = db.Column(db.TEXT)
    SchemeId = db.Column(db.BIGINT, db.ForeignKey('scheme.Id'))


class Scheme(db.Model):
    __tablename__ = "scheme"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'))
    Version = db.Column(db.BIGINT)
    Detail = db.Column(db.TEXT)
    SchemeHistory = db.relation('SchemeHistory')

    def __init__(self, version, contractId):
        self.Version = version
        self.ContractId = contractId


class ScriptHistory(db.Model):
    __tablename__ = "scripthistory"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'))
    Version = db.Column(db.BIGINT)
    RejectReason = db.Column(db.VARCHAR(1024))
    RejectTime = db.Column(db.DATETIME)
    ApplyRemark = db.Column(db.VARCHAR(1024))
    ApplyTime = db.Column(db.DATETIME)
    CreateTime = db.Column(db.TIMESTAMP)
    Detail = db.Column(db.TEXT)
    ScriptId = db.Column(db.BIGINT, db.ForeignKey('script.Id'))


class Script(db.Model):
    __tablename__ = "script"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'))
    Version = db.Column(db.BIGINT)
    Detail = db.Column(db.TEXT)
    ScriptHistory = db.relation('ScriptHistory')

    def __init__(self, version, contractId):
        self.Version = version
        self.ContractId = contractId


class ContractClipsHistory(db.Model):
    __tablename__ = "contractclipshistory"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'))
    ContractClipsId = db.Column(db.BIGINT, db.ForeignKey('contractclips.Id'))
    Version = db.Column(db.BIGINT)
    RejectReason = db.Column(db.VARCHAR(1024))
    RejectTime = db.Column(db.DATETIME)
    ApplyRemark = db.Column(db.VARCHAR(1024))
    ApplyTime = db.Column(db.DATETIME)
    CreateTime = db.Column(db.TIMESTAMP)
    Detail = db.Column(db.TEXT)


class ContractClips(db.Model):
    __tablename__ = "contractclips"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'))
    Version = db.Column(db.BIGINT)
    Detail = db.Column(db.TEXT)
    ContractClipsHistory = db.relation('ContractClipsHistory')

    def __init__(self, version, contractId):
        self.Version = version
        self.ContractId = contractId


class ReviewVideoHistory(db.Model):
    __tablename__ = "reviewvideohistory"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'))
    ReviewVideoId = db.Column(db.BIGINT, db.ForeignKey('reviewvideo.Id'))
    Version = db.Column(db.BIGINT)
    RejectReason = db.Column(db.VARCHAR(1024))
    RejectTime = db.Column(db.DATETIME)
    ApplyRemark = db.Column(db.VARCHAR(1024))
    ApplyTime = db.Column(db.DATETIME)
    CreateTime = db.Column(db.TIMESTAMP)
    Detail = db.Column(db.TEXT)


class ReviewVideo(db.Model):
    __tablename__ = "reviewvideo"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'))
    Version = db.Column(db.BIGINT)
    Detail = db.Column(db.TEXT)
    ReviewVideoHistory = db.relation('ReviewVideoHistory')

    def __init__(self, version, contractId):
        self.Version = version
        self.ContractId = contractId


class FinalVideoHistory(db.Model):
    __tablename__ = "finalvideohistory"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'))
    FinalVideoId = db.Column(db.BIGINT, db.ForeignKey('finalvideo.Id'))
    Version = db.Column(db.BIGINT)
    RejectReason = db.Column(db.VARCHAR(1024))
    RejectTime = db.Column(db.DATETIME)
    ApplyRemark = db.Column(db.VARCHAR(1024))
    ApplyTime = db.Column(db.DATETIME)
    CreateTime = db.Column(db.TIMESTAMP)
    Detail = db.Column(db.TEXT)


class FinalVideo(db.Model):
    __tablename__ = "finalvideo"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT, db.ForeignKey('contract.Id'))
    Version = db.Column(db.BIGINT)
    Detail = db.Column(db.TEXT)
    FinalVideoHistory = db.relation('FinalVideoHistory')

    def __init__(self, version, contractId):
        self.Version = version
        self.ContractId = contractId


class OrderState(IntEnum):
    UnPay, Payed = range(0, 2)

mysql.connector.conversion.MySQLConverter._orderstate_to_mysql = lambda self, x: x.value


class Order(db.Model):
    __tablename__ = "order"
    Id = db.Column(db.BIGINT, primary_key=True)
    SerialNumber = db.Column(db.VARCHAR(255))
    Subject = db.Column(db.VARCHAR(100))
    Description = db.Column(db.VARCHAR(255))
    Amount = db.Column(db.FLOAT)
    UseAccount = db.Column(db.FLOAT)
    State = db.Column(db.INT)
    PayUserId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    ReceiverId = db.Column(db.BIGINT, db.ForeignKey('user.Id'))
    CreateTime = db.Column(db.TIMESTAMP)
    PayUser = db.relation('User', foreign_keys='Order.PayUserId', lazy="joined")
    Receiver = db.relation('User', foreign_keys='Order.ReceiverId', lazy="joined")

    def __init__(self, SerialNumber, Subject, Description, Amount, PayUserId, ReceiverId):
        self.SerialNumber = SerialNumber
        self.Subject = Subject
        self.Description = Description
        self.Amount = Amount
        self.UseAccount = 0
        self.PayUserId = PayUserId
        self.ReceiverId = ReceiverId
        self.State = OrderState.UnPay


class OrderLog(db.Model):
    __tablename__ = "order_log"
    Id = db.Column(db.BIGINT, primary_key=True)
    OrderId = db.Column(db.BIGINT)
    OrderType = db.Column(db.VARCHAR(100))
    Log = db.Column(db.VARCHAR(255))
    Action = db.Column(db.VARCHAR(100))
    CreateTime = db.Column(db.DATETIME)

    def __init__(self, orderId, orderType, log, action):
        self.OrderType = orderType
        self.OrderId = orderId
        self.Log = log
        self.Action = action


class ContractOrderType(IntEnum):
    PayRent, PayRest = range(0, 2)

mysql.connector.conversion.MySQLConverter._contractordertype_to_mysql = lambda self, x: x.value


class ContractOrder(db.Model):
    __tablename__ = "contract_order"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT, db.ForeignKey("contract.Id"))
    OrderId = db.Column(db.BIGINT, db.ForeignKey("order.Id"))
    OrderType = db.Column(db.INT)
    Contract = db.relation('Contract', lazy="joined", backref=db.backref('ContractOrder', lazy='dynamic'))
    Order = db.relation('Order', lazy="joined")

    def __init__(self, ContractId, OrderId, OrderType):
        self.ContractId = ContractId
        self.OrderId = OrderId
        self.OrderType = OrderType


class ResourceShare(db.Model):
    __tablename__ = "resourceshare"
    Id = db.Column(db.BIGINT, primary_key=True)
    ResourceId = db.Column(db.BIGINT)
    ResourceType = db.Column(db.VARCHAR(10))
    ShareDomainId = db.Column(db.BIGINT, db.ForeignKey('domain.Id'))
    ShareDomain = db.relation('Domain', lazy='joined')

    def __init__(self, resource_id, resource_type, share_domain_id):
        self.ResourceId = resource_id
        self.ResourceType = resource_type
        self.ShareDomainId = share_domain_id


class MarkPoint(db.Model):
    __tablename__ = "markpoint"
    Id = db.Column(db.BIGINT, primary_key=True)
    AttachmentId = db.Column(db.BIGINT)
    Time = db.Column(db.TIME)
    Content = db.Column(db.TEXT)

    def __init__(self, attachmentId, time, content):
        self.AttachmentId = attachmentId
        self.Time = time
        self.Content = content


class ContractSegmentLog(db.Model):
    __tablename__ = "contractSegmentLog"
    Id = db.Column(db.BIGINT, primary_key=True)
    ContractId = db.Column(db.BIGINT)
    SegmentId = db.Column(db.BIGINT)
    RejectRemark = db.Column(db.VARCHAR(1024))
    RejectTime = db.Column(db.DATETIME)
    ApplyRemark = db.Column(db.VARCHAR(1024))
    ApplyTime = db.Column(db.DATETIME)
    bConfirm = db.Column(db.BOOLEAN)

    def __init__(self, cid, sid):
        self.ContractId = cid
        self.SegmentId = sid
        self.bConfirm = False


class Category(db.Model):
    __tablename__ = "category"
    Id = db.Column(db.BIGINT, primary_key=True)
    Name = db.Column(db.VARCHAR(20))
    Level = db.Column(db.INT)
    ParentId = db.Column(db.INT)

class Tag(db.Model):
    __tablename__ = "tag"
    Id = db.Column(db.BIGINT, primary_key=True)
    Name = db.Column(db.VARCHAR(20))
    UserId = db.Column(db.INT)

class ZoneItemType(IntEnum):
    Picture, Video = range(0, 2)

#注册MySQLConverter
mysql.connector.conversion.MySQLConverter._zoneitemtype_to_mysql = lambda self, x: x.value


class ZoneItemClassicalStatus(IntEnum):
    notApply, applying, applySuccuss, applyDeny = range(0, 4)

#注册MySQLConverter
mysql.connector.conversion.MySQLConverter._zoneitemclassicalstatus_to_mysql = lambda self, x: x.value

class ZoneItem(db.Model):
    __tablename__ = "zone_item"
    Id = db.Column(db.BIGINT, primary_key=True)
    DomainId = db.Column(db.BIGINT, db.ForeignKey('domain.Id'))
    ObjectId = db.Column(db.BIGINT, db.ForeignKey('object.Id'))
    Intro = db.Column(db.VARCHAR(255))
    Price = db.Column(db.FLOAT)
    Weight = db.Column(db.FLOAT)
    Type = db.Column(db.INT)
    Classical = db.Column(db.INT)
    Favorite = db.Column(db.INT)
    Portrait = db.Column(db.VARCHAR(255))
    ReferPrice = db.Column(db.FLOAT)
    BasePrice = db.Column(db.FLOAT)
    SchemePrice = db.Column(db.FLOAT)
    ShotPrice = db.Column(db.FLOAT)
    MusicPrice = db.Column(db.FLOAT)
    ActorPrice = db.Column(db.FLOAT)
    AEPrice = db.Column(db.FLOAT)
    ClassicalWeight = db.Column(db.FLOAT)
    ViewCount = db.Column(db.INT)
    Boutique = db.Column(db.BOOLEAN)
    Object = db.relation('Object', lazy="joined",  foreign_keys='ZoneItem.ObjectId')
    Domain = db.relation('Domain', lazy="joined", foreign_keys='ZoneItem.DomainId')

    def __init__(self, domain_id, object_id, intro):
        self.DomainId = domain_id
        self.ObjectId = object_id
        self.Intro = intro
        self.Favorite = 0
        self.ClassicalWeight = 0
        self.ViewCount = 0
        self.Boutique = 0


class RequirementTemplate(db.Model):
    __tablename__ = "requirement_template"
    Id = db.Column(db.BIGINT, primary_key=True)
    Category_1 = db.Column(db.INT)
    Category_2 = db.Column(db.INT)
    Detail = db.Column(db.TEXT)

    def __init__(self, category_1, category_2, content):
        self.Category_1 = category_1
        self.Category_2 = category_2
        self.Detail = content


class ExtendStorageOrder(db.Model):
    __tablename__ = "extendStorage_order"
    Id = db.Column(db.BIGINT, primary_key=True)
    ExtendTime = db.Column(db.INT)
    UseAccount = db.Column(db.BIGINT)
    ExtendStorageSize = db.Column(db.BIGINT)
    OrderId = db.Column(db.BIGINT, db.ForeignKey("order.Id"))
    CreateTime = db.Column(db.TIMESTAMP)
    Order = db.relation('Order', lazy="joined")

    def __init__(self, extendTime, useAccount, extendStorageSize, orderId):
        self.ExtendTime = extendTime
        self.UseAccount = useAccount
        self.ExtendStorageSize = extendStorageSize
        self.OrderId = orderId


class RechargeAccountOrder(db.Model):
    __tablename__ = "rechargeAccount_order"
    Id = db.Column(db.BIGINT, primary_key=True)
    Amount = db.Column(db.BIGINT)
    OrderId = db.Column(db.BIGINT, db.ForeignKey("order.Id"))
    CreateTime = db.Column(db.TIMESTAMP)
    Order = db.relation('Order', lazy="joined")

    def __init__(self, amount, orderId):
        self.Amount = amount
        self.OrderId = orderId


class MemberShipTaxOrder(db.Model):
    __tablename__ = "membershiptax_order"
    Id = db.Column(db.BIGINT, primary_key=True)
    OrgExpireTime = db.Column(db.DATETIME)
    ExpireTime = db.Column(db.DATETIME)
    OrderId = db.Column(db.BIGINT, db.ForeignKey("order.Id"))
    CreateTime = db.Column(db.TIMESTAMP)
    Order = db.relation('Order', lazy="joined")

    def __init__(self, orgExpireTime, expireTime, orderId):
        self.OrgExpireTime = orgExpireTime
        self.ExpireTime = expireTime
        self.OrderId = orderId


class CollectionProducer(db.Model):
    __tablename__ = "collection_producer"
    Id = db.Column(db.BIGINT, primary_key=True)
    DomainId = db.Column(db.BIGINT, db.ForeignKey("domain.Id"))
    UserId = db.Column(db.BIGINT)
    Domain = db.relation('Domain', lazy="joined")

    def __init__(self, domain_id, user_id):
        self.DomainId = domain_id
        self.UserId = user_id


class CollectionVideo(db.Model):
    __tablename__ = "collection_video"
    Id = db.Column(db.BIGINT, primary_key=True)
    ZoneItemId = db.Column(db.BIGINT, db.ForeignKey("zone_item.Id"))
    UserId = db.Column(db.BIGINT, db.ForeignKey("user.Id"))
    ZoneItem = db.relation('ZoneItem', lazy="joined")
    User = db.relation('User', lazy="joined")

    def __init__(self, item_id, user_id):
        self.ZoneItemId = item_id
        self.UserId = user_id


# ResourceType: 'requirement'
# MsgType: 'reply', 'cancelFocus', 'focus', 'apply'
# -----------------------------------
# ResourceType: 'contract'
# MsgType: 'negotiation', 'reply', 'action'
# -----------------------------------
class PlatformMsg(db.Model):
    __tablename__ = "platform_msg"
    Id = db.Column(db.BIGINT, primary_key=True)
    Title = db.Column(db.VARCHAR(100))
    Msg = db.Column(db.VARCHAR(255))
    SrcUserId = db.Column(db.BIGINT)
    DestUserId = db.Column(db.BIGINT)
    ResourceId = db.Column(db.BIGINT)
    ResourceType = db.Column(db.VARCHAR(100))
    MsgType = db.Column(db.VARCHAR(100))
    IsReaded = db.Column(db.BOOLEAN)
    IsAdopted = db.Column(db.BOOLEAN)
    CreateTime = db.Column(db.DATETIME)

    def __init__(self, title, msg, srcUserId, destUserId, resourceId, resourceType, msgType):
        self.Title = title
        self.Msg = msg
        self.SrcUserId = srcUserId
        self.DestUserId = destUserId
        self.ResourceId = resourceId
        self.ResourceType = resourceType
        self.MsgType = msgType
        self.IsReaded = 0
        self.IsAdopted = 0


class ApplyMoneyStatus(IntEnum):
    applying, deny, ok = range(0, 3)

#注册MySQLConverter
mysql.connector.conversion.MySQLConverter._applymoneystatus_to_mysql = lambda self, x: x.value


class ApplyMoney(db.Model):
    __tablename__ = "apply_money"
    Id = db.Column(db.INT, primary_key=True)
    DomainId = db.Column(db.INT, db.ForeignKey("domain.Id"))
    Money = db.Column(db.FLOAT)
    CreateTime = db.Column(db.TIMESTAMP)
    Status = db.Column(db.INT)
    UserId = db.Column(db.BIGINT)
    Domain = db.relation('Domain', lazy='joined')

    def __init__(self, domainId, userId, money):
        self.DomainId = domainId
        self.Money = money
        self.Status = 0
        self.UserId = userId
        self.CreateTime = datetime.datetime.now()


class Favortie(db.Model):
    __tablename__ = "favorite"
    Id = db.Column(db.INT, primary_key=True)
    ZoneItemId = db.Column(db.VARCHAR(255))
    UserId = db.Column(db.VARCHAR(255))

    def __init__(self, zi, ud):
        self.ZoneItemId = zi
        self.UserId = ud


# 微信接口访问凭证
class WeiXinToken(db.Model):
    __tablename__ = "weixin_token"
    Id = db.Column(db.INT, primary_key=True)
    AccessToken = db.Column(db.VARCHAR(1024))
    CreateTime = db.Column(db.TIMESTAMP)
    Expires_in = db.Column(db.INT)

    def __init__(self, access_token, expires_in):
        self.AccessToken = access_token
        self.Expires_in = expires_in
        self.CreateTime = datetime.datetime.now()


# 微信js接口访问凭证
class WeiXinJsTicket(db.Model):
    __tablename__ = "weixin_js_ticket"
    Id = db.Column(db.INT, primary_key=True)
    JsapiTicket = db.Column(db.VARCHAR(1024))
    CreateTime = db.Column(db.TIMESTAMP)
    Expires_in = db.Column(db.INT)
    NonceStr = db.Column(db.VARCHAR(255))
    Timestamp = db.Column(db.VARCHAR(255))
    Signature = db.Column(db.VARCHAR(1024))

    def __init__(self, Jsapi_ticket, expires_in):
        self.JsapiTicket = Jsapi_ticket
        self.Expires_in = expires_in
        self.CreateTime = datetime.datetime.now()


# 平台留言
class LeaveMsg(db.Model):
    __tablename__ = "leave_msg"
    Id = db.Column(db.BIGINT, primary_key=True)
    Msg = db.Column(db.VARCHAR(1024))
    Name = db.Column(db.VARCHAR(100))
    Phone = db.Column(db.VARCHAR(20))
    Email = db.Column(db.VARCHAR(100))
    CreateTime = db.Column(db.TIMESTAMP)
    Deal = db.Column(db.INT)

    def __init__(self, msg, name, phone, email):
        self.Msg = msg
        self.Name = name
        self.Phone = phone
        self.Email = email
        self.CreateTime = datetime.datetime.now()
        self.Deal = 0