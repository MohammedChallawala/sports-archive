-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: sportsarchive
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `broadcasters`
--

DROP TABLE IF EXISTS `broadcasters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `broadcasters` (
  `Broadcaster_Name` varchar(100) NOT NULL,
  `Location` varchar(100) DEFAULT NULL,
  `Competition_Name` varchar(100) DEFAULT NULL,
  `Platform` varchar(50) DEFAULT NULL,
  `Languages` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Broadcaster_Name`),
  KEY `Competition_Name` (`Competition_Name`),
  CONSTRAINT `broadcasters_ibfk_1` FOREIGN KEY (`Competition_Name`) REFERENCES `competitions` (`Competition_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `broadcasters`
--

LOCK TABLES `broadcasters` WRITE;
/*!40000 ALTER TABLE `broadcasters` DISABLE KEYS */;
INSERT INTO `broadcasters` VALUES ('Al Jazeera Sports','Qatar','Asian Games 2018','Satellite','Arabic'),('BeIN Sports','Middle East','ICC Cricket World Cup 2019','Satellite','Arabic, English'),('DAZN','Germany','Tour de France 2021','Streaming','German'),('ESPN','USA','Summer Olympics 2020','Cable','English, Spanish'),('Eurosport','France','Australian Open 2020','Satellite','English'),('Fox Sports','USA','Stanley Cup 2021','Cable','English'),('NBC Sports','USA','Winter Olympics 2018','Cable','English'),('Sky Sports','UK','UEFA Champions League 2019','Cable','English'),('TSN','Canada','NBA Finals 2021','Cable','French');
/*!40000 ALTER TABLE `broadcasters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `competitions`
--

DROP TABLE IF EXISTS `competitions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `competitions` (
  `Competition_Name` varchar(100) NOT NULL,
  `Location` varchar(100) DEFAULT NULL,
  `Duration` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Competition_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `competitions`
--

LOCK TABLES `competitions` WRITE;
/*!40000 ALTER TABLE `competitions` DISABLE KEYS */;
INSERT INTO `competitions` VALUES ('Asian Games 2018','Jakarta','15 Days'),('Australian Open 2020','Melbourne','14 Days'),('ICC Cricket World Cup 2019','England','50 Days'),('NBA Finals 2021','USA','7 Days'),('Stanley Cup 2021','Canada','60 Days'),('Summer Olympics 2020','Tokyo','30 Days'),('Tour de France 2021','France','23 Days'),('UEFA Champions League 2019','Europe','275 Days'),('Winter Olympics 2018','Pyeongchang','17 Days');
/*!40000 ALTER TABLE `competitions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment`
--

DROP TABLE IF EXISTS `equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment` (
  `Equipment_ID` int NOT NULL,
  `Equipment_Name` varchar(100) NOT NULL,
  `Weight` int DEFAULT NULL,
  `Dimensions` varchar(50) DEFAULT NULL,
  `Sport_ID` int DEFAULT NULL,
  `Supplier_Name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Equipment_ID`),
  KEY `Sport_ID` (`Sport_ID`),
  KEY `Supplier_Name` (`Supplier_Name`),
  CONSTRAINT `equipment_ibfk_1` FOREIGN KEY (`Sport_ID`) REFERENCES `sports_sportinfo` (`Sport_ID`),
  CONSTRAINT `equipment_ibfk_2` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers` (`Supplier_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment`
--

LOCK TABLES `equipment` WRITE;
/*!40000 ALTER TABLE `equipment` DISABLE KEYS */;
INSERT INTO `equipment` VALUES (1,'Javelin',800,'2.6m',1,'Athletics Supplier Co.'),(2,'Shot Put',7200,'12cm',2,'Track Masters Inc.'),(3,'Football',450,'22cm',3,'Football Gear Ltd.'),(4,'Basketball',600,'24cm',4,'Basketball Pro Supplies'),(5,'Tennis Racket',300,'68cm',5,'Tennis World'),(6,'Hockey Stick',800,'95cm',6,'Hockey Equipment Co.'),(7,'Cricket Bat',1200,'85cm',7,'Cricket Equipment Ltd.'),(8,'Table Tennis Paddle',150,'17cm',8,'Ping Pong Supplies'),(9,'Boxing Gloves',250,'30cm',9,'Boxing Gear Pro'),(10,'Archery Bow',1500,'1.5m',10,'Archery Supplies Inc.');
/*!40000 ALTER TABLE `equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organizers`
--

DROP TABLE IF EXISTS `organizers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organizers` (
  `Organizer_Name` varchar(100) NOT NULL,
  `Description` text,
  `Supplier_Name` varchar(100) DEFAULT NULL,
  `Chairman_FN` varchar(50) DEFAULT NULL,
  `Chairman_MN` varchar(50) DEFAULT NULL,
  `Chairman_LN` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Organizer_Name`),
  KEY `Supplier_Name` (`Supplier_Name`),
  CONSTRAINT `organizers_ibfk_1` FOREIGN KEY (`Supplier_Name`) REFERENCES `suppliers` (`Supplier_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organizers`
--

LOCK TABLES `organizers` WRITE;
/*!40000 ALTER TABLE `organizers` DISABLE KEYS */;
INSERT INTO `organizers` VALUES ('Asian Games Committee','Organizes and promotes the Asian Games for athletes across Asia.','Track Masters Inc.','Ahmed','H.','Khan'),('FIFA','Governing body of football (soccer) worldwide.','Football Gear Ltd.','Gianni',NULL,'Infantino'),('International Basketball Federation','Global governing body for basketball events and regulations.','Basketball Pro Supplies','Hamane',NULL,'Niang'),('International Cricket Council','Governing body for international cricket.','Cricket Equipment Ltd.','Shahid','A.','Afridi'),('International Tennis Federation','Governing body for world tennis, setting rules and organizing events.','Tennis World','David','H.','Haggerty'),('NCAA','Organizes college athletics and educational programs.','Track Masters Inc.','Mark','L.','Emmert'),('Olympics Committee','Responsible for organizing the Summer and Winter Olympic Games.','Athletics Supplier Co.','Thomas','A.','Bach'),('UEFA','Governing body for European football.','Football Gear Ltd.','Aleksander',NULL,'Ceferin'),('World Athletics','Governing body for track and field events worldwide.','Athletics Supplier Co.','Sebastian','X.','Coe'),('World Rugby','Responsible for promoting and organizing rugby tournaments globally.','Cricket Equipment Ltd.','Bill',NULL,'Beaumont');
/*!40000 ALTER TABLE `organizers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `organizers_competitions`
--

DROP TABLE IF EXISTS `organizers_competitions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `organizers_competitions` (
  `Organizer_Name` varchar(100) NOT NULL,
  `Competition_Name` varchar(100) NOT NULL,
  PRIMARY KEY (`Organizer_Name`,`Competition_Name`),
  CONSTRAINT `organizers_competitions_ibfk_1` FOREIGN KEY (`Organizer_Name`) REFERENCES `organizers` (`Organizer_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `organizers_competitions`
--

LOCK TABLES `organizers_competitions` WRITE;
/*!40000 ALTER TABLE `organizers_competitions` DISABLE KEYS */;
INSERT INTO `organizers_competitions` VALUES ('Asian Games Committee','Asian Games 2018'),('FIFA','World Cup 2018'),('International Basketball Federation','NBA Finals 2021'),('International Cricket Council','ICC Cricket World Cup 2019'),('International Tennis Federation','Australian Open 2020'),('NCAA','NCAA Championships'),('Olympics Committee','Summer Olympics 2020'),('UEFA','UEFA Champions League 2019'),('World Athletics','Tour de France 2021'),('World Rugby','Rugby World Cup 2019');
/*!40000 ALTER TABLE `organizers_competitions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `players` (
  `Player_ID` int NOT NULL,
  `Age` int NOT NULL,
  `Gender` varchar(10) DEFAULT NULL,
  `First_Name` varchar(50) DEFAULT NULL,
  `Middle_Name` varchar(50) DEFAULT NULL,
  `Last_Name` varchar(50) DEFAULT NULL,
  `Sponsor_Name` varchar(100) DEFAULT NULL,
  `Sport_ID` int DEFAULT NULL,
  PRIMARY KEY (`Player_ID`),
  KEY `Sport_ID` (`Sport_ID`),
  CONSTRAINT `players_ibfk_1` FOREIGN KEY (`Sport_ID`) REFERENCES `sports_sportinfo` (`Sport_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `players`
--

LOCK TABLES `players` WRITE;
/*!40000 ALTER TABLE `players` DISABLE KEYS */;
INSERT INTO `players` VALUES (1,24,'Male','Usain','Bolt','Bolt','Nike',1),(2,29,'Female','Serena',NULL,'Williams','Adidas',5),(3,27,'Male','Lionel',NULL,'Messi','Puma',3),(4,26,'Female','Simone',NULL,'Biles','Under Armour',2),(5,32,'Male','LeBron',NULL,'James','Nike',4),(6,28,'Male','Roger',NULL,'Federer','Wilson',5),(7,30,'Female','Megan',NULL,'Rapinoe','Nike',3),(8,22,'Male','Naomi',NULL,'Osaka','Yonex',5),(9,25,'Female','Katie',NULL,'Ledecky','Speedo',2),(10,31,'Male','Virat',NULL,'Kohli','Puma',6),(11,39,'Male','Cristiano','dos Santos Aveiro','Ronaldo','Nike',3);
/*!40000 ALTER TABLE `players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `records`
--

DROP TABLE IF EXISTS `records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `records` (
  `Player_ID` int NOT NULL,
  `Sport_ID` int NOT NULL,
  `Competition_Name` varchar(100) NOT NULL,
  `Tally` int DEFAULT NULL,
  `Duration` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Player_ID`,`Sport_ID`,`Competition_Name`),
  KEY `Sport_ID` (`Sport_ID`),
  KEY `Competition_Name` (`Competition_Name`),
  CONSTRAINT `records_ibfk_1` FOREIGN KEY (`Player_ID`) REFERENCES `players` (`Player_ID`),
  CONSTRAINT `records_ibfk_2` FOREIGN KEY (`Sport_ID`) REFERENCES `sports_sportinfo` (`Sport_ID`),
  CONSTRAINT `records_ibfk_3` FOREIGN KEY (`Competition_Name`) REFERENCES `competitions` (`Competition_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `records`
--

LOCK TABLES `records` WRITE;
/*!40000 ALTER TABLE `records` DISABLE KEYS */;
INSERT INTO `records` VALUES (1,1,'Summer Olympics 2020',3,'9.58 sec'),(2,5,'Winter Olympics 2018',7,'1 hr 30 min'),(3,3,'UEFA Champions League 2019',10,'120 min'),(4,2,'NBA Finals 2021',5,'10.1 sec'),(5,4,'ICC Cricket World Cup 2019',2,'4.2 sec'),(6,5,'Australian Open 2020',5,'3 hrs 12 min'),(7,3,'Winter Olympics 2018',6,'90 min'),(8,5,'Asian Games 2018',4,'2 hrs 15 min'),(9,2,'Summer Olympics 2020',4,'15.8 sec'),(10,6,'Tour de France 2021',1,'85 hrs 37 min');
/*!40000 ALTER TABLE `records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sponsors`
--

DROP TABLE IF EXISTS `sponsors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sponsors` (
  `Sponsor_Name` varchar(100) NOT NULL,
  `Sport_ID` int DEFAULT NULL,
  PRIMARY KEY (`Sponsor_Name`),
  KEY `Sport_ID` (`Sport_ID`),
  CONSTRAINT `sponsors_ibfk_1` FOREIGN KEY (`Sport_ID`) REFERENCES `sports_sportinfo` (`Sport_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sponsors`
--

LOCK TABLES `sponsors` WRITE;
/*!40000 ALTER TABLE `sponsors` DISABLE KEYS */;
INSERT INTO `sponsors` VALUES ('Coca-Cola',1),('Nike',1),('Adidas',2),('PepsiCo',2),('Puma',3),('Red Bull',3),('Gatorade',4),('Under Armour',4),('Reebok',5),('Visa',5);
/*!40000 ALTER TABLE `sponsors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sponsors_budget`
--

DROP TABLE IF EXISTS `sponsors_budget`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sponsors_budget` (
  `Sponsor_Name` varchar(100) NOT NULL,
  `Budget` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`Sponsor_Name`),
  CONSTRAINT `sponsors_budget_ibfk_1` FOREIGN KEY (`Sponsor_Name`) REFERENCES `sponsors` (`Sponsor_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sponsors_budget`
--

LOCK TABLES `sponsors_budget` WRITE;
/*!40000 ALTER TABLE `sponsors_budget` DISABLE KEYS */;
INSERT INTO `sponsors_budget` VALUES ('Adidas',500000.00),('Coca-Cola',800000.00),('Gatorade',400000.00),('Nike',1000000.00),('PepsiCo',600000.00),('Puma',300000.00),('Red Bull',350000.00),('Reebok',150000.00),('Under Armour',200000.00),('Visa',900000.00);
/*!40000 ALTER TABLE `sponsors_budget` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sponsors_competition`
--

DROP TABLE IF EXISTS `sponsors_competition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sponsors_competition` (
  `Sponsor_Name` varchar(100) NOT NULL,
  `Competition_Name` varchar(100) NOT NULL,
  PRIMARY KEY (`Sponsor_Name`,`Competition_Name`),
  KEY `Competition_Name` (`Competition_Name`),
  CONSTRAINT `sponsors_competition_ibfk_1` FOREIGN KEY (`Sponsor_Name`) REFERENCES `sponsors` (`Sponsor_Name`),
  CONSTRAINT `sponsors_competition_ibfk_2` FOREIGN KEY (`Competition_Name`) REFERENCES `competitions` (`Competition_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sponsors_competition`
--

LOCK TABLES `sponsors_competition` WRITE;
/*!40000 ALTER TABLE `sponsors_competition` DISABLE KEYS */;
INSERT INTO `sponsors_competition` VALUES ('Under Armour','Asian Games 2018'),('Reebok','Australian Open 2020'),('Puma','ICC Cricket World Cup 2019'),('Coca-Cola','Summer Olympics 2020'),('Nike','Summer Olympics 2020'),('Red Bull','Tour de France 2021'),('Visa','UEFA Champions League 2019'),('Adidas','Winter Olympics 2018'),('Gatorade','Winter Olympics 2018');
/*!40000 ALTER TABLE `sponsors_competition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sponsors_player`
--

DROP TABLE IF EXISTS `sponsors_player`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sponsors_player` (
  `Sponsor_Name` varchar(100) NOT NULL,
  `Player_ID` int NOT NULL,
  PRIMARY KEY (`Sponsor_Name`,`Player_ID`),
  KEY `Player_ID` (`Player_ID`),
  CONSTRAINT `sponsors_player_ibfk_1` FOREIGN KEY (`Sponsor_Name`) REFERENCES `sponsors` (`Sponsor_Name`),
  CONSTRAINT `sponsors_player_ibfk_2` FOREIGN KEY (`Player_ID`) REFERENCES `players` (`Player_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sponsors_player`
--

LOCK TABLES `sponsors_player` WRITE;
/*!40000 ALTER TABLE `sponsors_player` DISABLE KEYS */;
INSERT INTO `sponsors_player` VALUES ('Nike',1),('Adidas',2),('Puma',3),('Under Armour',4),('Nike',5),('Coca-Cola',6),('PepsiCo',7),('Red Bull',8),('Gatorade',9),('Visa',10),('Nike',11);
/*!40000 ALTER TABLE `sponsors_player` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sports_sportdetails`
--

DROP TABLE IF EXISTS `sports_sportdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sports_sportdetails` (
  `Sport_Name` varchar(100) NOT NULL,
  `Number_of_Players` int DEFAULT NULL,
  PRIMARY KEY (`Sport_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sports_sportdetails`
--

LOCK TABLES `sports_sportdetails` WRITE;
/*!40000 ALTER TABLE `sports_sportdetails` DISABLE KEYS */;
INSERT INTO `sports_sportdetails` VALUES ('Archery',1),('Basketball',10),('Boxing',2),('Cricket',11),('Football',22),('Hockey',6),('Javelin Throw',1),('Shot Put',1),('Table Tennis',2),('Tennis',2);
/*!40000 ALTER TABLE `sports_sportdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sports_sportinfo`
--

DROP TABLE IF EXISTS `sports_sportinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sports_sportinfo` (
  `Sport_ID` int NOT NULL,
  `Sport_Name` varchar(100) NOT NULL,
  `Weight` int DEFAULT NULL,
  `Age` int DEFAULT NULL,
  `Supplier_ID` int DEFAULT NULL,
  PRIMARY KEY (`Sport_ID`),
  UNIQUE KEY `Sport_Name` (`Sport_Name`),
  KEY `Supplier_ID` (`Supplier_ID`),
  CONSTRAINT `sports_sportinfo_ibfk_1` FOREIGN KEY (`Supplier_ID`) REFERENCES `suppliers` (`Supplier_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sports_sportinfo`
--

LOCK TABLES `sports_sportinfo` WRITE;
/*!40000 ALTER TABLE `sports_sportinfo` DISABLE KEYS */;
INSERT INTO `sports_sportinfo` VALUES (1,'Javelin Throw',800,18,1),(2,'Shot Put',7200,18,2),(3,'Football',450,16,3),(4,'Basketball',600,16,4),(5,'Tennis',300,16,5),(6,'Hockey',800,16,6),(7,'Cricket',1200,16,7),(8,'Table Tennis',150,12,8),(9,'Boxing',250,18,9),(10,'Archery',1500,18,10);
/*!40000 ALTER TABLE `sports_sportinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliers` (
  `Supplier_ID` int NOT NULL,
  `Supplier_Name` varchar(100) NOT NULL,
  `Contact_Info` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Supplier_ID`),
  UNIQUE KEY `Supplier_Name` (`Supplier_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
INSERT INTO `suppliers` VALUES (1,'Athletics Supplier Co.','contact@athleticssupplier.com'),(2,'Track Masters Inc.','info@trackmasters.com'),(3,'Football Gear Ltd.','sales@footballgear.com'),(4,'Basketball Pro Supplies','support@basketballpros.com'),(5,'Tennis World','contact@tennisworld.com'),(6,'Hockey Equipment Co.','info@hockeyequipment.com'),(7,'Cricket Equipment Ltd.','sales@cricketequipment.com'),(8,'Ping Pong Supplies','support@pingpongsupplies.com'),(9,'Boxing Gear Pro','info@boxinggearpro.com'),(10,'Archery Supplies Inc.','sales@archerysupplies.com');
/*!40000 ALTER TABLE `suppliers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(64) NOT NULL,
  `role` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9','admin'),(2,'test','ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae','viewer');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-27 10:41:31
