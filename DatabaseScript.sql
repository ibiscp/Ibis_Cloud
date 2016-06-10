CREATE DATABASE IF NOT EXISTS ibiscloud;

USE ibiscloud;

CREATE TABLE IF NOT EXISTS `log` (
`Id` int unsigned NOT NULL AUTO_INCREMENT,
`Path` varchar(200) NOT NULL,
`Message` varchar(200) NOT NULL,
`Size` bigint unsigned NOT NULL,
`Timestamp` timestamp NOT NULL,
PRIMARY KEY (`Id`));

CREATE TABLE IF NOT EXISTS `map` (
`Id` int(11) NOT NULL AUTO_INCREMENT,
`Source` varchar(200) NOT NULL,
`Destination` varchar(200) NOT NULL,
PRIMARY KEY (`Id`));

CREATE TABLE IF NOT EXISTS `server` (
`Id` int(11) NOT NULL AUTO_INCREMENT,
`Address` varchar(200) NOT NULL,
`User` varchar(200) NOT NULL,
PRIMARY KEY (`Id`));

INSERT INTO `server` (Address, User)
VALUES("187.65.245.244", "ibis");