
/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2021/6/16 13:33:16                           */
/*==============================================================*/

drop table if exists 联系人;

drop table if exists 发款;

drop table if exists 客户_贷款;

drop table if exists 贷款;

drop table if exists 员工服务类型;

drop table if exists 储蓄账户访问时间;

drop table if exists 储蓄账户;

drop table if exists 支票账户访问时间;

drop table if exists 支票账户;

drop table if exists 客户;

drop table if exists 普通员工;

drop table if exists 部门经理;

drop table if exists 部门;

drop table if exists 员工;

drop table if exists 支行;

/*==============================================================*/
/* Table: 储蓄账户                                                  */
/*==============================================================*/
create table 储蓄账户
(
   账户号                  char(50) not null,
   利率                   float,
   货币类型                 char(20),
   账户余额                 double,
   开户日期                 date,
   primary key (账户号)
);

/*==============================================================*/
/* Table: 储蓄账户访问时间                                              */
/*==============================================================*/
create table 储蓄账户访问时间
(
   支行名                  char(50) not null,
   客户身份证号               char(18) not null,
   账户号                  char(50) not null,
   最近访问日期               date,
   primary key (支行名, 客户身份证号)
);

/*==============================================================*/
/* Table: 发款                                                    */
/*==============================================================*/
create table 发款
(
   贷款号                  char(30) not null,
   发款系列号              int(4) NOT NULL AUTO_INCREMENT,		#对外隐藏，内部区分
   发款日期                date,
   发款金额                double,
   未发款数				   double,
   primary key (发款系列号,贷款号)
);

/*==============================================================*/
/* Table: 员工                                                    */
/*==============================================================*/
create table 员工
(
   员工身份证号             char(18) not null,
   姓名                     char(30),
   电话号码                 char(20),
   开始工作日期             date,
   primary key (员工身份证号)
);

/*==============================================================*/
/* Table: 员工服务类型                                                */
/*==============================================================*/
create table 员工服务类型
(
   员工身份证号               char(18) not null,
   客户身份证号               char(18) not null,
   类型                       char(20),
   primary key (员工身份证号, 客户身份证号)
);

/*==============================================================*/
/* Table: 客户                                                    */
/*==============================================================*/
create table 客户
(
   客户身份证号             char(18) not null,
   姓名                     char(30),
   联系电话                 char(20),
   家庭住址                 char(50),
   primary key (客户身份证号)
);

/*==============================================================*/
/* Table: "客户_贷款"                                               */
/*==============================================================*/
create table 客户_贷款
(
   客户身份证号            char(18) not null,
   贷款号                  char(30) not null,
   primary key (客户身份证号, 贷款号)
);

/*==============================================================*/
/* Table: 支票账户                                                  */
/*==============================================================*/
create table 支票账户
(
   账户号                  char(50) not null,
   透支额                  double,
   账户余额                 double,
   开户日期                 date,
   primary key (账户号)
);

/*==============================================================*/
/* Table: 支票账户访问时间                                              */
/*==============================================================*/
create table 支票账户访问时间
(
   支行名                  char(50) not null,
   客户身份证号               char(18) not null,
   账户号                  char(50) not null,
   最近访问日期               date,
   primary key (支行名, 客户身份证号)
);

/*==============================================================*/
/* Table: 支行                                                    */
/*==============================================================*/
create table 支行
(
   支行名                  char(50) not null,
   所在城市                 char(30),
   资产                   double,
   primary key (支行名)
);

/*==============================================================*/
/* Table: 普通员工                                                  */
/*==============================================================*/
create table 普通员工
(
   员工身份证号               char(18) not null,
   部门号                  char(50) not null,
   姓名                   char(30),
   电话号码                 char(20),
   开始工作日期               date,
   primary key (员工身份证号)
);

/*==============================================================*/
/* Table: 联系人                                                   */
/*==============================================================*/
create table 联系人
(
   客户身份证号               char(18) not null,
   姓名                   char(30),
   手机号                  char(20),
   邮箱地址                 char(50),
   与客户关系                char(15),
   primary key (客户身份证号)
);

/*==============================================================*/
/* Table: 贷款                                                    */
/*==============================================================*/
create table 贷款
(
   贷款号                  char(30) not null,
   支行名                  char(50) not null,
   贷款总金额              double,
   未发款数				   double,
   贷款状态				   char(10) default "未发放",
   最近发款日期			   date default '1000-01-01',
   primary key (贷款号)
);

/*==============================================================*/
/* Table: 部门                                                    */
/*==============================================================*/
create table 部门
(
   部门号                  char(50) not null,
   支行名                  char(50) not null,
   部门名称                 char(50),
   部门类型                 char(20),
   primary key (部门号)
);

/*==============================================================*/
/* Table: 部门经理                                                  */
/*==============================================================*/
create table 部门经理
(
   员工身份证号               char(18) not null,
   部门号                  char(50) not null,
   姓名                   char(30),
   电话号码                 char(20),
   开始工作日期               date,
   primary key (员工身份证号)
);

alter table 储蓄账户访问时间 add constraint FK_储蓄账户信息 foreign key (账户号)
      references 储蓄账户 (账户号) on delete restrict on update CASCADE;

alter table 储蓄账户访问时间 add constraint FK_客户_储蓄账户 foreign key (客户身份证号)
      references 客户 (客户身份证号) on delete restrict on update CASCADE;

alter table 储蓄账户访问时间 add constraint FK_支行_储蓄账户 foreign key (支行名)
      references 支行 (支行名) on delete restrict on update CASCADE;

alter table 发款 add constraint FK_逐次放款 foreign key (贷款号)
      references 贷款 (贷款号) on delete restrict on update CASCADE;

alter table 员工服务类型 add constraint FK_员工服务类型 foreign key (员工身份证号)
      references 员工 (员工身份证号) on delete restrict on update restrict;

alter table 员工服务类型 add constraint FK_员工服务类型2 foreign key (客户身份证号)
      references 客户 (客户身份证号) on delete restrict on update CASCADE;

alter table 客户_贷款 add constraint FK_客户_贷款 foreign key (客户身份证号)
      references 客户 (客户身份证号) on delete restrict on update CASCADE;

alter table 客户_贷款 add constraint FK_客户_贷款2 foreign key (贷款号)
      references 贷款 (贷款号) on delete restrict on update CASCADE;

alter table 支票账户访问时间 add constraint FK_客户_支票账户 foreign key (客户身份证号)
      references 客户 (客户身份证号) on delete restrict on update CASCADE;

alter table 支票账户访问时间 add constraint FK_支票账户信息 foreign key (账户号)
      references 支票账户 (账户号) on delete restrict on update CASCADE;

alter table 支票账户访问时间 add constraint FK_支行_支票账户 foreign key (支行名)
      references 支行 (支行名) on delete restrict on update CASCADE;

alter table 普通员工 add constraint FK_员工类型继承 foreign key (员工身份证号)
      references 员工 (员工身份证号) on delete restrict on update CASCADE;

alter table 普通员工 add constraint FK_部门_员工 foreign key (部门号)
      references 部门 (部门号) on delete restrict on update restrict;

alter table 联系人 add constraint FK_客户_联系人2 foreign key (客户身份证号)
      references 客户 (客户身份证号) on delete restrict on update CASCADE;

alter table 贷款 add constraint FK_支行_贷款 foreign key (支行名)
      references 支行 (支行名) on delete restrict on update CASCADE;

alter table 部门 add constraint FK_支行_部门 foreign key (支行名)
      references 支行 (支行名) on delete restrict on update restrict;

alter table 部门经理 add constraint FK_员工类型继承2 foreign key (员工身份证号)
      references 员工 (员工身份证号) on delete restrict on update restrict;

alter table 部门经理 add constraint FK_部门_经理2 foreign key (部门号)
      references 部门 (部门号) on delete restrict on update restrict;


Drop Trigger if exists 发款触发器;

Drop table if exists t;
create table t(id int primary key,col int);

Delimiter //
/*发款触发器*/
Create Trigger 发款触发器 before INSERT ON 发款 FOR EACH ROW
begin
	select 未发款数 from 贷款 where 贷款.贷款号 = new.贷款号 into @a;
    select 最近发款日期 from 贷款 where 贷款.贷款号 = new.贷款号 into @DKdata;
    select DATEDIFF(@DKdata,new.发款日期) into @DiffDate;
    if @DiffDate > 0 then
		insert into t values('das');    #ERROR CODE: 1136
	else
		if @a < new.发款金额 then
			SELECT E001 INTO @M_ERRMSG;		#抛出异常 1054
		else
			#更新未发放款
			update 贷款
			set 贷款.未发款数 = 贷款.未发款数 - new.发款金额
			where 贷款.贷款号 = new.贷款号;
            #更新最近发款日期
            update 贷款
			set 贷款.最近发款日期 = new.发款日期
			where 贷款.贷款号 = new.贷款号;
        
			select 未发款数 from 贷款 where 贷款.贷款号 = new.贷款号 into @b;
			set new.未发款数 = @b;
            
			if @b = 0 then
				update 贷款
				set 贷款.贷款状态 = "完结"
				where 贷款.贷款号 = new.贷款号;
			else
				update 贷款
				set 贷款.贷款状态 = "发放中"
				where 贷款.贷款号 = new.贷款号;
			end if;
        end if;
    end if;
end //
/*删除贷款信息存储过程*/
Drop procedure if exists delete_LoanInfo;
create procedure delete_LoanInfo (IN DKID char(30), OUT state INT)
begin
	Declare s INT default 0;
    Declare Loan_ID CHAR(30);
    declare Loan_states CHAR(10);
    
    Declare cursordel Cursor For Select 贷款状态 From 贷款 where 贷款.贷款号 = DKID;
    Declare continue Handler for NOT FOUND set s = 1;/*记录游标中的读取情况*/

	start transaction;
    
	select 贷款状态 from 贷款 where 贷款.贷款号 = DKID into Loan_states;
    if Loan_states = "发放中" then 
		set s = 2; 
	end if;

    delete from 客户_贷款 where 客户_贷款.贷款号 = DKID;
	delete from 发款 where 发款.贷款号 = DKID;
    delete from 贷款 where 贷款.贷款号 = DKID;
    
    set state = s;
    if s != 0 then
		rollback;
	end if;
end//

#增加账户所有者存储过程
/*Drop procedure if exists add_CXZH_owner;
create procedure add_CXZH_owner (IN ZHID char(50), IN NEWownerID char(30), OUT states INT)
begin
	Declare s1 INT default 0;
    Declare ZH_ID CHAR(50);
    Declare Bank_new char(50);
    Declare date_new date;
    
    start transaction;
    
    Declare cursor_CX Cursor For Select 账户号 From 储蓄账户访问时间 where 储蓄账户访问时间.账户号 = ZHID;
    Declare continue Handler for NOT FOUND set s = 1;#记录游标中的读取情况

	
    select distinct 支行名 from 储蓄账户访问时间 where 账户号 = ZHID into Bank_new;
    select date_format(now(),'%Y-%m-%d') into date_new;
    
    insert into 储蓄账户访问时间 Value (Bank_new,NEWownerID,ZHID,date_new)
    
    set states = s1;
    if s1 != 0 then
		rollback;
	end if;
end//*/

Delimiter ;




