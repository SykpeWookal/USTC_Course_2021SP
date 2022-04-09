create table Book
(
	ID       char(8),
	`name`   varchar(50) not null,
	author   varchar(10),
	price    float,
	`status` int DEFAULT 0,
	primary key(ID)
);

create table Reader
(
	ID       char(8),
    `name`   varchar(10),
    age      int,
    address  varchar(20),
    primary key(ID)
);

create table Borrow
(
	book_ID      char(8),
    Reader_ID    char(8),
    Borrow_Date  date,
    Return_Date  date,
    primary key(book_ID, Reader_ID),
    foreign key(book_ID) references Book(ID),
    foreign key(Reader_ID) references Reader(ID)
);