SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;

USE `supreme_umbrella`;

CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(40) NOT NULL,
  `password_hash` text NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `age_years` int NOT NULL,
  `interests` text NOT NULL,
  `city` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
