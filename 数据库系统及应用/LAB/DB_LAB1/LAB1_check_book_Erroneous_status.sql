Drop procedure if exists check_book_Erroneous_status;
delimiter //
create procedure check_book_Erroneous_status (OUT count_erroneous_status INT)
begin
	Declare state INT default 0;
    Declare cursor_ID CHAR(8);
    Declare cursor_status INT;
    Declare a INT;
    Declare cursor_count_erroneous_status Cursor For Select ID, `status` From Book;
    Declare continue Handler for NOT FOUND set state = 1;/*记录游标中的读取情况*/
    
    Set count_erroneous_status = 0; /*初始化*/
    Open cursor_count_erroneous_status;/*游标操作*/
    Repeat
		Fetch cursor_count_erroneous_status INTO cursor_ID, cursor_status;
        if state = 0 THEN    /*游标中记录未曾读取完*/
			if cursor_ID IN (Select Book_ID From Borrow) then
				Select Count(*) From Borrow Where Book_ID = cursor_ID and Return_Date is NULL INTO a;
                if a > 0 and cursor_status = 0 then 			/*已借出但status为0*/
					Set count_erroneous_status = count_erroneous_status + 1;
				end if;
                if a = 0 and cursor_status = 1 then 	/*未借出但status为1*/
					Set count_erroneous_status = count_erroneous_status + 1;
				end if;
			else   										/*没有借阅记录但status=1*/
				if cursor_status = 1 then
					Set count_erroneous_status = count_erroneous_status + 1;
				end if;
			end if;
		end if;
		Until state = 1
    End Repeat;
    Close cursor_count_erroneous_status;
end
//
delimiter ;

call check_book_Erroneous_status(@check_book_Erroneous_status);
select @check_book_Erroneous_status;