import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    "DROP TABLE IF EXISTS group_user CASCADE;",
    "DROP TABLE IF EXISTS event_user CASCADE;",
    "DROP TABLE IF EXISTS event_table CASCADE;",
    "DROP TABLE IF EXISTS group_table CASCADE;",
    "DROP TABLE IF EXISTS user_table CASCADE;",
    "DROP TABLE IF EXISTS comment_table CASCADE;",
    "CREATE TABLE user_table("
	"userid SERIAL NOT NULL UNIQUE,"
	"username varchar(255) NOT NULL UNIQUE,"
	"first_name varchar(255) NOT NULL,"
	"surname varchar(255) NOT NULL,"
	"email varchar(255) NOT NULL UNIQUE,"
	"passwrd varchar(255) NOT NULL,"
	"gender char(5),"
	"age integer,"
	"country varchar(50),"
	"city varchar(50),"
	"hobbies varchar(255),"
	"description varchar(255),"
	"PRIMARY KEY(userid)"
    ");",
    " CREATE TABLE group_table ("
	"group_id serial NOT NULL UNIQUE,"
	"group_name varchar(255) NOT NULL,"
	"isprivate boolean default  false,"
	"owner int NOT NULL,"
	"description varchar(255),"
	"give_permission boolean default false,"
	"unique(group_name,owner),"
	"primary key(group_id),"
	"foreign key(owner)"
	"	references user_table(userid)"
	"	on delete no action "
		" on update no action"
    ");",
    " CREATE TABLE event_table ("
	"event_id serial NOT NULL UNIQUE,"
	"group_id INT,"
	"event_name varchar(255) UNIQUE NOT NULL,"
	"place varchar(255) NOT NULL,"
	"owner int NOT NULL,"
	"day int NOT NULL,"
	"month int NOT NULL,"
	"year int NOT NULL,"
	"explanation varchar(255) ,"
    	"unique(event_name,owner,day,month,year),"
	"foreign key(owner)"
	"	references user_table(userid)"
	"	on delete cascade "
	"	on update cascade,"
	"foreign key(group_id)"
	"	references group_table(group_id)"
	"	on delete set null "
	"	on update cascade"
    ");",
    "CREATE TABLE event_user ("
	"event_id INT NOT NULL,"
	"user_id INT NOT NULL,"
    	" primary key(user_id, event_id),"
	"foreign key(event_id)"
	"	references event_table(event_id)"
	"	on delete cascade "
	"	on update cascade,"
	"foreign key(user_id)"
	"	references user_table(userid)"
	"	on delete cascade "
	"	on update cascade"
    ");",
    "CREATE TABLE group_user ("
	"user_id INT NOT NULL,"
	"group_id INT NOT NULL,"
    "       primary key(user_id, group_id),"
	"foreign key(user_id)"
	"	references user_table(userid)"
	"	on delete cascade"
	"	on update cascade,"
	"foreign key(group_id)"
	"	references group_table(group_id)"
	"	on delete cascade"
	"	on update cascade"
    ");",
    "CREATE TABLE comment_table("
	"comment_id SERIAL NOT NULL UNIQUE,"
	"owner varchar(255) NOT NULL,"
	"time varchar(255) NOT NULL,"
	"comment varchar(255) NOT NULL,"
	"subject varchar(255),"
	"event_id INT NOT NULL,"
	"is_edited Boolean DEFAULT FALSE,"
	"send_notification Boolean Default False,"
	"primary key(comment_id),"
	"foreign key(event_id)"
	"	references event_table(event_id)"
	"	on delete cascade"
	"	on update cascade,"
	"foreign key(owner)"
	"	references user_table(username)"
	"	on delete cascade"
	"	on update cascade"	
	");"
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
