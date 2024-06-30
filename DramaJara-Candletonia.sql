-- MariaDB dump 10.19-11.3.2-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: dbCandletonia
-- ------------------------------------------------------
-- Server version	11.3.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tblcustomer`
--

DROP TABLE IF EXISTS `tblcustomer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblcustomer` (
  `intCustomerID` int(11) NOT NULL AUTO_INCREMENT,
  `strFirstName` varchar(255) NOT NULL,
  `strMiddleName` varchar(255) DEFAULT NULL,
  `strLastName` varchar(255) NOT NULL,
  `strEmail` varchar(255) NOT NULL,
  `strContactNumber` varchar(45) NOT NULL,
  PRIMARY KEY (`intCustomerID`),
  UNIQUE KEY `idxCustomerDetails` (`strFirstName`,`strMiddleName`,`strLastName`,`strEmail`,`strContactNumber`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblcustomer`
--

LOCK TABLES `tblcustomer` WRITE;
/*!40000 ALTER TABLE `tblcustomer` DISABLE KEYS */;
INSERT INTO `tblcustomer` VALUES
(1,'Juan','Garcia','Dela Cruz','juan.garcia@gmail.com','09187482451'),
(2,'Maria','Santos','Lopez','ma.lopez@yahoo.com','09197482567'),
(3,'Mikaella','','Park','bini.mika@gmail.com','09090982331'),
(4,'Taylor','Eras','Swift','tswift@gmail.com','09190373841'),
(5,'Anna','Reyes','Tolentino','annatolentino@yahoo.com','09287488902'),
(6,'Migel','Ong','Lopez','migellopez@gmail.com','09323482555'),
(7,'Carmen','Mendoza','Gonzales','carmeng@yahoo.com','09546482908'),
(8,'Felipe','','Tan','felipetan@gmail.com','09908422879');
/*!40000 ALTER TABLE `tblcustomer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblcustomeraddress`
--

DROP TABLE IF EXISTS `tblcustomeraddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblcustomeraddress` (
  `intCustomerAddressID` int(11) NOT NULL AUTO_INCREMENT,
  `intCustomerID` int(11) NOT NULL,
  `strBlockUnit` varchar(255) NOT NULL,
  `strStreet` varchar(255) NOT NULL,
  `strCity` varchar(255) NOT NULL,
  `strProvince` varchar(255) NOT NULL,
  PRIMARY KEY (`intCustomerAddressID`),
  KEY `fkAddressCustomer` (`intCustomerID`),
  CONSTRAINT `fkAddressCustomer` FOREIGN KEY (`intCustomerID`) REFERENCES `tblcustomer` (`intCustomerID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblcustomeraddress`
--

LOCK TABLES `tblcustomeraddress` WRITE;
/*!40000 ALTER TABLE `tblcustomeraddress` DISABLE KEYS */;
INSERT INTO `tblcustomeraddress` VALUES
(1,1,'Unit 111','Main Street','Manila','Metro Manila'),
(2,2,'Unit 1212','P. Burgos Street','Manila','Metro Manila'),
(3,3,'Block 13','Ramos Street','Cebu City','Cebu'),
(4,4,'Unit 41','Ayala Avenue','Makati City','Metro Manila'),
(5,5,'Block 55','Malate Street','Manila','Metro Manila'),
(6,6,'Unit 67','Paseo de Roxas','Makati City','Metro Manila'),
(7,7,'Unit 14','Bacolod Street','Bacolod City','Negros Occidental'),
(8,8,'Unit 88','Rizal Avenue','Caloocan City','Metro Manila'),
(9,2,'Unit 99','Araneta Avenue','Pasay City','Metro Manila');
/*!40000 ALTER TABLE `tblcustomeraddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbldropoff`
--

DROP TABLE IF EXISTS `tbldropoff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbldropoff` (
  `intDropOffID` int(11) NOT NULL AUTO_INCREMENT,
  `strBlockUnit` varchar(255) NOT NULL,
  `strStreet` varchar(255) NOT NULL,
  `strCity` varchar(255) NOT NULL,
  `strProvince` varchar(255) NOT NULL,
  PRIMARY KEY (`intDropOffID`),
  UNIQUE KEY `idxDropOff` (`strBlockUnit`,`strStreet`,`strCity`,`strProvince`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbldropoff`
--

LOCK TABLES `tbldropoff` WRITE;
/*!40000 ALTER TABLE `tbldropoff` DISABLE KEYS */;
INSERT INTO `tbldropoff` VALUES
(1,'Unit 01','Roxas Boulevard','Manila','Metro Manila'),
(2,'Unit 02','Ayala Avenue','Makati City','Metro Manila'),
(3,'Unit 14','Bonifacio Global City','Taguig City','Metro Manila'),
(4,'Block 10','Ortigas Avenue','Pasig City','Metro Manila'),
(5,'Unit 16','Sunset Drive','Cainta','Rizal'),
(6,'Block 7','Quezon Avenue','Quezon City','Metro Manila'),
(7,'Unit 8','Tomas Morato Avenue','Quezon City','Metro Manila'),
(8,'Block 18','Davao City Proper','Davao City','Davao Del Sur'),
(9,'Unit 16','Cebu Business Park','Cebu City','Cebu'),
(10,'Unit 19','Bacolod City Proper','Bacolod City','Negros Ocicdental'),
(11,'Unit 10','Alabang','Muntinlupa City','Metro Manila'),
(12,'Unit 11','Greenhills','San Juan City','Metro Manila'),
(13,'Block 11','Anonas Street','Manila','Metro Manila'),
(14,'Unit 24','Iloilo City Proper','Iloilo City','Iloilo'),
(15,'Unit 28','Angeles City Proper','Angeles City','Pampanga');
/*!40000 ALTER TABLE `tbldropoff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblitem`
--

DROP TABLE IF EXISTS `tblitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblitem` (
  `intItemID` int(11) NOT NULL AUTO_INCREMENT,
  `txtDescription` text NOT NULL,
  `unitPrice` float(10,2) NOT NULL,
  `quantity` float(10,2) NOT NULL,
  `strUnitMeasurement` varchar(255) DEFAULT NULL,
  `intSupplierID` int(11) NOT NULL,
  PRIMARY KEY (`intItemID`),
  UNIQUE KEY `idxItemName` (`txtDescription`) USING HASH,
  KEY `fkItemSupplier` (`intSupplierID`),
  CONSTRAINT `fkItemSupplier` FOREIGN KEY (`intSupplierID`) REFERENCES `tblsupplier` (`intSupplierID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblitem`
--

LOCK TABLES `tblitem` WRITE;
/*!40000 ALTER TABLE `tblitem` DISABLE KEYS */;
INSERT INTO `tblitem` VALUES
(1,'Soy Wax',10.50,50.00,'kg',5),
(2,'Cotton Wicks',5.75,50.00,'pieces',2),
(3,'Glass Jars',8.25,30.00,'pieces',1),
(4,'Vanilla Fragrance Oil',15.00,300.00,'ml',5),
(5,'Purple Dye',7.50,150.00,'grams',2),
(6,'Decorative Labels',3.25,100.00,'pieces',1),
(7,'Packaging Boxes',12.75,50.00,'pieces',4),
(8,'Safety Labels',2.50,50.00,'pieces',3),
(9,'Packaging Tape',3.00,100.00,'meters',3),
(10,'Coconut Wax',10.50,50.00,'kg',5),
(11,'Lavender Fragrance Oil',15.00,300.00,'ml',5),
(12,'Citrus Fragrance Oil',15.00,300.00,'ml',5),
(13,'Ocean Fragrance Oil',15.00,300.00,'ml',5),
(14,'Yellow Dye',7.50,150.00,'grams',2),
(15,'Color Blue Dye',7.50,150.00,'grams',2);
/*!40000 ALTER TABLE `tblitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblorder`
--

DROP TABLE IF EXISTS `tblorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblorder` (
  `intOrderID` int(11) NOT NULL AUTO_INCREMENT,
  `intCustomerID` int(11) NOT NULL,
  `intShippingID` int(11) NOT NULL,
  `datOrderDate` date NOT NULL,
  `datDateDelivered` date NOT NULL,
  `intPaymentModeID` int(11) NOT NULL,
  PRIMARY KEY (`intOrderID`),
  KEY `fkOrderCustomer` (`intCustomerID`),
  KEY `fkOrderShipping` (`intShippingID`),
  KEY `fkOrderPaymentMode` (`intPaymentModeID`),
  CONSTRAINT `fkOrderCustomer` FOREIGN KEY (`intCustomerID`) REFERENCES `tblcustomer` (`intCustomerID`) ON UPDATE CASCADE,
  CONSTRAINT `fkOrderPaymentMode` FOREIGN KEY (`intPaymentModeID`) REFERENCES `tblpaymentmode` (`intPaymentModeID`) ON UPDATE CASCADE,
  CONSTRAINT `fkOrderShipping` FOREIGN KEY (`intShippingID`) REFERENCES `tblshipping` (`intShippingID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblorder`
--

LOCK TABLES `tblorder` WRITE;
/*!40000 ALTER TABLE `tblorder` DISABLE KEYS */;
INSERT INTO `tblorder` VALUES
(1,1,1,'2024-05-11','2024-05-15',2),
(2,2,2,'2024-06-07','2024-06-10',1),
(3,3,2,'2024-03-02','2024-03-05',1),
(4,4,2,'2024-02-08','2024-02-11',3),
(5,5,1,'2023-12-24','2023-12-28',3),
(6,6,1,'2023-11-28','2023-12-01',4),
(7,7,2,'2024-01-23','2024-01-26',1),
(8,8,2,'2024-02-14','2024-02-17',2);
/*!40000 ALTER TABLE `tblorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblorderproduct`
--

DROP TABLE IF EXISTS `tblorderproduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblorderproduct` (
  `intOrderID` int(11) NOT NULL,
  `intProductID` int(11) NOT NULL,
  `intQuantity` int(11) NOT NULL,
  PRIMARY KEY (`intOrderID`,`intProductID`),
  UNIQUE KEY `idxOrderProduct` (`intOrderID`,`intProductID`),
  KEY `fkProduct` (`intProductID`),
  CONSTRAINT `fkOrder` FOREIGN KEY (`intOrderID`) REFERENCES `tblorder` (`intOrderID`) ON UPDATE CASCADE,
  CONSTRAINT `fkProduct` FOREIGN KEY (`intProductID`) REFERENCES `tblproduct` (`intProductID`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblorderproduct`
--

LOCK TABLES `tblorderproduct` WRITE;
/*!40000 ALTER TABLE `tblorderproduct` DISABLE KEYS */;
INSERT INTO `tblorderproduct` VALUES
(1,1,1),
(1,3,1),
(2,1,2),
(3,4,2),
(4,5,1),
(5,2,2),
(5,3,2),
(6,1,1),
(6,2,1),
(6,3,1),
(7,2,3),
(8,5,2);
/*!40000 ALTER TABLE `tblorderproduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblpaymentmode`
--

DROP TABLE IF EXISTS `tblpaymentmode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblpaymentmode` (
  `intPaymentModeID` int(11) NOT NULL AUTO_INCREMENT,
  `txtDescription` text NOT NULL,
  PRIMARY KEY (`intPaymentModeID`),
  UNIQUE KEY `idxPaymentMode` (`txtDescription`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblpaymentmode`
--

LOCK TABLES `tblpaymentmode` WRITE;
/*!40000 ALTER TABLE `tblpaymentmode` DISABLE KEYS */;
INSERT INTO `tblpaymentmode` VALUES
(1,'Bank'),
(2,'GCash'),
(3,'Cash on Delivery'),
(4,'Maya');
/*!40000 ALTER TABLE `tblpaymentmode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblproduct`
--

DROP TABLE IF EXISTS `tblproduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblproduct` (
  `intProductID` int(11) NOT NULL AUTO_INCREMENT,
  `strName` varchar(255) NOT NULL,
  `txtDescription` text NOT NULL,
  `intQtyPerUnit` int(11) NOT NULL,
  `unitPrice` float(10,2) NOT NULL,
  `boolIsDiscontinued` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`intProductID`),
  UNIQUE KEY `idxProductName` (`strName`,`txtDescription`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblproduct`
--

LOCK TABLES `tblproduct` WRITE;
/*!40000 ALTER TABLE `tblproduct` DISABLE KEYS */;
INSERT INTO `tblproduct` VALUES
(1,'Vanilla Scented Candle','Scented candle with a soothing vanilla aroma.',1,75.00,1),
(2,'Lavender Scented Candle','Relaxing scented candle infused with lavender essence.',1,80.00,1),
(3,'Citrus Burst Scented Candle','Invigorating scented candle with citrus notes.',1,85.00,1),
(4,'Ocean Breeze Scented Candle','Refreshing scented candle inspired by the ocean.',1,75.00,1),
(5,'Summer Package','Summer sale promo package.',2,150.00,1);
/*!40000 ALTER TABLE `tblproduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblproductitem`
--

DROP TABLE IF EXISTS `tblproductitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblproductitem` (
  `intProductID` int(11) NOT NULL,
  `intItemID` int(11) NOT NULL,
  `quantity` float(10,2) NOT NULL,
  `strUnitMeasurement` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`intProductID`,`intItemID`),
  UNIQUE KEY `idxProductItem` (`intProductID`,`intItemID`),
  KEY `fkPIItem` (`intItemID`),
  CONSTRAINT `fkPIItem` FOREIGN KEY (`intItemID`) REFERENCES `tblitem` (`intItemID`) ON UPDATE CASCADE,
  CONSTRAINT `fkPIProduct` FOREIGN KEY (`intProductID`) REFERENCES `tblproduct` (`intProductID`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblproductitem`
--

LOCK TABLES `tblproductitem` WRITE;
/*!40000 ALTER TABLE `tblproductitem` DISABLE KEYS */;
INSERT INTO `tblproductitem` VALUES
(1,1,250.00,'grams'),
(1,2,1.00,'piece'),
(1,3,1.00,'piece'),
(1,4,10.00,'ml'),
(1,6,1.00,'piece'),
(1,7,1.00,'piece'),
(1,8,1.00,'piece'),
(1,9,50.00,'cm'),
(2,1,250.00,'grams'),
(2,2,1.00,'piece'),
(2,3,1.00,'piece'),
(2,5,10.00,'grams'),
(2,6,1.00,'piece'),
(2,7,1.00,'piece'),
(2,8,1.00,'piece'),
(2,9,50.00,'cm'),
(2,11,10.00,'ml'),
(3,1,250.00,'grams'),
(3,2,1.00,'piece'),
(3,3,1.00,'piece'),
(3,6,1.00,'piece'),
(3,7,1.00,'piece'),
(3,8,1.00,'piece'),
(3,9,50.00,'cm'),
(3,12,10.00,'ml'),
(3,14,10.00,'grams'),
(4,2,1.00,'piece'),
(4,3,1.00,'piece'),
(4,6,1.00,'piece'),
(4,7,1.00,'piece'),
(4,8,1.00,'piece'),
(4,9,50.00,'cm'),
(4,10,250.00,'grams'),
(4,13,10.00,'ml'),
(4,15,10.00,'grams'),
(5,1,250.00,'grams'),
(5,2,2.00,'piece'),
(5,3,2.00,'piece'),
(5,6,2.00,'piece'),
(5,7,2.00,'piece'),
(5,8,2.00,'piece'),
(5,9,100.00,'cm'),
(5,10,250.00,'grams'),
(5,12,10.00,'ml'),
(5,13,10.00,'ml'),
(5,14,10.00,'grams'),
(5,15,10.00,'grams');
/*!40000 ALTER TABLE `tblproductitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblshipping`
--

DROP TABLE IF EXISTS `tblshipping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblshipping` (
  `intShippingID` int(11) NOT NULL AUTO_INCREMENT,
  `strCompanyName` varchar(255) NOT NULL,
  `intDropOffID` int(11) NOT NULL,
  PRIMARY KEY (`intShippingID`),
  UNIQUE KEY `idxShippingDropOff` (`strCompanyName`),
  KEY `fkShippingDropOff` (`intDropOffID`),
  CONSTRAINT `fkShippingDropOff` FOREIGN KEY (`intDropOffID`) REFERENCES `tbldropoff` (`intDropOffID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblshipping`
--

LOCK TABLES `tblshipping` WRITE;
/*!40000 ALTER TABLE `tblshipping` DISABLE KEYS */;
INSERT INTO `tblshipping` VALUES
(1,'J&T Express',5),
(2,'LBC Express',13);
/*!40000 ALTER TABLE `tblshipping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblshippingcost`
--

DROP TABLE IF EXISTS `tblshippingcost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblshippingcost` (
  `intShippingCostID` int(11) NOT NULL AUTO_INCREMENT,
  `strCity` varchar(255) NOT NULL,
  `strProvince` varchar(255) NOT NULL,
  `shippingCost` float(10,2) NOT NULL,
  `intShippingID` int(11) NOT NULL,
  PRIMARY KEY (`intShippingCostID`),
  UNIQUE KEY `idxShippingDetails` (`strCity`,`strProvince`,`shippingCost`,`intShippingID`),
  KEY `fkShippingCost` (`intShippingID`),
  CONSTRAINT `fkShippingCost` FOREIGN KEY (`intShippingID`) REFERENCES `tblshipping` (`intShippingID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblshippingcost`
--

LOCK TABLES `tblshippingcost` WRITE;
/*!40000 ALTER TABLE `tblshippingcost` DISABLE KEYS */;
INSERT INTO `tblshippingcost` VALUES
(1,'Bacolod City','Negros Occidental',150.00,2),
(2,'Bacolod City','Negros Occidental',180.00,1),
(3,'Cebu City','Cebu',150.00,2),
(4,'Cebu City','Cebu',180.00,1),
(5,'Manila','Metro Manila',150.00,2),
(6,'Manila','Metro Manila',165.00,1);
/*!40000 ALTER TABLE `tblshippingcost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblsupplier`
--

DROP TABLE IF EXISTS `tblsupplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tblsupplier` (
  `intSupplierID` int(11) NOT NULL AUTO_INCREMENT,
  `strName` varchar(255) NOT NULL,
  `strEmail` varchar(255) NOT NULL,
  `strContactNumber` varchar(45) NOT NULL,
  `strBlockUnit` varchar(255) NOT NULL,
  `strStreet` varchar(255) NOT NULL,
  `strCity` varchar(255) NOT NULL,
  `strProvince` varchar(255) NOT NULL,
  `strCountry` varchar(255) NOT NULL,
  PRIMARY KEY (`intSupplierID`),
  UNIQUE KEY `idxSupplierIdentity` (`strName`,`strEmail`,`strContactNumber`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblsupplier`
--

LOCK TABLES `tblsupplier` WRITE;
/*!40000 ALTER TABLE `tblsupplier` DISABLE KEYS */;
INSERT INTO `tblsupplier` VALUES
(1,'ABC Trading','abc.trading@gmail.com','09257239831','Unit 10','Edsa Avenue','Mandaluyong','Metro Manila','Philippines'),
(2,'JYP Distributor','jyp.distributors@yahoo.com','09187482331','Unit 20','Ortigas Avenue','Pasig City','Metro Manila','Philippines'),
(3,'YG Suppliers','yg.suppliers@gmail.com','09257034891','Block 30','Araneta Avenue','Quezon City','Metro Manila','Philippines'),
(4,'Guo Co.','aliceguo.co@gmail.com','13257239831','Block 13','Nanjing Road','Shanghai','Shanghai Municipality','China'),
(5,'Alice Wax','alice.wax@yahoo.com','15187482331','Unit 7','Baiyun Avenue','Guangzhou','Guangdong','China');
/*!40000 ALTER TABLE `tblsupplier` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-01  0:13:52
