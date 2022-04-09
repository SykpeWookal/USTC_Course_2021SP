/*实体完整性：主键唯一标识一个实体，插入的信息没有主键无法成功插入*/
Insert Into Book (`name`, author, price, `status`) Values ('实体完整性', 'admini', 114, 1);
Insert Into Borrow (Reader_ID, Borrow_Date, Return_Date) Values ('r5', '2020-01-01', '2021-01-01');
Insert Into Borrow (Book_ID, Reader_ID, Borrow_Date, Return_Date) Values ('b1', 'r5', '2020-01-01', '2021-01-01');
Delete From Borrow Where Book_ID = 'b1' and Reader_ID = 'r5' and Borrow_Date = '2021-01-01';

/*参照完整性：主表中的主键信息在子表中必须存在，否则无法成功插入*/
Insert Into Borrow Values ('b99', 'r5', '2021-01-01', NULL);
Insert Into Borrow Values ('b1', 'r99', '2021-01-01', NULL); 

/*用户完整性：插入的数据必须满足表中定义的类型和约束条件，否则无法成功插入*/
Insert Into Book Values ('b15', null, 7, 1, 0);/*name不能为null*/