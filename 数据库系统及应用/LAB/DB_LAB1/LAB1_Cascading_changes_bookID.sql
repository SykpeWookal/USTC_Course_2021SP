Drop procedure if exists Cascading_changes_bookID;
delimiter //
create procedure Cascading_changes_bookID (IN OLD_BOOKID char(8), IN NEW_BOOKID char(8), OUT info char(50))
begin
    Declare if_old_bookid_exist INT default 0;/*旧ID是否存在*/
    Declare if_new_bookid_exist INT default 0;/*新ID是否存在*/
    Declare temp_name VARCHAR(20);
    Declare temp_author VARCHAR(10);
    Declare temp_price FLOAT;
    Declare temp_status INT default 0;
    set info = 'OK';    
    
    Select Count(*) From Book Where Book.ID = OLD_BOOKID INTO if_old_bookid_exist;
    Select Count(*) From Book Where Book.ID = NEW_BOOKID INTO if_new_bookid_exist;
    if if_old_bookid_exist = 0 Then             /*处理旧ID不存在的情况*/
		Set info = 'Old_Book_ID Is Not Exists!';
    elseif if_new_bookid_exist >= 1 THEN       /*处理新ID已经存在的情况*/
		Set info = 'New_Book_ID Is Already Exists!';
	else
    /*先将新的book表记录插入，再对borrow表更改外键引用，最后删除原book表中的记录*/
		 Select `name`, author, price, `status` INTO temp_name, temp_author, temp_price, temp_status 
		 From Book 
		 Where Book.ID = OLD_BOOKID;
		Insert Into Book (ID, `name`, author, price, `status`) 
		   Values (NEW_BOOKID, temp_name, temp_author, temp_price, temp_status);
		Update Borrow 
		Set Borrow.Book_ID = NEW_BOOKID 
		Where Borrow.Book_ID = OLD_BOOKID;
		Delete 
        From Book 
        Where Book.ID = OLD_BOOKID;
    end if;
    
    IF info <> 'OK' then
		ROLLBACK;
	else 
		commit;
	end if;
end //
delimiter ;


/*T4专用测试，b13号书有两条借阅记录，将书号从b13改为b100*/
Select * From Book ;
Select * From Borrow;
Call Cascading_changes_bookID('b13', 'b100', @info);
Select @info;
select * from book;
select * from borrow;

Call Cascading_changes_bookID('b100', 'b13', @info);
Select @info;