from flask import Flask, Blueprint, render_template, abort, request, session, url_for, redirect
from Config import *
from Tools.DataPaser import *
from Tools.Permision import *
from json import JSONDecoder
from jinja2 import TemplateNotFound
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import delete, or_, and_
from Models.Database import db
from Models.Index import *
from Models.CloudStorge import *
from Models.Platform import *
import jinja2

index = Blueprint('index', __name__, template_folder='templates', static_folder='static')

@jinja2.contextfilter
@index.app_template_filter()
def filter_prefex(context, value):
    npos = value.rfind('.')
    if npos != -1:
        file_name_no_prefix = value[0:npos]
    else:
        file_name_no_prefix = value
    return file_name_no_prefix


@index.route('/')
@incoming_params
def Index():
    try:
        cookies = request.cookies
        if u'DBToken' in cookies:
            try:
                user = db.session.query(User).filter(User.SessionId == cookies[u'DBToken']).one()
            except NoResultFound:
                user = ''
        else:
            user = ''
        banner = IndexBanner.query.all()
        set_claccical = db.session.query(ClassicalSetting).order_by(ClassicalSetting.Position).limit(3).all()
        # good_video = db.session.query(ZoneItem).filter(ZoneItem.Type == 1).join(Domain, Domain.Id == ZoneItem.DomainId).\
        #     filter(Domain.Status == 2).order_by(ZoneItem.Favorite.desc()).limit(3).all()
        recent_video = db.session.query(ZoneItem).filter(ZoneItem.Type == 1).join(Object, Object.Id == ZoneItem.ObjectId)\
            .join(Domain, Domain.Id == ZoneItem.DomainId).filter(and_(Domain.IsService == 1,Domain.ShowType !=0)).order_by(Object.ModifyTime.desc()).limit(1).all()
        channel = db.session.query(ChannelSetting).filter(ChannelSetting.ParentId == None).order_by(ChannelSetting.Position).all()
        # s_channel = db.session.query(ChannelSetting).filter(ChannelSetting.ParentId != None).order_by(ChannelSetting.Position).all()
        server = db.session.query(Domain).filter(and_(Domain.IsService == 1, Domain.ShowType == 2)).order_by(Domain.Price*Domain.Weight.desc()).all()
        #server = db.session.query(Domain).filter(and_(Domain.IsService == 1, Domain.Status == 2)).order_by(Domain.Price*Domain.Weight.desc()).all()
        #user_index = db.session.query(User).filter(User.type == 1).all()
        user_index = db.session.query(Domain).filter(and_(Domain.IsService == 0, Domain.ShowType == 2)).all()
        producer_visable = db.session.query(Settings).filter(Settings.Item == 'isProducerVisable').one().Value
        return render_template('index/index.html', floder=UPLOAD_FOLDER, banner=banner,
               set_classical=set_claccical, channel=channel, server=server, user=user,
               recent_video=recent_video, user_index=user_index,producer_visable=producer_visable)
    except TemplateNotFound:
        abort(404)

@index.route('/aboutus')
def aboutus():
    try:
        cookies = request.cookies
        if u'DBToken' in cookies:
            try:
                user = db.session.query(User).filter(User.SessionId == cookies[u'DBToken']).one()
            except NoResultFound:
                user = ''
        else:
            user = ''
        return render_template('index/aboutus.html', user=user)
    except TemplateNotFound:
        abort(404)

@index.route('/contact')
def contact():
    try:
        cookies = request.cookies
        if u'DBToken' in cookies:
            try:
                user = db.session.query(User).filter(User.SessionId == cookies[u'DBToken']).one()
            except NoResultFound:
                user = ''
        else:
            user = ''
        return render_template('index/contact.html', user=user)
    except TemplateNotFound:
        abort(404)

@index.route('/InitIndexChannel', methods=['GET', 'POST'])
@output_data
def InitIndexChannel():
    template = {}
    param = request.json_param
    index = 0

    for i in param['init_channel']:
        #以下查询语句，去掉：.filter(ZoneItem.Classical == ZoneItemClassicalStatus.applySuccuss)\
        videos = db.session.query(ZoneItem).join(Domain, Domain.Id == ZoneItem.DomainId)\
            .filter(and_(Domain.IsService == 1, Domain.ShowType !=0))\
            .join(Object, Object.Id == ZoneItem.ObjectId).filter(Object.Category_1 == i).filter(ZoneItem.Type == 1)\
            .order_by(ZoneItem.ClassicalWeight.desc()).limit(4).all()
        if len(videos) < 4:
            moreVideos = db.session.query(ZoneItem).join(Domain, Domain.Id == ZoneItem.DomainId)\
                .filter(and_(Domain.IsService == 1, Domain.ShowType !=0))\
                .join(Object, Object.Id == ZoneItem.ObjectId).filter(Object.Category_1 == i).filter(ZoneItem.Type == 1)\
                .order_by(ZoneItem.ClassicalWeight.desc()).limit(4 - len(videos)).all()
            videos.extend(moreVideos)

        category = db.session.query(Category).filter(Category.Id == i).one().Name
        backupName = category+"类型" #db.session.query(ChannelSetting).filter(ChannelSetting.CategoryId == i).one().BackupName

        if len(videos) <> 4:
            continue
        index = index + 1
        if index % 2 == 0:
            videos.reverse()

        template[i] = render_template("index/channel_index.html", videos=videos, categoryId=int(i),
                                      iOrder=index, category=category, backupName=backupName)
    return template

@index.route('/classical', defaults={'page': 1})
@index.route('/classical/<page>')
def classical(page):
    try:
        cookies = request.cookies
        if u'DBToken' in cookies:
            try:
                user = db.session.query(User).filter(User.SessionId == cookies[u'DBToken']).one()
            except NoResultFound:
                user=''
        else:
            user = ''
        page = int(page)
        ItemInPage = 36
        if ZoneItem.query.count() % ItemInPage == 0:
            page_count = ZoneItem.query.filter(classical == 2).count()/ItemInPage
        else:
            page_count = ZoneItem.query.filter(classical == 2).count()/ItemInPage + 1
        pre = page-1
        next = page+1
        object = db.session.query(ZoneItem).join(Domain, Domain.Id == ZoneItem.DomainId).filter(Domain.IsService == 1)\
            .filter(ZoneItem.Type == 1).offset((page-1)*ItemInPage).limit(ItemInPage).all()
        return render_template('index/classical.html', object=object, page=page, page_count=page_count,
                               pre=pre, next=next, user=user)
    except NoResultFound:
        abort(404)

@index.route('/channel', defaults={'page': 1, 's_channel': 0})
@index.route('/channel/<s_channel>/', defaults={'page': 1})
@index.route('/channel/<s_channel>/<page>')
def channel(s_channel, page):
    cookies = request.cookies
    if u'DBToken' in cookies:
        try:
            user = db.session.query(User).filter(User.SessionId == cookies[u'DBToken']).one()
        except NoResultFound:
            user = ''
    else:
        user = ''
    ItemInPage = 36
    page = int(page)
    s_channel = int(s_channel)
    category_1 = db.session.query(Category).filter(Category.Level == 1).all()
    category_2 = db.session.query(Category).filter(Category.Level == 2).all()
    channel_1 = 0
    channel_2 = 0
    pre = page-1
    next = page+1
    if s_channel == 0:
        count = ZoneItem.query.filter(classical == 2).count()
        if ZoneItem.query.count() % ItemInPage == 0:
            page_count = count/ItemInPage
        else:
            page_count = count/ItemInPage + 1
        zone_item = db.session.query(ZoneItem).join(Domain, Domain.Id == ZoneItem.DomainId).filter(Domain.IsService == 1)\
            .filter(ZoneItem.Type == 1).order_by(ZoneItem.Price*ZoneItem.Weight.desc())\
            .offset((page-1)*ItemInPage).limit(ItemInPage).all()
        return render_template('index/channel.html', zone_item=zone_item, page=page, page_count=page_count,
                               pre=pre, next=next, category_1=category_1, category_2=category_2, channel_1=channel_1,
                               channel_2=channel_2, s_channel=s_channel,user=user)
    else:
        category = db.session.query(Category).filter(Category.Id == s_channel).one()
        if category.Level == 1:
            channel_1 = s_channel
            count = db.session.query(ZoneItem).join(Object, Object.Id == ZoneItem.ObjectId).\
                    filter(Object.Category_1 == s_channel).count()
            zone_item = db.session.query(ZoneItem).join(Object, Object.Id == ZoneItem.ObjectId).\
                filter(Object.Category_1 == s_channel).join(Domain, Domain.Id == ZoneItem.DomainId).\
                filter(Domain.IsService == 1).filter(ZoneItem.Type == 1).\
                order_by(ZoneItem.Price * ZoneItem.Weight.desc()).offset((page-1)*ItemInPage).limit(ItemInPage).all()
        else:
            channel_1 = db.session.query(Category).filter(Category.Id == s_channel).one().ParentId
            channel_2 = s_channel
            count = db.session.query(ZoneItem).join(Object, Object.Id == ZoneItem.ObjectId).\
                    filter(Object.Category_2 == s_channel).count()
            zone_item = db.session.query(ZoneItem).join(Object, Object.Id == ZoneItem.ObjectId).\
                filter(Object.Category_2 == s_channel).join(Domain, Domain.Id == ZoneItem.DomainId).\
                filter(Domain.IsService == 1).filter(ZoneItem.Type == 1).\
                order_by(ZoneItem.Price * ZoneItem.Weight.desc()).offset((page-1)*ItemInPage).limit(ItemInPage).all()
        if count % ItemInPage == 0:
            page_count = count/ItemInPage
        else:
            page_count = count/ItemInPage + 1

        return render_template('index/channel.html', zone_item=zone_item, page=page, page_count=page_count,
                               pre=pre, next=next, category_1=category_1, category_2=category_2, channel_1=channel_1,
                               channel_2=channel_2, s_channel=s_channel, user=user)

@index.route('/company', defaults={'key': 'all', 'page': 1})
@index.route('/company/<key>', defaults={'page': 1})
@index.route('/company/<key>/<page>')
def company(key, page):
    cookies = request.cookies
    if u'DBToken' in cookies:
        try:
            user = db.session.query(User).filter(User.SessionId == cookies[u'DBToken']).one()
        except NoResultFound:
            user=''
    else:
        user = ''
    ItemInPage = 60
    page = int(page)
    pre = page-1
    next = page+1
    count = db.session.query(Domain).filter(Domain.IsService==1,Domain.ShowType!=0).count()
    if count % ItemInPage == 0:
            page_count = count/ItemInPage
    else:
        page_count = count/ItemInPage + 1
    try:
        if key == 'all':
            company = db.session.query(Domain).filter(Domain.IsService == 1,Domain.ShowType!=0).order_by(Domain.Price*Domain.Weight.desc())\
                .offset((page-1)*ItemInPage).limit(ItemInPage).all()
        else:
            if key == 'Trade':
                company = db.session.query(Domain).filter(Domain.IsService == 1,Domain.ShowType!=0).order_by(Domain.Trade.desc())\
                    .offset((page-1)*ItemInPage).limit(ItemInPage).all()
            if key == 'StarLevel':
                company = db.session.query(Domain).filter(Domain.IsService == 1,Domain.ShowType!=0).order_by(Domain.StarLevel.desc())\
                    .offset((page-1)*ItemInPage).limit(ItemInPage).all()
            if key == 'Focus':
                company = db.session.query(Domain).filter(Domain.IsService == 1,Domain.ShowType!=0).order_by(Domain.Focus.desc())\
                    .offset((page-1)*ItemInPage).limit(ItemInPage).all()
        return render_template('index/company.html', company=company, page=page, page_count=page_count,
                               pre=pre, next=next, key=key, count=count, user=user)
    except NoResultFound:
        abort(404)


@index.route('/users', defaults={'key': 'all', 'page': 1})
@index.route('/users/<key>', defaults={'page': 1})
@index.route('/users/<key>/<page>')
def users(key, page):
    ItemInPage = 60
    page = int(page)
    pre = page-1
    next = page+1
    count = db.session.query(Domain).filter(Domain.IsService==0,Domain.ShowType!=0).count()

    if count % ItemInPage == 0:
            page_count = count/ItemInPage
    else:
        page_count = count/ItemInPage + 1
    try:
        if key == 'all':
            domain = db.session.query(Domain).filter(Domain.IsService == 0,Domain.ShowType!=0).offset((page-1)*ItemInPage).limit(ItemInPage).all()
        return render_template('index/users.html', domain=domain, page=page, page_count=page_count,
                               pre=pre, next=next, key=key, count=count)
    except NoResultFound:
        abort(404)


@index.route('/player/<objectid>')
def player(objectid):
    try:
        object = db.session.query(Object).filter(Object.Id == objectid).one()
        domain = db.session.query(Domain).filter(Domain.OwnerUserId == object.OwnerUserId).one()
        zone_item = db.session.query(ZoneItem).filter(and_(ZoneItem.DomainId == domain.Id, ZoneItem.ObjectId == objectid)).first()
        if zone_item:
            zone_item.ViewCount += 1
            db.session.commit()
        more = db.session.query(ZoneItem)\
            .filter(and_(ZoneItem.Type == ZoneItemType.Video, ZoneItem.Id != zone_item.Id))\
            .join(Object, Object.Id == ZoneItem.ObjectId)\
            .filter(Object.Category_2 == object.Category_2)\
            .join(Domain, Domain.Id == ZoneItem.DomainId)\
            .filter(and_(Domain.IsService == 1, Domain.ShowType !=0))\
            .limit(9).all()
        if domain.Price != -1:
            if domain.Count <= 0:
                zone_item.Weight = 0
            else:
                domain.Count -= zone_item.Price
            db.session.commit()
        bCollectVideo = False
        bCollectProducer = False
        comments = []
        cookies = request.cookies
        if u'DBToken' in cookies:
            try:
                user = db.session.query(User).filter(User.SessionId == cookies[u'DBToken']).one()
                try:
                    CollectionVideo.query.filter_by(ZoneItemId=zone_item.Id, UserId=user.Id).one()
                    bCollectVideo = True
                except NoResultFound:
                    pass

                try:
                    CollectionProducer.query.filter_by(DomainId=zone_item.DomainId, UserId=user.Id).one()
                    bCollectProducer = True
                except NoResultFound:
                    pass

                try:
                    f = db.session.query(Favortie).filter(and_(Favortie.ZoneItemId == zone_item.Id,
                                                           Favortie.UserId == user.Id)).one()
                    favorite = True
                except NoResultFound:
                    favorite = ''
            except NoResultFound:
                user = ''
                favorite = ''
        else:
            user = ''
            favorite = ''
        comments = db.session.query(CommentVideo).filter(CommentVideo.ObjectId == objectid).order_by(CommentVideo.CreateTime.desc()).all()
        return render_template('index/player.html', object=object, user=user, domain=domain,
                               more=more, zone_item=zone_item, bCollectVideo=bCollectVideo,
                               bCollectProducer=bCollectProducer, comments=comments, favorite=favorite)
    except NoResultFound:
        abort(404)


@index.route('/zone/<domainid>')
def zone(domainid):
    try:
        domain = db.session.query(Domain).filter(Domain.Id == domainid).one()
        cookies = request.cookies
        if u'DBToken' in cookies:
            try:
                user = db.session.query(User).filter(User.SessionId == cookies[u'DBToken']).one()
            except NoResultFound:
                user = ''
        else:
            user = ''
        users = User.query.filter_by(DomainId=domain.Id).all()
        userId = []
        for u in users:
            userId.append(u.Id)
        if domain.IsService:
            reqs = db.session.query(Requirement).filter(Requirement.ServiceUserId.in_(userId))\
                .filter(Requirement.Status == RequirementStatus.RetainageNext).all()
        else:
            reqs = []
    except NoResultFound:
        abort(404)
    try:
        pic = db.session.query(ZoneItem).filter(and_(ZoneItem.DomainId == domain.Id, ZoneItem.Type == ZoneItemType.Picture)).all()
        video = db.session.query(ZoneItem).filter(and_(ZoneItem.DomainId == domain.Id, ZoneItem.Type == ZoneItemType.Video)).all()
        if domain.Price != -1:
            if domain.Count <= 0:
                domain.Weight = 0
            else:
                domain.Count -= domain.Price
            db.session.commit()
    except NoResultFound:
        pic = ''
        video = ''
    return render_template('index/zone.html', domain=domain, pic=pic, video=video, user=user, reqs=reqs)

@index.route('/collection/<int:uid>')
@incoming_params
def Collection(uid):
    cookies = request.cookies
    if u'DBToken' in cookies:
        try:
            user = db.session.query(User).filter(User.SessionId == cookies[u'DBToken']).one()
            if user.Id != uid:
                return redirect('/login#/loginPage')
        except NoResultFound:
            user = ''
            return redirect('/login#/loginPage')
    else:
        return redirect('/login#/loginPage')
    cp = CollectionProducer.query.filter_by(UserId=uid).all()
    cv = CollectionVideo.query.filter_by(UserId=uid).all()
    user = User.query.filter_by(Id=uid).one()
    return render_template('index/collection.html', params={'cp': cp, 'cv': cv}, user=user)


@index.route('/collection', methods=['POST'])
@output_data
def delCollection():
    incoming = request.json_param
    if incoming[u'type'] == 'video':
        CollectionVideo.query.filter_by(Id=incoming[u'targetId']).delete()
    else:
        cp = CollectionProducer.query.filter_by(Id=incoming[u'targetId']).one()
        domain = db.session.query(Domain).filter(Domain.Id == cp.DomainId).one()
        domain.Focus -= 1
        CollectionProducer.query.filter_by(Id=incoming[u'targetId']).delete()
    db.session.commit()
    return {}


@index.route('/collectVideo', methods=['POST'])
@output_data
def collection_video():
    incoming = request.json_param
    cookies = request.cookies
    if u'DBToken' in cookies:
        try:
            user = db.session.query(User).filter(User.SessionId == cookies[u'DBToken']).one()
            try:
                CollectionVideo.query.filter(and_(CollectionVideo.ZoneItemId == incoming[u'ZoneItemId'],
                                                  CollectionVideo.UserId == user.Id)).one()
            except NoResultFound:
                cv = CollectionVideo(incoming[u'ZoneItemId'], user.Id)
                db.session.add(cv)
                db.session.commit()
        except NoResultFound:
            user = ''
        return {'bSuccess': True}
    else:
        return {'bSuccess': False}




@index.route('/collectProducer', methods=['POST'])
@output_data
def collection_producer():
    incoming = request.json_param
    cookies = request.cookies
    if u'DBToken' in cookies:
        try:
            user = db.session.query(User).filter(User.SessionId == cookies[u'DBToken']).one()
        except NoResultFound:
            user = ''
            return {'bSuccess': False}
    else:
        return {'bSuccess': False}

    try:
        CollectionProducer.query.filter(and_(CollectionProducer.DomainId==incoming[u'DomainId'],
                                           CollectionProducer.UserId==user.Id)).one()
    except NoResultFound:
        cp = CollectionProducer(incoming[u'DomainId'], user.Id)
        domain = db.session.query(Domain).filter(Domain.Id == incoming[u'DomainId']).one()
        domain.Focus += 1
        db.session.add(cp)
        db.session.commit()
    return {'bSuccess': True}


@index.route('/favorVideo', methods=['POST'])
@output_data
@PermissionValidate()
def favor_video():
    incoming = request.json_param
    session = request.session
    try:
        zi = ZoneItem.query.filter_by(Id=incoming[u'ZoneItemId']).one()
    except NoResultFound:
        return {'bSuccess': False}
    try:
        f = db.session.query(Favortie).filter(and_(Favortie.ZoneItemId == incoming[u'ZoneItemId'],
                                                   Favortie.UserId == session['UserId'])).one()
        return {'bSuccess': True, 'count': zi.Favorite}
    except NoResultFound:
        f = Favortie(incoming[u'ZoneItemId'], session['UserId'])
        db.session.add(f)
    zi.Favorite += 1
    db.session.commit()
    return {'bSuccess': True, 'count': zi.Favorite}


@index.route('/addVideoComment', methods=['POST'])
@output_data
def addVideoComment():
    incoming = request.json_param
    cookies = request.cookies
    if u'DBToken' in cookies:
        user = db.session.query(User).filter(User.SessionId == cookies[u'DBToken']).one()
    else:
        return {'bSuccess': False}

    cv = CommentVideo(incoming[u'ObjectId'], user.Id, incoming[u'Content'])
    db.session.add(cv)
    db.session.commit()
    comments = db.session.query(CommentVideo).filter(CommentVideo.ObjectId == incoming[u'ObjectId']).order_by(CommentVideo.CreateTime.desc()).all()
    template = render_template("index/player_comment.html", comments=comments)
    return template


@index.route('/search', methods=['GET', 'POST'])
@incoming_params
def search():
    param = request.json_param
    if u'req' in param:
        if param[u'search'] == '':
            domain = db.session.query(Domain).filter(and_(Domain.IsService == 1,Domain.ShowType !=0)).limit(9).all()
            page = render_template('index/search_producer.html', domain=domain, search=param[u'search'],
                                   sh=param[u'sh'])
            from Main import api
            resp = api.make_response(page, 200)
            return resp
        else:
            searchPhase = "%" + param[u'search'] + "%"
            domain = Domain.query.filter(and_(Domain.CompanyName.like(searchPhase), Domain.IsService == 1))\
                .filter(Domain.ShowType !=0).all()
            page = render_template('index/search_producer.html', domain=domain, search=param[u'search'], sh=param[u'sh'])
            from Main import api
            resp = api.make_response(page, 200)
            return resp
    cookies = request.cookies
    if u'DBToken' in cookies:
        try:
            user = db.session.query(User).filter(User.SessionId == cookies[u'DBToken']).one()
        except NoResultFound:
            user=''
    else:
        user = ''

    domain = None
    searchPhase = "%" + param[u'search'] + "%"
    #因为业务方向问题，去掉综合搜索制作商
    #domain = Domain.query.filter(and_(Domain.CompanyName.like(searchPhase), Domain.IsService == 1))\
    #    .filter(Domain.ShowType !=0).all()
    #if param[u'search'] == '':
    #    return render_template('index/search.html', domain=domain, video=[], user=user, search=param[u'search'])

    if param[u'search'] == '':
        video = db.session.query(ZoneItem)\
            .join(Domain, Domain.Id == ZoneItem.DomainId)\
            .join(Object, Object.Id == ZoneItem.ObjectId)\
            .filter(Domain.IsService == 1)\
            .filter(ZoneItem.Type == ZoneItemType.Video)\
            .order_by(Object.ModifyTime.desc()).limit(9)\
            .all()
    else:
        video = db.session.query(ZoneItem)\
            .join(Domain, Domain.Id == ZoneItem.DomainId)\
            .join(Object, Object.Id == ZoneItem.ObjectId)\
            .filter(Domain.IsService == 1)\
            .filter(ZoneItem.Type == ZoneItemType.Video)\
            .filter(or_(Object.Name.like(searchPhase), Object.Tag.like(searchPhase), Object.Description.like(searchPhase)))\
            .all()

    return render_template('index/search.html', domain=domain, video=video, user=user, search=param[u'search'])

@index.route('/initserver', methods=['GET', 'POST'])
@incoming_params
def initserver():
    param = request.json_param
    domain = db.session.query(Domain).filter(Domain.Id.in_(param[u'sh'])).all()
    from Main import api
    resp = api.make_response(domain, 200)
    return resp


@index.route('/sitemap')
def sitemap():
    try:
        cookies = request.cookies
        if u'DBToken' in cookies:
            try:
                user = db.session.query(User).filter(User.SessionId == cookies[u'DBToken']).one()
            except NoResultFound:
                user = ''
        else:
            user = ''
        return render_template('index/sitemap.html', user=user)
    except TemplateNotFound:
        abort(404)

@index.route('/getCategory', methods=['GET', 'POST'])
@incoming_params
def getCategory():
    param = request.json_param
    c2 = db.session.query(Category).filter(Category.ParentId == param[u'id']).all()
    from Main import api
    resp = api.make_response(c2, 200)
    return resp

@index.route('/submit', methods=['GET', 'POST'])
@incoming_params
def submit():
    param = request.json_param
    try:
        cookies = request.cookies
        category_1 = db.session.query(Category).filter(Category.Level==1).all()
        category_2 = db.session.query(Category).filter(Category.Level==2).all()
        if u'DBToken' in cookies:
            try:
                user = db.session.query(User).filter(User.SessionId == cookies[u'DBToken']).one()
            except NoResultFound:
                user = ''
        else:
            user = ''
        if u'producerDomain' in cookies:
            producerDomain = db.session.query(Domain).filter(Domain.Id==cookies[u'producerDomain']).one()
        else:
            producerDomain = ''
        if u'requirename' in param:
            requirename = param[u'requirename']
        else:
            requirename = ''
        return render_template('index/submit.html', user=user, cookies=cookies, category_1=category_1,
                               category_2=category_2, producerDomain=producerDomain,requirename=requirename)
    except TemplateNotFound:
        abort(404)

@index.route('/publishRequirement', methods=['GET', 'POST'])
@incoming_params
@PermissionValidate()
@output_data
def publishRequirement():
    param = request.json_param
    session = request.session
    requirement = Requirement()
    if param[u'Status'] == 0:
        requirement.Status = 1
    else:
        requirement.Status = 2
    db.session.add(requirement)
    requirement.PublisherId = session['UserId']
    requirement.Title = param[u'Title']
    if u'Long' in param: #2016-11-04
        requirement.Long = param[u'Long']
    requirement.Amount = float(param[u'Amount'])
    requirement.Detail = param[u'Detail']
    requirement.Deadline = param[u'Deadline']
    if u'refer' in param:
        requirement.Refer = param[u'refer']
        requirement.ReferName = param[u'referName']
    # requirement.Category_1 = param[u'category_1']
    # requirement.Category_2 = param[u'category_2']
    db.session.flush()

    rs = RequirementSegment(requirement.Id, RequirementStatus.Published)
    db.session.add(rs)
    rs = RequirementSegment(requirement.Id, RequirementStatus.Contracting)
    db.session.add(rs)
    rs = RequirementSegment(requirement.Id, RequirementStatus.PayDeposit)
    db.session.add(rs)
    rs = RequirementSegment(requirement.Id, RequirementStatus.Reviewing)
    db.session.add(rs)
    rs = RequirementSegment(requirement.Id, RequirementStatus.PayAll)
    db.session.add(rs)
    rs = RequirementSegment(requirement.Id, RequirementStatus.Retainage)
    db.session.add(rs)

    specifyDomains = param[u'specifyProducers']
    if len(specifyDomains) > 0:
        for d in specifyDomains:
            try:
                ResourceShare.query.filter_by(ResourceId=requirement.Id, ResourceType='r', ShareDomainId=d).one()
            except NoResultFound:
                r = ResourceShare(requirement.Id, 'r', d)
                db.session.add(r)
    else:
        try:
            ResourceShare.query.filter_by(ResourceId=requirement.Id, ResourceType='r', ShareDomainId=0).one()
        except NoResultFound:
            r = ResourceShare(requirement.Id, 'r', 0)
            db.session.add(r)
    db.session.commit()
    return


#用于微信验证 on 2016-12-21
@index.route('/MP_verify_a19iolCUesS40hLm.txt')
def wx_js_safe_verify():
    return render_template('index/MP_verify_a19iolCUesS40hLm.txt')