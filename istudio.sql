create database Reatail_sales_data;
use  Reatail_sales_data;
create table Sales_data_transactions(
customer_id varchar(255),
trans_date varchar(255),
tran_amount int);
create table Sales_data_response(
customer_id varchar(255),
response int);
Load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Retail_Data_Transactions.csv'
Into table Sales_data_transactions
Fields terminated by ','
Lines terminated by '\n'
Ignore 1 rows;
create index idx_id ON Sales_data_transactions(customer_id);
