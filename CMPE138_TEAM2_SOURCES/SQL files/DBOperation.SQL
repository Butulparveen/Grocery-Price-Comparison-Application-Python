drop database if exists team2_app;
create database team2_app;
use team2_app;


drop table if exists Customer;
CREATE TABLE Customer(
cust_ID varchar(6) not null PRIMARY KEY,
cust_Name varchar(25) not null,
cust_password varchar(40) not null,
cust_phone varchar(15) not null,
cust_email varchar(40) not null,
cust_street varchar(30),
cust_zip varchar(5),
cust_city varchar(20),
cust_state varchar(20)
 );
 
INSERT INTO Customer VALUES('C10001','SUHAS',SHA1('suhas@123') ,'66677788800','SUH@ABC.COM','101 WASHINGTON SQ','95110','SAN JOSE','CA');
INSERT INTO Customer VALUES('C10002','ROHIT',SHA1('rohit@123'),'66677788801','ROH@ABC.COM','102 WASHINGTON SQ','95110','SAN JOSE','CA');
INSERT INTO Customer VALUES('C10003','BUTUL',SHA1('butul@123'),'66677788802','BUT@ABC.COM','40 JULIAN ST','95112','SAN JOSE','CA');
INSERT INTO Customer VALUES('C10004','AFROZ',SHA1('afroz@123'),'66677788803','AFR@ABC.COM','41 JULIAN ST','95112','SAN JOSE','CA');
INSERT INTO Customer VALUES('C10005','DI',SHA1('di@123'),'66677788804','BUT@ABC.COM','40 JULIAN ST','95112','SAN JOSE','CA');
INSERT INTO Customer VALUES('C10006','ROHITH',SHA1('rohith@123'),'66677788805','ROHH@ABC.COM','60 JAMES ST','95115','SAN JOSE','CA');



drop table if exists Store;
CREATE TABLE Store(
store_id varchar(6) not null PRIMARY KEY,
store_name varchar(20) not null ,
store_street varchar(30),
store_zip varchar(5),
store_city varchar(20),
store_state varchar(20),
store_website varchar(40)
);

INSERT INTO Store VALUES('ST1001','TARGET','COL AVE','95110','SAN JOSE','CA','TARGET.COM');
INSERT INTO Store VALUES('ST1002','TARGET','ELCAMINO ST','95112','SAN JOSE','CA','TARGET.COM');
INSERT INTO Store VALUES('ST1003','WALMART','COL AVE','95110','SAN JOSE','CA','WALMART.COM');
INSERT INTO Store VALUES('ST1004','WALMART','COL AVE','95112','SAN JOSE','CA','WALMART.COM');
INSERT INTO Store VALUES('ST1005','COSTCO','110 WASHINGTON SQ','95115','SAN JOSE','CA','COSTCO.COM');
INSERT INTO Store VALUES('ST1006','COSTCO','200 RYLAND ST','95110','SAN JOSE','CA','COSTCO.COM');


drop table if exists Authorized_person;
CREATE TABLE Authorized_person(
m_id varchar(6) not null PRIMARY KEY,
m_password varchar(40) not null,
m_phone varchar(15),
store_id varchar(6) REFERENCES Store(store_id) ON DELETE SET NULL);




INSERT INTO Authorized_person VALUES('MAN101',sha1('man@321'),'1001001001','ST1001');
INSERT INTO Authorized_person VALUES('MAN102',sha1('man@321'),'1001001002','ST1002');
INSERT INTO Authorized_person VALUES('MAN103',sha1('man@321'),'1001001003','ST1003');
INSERT INTO Authorized_person VALUES('MAN104',sha1('man@321'),'1001001004','ST1004');
INSERT INTO Authorized_person VALUES('MAN105',sha1('man@321'),'1001001005','ST1005');
INSERT INTO Authorized_person VALUES('MAN106',sha1('man@321'),'1001001006','ST1006');


drop table if exists Item;
CREATE TABLE Item(
item_id varchar(6) not null PRIMARY KEY,
brand varchar(20) not null,
item_name varchar(20) not null,
unit FLOAT(10) not null,
category varchar(20)  DEFAULT 'Misc',
CONSTRAINT constraint_category_name 
	CHECK(category IN ("Frozen Food","Bread Bakery","Canned" ,"Meat Seafood","diary","Misc","snacks"))
);



INSERT INTO Item VALUES('IT1001',"Nestle","vanilla icecream",'0.5',"Frozen Food");
INSERT INTO Item VALUES('IT1002',"Breyers", "chocolate icecream",'0.75',"Frozen Food");
INSERT INTO Item VALUES('IT1003',"Birds Eye", "peas",'1.0',"Frozen Food");

INSERT INTO Item VALUES('IT1004',"Nature","Whole bread",'2.0',"Bread Bakery");
INSERT INTO Item VALUES('IT1005',"Dave", "Crossaint",'0.75',"Bread Bakery");
INSERT INTO Item VALUES('IT1006',"Oroweat", "Muffin",'0.5',"Bread Bakery");

INSERT INTO Item VALUES('IT1007',"Del Monte","Baked Beans",'1.0',"Canned");
INSERT INTO Item VALUES('IT1008',"Del Monte", "Corn",'0.5',"Canned");
INSERT INTO Item VALUES('IT1009',"Rotel", "Crushed Tomatoes",'1.5',"Canned");

INSERT INTO Item VALUES('IT1010',"All Natural","Chicken",'3',"Meat Seafood");
INSERT INTO Item VALUES('IT1011',"USDA", "Beef",'2.25',"Meat Seafood");
INSERT INTO Item VALUES('IT1012',"Gorton", "Shrimp",'1.0',"Meat Seafood");

INSERT INTO Item VALUES('IT1013',"GoodGather","Whole Milk",'4',"diary");
INSERT INTO Item VALUES('IT1014',"GoodGather", "Almond Milk",'2',"diary");
INSERT INTO Item VALUES('IT1015',"Country Crock", "salted butter",'0.9',"diary");


INSERT INTO Item VALUES('IT1016',"Kirkland","Potato Chips",'0.5',"snacks");
INSERT INTO Item VALUES('IT1017',"Doritos", "Nachos",'0.2',"snacks");
INSERT INTO Item VALUES('IT1018',"Lays", "Classic Potato Chips",'0.5',"snacks");

INSERT INTO Item(item_id,brand,item_name,unit) VALUES('IT1019',"Kirkland","Brown Rice",'30');
INSERT INTO Item(item_id,brand,item_name,unit) VALUES('IT1020',"Axe", "Deo",'0.1');




#price_per_unit is implemented in view
drop table if exists Offers;
CREATE TABLE Offers(
store_id varchar(6) not null,
item_id varchar(6) not null,
price FLOAT(10) not null,
best_before_date date,
quantity_in_stock INTEGER,
PRIMARY KEY(item_id,store_id),
foreign  key (item_id) REFERENCES ITEM(item_id),
foreign  key (store_id) REFERENCES STORE(store_id)
);




INSERT INTO Offers VALUES('ST1001','IT1001','5','2022-10-15','15');
INSERT INTO Offers VALUES('ST1001','IT1002','40','2022-10-15','25');
INSERT INTO Offers VALUES('ST1002','IT1001','4','2022-10-15','10');
INSERT INTO Offers VALUES('ST1002','IT1002','2','2022-10-15','50');
INSERT INTO Offers VALUES('ST1003','IT1003','10','2022-10-15','25');
INSERT INTO Offers VALUES('ST1004','IT1004','12','2022-10-15','07');
INSERT INTO Offers VALUES('ST1004','IT1001','5','2022-10-15','07');
INSERT INTO Offers VALUES('ST1006','IT1001','4','2022-10-15','49');
INSERT INTO Offers VALUES('ST1006','IT1002','10','2023-10-15','07');
INSERT INTO Offers VALUES('ST1005','IT1003','10','2023-10-15','07');
INSERT INTO Offers VALUES('ST1005','IT1002','10','2023-10-15','07');
INSERT INTO Offers VALUES('ST1005','IT1004','4','2022-10-15','07');


INSERT INTO Offers VALUES('ST1004','IT1006','5','2022-10-15','07');
INSERT INTO Offers VALUES('ST1006','IT1007','4','2022-10-15','49');
INSERT INTO Offers VALUES('ST1006','IT1008','10','2023-10-15','07');
INSERT INTO Offers VALUES('ST1005','IT1009','10','2023-10-15','07');
INSERT INTO Offers VALUES('ST1005','IT1005','10','2023-10-15','07');
INSERT INTO Offers VALUES('ST1005','IT1006','4','2022-10-15','07');


INSERT INTO Offers VALUES('ST1006','IT1011','5','2022-10-15','10');
INSERT INTO Offers VALUES('ST1006','IT1010','4','2022-10-15','07');
INSERT INTO Offers VALUES('ST1001','IT1012','6','2022-10-15','20');
INSERT INTO Offers VALUES('ST1002','IT1012','10','2022-10-15','08');
INSERT INTO Offers VALUES('ST1003','IT1013','9','2022-10-15','22');
INSERT INTO Offers VALUES('ST1004','IT1014','5','2022-10-15','17');
INSERT INTO Offers VALUES('ST1001','IT1016','7','2022-10-15','19');
INSERT INTO Offers VALUES('ST1002','IT1017','6','2022-10-15','18');
INSERT INTO Offers VALUES('ST1005','IT1015','7','2022-10-15','19');
INSERT INTO Offers VALUES('ST1002','IT1018','6','2022-10-15','18');


drop table if exists Shopping_list;
CREATE TABLE Shopping_list
(cust_id varchar(6) not null,
shopping_list_id varchar(6) not null,
PRIMARY KEY(shopping_list_id),
foreign  key (cust_id) REFERENCES customer(cust_id)
);


INSERT INTO Shopping_list VALUES('C10001','SL1001');
INSERT INTO Shopping_list VALUES('C10001','SL1002');
INSERT INTO Shopping_list VALUES('C10002','SL1003');
INSERT INTO Shopping_list VALUES('C10003','SL1004');
INSERT INTO Shopping_list VALUES('C10004','SL1005');
INSERT INTO Shopping_list VALUES('C10005','SL1006');
INSERT INTO Shopping_list VALUES('C10006','SL1007');


drop table if exists Contains;
CREATE TABLE Contains(
shopping_list_id varchar(6) not null,
item_id varchar(6) not null,
quantity INTEGER not null,
PRIMARY KEY(shopping_list_id,item_id),
foreign  key (shopping_list_id) REFERENCES Shopping_list(shopping_list_id),
foreign  key (item_id) REFERENCES ITEM(item_id)
);


INSERT INTO Contains VALUES('SL1001','IT1001','2');
INSERT INTO Contains VALUES('SL1001','IT1002','1');
INSERT INTO Contains VALUES('SL1002','IT1008','4');
INSERT INTO Contains VALUES('SL1003','IT1003','3');
INSERT INTO Contains VALUES('SL1004','IT1004','4');
INSERT INTO Contains VALUES('SL1005','IT1004','7');
INSERT INTO Contains VALUES('SL1006','IT1005','9');
INSERT INTO Contains VALUES('SL1007','IT1006','3');
INSERT INTO Contains VALUES('SL1007','IT1007','8');
INSERT INTO Contains VALUES('SL1003','IT1008','3');
INSERT INTO Contains VALUES('SL1005','IT1016','4');
INSERT INTO Contains VALUES('SL1006','IT1010','7');
INSERT INTO Contains VALUES('SL1007','IT1012','9');
INSERT INTO Contains VALUES('SL1006','IT1011','3');
INSERT INTO Contains VALUES('SL1001','IT1017','8');

drop table if exists Orders;
CREATE TABLE Orders(
order_id varchar(6) not null primary key,
shopping_list_id varchar(6) NOT NULL, 
created_on DATETIME NOT NULL DEFAULT NOW(),
delivery_date DATETIME NOT NULL DEFAULT (NOW()+INTERVAL 1 DAY),
payment_method varchar(10) default "CARD",
total_cost integer default 0,
foreign key(shopping_list_id) REFERENCES Shopping_list(shopping_list_id),
CONSTRAINT constraint_PAYMENT_TYPE CHECK(payment_method IN ("CARD","CASH","WALLET"))
);




INSERT INTO Orders(order_id,shopping_list_id,payment_method,total_cost)  VALUES('OR1001','SL1001',"CARD",30);
INSERT INTO Orders(order_id,shopping_list_id,payment_method,total_cost)  VALUES('OR1002','SL1002',"WALLET",20);



drop table if exists Record;
CREATE TABLE Record(
order_id varchar(6) NOT NULL,
item_id varchar(6) NOT NULL,
quantity INTEGER,
primary key(order_id,item_id),
foreign key (order_id) REFERENCES Orders(order_id) on delete cascade,
foreign key (item_id) REFERENCES Item(item_id)
);



INSERT INTO  Record VALUES ('OR1001','IT1001',3);
INSERT INTO  Record VALUES ('OR1002','IT1002',8);



drop table if exists Process_Order;
CREATE TABLE Process_Order(
order_id varchar(6) not null,
store_id varchar(6) NOT NULL,
primary key(order_id,store_id),
foreign key (order_id) REFERENCES Orders(order_id) on delete cascade,
foreign key (store_id) REFERENCES Store(store_id)
);


INSERT INTO Process_Order VALUES('OR1001','ST1001');	
	


CREATE VIEW `price_per_unit_view` AS
select store_id,offers.item_id,price,unit, (offers.price/item.unit) as price_per_unit 
from offers join item
on offers.item_id=item.item_id
order by store_id;




CREATE VIEW `Shopping_list_total_view` AS
select CONTAINS.item_id,quantity,store_id,price , quantity*price as item_total from CONTAINS JOIN OFFERS ON CONTAINS.ITEM_ID=OFFERS.ITEM_ID;






DROP PROCEDURE if exists Find_cheapest_store_given_itemID;
DELIMITER $$
CREATE PROCEDURE `Find_cheapest_store_given_itemID` 
(IN item_id_param varchar(6),
IN shopping_list_id_param varchar(6),
 OUT store_id_param varchar(6),
 OUT Quantity_in_Stock_param integer,
 OUT price_pram integer)
BEGIN
select store_id into store_id_param  
 from  CONTAINS JOIN OFFERS ON CONTAINS.ITEM_ID=OFFERS.ITEM_ID
 where  CONTAINS.item_id=item_id_param and shopping_list_id=shopping_list_id_param and price =
 (select min(price)  from  CONTAINS JOIN OFFERS ON CONTAINS.ITEM_ID=OFFERS.ITEM_ID where  CONTAINS.item_id=item_id_param);
select  quantity_in_stock into  Quantity_in_Stock_param 
 from  CONTAINS JOIN OFFERS ON CONTAINS.ITEM_ID=OFFERS.ITEM_ID
 where  CONTAINS.item_id=item_id_param and shopping_list_id=shopping_list_id_param and price =
 (select min(price)  from  CONTAINS JOIN OFFERS ON CONTAINS.ITEM_ID=OFFERS.ITEM_ID where  CONTAINS.item_id=item_id_param);
select price into price_pram
 from  CONTAINS JOIN OFFERS ON CONTAINS.ITEM_ID=OFFERS.ITEM_ID
 where  CONTAINS.item_id=item_id_param and shopping_list_id=shopping_list_id_param and price =
 (select min(price)  from  CONTAINS JOIN OFFERS ON CONTAINS.ITEM_ID=OFFERS.ITEM_ID where  CONTAINS.item_id=item_id_param);
END $$
DELIMITER ;

drop procedure if exists authenticate_customer;
DELIMITER $$
CREATE PROCEDURE `authenticate_customer` (IN cust_ID_param varchar(6) ,IN cust_password_param varchar(40),OUT validated bool)
BEGIN

if exists(select  * from Customer 
		  where cust_ID=cust_ID_param and cust_password=sha1(cust_password_param))
then set validated=true;
else set validated=false;
end if;
END $$
DELIMITER ;



drop procedure if exists authenticate_manager;
DELIMITER $$
CREATE PROCEDURE `authenticate_manager` (IN m_ID_param varchar(6) ,IN m_password_param varchar(40),OUT validated bool)
BEGIN

if exists(select  * from Authorized_person
		  where m_id=m_ID_param and m_password=sha1(m_password_param))
then set validated=true;
else set validated=false;
end if;
END $$
DELIMITER ;