# 插入支行
insert into 支行 value('Bank1', 'NewYork', 100000000);
insert into 支行 value('Bank2', 'ShangHai', 200000000);
insert into 支行 value('Bank3', 'Tokyo', 300000000);
insert into 支行 value('Bank4', 'Paris', 400000000);
insert into 支行 value('Bank5', 'BeiJing', 500000000);

#select * from 支行;

# 插入客户
insert into 客户 value('C1', '测试客户1', '13811111111', 'BeiJing');
insert into 客户 value('C2', '测试客户2', '13822222222', 'NewYork');
insert into 客户 value('C3', '测试客户3', '13833333333', 'Paris');
insert into 客户 value('C4', '测试客户4', '13844444444', 'Sydney');
insert into 客户 value('C5', '测试客户5', '13855555555', 'Tokyo');
insert into 客户 value('C6', '测试客户6', '13866666666', 'Berlin');
insert into 客户 value('C7', '测试客户7', '13877777777', 'Moscow');

#插入联系人
insert into 联系人 value('C1', '联系人1','11111111','1@163.com','父');
insert into 联系人 value('C2', '联系人2','22222222','2@163.com','父');
insert into 联系人 value('C3', '联系人3','33333333','3@163.com','父');
insert into 联系人 value('C4', '联系人4','44444444','4@163.com','父');
insert into 联系人 value('C5', '联系人5','55555555','5@163.com','父');
insert into 联系人 value('C6', '联系人6','66666666','6@163.com','父');
insert into 联系人 value('C7', '联系人7','77777777','7@163.com','父');

#select distinct * from 客户,联系人 where 客户.客户身份证号=联系人.客户身份证号;
#select distinct * from 客户 left join 联系人 USING(客户身份证号);
#select distinct * from 客户 where 客户.客户身份证号 = 'C1';


# 插入储蓄账户
insert into 储蓄账户 value('CX01', 0.01 , 'RMB', '1000','2020-01-01');
insert into 储蓄账户 value('CX02', 0.02 , 'USD', '1000','2020-01-01');
insert into 储蓄账户 value('CX03', 0.03 , 'EUR', '1000','2020-01-01');
insert into 储蓄账户 value('CX04', 0.04 , 'GBP', '1000','2020-01-01');
insert into 储蓄账户 value('CX05', 0.05 , 'CHF', '1000','2020-01-01');
insert into 储蓄账户 value('CX06', 0.06 , 'JPY', '1000','2020-01-01');
insert into 储蓄账户 value('CX07', 0.07 , 'CAD', '1000','2020-01-01');
insert into 储蓄账户 value('CX08', 0.08 , 'RMB', '1000','2020-01-01');

#select * from 储蓄账户;

#插入储蓄账户访问时间
insert into 储蓄账户访问时间 value('Bank1', 'C1' , 'CX01','2020-01-02');
insert into 储蓄账户访问时间 value('Bank2', 'C2' , 'CX02','2020-01-03');
insert into 储蓄账户访问时间 value('Bank3', 'C3' , 'CX03','2020-01-05');
insert into 储蓄账户访问时间 value('Bank4', 'C4' , 'CX04','2020-01-02');
insert into 储蓄账户访问时间 value('Bank5', 'C5' , 'CX05','2020-01-03');
insert into 储蓄账户访问时间 value('Bank1', 'C6' , 'CX06','2020-01-05');
insert into 储蓄账户访问时间 value('Bank2', 'C1' , 'CX07','2020-01-02');
insert into 储蓄账户访问时间 value('Bank3', 'C2' , 'CX08','2020-01-03');
insert into 储蓄账户访问时间 value('Bank1', 'C2' , 'CX01','2020-01-05');#C1,C2在bank1共有账户cx1


#select * from 储蓄账户访问时间;


#select distinct * from 储蓄账户 left join 储蓄账户访问时间 USING(账户号);


# 插入支票账户
insert into 支票账户 value('ZP01', 1000 , 100,'2020-02-01');
insert into 支票账户 value('ZP02', 2000 , 200,'2020-02-02');
insert into 支票账户 value('ZP03', 3000 , 300,'2020-02-03');
insert into 支票账户 value('ZP04', 4000 , 400,'2020-02-04');
insert into 支票账户 value('ZP05', 5000 , 500,'2020-02-05');
insert into 支票账户 value('ZP06', 6000 , 600,'2020-02-06');

#select * from 支票账户;

#插入支票账户访问时间
insert into 支票账户访问时间 value('Bank1', 'C1' , 'ZP01','2020-02-02');
insert into 支票账户访问时间 value('Bank2', 'C2' , 'ZP02','2020-02-02');
insert into 支票账户访问时间 value('Bank3', 'C3' , 'ZP03','2020-02-02');
insert into 支票账户访问时间 value('Bank4', 'C4' , 'ZP04','2020-02-02');
insert into 支票账户访问时间 value('Bank5', 'C3' , 'ZP05','2020-02-03');
insert into 支票账户访问时间 value('Bank1', 'C4' , 'ZP06','2020-02-04');

#select * from 支票账户访问时间;
#select distinct * from 支票账户 left join 支票账户访问时间 USING(账户号);

select 客户.客户身份证号, SUM(储蓄账户.账户余额)+SUM(支票账户.账户余额) as balance
from 客户,储蓄账户,储蓄账户访问时间,支票账户,支票账户访问时间
where 客户.客户身份证号 = 储蓄账户访问时间.客户身份证号 and 
	  客户.客户身份证号 = 支票账户访问时间.客户身份证号 and 
      储蓄账户.账户号 = 储蓄账户访问时间.账户号 and
      支票账户.账户号 = 支票账户访问时间.账户号 
group by 客户.客户身份证号;



#插入贷款信息
insert into 贷款 value('DK01', 'Bank1' , '10000','10000','未发款','1000-01-01');
insert into 贷款 value('DK02', 'Bank1' , '17000','17000','未发款','1000-01-01');
insert into 贷款 value('DK03', 'Bank1' , '18000','18000','未发款','1000-01-01');
insert into 贷款 value('DK04', 'Bank2' , '20000','10000','未发款','1000-01-01');
insert into 贷款 value('DK05', 'Bank2' , '20000','20000','未发款','1000-01-01');
insert into 贷款 value('DK06', 'Bank3' , '30000','30000','未发款','1000-01-01');
insert into 贷款 value('DK07', 'Bank4' , '40000','40000','未发款','1000-01-01');
insert into 贷款 value('DK08', 'Bank5' , '50000','50000','未发款','1000-01-01');

select * from 贷款;

#插入客户_贷款信息
insert into 客户_贷款 value('C1', 'DK01');
insert into 客户_贷款 value('C1', 'DK02');
insert into 客户_贷款 value('C1', 'DK03');
insert into 客户_贷款 value('C2', 'DK04');
insert into 客户_贷款 value('C2', 'DK05');
insert into 客户_贷款 value('C3', 'DK06');
insert into 客户_贷款 value('C4', 'DK07');
insert into 客户_贷款 value('C5', 'DK08');

#select * from 客户_贷款;

#插入发款信息
insert into 发款 (贷款号,发款日期,发款金额)value('DK01', '2020-05-05' , '1000');
insert into 发款 (贷款号,发款日期,发款金额)value('DK01', '2020-05-06' , '2000');
insert into 发款 (贷款号,发款日期,发款金额)value('DK01', '2020-05-07' , '3000');
insert into 发款 (贷款号,发款日期,发款金额)value('DK01', '2020-05-08' , '4000');
#insert into 发款 (贷款号,发款日期,发款金额)value('DK01', '2020-05-09' , '4000');
insert into 发款 (贷款号,发款日期,发款金额)value('DK02', '2020-01-01' , '1234');
#insert into 发款 (贷款号,发款日期,发款金额)value('DK02', '2019-01-01' , '1234');

select * from 发款;

select 贷款号,支行名,贷款总金额,客户身份证号,发款日期,发款金额,发款.未发款数,贷款状态 from (贷款 left join 客户_贷款 USING(贷款号))left join 发款 USING(贷款号);

call delete_LoanInfo('DK02',@TEST);
SELECT @TEST;
#按月统计发款
select 支行名,DATE_FORMAT(发款日期,'%Y-%m') 月份,count(发款日期) 发款次数 ,SUM(发款金额) 发款总额
from (select 支行名,贷款号,发款日期,发款金额 from (支行 left join 贷款 Using(支行名)) left join 发款 Using(贷款号)) C1
group by 支行名,月份;
#按季度统计发款
select 支行名, DATE_FORMAT(发款日期,'%Y')年度, QUARTER(发款日期)季度, count(发款日期) 发款次数 ,SUM(发款金额) 发款总额
from (select 支行名,贷款号,发款日期,发款金额 from (支行 left join 贷款 Using(支行名)) left join 发款 Using(贷款号)) C1
group by 支行名,年度,季度;
#按年统计发款
select 支行名,DATE_FORMAT(发款日期,'%Y')年度,count(发款日期) 发款次数 ,SUM(发款金额) 发款总额
from (select 支行名,贷款号,发款日期,发款金额 from (支行 left join 贷款 Using(支行名)) left join 发款 Using(贷款号)) C1
group by 支行名,年度;


#按月统计银行储蓄总额以及客户人数
select S1.支行名, S1.月份, 新增客户人数, 存储总额
from
   (select 支行名, DATE_FORMAT(开户日期,'%Y-%m') 月份, SUM(账户余额) 存储总额
	from ((select distinct 支行名,账户号,账户余额,开户日期
			from 支行 left join ((储蓄账户 left join 储蓄账户访问时间 Using(账户号))) Using(支行名))
			Union
			(select distinct 支行名,账户号,账户余额,开户日期
			from 支行 left join ((支票账户 left join 支票账户访问时间 Using(账户号))) Using(支行名))) C1
	group by 支行名,月份) S1,
   (
	select 支行名,DATE_FORMAT(开户日期,'%Y-%m') 月份, count(distinct 客户身份证号) 新增客户人数 
	from ((select 支行名,账户号,账户余额,开户日期,客户身份证号
			from 支行 left join ((储蓄账户 left join 储蓄账户访问时间 Using(账户号))) Using(支行名))
			Union
			(select 支行名,账户号,账户余额,开户日期,客户身份证号
			from 支行 left join ((支票账户 left join 支票账户访问时间 Using(账户号))) Using(支行名))) C1
	group by 支行名,月份) S2
where S1.支行名 = S2.支行名 and S1.月份 = S2.月份;


#按季度统计银行储蓄总额以及客户人数
select S1.支行名, S1.年度, S1.季度, 新增客户人数, 存储总额
from
   (select 支行名, DATE_FORMAT(开户日期,'%Y') 年度, QUARTER(开户日期)季度, SUM(账户余额) 存储总额
	from ((select distinct 支行名,账户号,账户余额,开户日期
			from 支行 left join ((储蓄账户 left join 储蓄账户访问时间 Using(账户号))) Using(支行名))
			Union
			(select distinct 支行名,账户号,账户余额,开户日期
			from 支行 left join ((支票账户 left join 支票账户访问时间 Using(账户号))) Using(支行名))) C1
	group by 支行名,年度,季度) S1,
   (
	select 支行名,DATE_FORMAT(开户日期,'%Y') 年度, QUARTER(开户日期)季度, count(distinct 客户身份证号) 新增客户人数 
	from ((select 支行名,账户号,账户余额,开户日期,客户身份证号
			from 支行 left join ((储蓄账户 left join 储蓄账户访问时间 Using(账户号))) Using(支行名))
			Union
			(select 支行名,账户号,账户余额,开户日期,客户身份证号
			from 支行 left join ((支票账户 left join 支票账户访问时间 Using(账户号))) Using(支行名))) C1
	group by 支行名,年度,季度) S2
where S1.支行名 = S2.支行名 and S1.年度 = S2.年度 and S1.季度 = S2.季度;


#按月统计银行储蓄总额以及客户人数
select S1.支行名, S1.年度, 新增客户人数, 存储总额
from
   (select 支行名, DATE_FORMAT(开户日期,'%Y') 年度, SUM(账户余额) 存储总额
	from ((select distinct 支行名,账户号,账户余额,开户日期
			from 支行 left join ((储蓄账户 left join 储蓄账户访问时间 Using(账户号))) Using(支行名))
			Union
			(select distinct 支行名,账户号,账户余额,开户日期
			from 支行 left join ((支票账户 left join 支票账户访问时间 Using(账户号))) Using(支行名))) C1
	group by 支行名,年度) S1,
   (
	select 支行名,DATE_FORMAT(开户日期,'%Y') 年度, count(distinct 客户身份证号) 新增客户人数 
	from ((select 支行名,账户号,账户余额,开户日期,客户身份证号
			from 支行 left join ((储蓄账户 left join 储蓄账户访问时间 Using(账户号))) Using(支行名))
			Union
			(select 支行名,账户号,账户余额,开户日期,客户身份证号
			from 支行 left join ((支票账户 left join 支票账户访问时间 Using(账户号))) Using(支行名))) C1
	group by 支行名,年度) S2
where S1.支行名 = S2.支行名 and S1.年度 = S2.年度;



(select 支行名,账户号,账户余额,开户日期,客户身份证号
from 支行 left join ((储蓄账户 left join 储蓄账户访问时间 Using(账户号))) Using(支行名))
Union
(select 支行名,账户号,账户余额,开户日期,客户身份证号
from 支行 left join ((支票账户 left join 支票账户访问时间 Using(账户号))) Using(支行名));



(select 客户身份证号,姓名,联系电话,家庭住址,账户号,支行名,最近访问日期,开户日期,账户余额
from 客户 left join (储蓄账户访问时间 left join 储蓄账户 Using(账户号))Using(客户身份证号))
union
(select 客户身份证号,姓名,联系电话,家庭住址,账户号,支行名,最近访问日期,开户日期,账户余额
from 客户 left join (支票账户访问时间 left join 支票账户 Using(账户号))Using(客户身份证号));

select 客户身份证号,姓名,联系电话,家庭住址,贷款号,支行名,贷款总金额,未发款数,贷款状态,最近发款日期
from (客户 left join 客户_贷款 Using(客户身份证号)) left join 贷款 Using(贷款号);


select 贷款号,支行名,贷款总金额,客户身份证号,发款日期,发款金额,发款.未发款数,贷款状态 
              from (贷款 left join 客户_贷款 USING(贷款号))left join 发款 USING(贷款号) 
              where 1 = 1;

