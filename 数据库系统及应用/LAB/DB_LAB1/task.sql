/*1、检索读者rose的读者号和地址*/
select ID,address
from reader
where reader.`name` = 'rose';

/*2、检索读者rose所借阅的所有书的图书名和借出日期*/
select Book.`name`, Borrow_Date
from  Book,Reader,Borrow
where Book.ID = Borrow.book_ID and
	  Reader.ID = Borrow.Reader_ID and
      Reader.`name` = 'rose';

/*3、检索未借阅图书的读者姓名*/
select `name`
from Reader
where ID NOT IN (select Reader_ID from Borrow);

/*4、检索Ullman所写的书的书名和单价*/
select `name`, price
from Book
where author = 'Ullman';

/*5、检索“李林”借阅未还的图书的图书号和书名*/
select Book.ID, Book.`name`
from Book, Reader, Borrow
where Book.ID = Borrow.book_ID and
	  Reader.ID = Borrow.Reader_ID and
      Reader.`name` = '李林' and
      Borrow.Return_Date is null;
      
/*6、检索借阅图书数目超过3本的读者姓名*/
select Reader.`name`
from Reader, (select Reader_ID
			  from Borrow
			  group by Reader_ID
              having count(*) > 3) b1
where Reader.ID = b1.Reader_ID;

/*7、检索没有借阅读者“李林”所借过的任何一本书的读者姓名和读者号*/
select reader.`name`, reader.ID
from reader
where reader.ID NOT IN ( /*以下选出借了李林借过的书的读者*/
		select reader_ID
        from reader r1, borrow b1
        where r1.ID = b1.Reader_ID and b1.book_ID IN(
				Select b2.book_ID
				From Borrow b2, Reader r2
                where b2.Reader_ID = r2.ID and
                      r2.`name` = '李林'
			 )
      );

/*8、检索书名中包含“Oracle”的图书书名以及图书号*/
select Book.`name`, Book.ID
from Book
where Book.`name` like '%Oracle%';

/*9、创建一个读者借书信息的视图，该视图包含读者号、姓名、所借图书号、图书名和借期；*/
Drop View IF EXISTS R_B_info;/*方便每次执行调试，判断视图是否存在，若存在则执行删除视图  */

create view R_B_info(R_ID, R_name, B_ID, B_name, borrow_date)
as select Reader.ID, Reader.`name`, Book.ID, Book.`name`, borrow.Borrow_Date
   from Reader, Book, Borrow
   where Reader.ID = Borrow.Reader_ID and
		 Book.ID = Borrow.book_ID;
/*测试视图*/ select * from R_B_info ;

/*9、使用上述视图查询最近一年所有读者的读者号以及所借阅的不同图书数*/
SELECT R_ID, count(*) as '借阅次数'
FROM R_B_info
WHERE R_B_info.Borrow_Date > DATE_SUB(CURDATE(), INTERVAL 1 YEAR) 
group by R_ID;