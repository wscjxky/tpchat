/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2014/8/23 11:22:02                           */
/*==============================================================*/


drop table if exists `domain`;

drop table if exists `file`;

drop table if exists `group`;

drop table if exists `groupuser`;

drop table if exists `object`;

drop table if exists `role`;

drop table if exists `share`;

drop table if exists `shareuser`;

drop table if exists `shareusercache`;

drop table if exists `user`;

drop table if exists `userrole`;

/*==============================================================*/
/* Table: `domain`                                              */
/*==============================================================*/
create table `domain`
(
   Id                   bigint not null auto_increment,
   DomainName           varchar(255) not null,
   OwnerUserId          bigint not null,
   ExpireTime           datetime not null,
   CreateTime           timestamp,
   primary key (Id)
);

/*==============================================================*/
/* Table: `file`                                                */
/*==============================================================*/
create table `file`
(
   Id                   bigint not null auto_increment,
   Size                 bigint not null,
   MD5                  binary(16) not null,
   RefCount             bigint,
   Path                 national varchar(4096) not null,
   Ext                  national varchar(100) not null,
   Status               int comment '0--正在上传
                        1--已上传',
   CreateTime           timestamp not null default CURRENT_TIMESTAMP,
   primary key (Id)
);

/*==============================================================*/
/* Table: `group`                                               */
/*==============================================================*/
create table `group`
(
   Id                   bigint not null auto_increment,
   ShareObjectId        bigint,
   GroupName            varchar(50),
   GroupRead            bit(1),
   GroupWrite           bit(1),
   GroupCreate          bit(1),
   GroupDelete          bit(1),
   CreateTime           timestamp,
   primary key (Id)
);

/*==============================================================*/
/* Table: `groupuser`                                           */
/*==============================================================*/
create table `groupuser`
(
   Id                   bigint not null auto_increment,
   GroupId              bigint,
   UserId               bigint,
   CreateTime           timestamp,
   primary key (Id)
);

/*==============================================================*/
/* Table: `object`                                              */
/*==============================================================*/
create table `object`
(
   Id                   bigint(20) not null auto_increment,
   OwnerUserId          bigint,
   CreatorUserId        bigint,
   _Left_               bigint(20),
   _Right_              bigint(20),
   Name                 national varchar(255) not null,
   FileId               bigint,
   ParentId             bigint,
   Type                 int,
   Size                 bigint,
   Extend               varchar(255),
   Status               int,
   Remark               varchar(255),
   ModifyTime           timestamp not null default CURRENT_TIMESTAMP,
   CreateTime           timestamp,
   primary key (Id)
);

/*==============================================================*/
/* Table: `role`                                                */
/*==============================================================*/
create table `role`
(
   Id                   bigint not null auto_increment,
   CreatorId            bigint not null,
   DomainId             bigint not null,
   Name                 varchar(255) not null,
   DomainAdmin          bit(1) not null default 0,
   DomainWrite          bit(1) not null,
   DomainCreate         bit(1) not null,
   DomainShare          bit(1),
   DomainDelete         bit(1) not null,
   CreateTime           timestamp,
   primary key (Id)
);

/*==============================================================*/
/* Table: `share`                                               */
/*==============================================================*/
create table `share`
(
   Id                   bigint not null auto_increment,
   ObjectId             bigint,
   CreatorUserId        bigint,
   Name                 national varchar(255) not null,
   CreateTime           timestamp,
   primary key (Id)
);

/*==============================================================*/
/* Table: `shareuser`                                           */
/*==============================================================*/
create table `shareuser`
(
   Id                   bigint not null auto_increment,
   ShareObjectId        bigint,
   UserId               bigint,
   UserRead             bit(1),
   UserWrite            bit(1),
   UserCreate           bit(1),
   UserDelete           bit(1),
   CreateTime           timestamp,
   primary key (Id)
);

/*==============================================================*/
/* Table: `shareusercache`                                      */
/*==============================================================*/
create table `shareusercache`
(
   Id                   bigint not null auto_increment,
   ShareObjectId        bigint,
   UserId               bigint,
   UserRead             bit(1),
   UserWrite            bit(1),
   UserCreate           bit(1),
   UserDelete           bit(1),
   CreateTime           timestamp,
   primary key (Id)
);

alter table `shareusercache` comment '用于保存 组和共享用户的计算结果';

/*==============================================================*/
/* Table: `user`                                                */
/*==============================================================*/
create table `user`
(
   Id                   bigint(20) not null auto_increment,
   NipUserId            bigint,
   DomainId             bigint,
   DomainName           varchar(100),
   Password             char(32),
   SessionId            varchar(50),
   Email                national varchar(100),
   NickName             national varchar(100),
   StorageSize          bigint(20),
   UsedSize             bigint(20) not null,
   CreateTime           timestamp not null default CURRENT_TIMESTAMP,
   DomainPermissionInvalidate bit(1) not null,
   primary key (Id)
);

/*==============================================================*/
/* Table: `userrole`                                            */
/*==============================================================*/
create table `userrole`
(
   Id                   bigint not null auto_increment,
   UserId               bigint,
   RoleId               bigint,
   CreateTime           timestamp,
   primary key (Id)
);

