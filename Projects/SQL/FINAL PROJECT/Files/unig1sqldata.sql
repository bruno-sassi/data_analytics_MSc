CREATE DATABASE  IF NOT EXISTS `university` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `university`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: university
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `addresses`
--

DROP TABLE IF EXISTS `addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addresses` (
  `address_id` int NOT NULL AUTO_INCREMENT,
  `street` varchar(100) NOT NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `zip_code` varchar(20) NOT NULL,
  `country` varchar(50) NOT NULL,
  PRIMARY KEY (`address_id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses`
--

LOCK TABLES `addresses` WRITE;
/*!40000 ALTER TABLE `addresses` DISABLE KEYS */;
INSERT INTO `addresses` VALUES (1,'123 Main St','New York','NY','10001','USA'),(2,'456 Elm St','Los Angeles','CA','90001','USA'),(3,'789 Oak St','Chicago','IL','60601','USA'),(4,'101 Pine St','Houston','TX','77001','USA'),(5,'202 Maple St','Phoenix','AZ','85001','USA'),(6,'303 Birch St','Philadelphia','PA','19019','USA'),(7,'404 Cedar St','San Antonio','TX','78201','USA'),(8,'505 Walnut St','San Diego','CA','92101','USA'),(9,'606 Cherry St','Dallas','TX','75201','USA'),(10,'707 Spruce St','San Jose','CA','95101','USA'),(11,'808 Palm St','Austin','TX','73301','USA'),(12,'909 Willow St','Jacksonville','FL','32099','USA'),(13,'1010 Ash St','San Francisco','CA','94101','USA'),(14,'1111 Birch St','Indianapolis','IN','46201','USA'),(15,'1212 Cedar St','Columbus','OH','43085','USA'),(16,'1313 Elm St','Fort Worth','TX','76101','USA'),(17,'1414 Oak St','Charlotte','NC','28201','USA'),(18,'1515 Pine St','Seattle','WA','98101','USA'),(19,'1616 Maple St','Denver','CO','80201','USA'),(20,'1717 Walnut St','Washington','DC','20001','USA'),(21,'1818 Cedar St','Boston','MA','02101','USA'),(22,'1919 Birch St','El Paso','TX','79901','USA'),(23,'2020 Palm St','Detroit','MI','48201','USA'),(24,'2121 Willow St','Nashville','TN','37201','USA'),(25,'2222 Ash St','Memphis','TN','37501','USA'),(26,'2323 Oak St','Louisville','KY','40201','USA'),(27,'2424 Pine St','Baltimore','MD','21201','USA'),(28,'2525 Maple St','Milwaukee','WI','53201','USA'),(29,'2626 Elm St','Portland','OR','97201','USA'),(30,'2727 Cedar St','Las Vegas','NV','89101','USA'),(31,'2828 Birch St','Oklahoma City','OK','73101','USA'),(32,'2929 Walnut St','Albuquerque','NM','87101','USA'),(33,'3030 Cherry St','Tucson','AZ','85701','USA'),(34,'3131 Spruce St','Fresno','CA','93701','USA'),(35,'3232 Palm St','Sacramento','CA','94203','USA'),(36,'3333 Willow St','Kansas City','MO','64101','USA'),(37,'3434 Ash St','Mesa','AZ','85201','USA'),(38,'3535 Oak St','Atlanta','GA','30301','USA'),(39,'3636 Pine St','Colorado Springs','CO','80901','USA'),(40,'3737 Maple St','Raleigh','NC','27601','USA'),(41,'6868 Oak St','Lubbock','TX','79401','USA'),(42,'6969 Pine St','Chandler','AZ','85224','USA'),(43,'7070 Maple St','Scottsdale','AZ','85251','USA'),(44,'7171 Cedar St','Reno','NV','89501','USA'),(45,'7272 Birch St','Laredo','TX','78040','USA'),(46,'7373 Walnut St','Garland','TX','75040','USA'),(47,'7474 Cherry St','Glendale','AZ','85301','USA'),(48,'7575 Spruce St','Hialeah','FL','33010','USA'),(49,'7676 Palm St','Norfolk','VA','23501','USA'),(50,'7777 Willow St','Fremont','CA','94536','USA'),(51,'7878 Ash St','Boise','ID','83701','USA'),(52,'7979 Oak St','Richmond','VA','23219','USA'),(53,'8080 Pine St','Spokane','WA','99201','USA'),(54,'8181 Maple St','Baton Rouge','LA','70801','USA'),(55,'8282 Cedar St','Tacoma','WA','98401','USA'),(56,'8383 Birch St','Des Moines','IA','50301','USA'),(57,'8484 Walnut St','San Bernardino','CA','92401','USA'),(58,'8585 Cherry St','Modesto','CA','95350','USA'),(59,'8686 Spruce St','Fontana','CA','92335','USA'),(60,'8787 Palm St','Santa Clarita','CA','91350','USA'),(61,'8888 Willow St','Birmingham','AL','35203','USA'),(62,'8989 Ash St','Oxnard','CA','93030','USA'),(63,'9090 Oak St','Fayetteville','NC','28301','USA'),(64,'9191 Pine St','Moreno Valley','CA','92551','USA'),(65,'9292 Maple St','Rochester','NY','14602','USA'),(66,'9393 Cedar St','Glendale','CA','91201','USA'),(67,'9494 Birch St','Yonkers','NY','10701','USA'),(68,'9595 Walnut St','Huntington Beach','CA','92646','USA'),(69,'9696 Cherry St','Aurora','IL','60505','USA'),(70,'9797 Spruce St','Montgomery','AL','36104','USA');
/*!40000 ALTER TABLE `addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_semesters`
--

DROP TABLE IF EXISTS `course_semesters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_semesters` (
  `course_semester_id` int NOT NULL AUTO_INCREMENT,
  `course_id` int DEFAULT NULL,
  `semester_id` int DEFAULT NULL,
  PRIMARY KEY (`course_semester_id`),
  KEY `course_id` (`course_id`),
  KEY `semester_id` (`semester_id`),
  CONSTRAINT `course_semesters_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`),
  CONSTRAINT `course_semesters_ibfk_2` FOREIGN KEY (`semester_id`) REFERENCES `semesters` (`semester_id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_semesters`
--

LOCK TABLES `course_semesters` WRITE;
/*!40000 ALTER TABLE `course_semesters` DISABLE KEYS */;
INSERT INTO `course_semesters` VALUES (1,1,1),(2,2,1),(3,3,1),(4,4,1),(5,5,1),(6,6,1),(7,7,1),(8,8,1),(9,9,1),(10,10,1),(11,11,2),(12,12,2),(13,13,2),(14,14,2),(15,15,2),(16,16,2),(17,17,2),(18,18,2),(19,19,2),(20,20,2),(21,21,3),(22,22,3),(23,23,3),(24,24,3),(25,25,3),(26,26,3),(27,27,3),(28,28,3),(29,29,3),(30,30,3),(31,31,4),(32,32,4),(33,33,4),(34,34,4),(35,35,4),(36,36,4),(37,37,4),(38,38,4),(39,39,4),(40,40,4),(41,41,5),(42,42,5),(43,43,5),(44,44,5),(45,45,5),(46,46,5),(47,47,5),(48,48,5),(49,49,5),(50,50,5),(51,1,6),(52,2,6),(53,3,6),(54,4,6),(55,5,6),(56,6,6),(57,7,6),(58,8,6),(59,9,6),(60,10,6),(61,11,7),(62,12,7),(63,13,7),(64,14,7),(65,15,7),(66,16,7),(67,17,7),(68,18,7),(69,19,7),(70,20,7),(71,21,8),(72,22,8),(73,23,8),(74,24,8),(75,25,8),(76,26,8),(77,27,8),(78,28,8),(79,29,8),(80,30,8),(81,31,9),(82,32,9),(83,33,9),(84,34,9),(85,35,9),(86,36,9),(87,37,9),(88,38,9),(89,39,9),(90,40,9),(91,41,10),(92,42,10),(93,43,10),(94,44,10),(95,45,10),(96,46,10),(97,47,10),(98,48,10),(99,49,10),(100,50,10);
/*!40000 ALTER TABLE `course_semesters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `course_id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(100) NOT NULL,
  `department_id` int DEFAULT NULL,
  `instructor_id` int DEFAULT NULL,
  `credits` int DEFAULT NULL,
  PRIMARY KEY (`course_id`),
  KEY `department_id` (`department_id`),
  KEY `instructor_id` (`instructor_id`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`),
  CONSTRAINT `courses_ibfk_2` FOREIGN KEY (`instructor_id`) REFERENCES `instructors` (`instructor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (1,'Introduction to Programming',1,1,3),(2,'Calculus I',2,2,4),(3,'Classical Mechanics',3,3,3),(4,'World History',4,4,3),(5,'English Literature',5,5,3),(6,'Organic Chemistry',6,6,4),(7,'Cell Biology',7,7,3),(8,'Microeconomics',8,8,3),(9,'Cognitive Psychology',9,9,3),(10,'Sociology of Culture',10,10,3),(11,'Data Structures',1,11,4),(12,'Linear Algebra',2,12,4),(13,'Quantum Mechanics',3,13,4),(14,'Ancient Civilizations',4,14,3),(15,'Creative Writing',5,15,3),(16,'Inorganic Chemistry',6,16,4),(17,'Genetics',7,17,4),(18,'Macroeconomics',8,18,3),(19,'Developmental Psychology',9,19,3),(20,'Social Theory',10,20,3),(21,'Algorithms',1,1,4),(22,'Differential Equations',2,2,4),(23,'Thermodynamics',3,3,4),(24,'Modern History',4,4,3),(25,'Shakespeare Studies',5,5,3),(26,'Analytical Chemistry',6,6,4),(27,'Ecology',7,7,3),(28,'International Trade',8,8,3),(29,'Abnormal Psychology',9,9,3),(30,'Urban Sociology',10,10,3),(31,'Database Systems',1,11,4),(32,'Probability Theory',2,12,4),(33,'Electromagnetism',3,13,4),(34,'European History',4,14,3),(35,'Poetry Workshop',5,15,3),(36,'Physical Chemistry',6,16,4),(37,'Microbiology',7,17,4),(38,'Public Finance',8,18,3),(39,'Social Psychology',9,19,3),(40,'Gender Studies',10,20,3),(41,'Operating Systems',1,1,4),(42,'Numerical Analysis',2,2,4),(43,'Astrophysics',3,3,4),(44,'American History',4,4,3),(45,'Fiction Writing',5,5,3),(46,'Biochemistry',6,6,4),(47,'Evolutionary Biology',7,7,4),(48,'Econometrics',8,8,4),(49,'Clinical Psychology',9,9,3),(50,'Criminology',10,10,3);
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `department_id` int NOT NULL AUTO_INCREMENT,
  `department_name` varchar(100) NOT NULL,
  PRIMARY KEY (`department_id`),
  UNIQUE KEY `department_name` (`department_name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (7,'Biology'),(6,'Chemistry'),(1,'Computer Science'),(8,'Economics'),(5,'English'),(4,'History'),(2,'Mathematics'),(3,'Physics'),(9,'Psychology'),(10,'Sociology');
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrollments`
--

DROP TABLE IF EXISTS `enrollments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enrollments` (
  `enrollment_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `course_id` int DEFAULT NULL,
  `enrollment_date` date NOT NULL,
  PRIMARY KEY (`enrollment_id`),
  KEY `student_id` (`student_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `enrollments_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  CONSTRAINT `enrollments_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrollments`
--

LOCK TABLES `enrollments` WRITE;
/*!40000 ALTER TABLE `enrollments` DISABLE KEYS */;
INSERT INTO `enrollments` VALUES (1,1,1,'2023-08-25'),(2,2,2,'2023-08-26'),(3,3,3,'2023-08-27'),(4,4,4,'2023-08-28'),(5,5,5,'2023-08-29'),(6,6,6,'2023-08-30'),(7,7,7,'2023-08-31'),(8,8,8,'2023-09-01'),(9,9,9,'2023-09-02'),(10,10,10,'2023-09-03'),(11,11,11,'2023-09-04'),(12,12,12,'2023-09-05'),(13,13,13,'2023-09-06'),(14,14,14,'2023-09-07'),(15,15,15,'2023-09-08'),(16,16,16,'2023-09-09'),(17,17,17,'2023-09-10'),(18,18,18,'2023-09-11'),(19,19,19,'2023-09-12'),(20,20,20,'2023-09-13'),(21,21,21,'2024-01-15'),(22,22,22,'2024-01-16'),(23,23,23,'2024-01-17'),(24,24,24,'2024-01-18'),(25,25,25,'2024-01-19'),(26,26,26,'2024-01-20'),(27,27,27,'2024-01-21'),(28,28,28,'2024-01-22'),(29,29,29,'2024-01-23'),(30,30,30,'2024-01-24'),(31,31,31,'2024-01-25'),(32,32,32,'2024-01-26'),(33,33,33,'2024-01-27'),(34,34,34,'2024-01-28'),(35,35,35,'2024-01-29'),(36,36,36,'2024-01-30'),(37,37,37,'2024-01-31'),(38,38,38,'2024-02-01'),(39,39,39,'2024-02-02'),(40,40,40,'2024-02-03'),(41,41,41,'2024-02-04'),(42,42,42,'2024-02-05'),(43,43,43,'2024-02-06'),(44,44,44,'2024-02-07'),(45,45,45,'2024-02-08'),(46,46,46,'2024-02-09'),(47,47,47,'2024-02-10'),(48,48,48,'2024-02-11'),(49,49,49,'2024-02-12'),(50,50,50,'2024-02-13'),(51,51,1,'2023-08-25'),(52,52,2,'2023-08-26'),(53,53,3,'2023-08-27'),(54,54,4,'2023-08-28'),(55,55,5,'2023-08-29'),(56,56,6,'2023-08-30'),(57,57,7,'2023-08-31'),(58,58,8,'2023-09-01'),(59,59,9,'2023-09-02'),(60,60,10,'2023-09-03'),(61,61,11,'2023-09-04'),(62,62,12,'2023-09-05'),(63,63,13,'2023-09-06'),(64,64,14,'2023-09-07'),(65,65,15,'2023-09-08'),(66,66,16,'2023-09-09'),(67,67,17,'2023-09-10'),(68,68,18,'2023-09-11'),(69,69,19,'2023-09-12'),(70,70,20,'2023-09-13');
/*!40000 ALTER TABLE `enrollments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grades`
--

DROP TABLE IF EXISTS `grades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grades` (
  `grade_id` int NOT NULL AUTO_INCREMENT,
  `enrollment_id` int DEFAULT NULL,
  `grade` char(1) DEFAULT NULL,
  PRIMARY KEY (`grade_id`),
  UNIQUE KEY `enrollment_id` (`enrollment_id`),
  CONSTRAINT `grades_ibfk_1` FOREIGN KEY (`enrollment_id`) REFERENCES `enrollments` (`enrollment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grades`
--

LOCK TABLES `grades` WRITE;
/*!40000 ALTER TABLE `grades` DISABLE KEYS */;
INSERT INTO `grades` VALUES (1,1,'A'),(2,2,'B'),(3,3,'A'),(4,4,'C'),(5,5,'B'),(6,6,'A'),(7,7,'B'),(8,8,'C'),(9,9,'A'),(10,10,'B'),(11,11,'A'),(12,12,'C'),(13,13,'A'),(14,14,'B'),(15,15,'A'),(16,16,'C'),(17,17,'A'),(18,18,'B'),(19,19,'A'),(20,20,'C'),(21,21,'A'),(22,22,'B'),(23,23,'A'),(24,24,'C'),(25,25,'A'),(26,26,'B'),(27,27,'A'),(28,28,'C'),(29,29,'A'),(30,30,'B'),(31,31,'A'),(32,32,'C'),(33,33,'A'),(34,34,'B'),(35,35,'A'),(36,36,'C'),(37,37,'A'),(38,38,'B'),(39,39,'A'),(40,40,'C'),(41,41,'A'),(42,42,'B'),(43,43,'A'),(44,44,'C'),(45,45,'A'),(46,46,'B'),(47,47,'A'),(48,48,'C'),(49,49,'A'),(50,50,'B'),(51,51,'A'),(52,52,'B'),(53,53,'A'),(54,54,'C'),(55,55,'B'),(56,56,'A'),(57,57,'B'),(58,58,'C'),(59,59,'A'),(60,60,'B'),(61,61,'A'),(62,62,'C'),(63,63,'A'),(64,64,'B'),(65,65,'A'),(66,66,'C'),(67,67,'A'),(68,68,'B'),(69,69,'A'),(70,70,'C');
/*!40000 ALTER TABLE `grades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instructors`
--

DROP TABLE IF EXISTS `instructors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instructors` (
  `instructor_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `department_id` int DEFAULT NULL,
  `address_id` int DEFAULT NULL,
  PRIMARY KEY (`instructor_id`),
  UNIQUE KEY `email` (`email`),
  KEY `department_id` (`department_id`),
  KEY `address_id` (`address_id`),
  CONSTRAINT `instructors_ibfk_1` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`),
  CONSTRAINT `instructors_ibfk_2` FOREIGN KEY (`address_id`) REFERENCES `addresses` (`address_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instructors`
--

LOCK TABLES `instructors` WRITE;
/*!40000 ALTER TABLE `instructors` DISABLE KEYS */;
INSERT INTO `instructors` VALUES (1,'Michael','Scott','michael.scott@example.com',1,1),(2,'Sarah','Connor','sarah.connor@example.com',2,2),(3,'David','Smith','david.smith@example.com',3,3),(4,'Laura','Brown','laura.brown@example.com',4,4),(5,'Kevin','Johnson','kevin.johnson@example.com',5,5),(6,'Emily','Davis','emily.davis@example.com',6,6),(7,'James','Wilson','james.wilson@example.com',7,7),(8,'Olivia','Martinez','olivia.martinez@example.com',8,8),(9,'Daniel','Anderson','daniel.anderson@example.com',9,9),(10,'Sophia','Thomas','sophia.thomas@example.com',10,10),(11,'William','Taylor','william.taylor@example.com',1,11),(12,'Ava','Moore','ava.moore@example.com',2,12),(13,'Ethan','Jackson','ethan.jackson@example.com',3,13),(14,'Mia','White','mia.white@example.com',4,14),(15,'Alexander','Harris','alexander.harris@example.com',5,15),(16,'Charlotte','Clark','charlotte.clark@example.com',6,16),(17,'Benjamin','Lewis','benjamin.lewis@example.com',7,17),(18,'Amelia','Young','amelia.young@example.com',8,18),(19,'Lucas','Hall','lucas.hall@example.com',9,19),(20,'Harper','Allen','harper.allen@example.com',10,20);
/*!40000 ALTER TABLE `instructors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prerequisites`
--

DROP TABLE IF EXISTS `prerequisites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prerequisites` (
  `prerequisite_id` int NOT NULL AUTO_INCREMENT,
  `course_id` int DEFAULT NULL,
  `prerequisite_course_id` int DEFAULT NULL,
  PRIMARY KEY (`prerequisite_id`),
  KEY `course_id` (`course_id`),
  KEY `prerequisite_course_id` (`prerequisite_course_id`),
  CONSTRAINT `prerequisites_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`),
  CONSTRAINT `prerequisites_ibfk_2` FOREIGN KEY (`prerequisite_course_id`) REFERENCES `courses` (`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prerequisites`
--

LOCK TABLES `prerequisites` WRITE;
/*!40000 ALTER TABLE `prerequisites` DISABLE KEYS */;
INSERT INTO `prerequisites` VALUES (1,2,1),(2,3,2),(3,6,2),(4,7,6),(5,11,1),(6,12,2),(7,13,3),(8,16,6),(9,17,7),(10,18,8),(11,21,11),(12,22,12),(13,23,3),(14,26,16),(15,27,7),(16,28,8),(17,31,11),(18,32,12),(19,33,13),(20,36,16),(21,37,7),(22,38,18),(23,41,21),(24,42,22),(25,43,13),(26,46,26),(27,47,17),(28,48,32);
/*!40000 ALTER TABLE `prerequisites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semesters`
--

DROP TABLE IF EXISTS `semesters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `semesters` (
  `semester_id` int NOT NULL AUTO_INCREMENT,
  `semester_name` varchar(50) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  PRIMARY KEY (`semester_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `semesters`
--

LOCK TABLES `semesters` WRITE;
/*!40000 ALTER TABLE `semesters` DISABLE KEYS */;
INSERT INTO `semesters` VALUES (1,'Fall 2023','2023-09-01','2023-12-15'),(2,'Spring 2024','2024-01-15','2024-05-15'),(3,'Summer 2024','2024-06-01','2024-08-15'),(4,'Fall 2024','2024-09-01','2024-12-15'),(5,'Spring 2025','2025-01-15','2025-05-15'),(6,'Summer 2025','2025-06-01','2025-08-15'),(7,'Fall 2025','2025-09-01','2025-12-15'),(8,'Spring 2026','2026-01-15','2026-05-15'),(9,'Summer 2026','2026-06-01','2026-08-15'),(10,'Fall 2026','2026-09-01','2026-12-15');
/*!40000 ALTER TABLE `semesters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `student_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `date_of_birth` date NOT NULL,
  `address_id` int DEFAULT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `email` (`email`),
  KEY `address_id` (`address_id`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`address_id`) REFERENCES `addresses` (`address_id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'John','Doe','john.doe@example.com','2000-05-15',1),(2,'Jane','Smith','jane.smith@example.com','2001-08-22',2),(3,'Alice','Johnson','alice.johnson@example.com','1999-12-30',3),(4,'Bob','Brown','bob.brown@example.com','2000-03-10',4),(5,'Charlie','Davis','charlie.davis@example.com','2001-07-05',5),(6,'David','Wilson','david.wilson@example.com','2000-09-12',6),(7,'Eva','Martinez','eva.martinez@example.com','2001-02-18',7),(8,'Frank','Anderson','frank.anderson@example.com','1999-11-25',8),(9,'Grace','Thomas','grace.thomas@example.com','2000-04-30',9),(10,'Henry','Taylor','henry.taylor@example.com','2001-06-14',10),(11,'Ivy','Moore','ivy.moore@example.com','2000-10-05',11),(12,'Jack','Jackson','jack.jackson@example.com','2001-01-20',12),(13,'Karen','White','karen.white@example.com','1999-07-15',13),(14,'Leo','Harris','leo.harris@example.com','2000-12-01',14),(15,'Mia','Clark','mia.clark@example.com','2001-03-25',15),(16,'Noah','Lewis','noah.lewis@example.com','2000-06-10',16),(17,'Olivia','Young','olivia.young@example.com','2001-09-05',17),(18,'Peter','Hall','peter.hall@example.com','1999-04-12',18),(19,'Quinn','Allen','quinn.allen@example.com','2000-08-20',19),(20,'Rachel','King','rachel.king@example.com','2001-11-15',20),(21,'Sam','Wright','sam.wright@example.com','2000-02-28',1),(22,'Tina','Scott','tina.scott@example.com','2001-05-10',2),(23,'Uma','Green','uma.green@example.com','1999-10-22',3),(24,'Victor','Adams','victor.adams@example.com','2000-01-15',4),(25,'Wendy','Baker','wendy.baker@example.com','2001-04-30',5),(26,'Xander','Gonzalez','xander.gonzalez@example.com','2000-07-12',6),(27,'Yara','Nelson','yara.nelson@example.com','2001-10-05',7),(28,'Zack','Carter','zack.carter@example.com','1999-03-18',8),(29,'Amy','Perez','amy.perez@example.com','2000-06-22',9),(30,'Ben','Roberts','ben.roberts@example.com','2001-09-15',10),(31,'Cara','Turner','cara.turner@example.com','2000-12-10',11),(32,'Duke','Phillips','duke.phillips@example.com','2001-02-25',12),(33,'Eve','Campbell','eve.campbell@example.com','1999-05-30',13),(34,'Finn','Parker','finn.parker@example.com','2000-08-15',14),(35,'Gina','Evans','gina.evans@example.com','2001-11-10',15),(36,'Hank','Edwards','hank.edwards@example.com','2000-03-05',16),(37,'Iris','Collins','iris.collins@example.com','2001-06-20',17),(38,'Jake','Stewart','jake.stewart@example.com','1999-09-12',18),(39,'Kara','Sanchez','kara.sanchez@example.com','2000-12-25',19),(40,'Liam','Morris','liam.morris@example.com','2001-04-10',20),(41,'Maya','Rivera','maya.rivera@example.com','2000-07-15',1),(42,'Nate','Cook','nate.cook@example.com','2001-10-20',2),(43,'Olive','Morgan','olive.morgan@example.com','1999-01-25',3),(44,'Paul','Bell','paul.bell@example.com','2000-04-30',4),(45,'Quincy','Murphy','quincy.murphy@example.com','2001-07-05',5),(46,'Riley','Bailey','riley.bailey@example.com','2000-10-10',6),(47,'Sadie','Cooper','sadie.cooper@example.com','2001-01-15',7),(48,'Theo','Richardson','theo.richardson@example.com','1999-04-20',8),(49,'Uma','Howard','uma.howard@example.com','2000-07-25',9),(50,'Violet','Ward','violet.ward@example.com','2001-10-30',10),(51,'Wyatt','Torres','wyatt.torres@example.com','2000-02-05',11),(52,'Xena','Peterson','xena.peterson@example.com','2001-05-10',12),(53,'Yosef','Gray','yosef.gray@example.com','1999-08-15',13),(54,'Zara','Ramirez','zara.ramirez@example.com','2000-11-20',14),(55,'Aaron','James','aaron.james@example.com','2001-02-25',15),(56,'Bella','Watson','bella.watson@example.com','2000-05-30',16),(57,'Caleb','Brooks','caleb.brooks@example.com','2001-08-05',17),(58,'Daisy','Kelly','daisy.kelly@example.com','1999-11-10',18),(59,'Eli','Sanders','eli.sanders@example.com','2000-02-15',19),(60,'Fiona','Price','fiona.price@example.com','2001-05-20',20),(61,'Gavin','Bennett','gavin.bennett@example.com','2000-08-25',1),(62,'Hazel','Wood','hazel.wood@example.com','2001-11-30',2),(63,'Ivan','Barnes','ivan.barnes@example.com','1999-03-05',3),(64,'Jade','Ross','jade.ross@example.com','2000-06-10',4),(65,'Kai','Henderson','kai.henderson@example.com','2001-09-15',5),(66,'Luna','Coleman','luna.coleman@example.com','2000-12-20',6),(67,'Milo','Jenkins','milo.jenkins@example.com','2001-03-25',7),(68,'Nora','Perry','nora.perry@example.com','1999-06-30',8),(69,'Owen','Powell','owen.powell@example.com','2000-10-05',9),(70,'Penny','Long','penny.long@example.com','2001-01-10',10);
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-24  4:04:49
