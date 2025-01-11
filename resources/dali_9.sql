-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 13, 2024 at 06:24 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dali_9`
--

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `id_item` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `quantity` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `category` varchar(255) NOT NULL,
  `imagepath` varchar(255) NOT NULL,
  `barcode` varchar(13) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`id_item`, `name`, `quantity`, `price`, `category`, `imagepath`, `barcode`) VALUES
(2, 'Apples', '1 kg', 150.00, 'Fruit & Vegetables', 'resources/itemimages/2.png', '9011188511100'),
(3, 'Bananas', '1 kg', 60.00, 'Fruit & Vegetables', 'resources/itemimages/3.png', '9011188511101'),
(4, 'Oranges', '1 kg', 120.00, 'Fruit & Vegetables', 'resources/itemimages/4.png', '9011188511102'),
(5, 'Grapes', '1 kg', 200.00, 'Fruit & Vegetables', 'resources/itemimages/5.png', '9011188511103'),
(6, 'Strawberries', '250 g', 180.00, 'Fruit & Vegetables', 'resources/itemimages/6.png', '9011188511104'),
(7, 'Blueberries', '125 g', 150.00, 'Fruit & Vegetables', 'resources/itemimages/7.png', '9011188511105'),
(8, 'Potatoes', '1 kg', 80.00, 'Fruit & Vegetables', 'resources/itemimages/8.png', '9011188511106'),
(9, 'Onions', '1 kg', 100.00, 'Fruit & Vegetables', 'resources/itemimages/9.png', '9011188511107'),
(10, 'Carrots', '1 kg', 70.00, 'Fruit & Vegetables', 'resources/itemimages/10.png', '9011188511108'),
(11, 'Tomatoes', '1 kg', 60.00, 'Fruit & Vegetables', 'resources/itemimages/11.png', '9011188511109'),
(12, 'Milk', '1 L', 70.00, 'Dairy Products', 'resources/itemimages/12.png', '9011188511110'),
(13, 'Cheese', '200 g', 120.00, 'Dairy Products', 'resources/itemimages/13.png', '9011188511111'),
(14, 'Yogurt', '150 g', 35.00, 'Dairy Products', 'resources/itemimages/14.png', '9011188511112'),
(15, 'Butter', '225 g', 150.00, 'Dairy Products', 'resources/itemimages/15.png', '9011188511113'),
(16, 'Cream', '250 ml', 60.00, 'Dairy Products', 'resources/itemimages/16.png', '9011188511114'),
(17, 'Chicken Breast', '1 kg', 200.00, 'Meat & Seafood', 'resources/itemimages/17.png', '9011188511115'),
(18, 'Ground Beef', '1 kg', 350.00, 'Meat & Seafood', 'resources/itemimages/18.png', '9011188511116'),
(19, 'Bacon', '1 kg', 300.00, 'Meat & Seafood', 'resources/itemimages/19.png', '9011188511117'),
(20, 'Salmon Fillet', '1 kg', 600.00, 'Meat & Seafood', 'resources/itemimages/20.png', '9011188511118'),
(21, 'Shrimp', '1 kg', 500.00, 'Meat & Seafood', 'resources/itemimages/21.png', '9011188511119'),
(22, 'Bread', 'loaf', 60.00, 'Bakery Items', 'resources/itemimages/22.png', '9011188511120'),
(23, 'Bagels', 'pack of 6', 70.00, 'Bakery Items', 'resources/itemimages/23.png', '9011188511121'),
(24, 'Croissants', 'each', 35.00, 'Bakery Items', 'resources/itemimages/24.png', '9011188511122'),
(25, 'Tortillas', 'pack of 10', 80.00, 'Bakery Items', 'resources/itemimages/25.png', '9011188511123'),
(26, 'Muffins', 'each', 40.00, 'Bakery Items', 'resources/itemimages/26.png', '9011188511124'),
(27, 'Rice', '5 kg', 250.00, 'Pantry Staples', 'resources/itemimages/27.png', '9011188511125'),
(28, 'Pasta', '500 g', 70.00, 'Pantry Staples', 'resources/itemimages/28.png', '9011188511126'),
(29, 'Canned Beans', '155 g', 35.00, 'Pantry Staples', 'resources/itemimages/29.png', '9011188511127'),
(30, 'Olive Oil', '500 ml', 250.00, 'Pantry Staples', 'resources/itemimages/30.png', '9011188511128'),
(31, 'Flour', '1 kg', 50.00, 'Pantry Staples', 'resources/itemimages/31.png', '9011188511129'),
(32, 'Potato Chips', '150 g', 50.00, 'Snacks', 'resources/itemimages/32.png', '9011188511130'),
(33, 'Popcorn', 'microwave pack', 35.00, 'Snacks', 'resources/itemimages/33.png', '9011188511131'),
(34, 'Chocolate Bars', '50 g', 40.00, 'Snacks', 'resources/itemimages/34.png', '9011188511132'),
(35, 'Granola Bars', 'pack of 6', 120.00, 'Snacks', 'resources/itemimages/35.png', '9011188511133'),
(36, 'Cookies', 'pack of 4', 60.00, 'Snacks', 'resources/itemimages/36.png', '9011188511134'),
(37, 'Coffee', '200 g', 150.00, 'Beverages', 'resources/itemimages/37.png', '9011188511135'),
(38, 'Tea', 'box of 20', 80.00, 'Beverages', 'resources/itemimages/38.png', '9011188511136'),
(39, 'Orange Juice', '1 L', 90.00, 'Beverages', 'resources/itemimages/39.png', '9011188511137'),
(40, 'Bottled Water', '500 ml', 15.00, 'Beverages', 'resources/itemimages/40.png', '9011188511138'),
(41, 'Soda', '330 ml can', 25.00, 'Beverages', 'resources/itemimages/41.png', '9011188511139'),
(42, 'Frozen Pizza', 'each', 200.00, 'Frozen Foods', 'resources/itemimages/42.png', '9011188511140'),
(43, 'Ice Cream', '1.5 L', 250.00, 'Frozen Foods', 'resources/itemimages/43.png', '9011188511141'),
(44, 'Frozen Vegetables', '500 g', 80.00, 'Frozen Foods', 'resources/itemimages/44.png', '9011188511142'),
(45, 'Frozen French Fries', '1 kg', 150.00, 'Frozen Foods', 'resources/itemimages/45.png', '9011188511143'),
(46, 'Frozen Waffles', 'pack of 10', 120.00, 'Frozen Foods', 'resources/itemimages/46.png', '9011188511144'),
(47, 'Dish Soap', '500 ml', 60.00, 'Household Essentials', 'resources/itemimages/47.png', '9011188511145'),
(48, 'Laundry Detergent', '1 kg', 100.00, 'Household Essentials', 'resources/itemimages/48.png', '9011188511146'),
(49, 'Paper Towels', 'roll', 30.00, 'Household Essentials', 'resources/itemimages/49.png', '9011188511147'),
(50, 'Toilet Paper', 'pack of 4 ', 50.00, 'Household Essentials', 'resources/itemimages/50.png', '9011188511148'),
(51, 'Trash Bags', 'pack of 10', 70.00, 'Household Essentials', 'resources/itemimages/51.png', '9011188511149');

-- --------------------------------------------------------

--
-- Table structure for table `orderitems`
--

CREATE TABLE `orderitems` (
  `id_order` int(11) NOT NULL,
  `id_item` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orderitems`
--

INSERT INTO `orderitems` (`id_order`, `id_item`, `quantity`) VALUES
(1, 1, 1),
(7, 45, 2),
(7, 4, 4),
(7, 6, 1),
(7, 8, 2),
(7, 3, 1),
(7, 47, 1),
(7, 2, 10),
(7, 12, 3),
(7, 48, 1),
(7, 43, 5),
(9, 2, 5),
(9, 5, 6),
(9, 7, 5),
(9, 3, 6),
(9, 8, 2);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id_order` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `datetime_initiate` datetime NOT NULL,
  `datetime_completed` datetime NOT NULL,
  `iscompleted` tinyint(1) NOT NULL DEFAULT 0,
  `total` decimal(10,2) NOT NULL DEFAULT 0.00,
  `cash` decimal(10,2) NOT NULL DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id_order`, `id_user`, `datetime_initiate`, `datetime_completed`, `iscompleted`, `total`, `cash`) VALUES
(7, 1, '2024-11-30 21:01:51', '0000-00-00 00:00:00', 0, 4360.00, 0.00),
(9, 1, '2024-12-05 13:43:04', '0000-00-00 00:00:00', 0, 3220.00, 0.00);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(32) NOT NULL,
  `password` varchar(32) NOT NULL,
  `type` int(11) NOT NULL,
  `name` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `type`, `name`) VALUES
(0, 'admin', '21232f297a57a5a743894a0e4a801fc3', 0, 'Administrator'),
(1, 'customer', '91ec1f9324753048c0096d036a694f86', 1, 'Customer');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`id_item`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id_order`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `id_item` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=153;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id_order` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
