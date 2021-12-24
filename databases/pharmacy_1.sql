-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Час створення: Гру 24 2021 р., 03:24
-- Версія сервера: 10.4.22-MariaDB
-- Версія PHP: 8.0.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База даних: `pharmacy_1_clear`
--

-- --------------------------------------------------------

--
-- Структура таблиці `client`
--

CREATE TABLE `client` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(30) NOT NULL,
  `email` varchar(40) NOT NULL,
  `age` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблиці `doctor`
--

CREATE TABLE `doctor` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(20) NOT NULL,
  `type` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблиці `medicine`
--

CREATE TABLE `medicine` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(20) NOT NULL,
  `prescription` tinyint(1) NOT NULL,
  `text` text NOT NULL,
  `age` int(2) NOT NULL,
  `price` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблиці `order`
--

CREATE TABLE `order` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `bonuscard` tinyint(1) NOT NULL,
  `id_client` bigint(20) UNSIGNED NOT NULL,
  `id_provizor` bigint(20) UNSIGNED DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `datatime` datetime NOT NULL,
  `id_medicine` bigint(20) UNSIGNED NOT NULL,
  `id_prescription` bigint(20) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблиці `prescription`
--

CREATE TABLE `prescription` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `id_doctor` bigint(20) UNSIGNED NOT NULL,
  `id_client` bigint(20) UNSIGNED NOT NULL,
  `id_medicine` bigint(20) UNSIGNED NOT NULL,
  `datatime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблиці `provizor`
--

CREATE TABLE `provizor` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Індекси збережених таблиць
--

--
-- Індекси таблиці `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Індекси таблиці `doctor`
--
ALTER TABLE `doctor`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Індекси таблиці `medicine`
--
ALTER TABLE `medicine`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Індекси таблиці `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`),
  ADD KEY `id_client` (`id_client`),
  ADD KEY `id_provizor` (`id_provizor`),
  ADD KEY `id_medicine` (`id_medicine`),
  ADD KEY `id_prescription` (`id_prescription`);

--
-- Індекси таблиці `prescription`
--
ALTER TABLE `prescription`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`),
  ADD KEY `id_client` (`id_client`),
  ADD KEY `id_doctor` (`id_doctor`),
  ADD KEY `id_medicine` (`id_medicine`);

--
-- Індекси таблиці `provizor`
--
ALTER TABLE `provizor`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- AUTO_INCREMENT для збережених таблиць
--

--
-- AUTO_INCREMENT для таблиці `client`
--
ALTER TABLE `client`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1584615718;

--
-- AUTO_INCREMENT для таблиці `doctor`
--
ALTER TABLE `doctor`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=554708074;

--
-- AUTO_INCREMENT для таблиці `medicine`
--
ALTER TABLE `medicine`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблиці `order`
--
ALTER TABLE `order`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT для таблиці `prescription`
--
ALTER TABLE `prescription`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблиці `provizor`
--
ALTER TABLE `provizor`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=554708074;

--
-- Обмеження зовнішнього ключа збережених таблиць
--

--
-- Обмеження зовнішнього ключа таблиці `order`
--
ALTER TABLE `order`
  ADD CONSTRAINT `order_ibfk_1` FOREIGN KEY (`id_client`) REFERENCES `client` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `order_ibfk_2` FOREIGN KEY (`id_provizor`) REFERENCES `provizor` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `order_ibfk_3` FOREIGN KEY (`id_medicine`) REFERENCES `medicine` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `order_ibfk_4` FOREIGN KEY (`id_prescription`) REFERENCES `prescription` (`id`);

--
-- Обмеження зовнішнього ключа таблиці `prescription`
--
ALTER TABLE `prescription`
  ADD CONSTRAINT `prescription_ibfk_1` FOREIGN KEY (`id_medicine`) REFERENCES `medicine` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `prescription_ibfk_2` FOREIGN KEY (`id_doctor`) REFERENCES `doctor` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `prescription_ibfk_3` FOREIGN KEY (`id_client`) REFERENCES `client` (`id`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
