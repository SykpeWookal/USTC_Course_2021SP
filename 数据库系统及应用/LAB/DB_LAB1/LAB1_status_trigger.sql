Drop Trigger if exists Update_Borrowbook;
Drop Trigger if exists Update_Returnbook;

Delimiter //
/*借阅触发器，当向borrow表插入记录时触发，若未填入归还日期，则将status改为1*/
Create Trigger Update_Borrowbook AFTER INSERT ON Borrow FOR EACH ROW
begin
	IF new.Return_Date is NULL THEN
		update Book
        Set `status` = 1
        Where ID = new.Book_ID;
	END IF;
end //
/*归还触发器，当修改borrow表信息时填充归还日期字段，则触发将借阅状态改为0*/
Create Trigger Update_Returnbook AFTER update ON Borrow FOR EACH ROW
begin
	IF old.Return_Date is NULL and new.Return_Date is NOT NULL THEN
		update Book 
        Set `status` = 0
        Where ID = new.Book_ID;
	END IF;
end //
Delimiter ;

select * from borrow;
select * from book;
Insert Into Borrow Values ('b10', 'r1', '2021-01-01', NULL); 
select * from borrow;
select * from book;
Delete From Borrow Where Book_ID = 'b10' and Reader_ID = 'r1' and Borrow_Date = '2021-01-01';
select * from borrow;
select * from book;