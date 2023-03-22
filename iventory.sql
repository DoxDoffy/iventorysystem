-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 22, 2023 at 09:32 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.0.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `iventory`
--

-- --------------------------------------------------------

--
-- Table structure for table `recordperi`
--

CREATE TABLE `recordperi` (
  `peri_no` int(11) NOT NULL,
  `peri_id` varchar(100) NOT NULL,
  `peri_total` varchar(100) NOT NULL,
  `peri_remarks` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `recordperi`
--

INSERT INTO `recordperi` (`peri_no`, `peri_id`, `peri_total`, `peri_remarks`) VALUES
(1, 'haha', '20', 'eyeyeyey'),
(3, 'gggg', '22', '222ggg'),
(6, '4t4t', '44', 'wt4t'),
(8, 'yyy', '22', '2323');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `recordperi`
--
ALTER TABLE `recordperi`
  ADD PRIMARY KEY (`peri_no`),
  ADD UNIQUE KEY `peri_id` (`peri_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `recordperi`
--
ALTER TABLE `recordperi`
  MODIFY `peri_no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
