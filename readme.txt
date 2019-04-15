ssh marco.omnib.it
mysql -u root -p

mysql> SELECT Host, Db, User FROM db;
+-----------+--------------------+---------------+
| Host      | Db                 | User          |
+-----------+--------------------+---------------+
| %         | agenda             | root          |
| %         | agenda             | user          |
| %         | boll               | cisco         |
| %         | fermiLan           | marco         |
| %         | toniaAlarm         | tonia         |
| localhost | agenda             | studente      |
| localhost | performance_schema | mysql.session |
| localhost | sys                | mysql.sys     |
+-----------+--------------------+---------------+
8 rows in set (0,00 sec)

mysql> SELECT Host, USER FROM user;
+-----------+------------------+
| Host      | USER             |
+-----------+------------------+
| %         | cisco            |
| %         | marco            |
| %         | root             |
| %         | studente         |
| %         | tonia            |
| %         | user             |
| 127.0.0.1 | root             |
| ::1       | root             |
| locahost  | studente         |
| localhost | debian-sys-maint |
| localhost | mysql.session    |
| localhost | mysql.sys        |
| localhost | root             |
| localhost | studente         |
| server    | root             |
+-----------+------------------+
15 rows in set (0,00 sec)

create schema toniaAlarm
GRANT ALL PRIVILEGES ON toniaAlarm.* TO 'tonia'@'%' IDENTIFIED BY '*****';
GRANT ALL PRIVILEGES ON toniaAlarm.* TO 'root'@'%'
FLUSH PRIVILEGES

ALTER DATABASE toniaAlarm CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE `toniaAlarm`.`sounds` (
  `soundId` int(11) NOT NULL AUTO_INCREMENT,
  `originalFileName` varchar(255) NOT NULL,
  `storeFileName` varchar(255) NOT NULL,
  `sizeSeconds` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`soundId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `toniaAlarm`.`users` (
  `userId` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `pw` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`userId`, `username`)
  ) ENGINE=MyISAM DEFAULT CHARSET=utf8;;

INSERT INTO `toniaAlarm`.`users` (`userId`, `username`, `pw`) VALUES ('1', 'tonia', '*****');
