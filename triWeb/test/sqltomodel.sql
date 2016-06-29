use testbeds;
show tables;
select * from triWeb_devicemodel;
select * from triWeb_testbedmodel;
select * from triWeb_climodel;
delete from triWeb_devicemodel where type='cos';
Desc triWeb_climodel;