-- POSTGRESQL DATABASE SETUP

# SYS USER DEFINITION

-- drop table sys_user;
-- drop sequence sys_user_seq;

create sequence sys_user_seq start 1 cache 1 increment by 1;

create table sys_user(
    id_user integer,
    username varchar(50),
    email varchar(255),
    password varchar(255),
    created_at_ts timestamp,
    created_by integer,
    change_password boolean,
    last_login timestamp,


    constraint sys_user_pk primary key (id_user)    
) tablespace sys_data_ts;
