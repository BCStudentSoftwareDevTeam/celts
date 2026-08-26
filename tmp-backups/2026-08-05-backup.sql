-- MySQL dump 10.13  Distrib 8.4.8, for macos15.7 (arm64)
--
-- Host: localhost    Database: celts
-- ------------------------------------------------------
-- Server version	8.4.8

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activitylog`
--

DROP TABLE IF EXISTS `activitylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activitylog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `createdBy_id` varchar(255) NOT NULL,
  `createdOn` datetime NOT NULL,
  `logContent` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `activitylog_createdBy_id` (`createdBy_id`),
  CONSTRAINT `activitylog_ibfk_1` FOREIGN KEY (`createdBy_id`) REFERENCES `user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activitylog`
--

LOCK TABLES `activitylog` WRITE;
/*!40000 ALTER TABLE `activitylog` DISABLE KEYS */;
INSERT INTO `activitylog` VALUES (1,'ramsayb2','2021-12-15 00:00:00','Made Liberty Admin.'),(2,'neillz','2021-12-15 00:00:00','Created Adoption Event.');
/*!40000 ALTER TABLE `activitylog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attachmentupload`
--

DROP TABLE IF EXISTS `attachmentupload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attachmentupload` (
  `id` int NOT NULL AUTO_INCREMENT,
  `event_id` int DEFAULT NULL,
  `course_id` int DEFAULT NULL,
  `program_id` int DEFAULT NULL,
  `proposal_id` int DEFAULT NULL,
  `isDisplayed` tinyint(1) NOT NULL,
  `fileName` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `attachmentupload_event_id` (`event_id`),
  KEY `attachmentupload_course_id` (`course_id`),
  KEY `attachmentupload_program_id` (`program_id`),
  KEY `attachmentupload_proposal_id` (`proposal_id`),
  CONSTRAINT `attachmentupload_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`),
  CONSTRAINT `attachmentupload_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`),
  CONSTRAINT `attachmentupload_ibfk_3` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`),
  CONSTRAINT `attachmentupload_ibfk_4` FOREIGN KEY (`proposal_id`) REFERENCES `cceminorproposal` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attachmentupload`
--

LOCK TABLES `attachmentupload` WRITE;
/*!40000 ALTER TABLE `attachmentupload` DISABLE KEYS */;
INSERT INTO `attachmentupload` VALUES (1,1,NULL,NULL,NULL,0,'Map1.pdf'),(2,2,NULL,NULL,NULL,0,'adfsfdhqwre_;ldgfk####l;kgfdg.jpg'),(3,NULL,NULL,1,NULL,0,'1.jpg'),(4,NULL,NULL,2,NULL,0,'2.jpg'),(5,NULL,NULL,3,NULL,0,'3.jpg'),(6,NULL,NULL,4,NULL,0,'4.jpeg'),(7,NULL,NULL,5,NULL,0,'5.jpg'),(8,NULL,NULL,6,NULL,0,'6.jpg'),(9,NULL,NULL,7,NULL,0,'7.jpeg'),(10,NULL,NULL,8,NULL,0,'8.jpeg'),(11,NULL,NULL,10,NULL,0,'10.jpg');
/*!40000 ALTER TABLE `attachmentupload` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backgroundcheck`
--

DROP TABLE IF EXISTS `backgroundcheck`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `backgroundcheck` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL,
  `type_id` varchar(255) NOT NULL,
  `backgroundCheckStatus` varchar(255) NOT NULL,
  `dateCompleted` date DEFAULT NULL,
  `deletionDate` datetime DEFAULT NULL,
  `deletedBy` text,
  PRIMARY KEY (`id`),
  KEY `backgroundcheck_user_id` (`user_id`),
  KEY `backgroundcheck_type_id` (`type_id`),
  CONSTRAINT `backgroundcheck_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`),
  CONSTRAINT `backgroundcheck_ibfk_2` FOREIGN KEY (`type_id`) REFERENCES `backgroundchecktype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backgroundcheck`
--

LOCK TABLES `backgroundcheck` WRITE;
/*!40000 ALTER TABLE `backgroundcheck` DISABLE KEYS */;
INSERT INTO `backgroundcheck` VALUES (1,'khatts','CAN','Passed','2021-10-12',NULL,NULL),(2,'mupotsal','SHS','Submitted','2021-10-12',NULL,NULL);
/*!40000 ALTER TABLE `backgroundcheck` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backgroundchecktype`
--

DROP TABLE IF EXISTS `backgroundchecktype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `backgroundchecktype` (
  `id` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backgroundchecktype`
--

LOCK TABLES `backgroundchecktype` WRITE;
/*!40000 ALTER TABLE `backgroundchecktype` DISABLE KEYS */;
INSERT INTO `backgroundchecktype` VALUES ('BSL','Berea Student Life Background Check'),('CAN','Child Abuse and Neglect Background Check'),('DDC','Defensive Driving Certification'),('FBI','Federal Criminal Background Check'),('SHS','Safe Hiring Solutions');
/*!40000 ALTER TABLE `backgroundchecktype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bonnercohort`
--

DROP TABLE IF EXISTS `bonnercohort`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bonnercohort` (
  `id` int NOT NULL AUTO_INCREMENT,
  `year` int NOT NULL,
  `user_id` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `bonnercohort_year_user_id` (`year`,`user_id`),
  KEY `bonnercohort_user_id` (`user_id`),
  CONSTRAINT `bonnercohort_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bonnercohort`
--

LOCK TABLES `bonnercohort` WRITE;
/*!40000 ALTER TABLE `bonnercohort` DISABLE KEYS */;
INSERT INTO `bonnercohort` VALUES (1,2020,'neillz'),(2,2020,'ramsayb2'),(5,2021,'mupotsal'),(6,2021,'neillz'),(3,2021,'qasema'),(7,2021,'ramsayb2'),(9,2022,'ayisie'),(14,2022,'hoerstl'),(8,2022,'khatts'),(12,2022,'makindeo'),(13,2022,'michels'),(10,2022,'neillz'),(11,2022,'ramsayb2');
/*!40000 ALTER TABLE `bonnercohort` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cceminorproposal`
--

DROP TABLE IF EXISTS `cceminorproposal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cceminorproposal` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` varchar(255) NOT NULL,
  `term_id` int NOT NULL,
  `proposalType` varchar(255) NOT NULL,
  `experienceName` varchar(255) DEFAULT NULL,
  `experienceType` varchar(255) DEFAULT NULL,
  `contentAreas` text,
  `experienceDescription` varchar(255) DEFAULT NULL,
  `roleDescription` varchar(255) DEFAULT NULL,
  `orgName` varchar(255) NOT NULL,
  `orgAddress` varchar(255) NOT NULL,
  `orgPhone` varchar(255) NOT NULL,
  `orgWebsite` varchar(255) NOT NULL,
  `supervisorPhone` varchar(255) NOT NULL,
  `supervisorName` varchar(255) NOT NULL,
  `supervisorEmail` varchar(255) NOT NULL,
  `totalHours` int DEFAULT NULL,
  `totalWeeks` int DEFAULT NULL,
  `createdOn` datetime NOT NULL,
  `createdBy_id` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cceminorproposal_student_id` (`student_id`),
  KEY `cceminorproposal_term_id` (`term_id`),
  KEY `cceminorproposal_createdBy_id` (`createdBy_id`),
  CONSTRAINT `cceminorproposal_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `user` (`username`),
  CONSTRAINT `cceminorproposal_ibfk_2` FOREIGN KEY (`term_id`) REFERENCES `term` (`id`),
  CONSTRAINT `cceminorproposal_ibfk_3` FOREIGN KEY (`createdBy_id`) REFERENCES `user` (`username`),
  CONSTRAINT `cceminorproposal_chk_1` CHECK ((`status` in (_utf8mb4'Draft',_utf8mb4'Submitted',_utf8mb4'Approved',_utf8mb4'Denied',_utf8mb4'Completed')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cceminorproposal`
--

LOCK TABLES `cceminorproposal` WRITE;
/*!40000 ALTER TABLE `cceminorproposal` DISABLE KEYS */;
/*!40000 ALTER TABLE `cceminorproposal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celtslabor`
--

DROP TABLE IF EXISTS `celtslabor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `celtslabor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL,
  `positionTitle` varchar(255) NOT NULL,
  `term_id` int NOT NULL,
  `isAcademicYear` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `celtslabor_user_id` (`user_id`),
  KEY `celtslabor_term_id` (`term_id`),
  CONSTRAINT `celtslabor_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`),
  CONSTRAINT `celtslabor_ibfk_2` FOREIGN KEY (`term_id`) REFERENCES `term` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celtslabor`
--

LOCK TABLES `celtslabor` WRITE;
/*!40000 ALTER TABLE `celtslabor` DISABLE KEYS */;
INSERT INTO `celtslabor` VALUES (1,'mupotsal','Habitat For Humanity Cord.',2,1),(2,'ayisie','Bonner Manager',3,0),(3,'ayisie','AGP Team Memeber',2,1);
/*!40000 ALTER TABLE `celtslabor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `certification`
--

DROP TABLE IF EXISTS `certification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certification` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `isArchived` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certification`
--

LOCK TABLES `certification` WRITE;
/*!40000 ALTER TABLE `certification` DISABLE KEYS */;
INSERT INTO `certification` VALUES (1,'Bonner',0),(2,'CCE Minor',0),(3,'CPR',0),(4,'Confidentiality',0),(5,'I9',0);
/*!40000 ALTER TABLE `certification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `certificationattempt`
--

DROP TABLE IF EXISTS `certificationattempt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certificationattempt` (
  `id` int NOT NULL AUTO_INCREMENT,
  `certification_id` int NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `dateStarted` date NOT NULL,
  `termStarted_id` int NOT NULL,
  `dateEnded` date DEFAULT NULL,
  `endReason` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `certificationattempt_certification_id` (`certification_id`),
  KEY `certificationattempt_user_id` (`user_id`),
  KEY `certificationattempt_termStarted_id` (`termStarted_id`),
  CONSTRAINT `certificationattempt_ibfk_1` FOREIGN KEY (`certification_id`) REFERENCES `certification` (`id`),
  CONSTRAINT `certificationattempt_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`),
  CONSTRAINT `certificationattempt_ibfk_3` FOREIGN KEY (`termStarted_id`) REFERENCES `term` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certificationattempt`
--

LOCK TABLES `certificationattempt` WRITE;
/*!40000 ALTER TABLE `certificationattempt` DISABLE KEYS */;
/*!40000 ALTER TABLE `certificationattempt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `certificationrequirement`
--

DROP TABLE IF EXISTS `certificationrequirement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certificationrequirement` (
  `id` int NOT NULL AUTO_INCREMENT,
  `certification_id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `frequency` varchar(255) NOT NULL,
  `isRequired` tinyint(1) NOT NULL,
  `order` smallint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `certificationrequirement_certification_id` (`certification_id`),
  CONSTRAINT `certificationrequirement_ibfk_1` FOREIGN KEY (`certification_id`) REFERENCES `certification` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certificationrequirement`
--

LOCK TABLES `certificationrequirement` WRITE;
/*!40000 ALTER TABLE `certificationrequirement` DISABLE KEYS */;
INSERT INTO `certificationrequirement` VALUES (1,1,'Bonner Orientation','once',1,1),(2,1,'All Bonner Meeting','term',1,2),(3,1,'First Year Service Trip','once',1,3),(4,1,'Sophomore Exchange','once',1,4),(5,1,'Junior Recommitment','once',1,5),(6,1,'Senior Legacy Training','once',1,6),(7,1,'Senior Presentation of Learning','once',1,7),(8,1,'Bonner Congress','once',0,NULL),(9,1,'Bonner Student Leadership Institute','once',0,NULL),(10,3,'CPR Training','once',1,2),(11,3,'Volunteer Training','once',1,1),(12,2,'Community Engagement 1','once',1,NULL),(13,2,'Community Engagement 2','once',1,NULL),(14,2,'Community Engagement 3','once',1,NULL),(15,2,'Community Engagement 4','once',1,NULL),(16,2,'Summer Program','once',1,NULL);
/*!40000 ALTER TABLE `certificationrequirement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `id` int NOT NULL AUTO_INCREMENT,
  `courseName` varchar(255) NOT NULL,
  `courseAbbreviation` varchar(255) NOT NULL,
  `sectionDesignation` varchar(255) NOT NULL,
  `courseCredit` float NOT NULL,
  `term_id` int DEFAULT NULL,
  `status_id` int NOT NULL,
  `createdBy_id` varchar(255) NOT NULL,
  `serviceLearningDesignatedSections` text NOT NULL,
  `previouslyApprovedDescription` text NOT NULL,
  `isPermanentlyDesignated` tinyint(1) NOT NULL,
  `isAllSectionsServiceLearning` tinyint(1) NOT NULL,
  `isRegularlyOccurring` tinyint(1) NOT NULL,
  `isPreviouslyApproved` tinyint(1) NOT NULL,
  `hasSlcComponent` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `course_term_id` (`term_id`),
  KEY `course_status_id` (`status_id`),
  KEY `course_createdBy_id` (`createdBy_id`),
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`term_id`) REFERENCES `term` (`id`),
  CONSTRAINT `course_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `coursestatus` (`id`),
  CONSTRAINT `course_ibfk_3` FOREIGN KEY (`createdBy_id`) REFERENCES `user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'Databases','','',0,3,1,'ramsayb2','','',0,1,0,0,0),(2,'Spanish Help','SPN 104','',0,2,2,'heggens','','',0,1,0,0,0),(3,'Frenchy Help','FRN 103','',0,3,3,'ramsayb2','','',0,1,0,0,0),(4,'Testing','','',0,2,1,'heggens','','',0,1,0,0,0);
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseinstructor`
--

DROP TABLE IF EXISTS `courseinstructor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courseinstructor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `user_id` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `courseinstructor_course_id` (`course_id`),
  KEY `courseinstructor_user_id` (`user_id`),
  CONSTRAINT `courseinstructor_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`),
  CONSTRAINT `courseinstructor_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseinstructor`
--

LOCK TABLES `courseinstructor` WRITE;
/*!40000 ALTER TABLE `courseinstructor` DISABLE KEYS */;
INSERT INTO `courseinstructor` VALUES (1,1,'ramsayb2'),(2,2,'ramsayb2'),(3,2,'neillz'),(4,3,'heggens'),(5,4,'ramsayb2'),(6,4,'qasema'),(7,1,'bledsoef');
/*!40000 ALTER TABLE `courseinstructor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseparticipant`
--

DROP TABLE IF EXISTS `courseparticipant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courseparticipant` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `hoursEarned` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `courseparticipant_course_id` (`course_id`),
  KEY `courseparticipant_user_id` (`user_id`),
  CONSTRAINT `courseparticipant_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`),
  CONSTRAINT `courseparticipant_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseparticipant`
--

LOCK TABLES `courseparticipant` WRITE;
/*!40000 ALTER TABLE `courseparticipant` DISABLE KEYS */;
INSERT INTO `courseparticipant` VALUES (1,1,'neillz',2),(2,2,'neillz',3),(3,2,'khatts',4),(4,2,'khatts',4),(5,1,'khatts',1),(6,1,'bledsoef',1),(7,1,'ayisie',1);
/*!40000 ALTER TABLE `courseparticipant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coursequestion`
--

DROP TABLE IF EXISTS `coursequestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coursequestion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `questionContent` text NOT NULL,
  `questionNumber` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `coursequestion_course_id` (`course_id`),
  CONSTRAINT `coursequestion_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coursequestion`
--

LOCK TABLES `coursequestion` WRITE;
/*!40000 ALTER TABLE `coursequestion` DISABLE KEYS */;
INSERT INTO `coursequestion` VALUES (1,1,'This is testing for the first question.',1),(2,1,'This is testing for the second question.',2),(3,1,'This is testing for the third question.',3),(4,1,'This is testing for the fourth question.',4),(5,1,'This is testing for the fifth question.',5),(6,1,'This is testing for the sixth question.',6),(7,2,'This is testing for the first question.',1),(8,2,'This is testing for the second question.',2),(9,2,'This is testing for the third question.',3),(10,2,'This is testing for the fourth question.',4),(11,2,'This is testing for the fifth question.',5),(12,2,'This is testing for the sixth question.',6),(13,3,'This is testing for the first question.',1),(14,3,'This is testing for the second question.',2),(15,3,'This is testing for the third question.',3),(16,3,'This is testing for the fourth question.',4),(17,3,'This is testing for the fifth question.',5),(18,3,'This is testing for the sixth question.',6),(19,4,'This is testing for the first question.',1),(20,4,'This is testing for the second question.',2),(21,4,'This is testing for the third question.',3),(22,4,'This is testing for the fourth question.',4),(23,4,'This is testing for the fifth question.',5),(24,4,'This is testing for the sixth question.',6);
/*!40000 ALTER TABLE `coursequestion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coursestatus`
--

DROP TABLE IF EXISTS `coursestatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coursestatus` (
  `id` int NOT NULL AUTO_INCREMENT,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coursestatus`
--

LOCK TABLES `coursestatus` WRITE;
/*!40000 ALTER TABLE `coursestatus` DISABLE KEYS */;
INSERT INTO `coursestatus` VALUES (1,'Draft'),(2,'Submitted'),(3,'Approved'),(4,'Imported');
/*!40000 ALTER TABLE `coursestatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emaillog`
--

DROP TABLE IF EXISTS `emaillog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emaillog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `event_id` int NOT NULL,
  `subject` varchar(255) NOT NULL,
  `templateUsed_id` int NOT NULL,
  `recipientsCategory` varchar(255) NOT NULL,
  `recipients` varchar(255) NOT NULL,
  `dateSent` datetime NOT NULL,
  `sender` varchar(255) NOT NULL,
  `attachmentName` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `emaillog_event_id` (`event_id`),
  KEY `emaillog_templateUsed_id` (`templateUsed_id`),
  CONSTRAINT `emaillog_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`),
  CONSTRAINT `emaillog_ibfk_2` FOREIGN KEY (`templateUsed_id`) REFERENCES `emailtemplate` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emaillog`
--

LOCK TABLES `emaillog` WRITE;
/*!40000 ALTER TABLE `emaillog` DISABLE KEYS */;
INSERT INTO `emaillog` VALUES (1,5,'Location Change for {event_name}',2,'RSVP\'d','neillz','2022-05-07 00:00:00','neillz',NULL),(2,5,'Time Change for {event_name}',2,'RSVP\'d','ramsayb2','2022-06-05 00:00:00','neillz',NULL),(3,5,'Time Change for {event_name}',2,'RSVP\'d','ramsayb2','2022-05-04 00:00:00','neillz',NULL),(4,4,'Time Change for {event_name}',2,'RSVP\'d','neillz','2022-05-02 00:00:00','ramsayb2',NULL),(5,3,'Location Change for {event_name}',1,'Interested','neillz','2022-06-06 00:00:00','ramsayb2',NULL);
/*!40000 ALTER TABLE `emaillog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emailtemplate`
--

DROP TABLE IF EXISTS `emailtemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emailtemplate` (
  `id` int NOT NULL AUTO_INCREMENT,
  `subject` varchar(255) NOT NULL,
  `body` text NOT NULL,
  `action` varchar(255) NOT NULL,
  `purpose` varchar(255) NOT NULL,
  `replyToAddress` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emailtemplate`
--

LOCK TABLES `emailtemplate` WRITE;
/*!40000 ALTER TABLE `emailtemplate` DISABLE KEYS */;
INSERT INTO `emailtemplate` VALUES (1,'Test Email','Hello {recipient_name}, This is a test event named {event_name} located in {location}. Other info: {start_date} and this {start_time}-{end_time}.','sent','Test','j5u6j9w6v1h0p3g1@bereacs.slack.com'),(2,'Test Email 2','Hello {recipient_name}, This is another test event named {event_name} located in {location}. Other info: {start_date} and this {start_time}-{end_time}. The link is {event_link}','sent','Test2','j5u6j9w6v1h0p3g1@bereacs.slack.com'),(3,'Event Reminder','Hello! This is a reminder that you have an event coming up tomorrow, {start_date}. The event is {event_name} and it will be taking place at {location} on {start_time}. The link is {event_link}. The event is scheduled to happen {relative_time} from now.','sent','Reminder','j5u6j9w6v1h0p3g1@bereacs.slack.com');
/*!40000 ALTER TABLE `emailtemplate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emergencycontact`
--

DROP TABLE IF EXISTS `emergencycontact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emergencycontact` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `relationship` varchar(255) NOT NULL,
  `homePhone` varchar(255) NOT NULL,
  `workPhone` varchar(255) NOT NULL,
  `cellPhone` varchar(255) NOT NULL,
  `emailAddress` varchar(255) NOT NULL,
  `homeAddress` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `emergencycontact_user_id` (`user_id`),
  CONSTRAINT `emergencycontact_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emergencycontact`
--

LOCK TABLES `emergencycontact` WRITE;
/*!40000 ALTER TABLE `emergencycontact` DISABLE KEYS */;
/*!40000 ALTER TABLE `emergencycontact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `term_id` int NOT NULL,
  `description` text NOT NULL,
  `timeStart` time NOT NULL,
  `timeEnd` time NOT NULL,
  `location` varchar(255) NOT NULL,
  `isFoodProvided` tinyint(1) NOT NULL,
  `isLaborOnly` tinyint(1) NOT NULL,
  `isTraining` tinyint(1) NOT NULL,
  `isRsvpRequired` tinyint(1) NOT NULL,
  `isService` tinyint(1) NOT NULL,
  `isEngagement` tinyint(1) NOT NULL,
  `isAllVolunteerTraining` tinyint(1) NOT NULL,
  `rsvpLimit` int DEFAULT NULL,
  `startDate` date NOT NULL,
  `seriesId` int DEFAULT NULL,
  `isRepeating` tinyint(1) NOT NULL,
  `contactEmail` varchar(255) DEFAULT NULL,
  `contactName` varchar(255) DEFAULT NULL,
  `program_id` int NOT NULL,
  `isCanceled` tinyint(1) NOT NULL,
  `deletionDate` datetime DEFAULT NULL,
  `deletedBy` text,
  PRIMARY KEY (`id`),
  KEY `event_term_id` (`term_id`),
  KEY `event_program_id` (`program_id`),
  CONSTRAINT `event_ibfk_1` FOREIGN KEY (`term_id`) REFERENCES `term` (`id`),
  CONSTRAINT `event_ibfk_2` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (1,'Empty Bowls Spring Event 1',2,'Empty Bowls Spring 2021','18:00:00','21:00:00','Seabury Center',0,0,1,0,0,0,0,NULL,'2021-10-12',NULL,0,'testEmail','testName',1,0,NULL,NULL),(2,'Hunger Hurts',2,'Will donate Food to Community','18:00:00','21:00:00','Berea Community School',0,0,0,0,0,0,0,NULL,'2021-11-12',NULL,0,'testEmail','testName',1,0,NULL,NULL),(3,'Adoption 101',4,'Lecture on adoption','18:00:00','21:00:00','Alumni Patio',0,0,1,0,0,0,0,NULL,'2021-12-12',NULL,0,'testEmail','testName',3,0,NULL,NULL),(4,'First Meetup',4,'Berea Buddies First Meetup','06:00:00','09:00:00','Stephenson Building',0,0,0,0,0,0,0,NULL,'2021-06-25',NULL,0,'testEmail','testName',2,0,NULL,NULL),(5,'Tutoring',4,'Tutoring Training','15:00:00','21:00:00','Woodspen',0,0,0,0,0,0,0,NULL,'2021-06-18',NULL,0,'testEmail','testName',2,0,NULL,NULL),(6,'Meet & Greet with Grandparent',4,'Students meet with grandparent for the first time','18:00:00','21:00:00','Woods-Penniman',0,0,1,0,0,0,0,NULL,'2021-08-12',NULL,0,'testEmail','testName',3,0,NULL,NULL),(7,'Empty Bowl with Community',4,'Open to Berea community','18:00:00','21:00:00','Berea Community Park',0,0,0,0,0,0,0,NULL,'2021-12-12',NULL,0,'testEmail','testName',1,0,NULL,NULL),(8,'Berea Buddies Second Meeting',3,'Play game to bond with buddy','18:00:00','21:00:00','Stephenson Building',0,0,1,0,0,0,0,NULL,'2021-12-12',NULL,0,'testEmail','testName',2,0,NULL,NULL),(9,'Field Trip with Buddies',3,'A small trip to Berea Farm','18:00:00','21:00:00','Berea Farm',0,0,1,0,0,0,0,NULL,'2021-12-12',NULL,0,'testEmail','testName',2,0,NULL,NULL),(10,'Adopt-a-Grandparent Training',1,'Training event for the Adopt-a-Grandparent program.','18:00:00','21:00:00','Stephenson Building',0,0,1,0,0,0,0,NULL,'2021-01-12',NULL,0,'testEmail','testName',3,0,NULL,NULL),(11,'Celts Admin Meeting',4,'Not a required event','18:00:00','21:00:00','Stephenson Building',0,0,0,0,0,0,0,NULL,'2021-06-12',NULL,0,'testEmail','testName',9,0,NULL,NULL),(12,'Dinner with Grandparent',4,'Second event with grandparent','18:00:00','21:00:00','Boone Tavern',0,0,0,0,0,0,0,NULL,'2021-06-12',NULL,0,'testEmail','testName',3,0,NULL,NULL),(13,'Community Clean Up',3,'This event doesn\'t belong to any major program','18:00:00','21:00:00','Berea Community Park',0,0,0,0,0,0,0,NULL,'2021-06-12',NULL,0,'testEmail','testName',9,0,NULL,NULL),(14,'All Volunteer Training',1,'testing multiple programs','18:00:00','21:00:00','Woods-Penniman',0,0,1,0,0,0,1,NULL,'2021-06-12',NULL,0,'testEmail','testName',9,0,NULL,NULL),(15,'Training Event',4,'Test for training','18:00:00','21:00:00','Alumni Building',0,0,1,0,0,0,0,NULL,'2021-06-12',NULL,0,'testEmail','testName',9,0,NULL,NULL),(16,'Training Event',4,'Test for training','18:00:00','21:00:00','Alumni Building',0,0,1,0,0,0,0,NULL,'2021-06-12',NULL,0,'testEmail','testName',9,0,NULL,NULL);
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventcohort`
--

DROP TABLE IF EXISTS `eventcohort`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventcohort` (
  `id` int NOT NULL AUTO_INCREMENT,
  `event_id` int NOT NULL,
  `year` int NOT NULL,
  `invited_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `eventcohort_event_id_year` (`event_id`,`year`),
  KEY `eventcohort_event_id` (`event_id`),
  CONSTRAINT `eventcohort_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventcohort`
--

LOCK TABLES `eventcohort` WRITE;
/*!40000 ALTER TABLE `eventcohort` DISABLE KEYS */;
/*!40000 ALTER TABLE `eventcohort` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventparticipant`
--

DROP TABLE IF EXISTS `eventparticipant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventparticipant` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL,
  `event_id` int NOT NULL,
  `hoursEarned` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `eventparticipant_user_id` (`user_id`),
  KEY `eventparticipant_event_id` (`event_id`),
  CONSTRAINT `eventparticipant_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`),
  CONSTRAINT `eventparticipant_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventparticipant`
--

LOCK TABLES `eventparticipant` WRITE;
/*!40000 ALTER TABLE `eventparticipant` DISABLE KEYS */;
INSERT INTO `eventparticipant` VALUES (1,'neillz',1,2),(2,'khatts',1,2),(3,'neillz',2,2),(4,'bryanta',5,0),(5,'khatts',3,3),(6,'ayisie',1,0),(7,'partont',2,5),(8,'khatts',6,3),(9,'khatts',10,3);
/*!40000 ALTER TABLE `eventparticipant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventrsvp`
--

DROP TABLE IF EXISTS `eventrsvp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventrsvp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL,
  `event_id` int NOT NULL,
  `rsvpTime` datetime NOT NULL,
  `rsvpWaitlist` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `eventrsvp_user_id_event_id` (`user_id`,`event_id`),
  KEY `eventrsvp_user_id` (`user_id`),
  KEY `eventrsvp_event_id` (`event_id`),
  CONSTRAINT `eventrsvp_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`),
  CONSTRAINT `eventrsvp_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventrsvp`
--

LOCK TABLES `eventrsvp` WRITE;
/*!40000 ALTER TABLE `eventrsvp` DISABLE KEYS */;
INSERT INTO `eventrsvp` VALUES (1,'mupotsal',7,'2026-08-05 16:34:37',0),(2,'khatts',3,'2026-08-05 16:34:37',0),(3,'agliullovak',6,'2026-08-05 16:34:37',0),(4,'ayisie',1,'2026-08-05 16:34:37',0),(5,'bryanta',5,'2026-08-05 16:34:37',0),(6,'neillz',2,'2026-08-05 16:34:37',0),(7,'partont',2,'2026-08-05 16:34:37',0),(8,'lamichhanes2',9,'2026-08-05 16:34:37',0);
/*!40000 ALTER TABLE `eventrsvp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventrsvplog`
--

DROP TABLE IF EXISTS `eventrsvplog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventrsvplog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `createdBy_id` varchar(255) NOT NULL,
  `createdOn` datetime NOT NULL,
  `rsvpLogContent` varchar(255) NOT NULL,
  `event_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `eventrsvplog_createdBy_id` (`createdBy_id`),
  KEY `eventrsvplog_event_id` (`event_id`),
  CONSTRAINT `eventrsvplog_ibfk_1` FOREIGN KEY (`createdBy_id`) REFERENCES `user` (`username`),
  CONSTRAINT `eventrsvplog_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventrsvplog`
--

LOCK TABLES `eventrsvplog` WRITE;
/*!40000 ALTER TABLE `eventrsvplog` DISABLE KEYS */;
/*!40000 ALTER TABLE `eventrsvplog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventtemplate`
--

DROP TABLE IF EXISTS `eventtemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventtemplate` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `tag` varchar(255) NOT NULL,
  `templateJSON` varchar(255) NOT NULL,
  `templateFile` varchar(255) NOT NULL,
  `isVisible` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventtemplate`
--

LOCK TABLES `eventtemplate` WRITE;
/*!40000 ALTER TABLE `eventtemplate` DISABLE KEYS */;
INSERT INTO `eventtemplate` VALUES (1,'Single Program','single-program','{}','createEvent.html',0),(2,'All Volunteer Training','all-volunteer','{\"name\": \"All Volunteer Training\",\"description\": \"Training for all CELTS programs\", \"isTraining\": true, \"isService\": false, \"isRequired\": true, \"isAllVolunteerTraining\": true, \"rsvpLimit\": \"\"}','createEvent.html',1);
/*!40000 ALTER TABLE `eventtemplate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventview`
--

DROP TABLE IF EXISTS `eventview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventview` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL,
  `event_id` int NOT NULL,
  `viewedOn` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `eventview_user_id` (`user_id`),
  KEY `eventview_event_id` (`event_id`),
  CONSTRAINT `eventview_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`),
  CONSTRAINT `eventview_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventview`
--

LOCK TABLES `eventview` WRITE;
/*!40000 ALTER TABLE `eventview` DISABLE KEYS */;
/*!40000 ALTER TABLE `eventview` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `individualrequirement`
--

DROP TABLE IF EXISTS `individualrequirement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `individualrequirement` (
  `id` int NOT NULL AUTO_INCREMENT,
  `program_id` int DEFAULT NULL,
  `course_id` int DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `username_id` varchar(255) NOT NULL,
  `term_id` int DEFAULT NULL,
  `requirement_id` int NOT NULL,
  `addedBy_id` varchar(255) NOT NULL,
  `addedOn` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_id` (`username_id`,`requirement_id`),
  KEY `individualrequirement_program_id` (`program_id`),
  KEY `individualrequirement_course_id` (`course_id`),
  KEY `individualrequirement_username_id` (`username_id`),
  KEY `individualrequirement_term_id` (`term_id`),
  KEY `individualrequirement_requirement_id` (`requirement_id`),
  KEY `individualrequirement_addedBy_id` (`addedBy_id`),
  CONSTRAINT `individualrequirement_ibfk_1` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`),
  CONSTRAINT `individualrequirement_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`),
  CONSTRAINT `individualrequirement_ibfk_3` FOREIGN KEY (`username_id`) REFERENCES `user` (`username`),
  CONSTRAINT `individualrequirement_ibfk_4` FOREIGN KEY (`term_id`) REFERENCES `term` (`id`),
  CONSTRAINT `individualrequirement_ibfk_5` FOREIGN KEY (`requirement_id`) REFERENCES `certificationrequirement` (`id`),
  CONSTRAINT `individualrequirement_ibfk_6` FOREIGN KEY (`addedBy_id`) REFERENCES `user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `individualrequirement`
--

LOCK TABLES `individualrequirement` WRITE;
/*!40000 ALTER TABLE `individualrequirement` DISABLE KEYS */;
INSERT INTO `individualrequirement` VALUES (1,NULL,1,NULL,'ayisie',3,12,'ramsayb2','0000-00-00 00:00:00'),(2,1,NULL,NULL,'ayisie',3,14,'ramsayb2','0000-00-00 00:00:00'),(4,NULL,1,NULL,'bledsoef',3,14,'ramsayb2','0000-00-00 00:00:00'),(5,NULL,1,NULL,'khatts',3,14,'ramsayb2','0000-00-00 00:00:00'),(6,NULL,NULL,'Name of Summer activity','khatts',3,16,'ramsayb2','0000-00-00 00:00:00');
/*!40000 ALTER TABLE `individualrequirement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `insuranceinfo`
--

DROP TABLE IF EXISTS `insuranceinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insuranceinfo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL,
  `insuranceType` int NOT NULL,
  `policyHolderName` varchar(255) NOT NULL,
  `policyHolderRelationship` varchar(255) NOT NULL,
  `insuranceCompany` varchar(255) NOT NULL,
  `policyNumber` varchar(255) NOT NULL,
  `groupNumber` varchar(255) NOT NULL,
  `healthIssues` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `insuranceinfo_user_id` (`user_id`),
  CONSTRAINT `insuranceinfo_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insuranceinfo`
--

LOCK TABLES `insuranceinfo` WRITE;
/*!40000 ALTER TABLE `insuranceinfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `insuranceinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interest`
--

DROP TABLE IF EXISTS `interest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interest` (
  `id` int NOT NULL AUTO_INCREMENT,
  `program_id` int NOT NULL,
  `user_id` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `interest_program_id` (`program_id`),
  KEY `interest_user_id` (`user_id`),
  CONSTRAINT `interest_ibfk_1` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`),
  CONSTRAINT `interest_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interest`
--

LOCK TABLES `interest` WRITE;
/*!40000 ALTER TABLE `interest` DISABLE KEYS */;
INSERT INTO `interest` VALUES (1,1,'khatts'),(2,1,'bryanta'),(3,2,'lamichhanes2'),(4,3,'lamichhanes2'),(5,2,'ramsayb2'),(6,3,'ramsayb2');
/*!40000 ALTER TABLE `interest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `migratehistory`
--

DROP TABLE IF EXISTS `migratehistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `migratehistory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `migrated` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `migratehistory`
--

LOCK TABLES `migratehistory` WRITE;
/*!40000 ALTER TABLE `migratehistory` DISABLE KEYS */;
/*!40000 ALTER TABLE `migratehistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `note`
--

DROP TABLE IF EXISTS `note`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `note` (
  `id` int NOT NULL AUTO_INCREMENT,
  `createdBy_id` varchar(255) NOT NULL,
  `createdOn` datetime NOT NULL,
  `noteContent` text NOT NULL,
  `isPrivate` tinyint(1) NOT NULL,
  `noteType` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `note_createdBy_id` (`createdBy_id`),
  CONSTRAINT `note_ibfk_1` FOREIGN KEY (`createdBy_id`) REFERENCES `user` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `note`
--

LOCK TABLES `note` WRITE;
/*!40000 ALTER TABLE `note` DISABLE KEYS */;
INSERT INTO `note` VALUES (1,'ramsayb2','2021-10-12 00:00:00','I think the training is put in wrong',0,'ban'),(2,'mupotsal','2021-10-12 00:00:00','I agree with your comment on training',0,'question'),(3,'mupotsal','2021-10-12 00:00:00','tells bad jokes',1,'ban'),(4,'neillz','2021-11-26 00:00:00','Allergic to water',0,'profile'),(5,'neillz','2021-11-30 00:00:00','Allergic to food',0,'profile'),(6,'ramsayb2','2021-11-30 00:00:00','Run when in sight',0,'profile'),(7,'ramsayb2','2026-08-05 16:34:49','45wterghysfb',0,'profile'),(8,'ramsayb2','2026-08-05 16:35:01','wtrhsgbbf',0,'profile');
/*!40000 ALTER TABLE `note` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profilenote`
--

DROP TABLE IF EXISTS `profilenote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profilenote` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL,
  `note_id` int NOT NULL,
  `isBonnerNote` tinyint(1) NOT NULL,
  `isCCEMinorNote` tinyint(1) NOT NULL,
  `viewTier` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `profilenote_user_id` (`user_id`),
  KEY `profilenote_note_id` (`note_id`),
  CONSTRAINT `profilenote_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`),
  CONSTRAINT `profilenote_ibfk_2` FOREIGN KEY (`note_id`) REFERENCES `note` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profilenote`
--

LOCK TABLES `profilenote` WRITE;
/*!40000 ALTER TABLE `profilenote` DISABLE KEYS */;
INSERT INTO `profilenote` VALUES (1,'neillz',4,0,0,2),(2,'ramsayb2',5,0,0,3),(3,'partont',6,1,0,1),(5,'khatts',8,0,1,1);
/*!40000 ALTER TABLE `profilenote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program`
--

DROP TABLE IF EXISTS `program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `program` (
  `id` int NOT NULL AUTO_INCREMENT,
  `programName` varchar(255) NOT NULL,
  `instagramUrl` text,
  `facebookUrl` text,
  `bereaUrl` text,
  `programDescription` text NOT NULL,
  `partner` varchar(255) DEFAULT NULL,
  `isBonnerScholars` tinyint(1) NOT NULL,
  `isOtherCeltsSponsored` tinyint(1) NOT NULL,
  `contactName` varchar(255) DEFAULT NULL,
  `contactEmail` varchar(255) DEFAULT NULL,
  `defaultLocation` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program`
--

LOCK TABLES `program` WRITE;
/*!40000 ALTER TABLE `program` DISABLE KEYS */;
INSERT INTO `program` VALUES (1,'Hunger Initiatives',NULL,NULL,NULL,'Each year 200 people stand in line to get into Woods-Penniman for the Annual Empty Bowls Event sponsored by the Berea College ceramics students and CELTS. Students, faculty, staff and community members each pay $10 for a beautiful bowl, soup and the privilege of helping those in need in our community.',NULL,0,0,'','',''),(2,'Berea Buddies','https://www.instagram.com/bereabuddies/','https://www.facebook.com/BereaBuddies','https://www.berea.edu/centers/center-for-excellence-in-learning-through-service/programs/berea-buddies','The Berea Buddies program is dedicated to establishing long-term mentorships between Berea youth (Little Buddies) and Berea College students (Big Buddies). Volunteers serve children by offering them friendship and quality time. Big and Little Buddies meet each other every Monday or Tuesday during the academic year, except on school and national holidays, to enjoy structured activities around campus.',NULL,0,0,'','bereabuddies@berea.edu',''),(3,'Adopt-a-Grandparent','https://www.instagram.com/agp_celts/','https://www.facebook.com/profile.php?id=100085958053273','https://www.berea.edu/centers/center-for-excellence-in-learning-through-service/programs/adopt-a-grandparent','Adopt-a-Grandparent (AGP) is an outreach program for Berea elders. The program matches college student volunteers with residents of local long-term care centers. Volunteers visit with residents for at least an hour per week, and participate in special monthly programs.',NULL,0,0,'','',''),(4,'People Who Care','https://www.instagram.com/pwc_bc/','https://www.facebook.com/peoplewhocareBC','https://www.berea.edu/centers/center-for-excellence-in-learning-through-service/programs/people-who-care-program','People Who Care (PWC) helps to connect Berea College students with organizations and opportunities that promote change through advocacy, education, action, and direct community service. Volunteers may serve at local shelters, work with the Fair Trade University Campaign, or help to raise awareness about local issues like domestic violence, homelessness, fair trade, and AIDS awareness education. Students are welcome to participate as volunteers in PWC’s projects.',NULL,0,0,'','',''),(5,'Bonner Scholars',NULL,NULL,'https://www.berea.edu/centers/center-for-excellence-in-learning-through-service/bonner-scholars-program','The Bonner Scholars Program is a unique opportunity for students who want to combine a strong commitment to service with personal growth, teamwork, leadership development, and scholarship. Students who have completed an application for the Berea College class of 2026 may apply to be a Bonner Scholar.',NULL,1,0,'','',''),(6,'Habitat for Humanity','https://www.instagram.com/bc_habitat/','https://www.facebook.com/profile.php?id=100068874352425','https://www.berea.edu/centers/center-for-excellence-in-learning-through-service/programs/habitat-for-humanity','Through the work of Habitat for Humanity International, thousands of low-income families have found hope through affordable housing. Hard work and volunteering have resulted in the organization sheltering more than two million people worldwide.',NULL,0,0,'','',''),(7,'Berea Teen Mentoring','https://www.instagram.com/bereateenmentoring/','https://www.facebook.com/BereaTeenMentoring','https://www.berea.edu/centers/center-for-excellence-in-learning-through-service/programs/berea-teen-mentoring','Berea Teen Mentoring (BTM) brings Berea community youth, from ages 13-18, into a group setting for mentorship and enrichment programs. Staff members are assisted during the weekly program by Berea College student volunteers, who act as mentors for these program participants. The mission of the program is to stimulate and cultivate personal growth for young adults in the Berea community.',NULL,0,0,'','',''),(8,'Hispanic Outreach Program','https://www.instagram.com/hop.bc_/','https://www.facebook.com/HOPBerea','https://www.berea.edu/centers/center-for-excellence-in-learning-through-service/programs/hispanic-outreach-program','The Hispanic Outreach Program (HOP) is a service-learning effort which brings together CELTS, several community organizations, and the Department of Foreign Languages at Berea College. HOP aims to build bridges among the Spanish-speaking and English-speaking residents of Madison County.',NULL,0,0,'','',''),(9,'CELTS-Sponsored Event','https://www.instagram.com/bereacollegecelts/','https://www.facebook.com/BereaCollegeCELTS','https://www.berea.edu/centers/center-for-excellence-in-learning-through-service','This program hosts a myriad of different celts sponsored events that are not owned by any other program.',NULL,0,1,'','',''),(10,'Berea Tutoring','https://www.instagram.com/bereatutoring/','https://www.facebook.com/CELTSbereatutoring','https://www.berea.edu/centers/center-for-excellence-in-learning-through-service/programs/berea-tutoring','Berea Tutoring provides an encouraging atmosphere for local students who need help in achieving academic success, and for college volunteers who want to learn more about teaching or volunteering. Our mission is to increase conceptual understanding in academic subject areas, enrich educational experiences, and build self-confidence by providing college-aged tutors to local school children.',NULL,0,0,'','','');
/*!40000 ALTER TABLE `program` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programban`
--

DROP TABLE IF EXISTS `programban`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programban` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL,
  `program_id` int NOT NULL,
  `endDate` date DEFAULT NULL,
  `banNote_id` int NOT NULL,
  `unbanNote_id` int DEFAULT NULL,
  `removeFromTranscript` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `programban_user_id` (`user_id`),
  KEY `programban_program_id` (`program_id`),
  KEY `programban_banNote_id` (`banNote_id`),
  KEY `programban_unbanNote_id` (`unbanNote_id`),
  CONSTRAINT `programban_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`),
  CONSTRAINT `programban_ibfk_2` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`),
  CONSTRAINT `programban_ibfk_3` FOREIGN KEY (`banNote_id`) REFERENCES `note` (`id`),
  CONSTRAINT `programban_ibfk_4` FOREIGN KEY (`unbanNote_id`) REFERENCES `note` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programban`
--

LOCK TABLES `programban` WRITE;
/*!40000 ALTER TABLE `programban` DISABLE KEYS */;
INSERT INTO `programban` VALUES (1,'khatts',3,'2027-07-31',1,NULL,0),(2,'ayisie',1,'2027-01-02',3,NULL,0);
/*!40000 ALTER TABLE `programban` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programmanager`
--

DROP TABLE IF EXISTS `programmanager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programmanager` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL,
  `program_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `programmanager_user_id` (`user_id`),
  KEY `programmanager_program_id` (`program_id`),
  CONSTRAINT `programmanager_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`username`),
  CONSTRAINT `programmanager_ibfk_2` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programmanager`
--

LOCK TABLES `programmanager` WRITE;
/*!40000 ALTER TABLE `programmanager` DISABLE KEYS */;
INSERT INTO `programmanager` VALUES (1,'khatts',1),(2,'mupotsal',2),(3,'neillz',1),(4,'neillz',10);
/*!40000 ALTER TABLE `programmanager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questionnote`
--

DROP TABLE IF EXISTS `questionnote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questionnote` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question_id` int NOT NULL,
  `note_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `questionnote_question_id` (`question_id`),
  KEY `questionnote_note_id` (`note_id`),
  CONSTRAINT `questionnote_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `coursequestion` (`id`),
  CONSTRAINT `questionnote_ibfk_2` FOREIGN KEY (`note_id`) REFERENCES `note` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questionnote`
--

LOCK TABLES `questionnote` WRITE;
/*!40000 ALTER TABLE `questionnote` DISABLE KEYS */;
INSERT INTO `questionnote` VALUES (1,1,2);
/*!40000 ALTER TABLE `questionnote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `requirementmatch`
--

DROP TABLE IF EXISTS `requirementmatch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `requirementmatch` (
  `id` int NOT NULL AUTO_INCREMENT,
  `requirement_id` int NOT NULL,
  `event_id` int DEFAULT NULL,
  `course_id` int DEFAULT NULL,
  `engagementRequest_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `requirementmatch_requirement_id` (`requirement_id`),
  KEY `requirementmatch_event_id` (`event_id`),
  KEY `requirementmatch_course_id` (`course_id`),
  KEY `requirementmatch_engagementRequest_id` (`engagementRequest_id`),
  CONSTRAINT `requirementmatch_ibfk_1` FOREIGN KEY (`requirement_id`) REFERENCES `certificationrequirement` (`id`),
  CONSTRAINT `requirementmatch_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`),
  CONSTRAINT `requirementmatch_ibfk_3` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`),
  CONSTRAINT `requirementmatch_ibfk_4` FOREIGN KEY (`engagementRequest_id`) REFERENCES `cceminorproposal` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `requirementmatch`
--

LOCK TABLES `requirementmatch` WRITE;
/*!40000 ALTER TABLE `requirementmatch` DISABLE KEYS */;
/*!40000 ALTER TABLE `requirementmatch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `term`
--

DROP TABLE IF EXISTS `term`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `term` (
  `id` int NOT NULL AUTO_INCREMENT,
  `description` varchar(255) NOT NULL,
  `year` int NOT NULL,
  `academicYear` varchar(255) NOT NULL,
  `isSummer` tinyint(1) NOT NULL,
  `isCurrentTerm` tinyint(1) NOT NULL,
  `termOrder` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `term`
--

LOCK TABLES `term` WRITE;
/*!40000 ALTER TABLE `term` DISABLE KEYS */;
INSERT INTO `term` VALUES (1,'Fall 2020',2020,'2020-2021',0,0,'2020-3'),(2,'Spring 2021',2021,'2020-2021',0,0,'2021-1'),(3,'Summer 2021',2021,'2020-2021',1,1,'2021-2'),(4,'Fall 2021',2021,'2021-2022',0,0,'2021-3'),(5,'Spring 2022',2022,'2021-2022',0,0,'2022-1'),(6,'Summer 2022',2022,'2021-2022',1,0,'2022-2'),(7,'Fall 2022',2022,'2022-2023',0,0,'2022-3'),(8,'Spring 2023',2023,'2022-2023',0,0,'2023-1'),(9,'Spring 2024',2024,'2023-2024',0,0,'2024-1'),(10,'Fall 2023',2023,'2023-2024',0,0,'2023-3');
/*!40000 ALTER TABLE `term` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `username` varchar(255) NOT NULL,
  `bnumber` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phoneNumber` varchar(255) DEFAULT NULL,
  `firstName` varchar(255) NOT NULL,
  `lastName` varchar(255) NOT NULL,
  `cpoNumber` varchar(255) NOT NULL,
  `isStudent` tinyint(1) NOT NULL,
  `major` varchar(255) DEFAULT NULL,
  `rawClassLevel` varchar(255) DEFAULT NULL,
  `isFaculty` tinyint(1) NOT NULL,
  `isStaff` tinyint(1) NOT NULL,
  `isCeltsAdmin` tinyint(1) NOT NULL,
  `isCeltsStudentStaff` tinyint(1) NOT NULL,
  `dietRestriction` text,
  `minorInterest` tinyint(1) DEFAULT NULL,
  `hasGraduated` tinyint(1) NOT NULL,
  `declaredMinor` tinyint(1) NOT NULL,
  PRIMARY KEY (`username`),
  UNIQUE KEY `user_bnumber` (`bnumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('agliullovak','B00759117','agliullovak@berea.edu','(555)555-5555','Karina','Agliullova','',1,NULL,NULL,0,0,0,0,NULL,NULL,0,0),('ayisie','B00739736','ayisie@berea.edu','(220)290-3939','Ebenezer','Ayisi','',1,'Chemistry','Junior',0,0,0,0,NULL,NULL,0,1),('bledsoef','B00776544','bledsoef@berea.edu','(123)456-7890','Finn','Bledsoe','',0,NULL,NULL,0,1,0,0,NULL,NULL,0,1),('bryanta','B00708826','bryanta@berea.edu','(859)433-1159','Alex','Bryant','',1,'Biology','Senior',0,0,0,0,NULL,NULL,0,0),('glek','B00792345','glek@berea.edu','(555)579-5555','Kafui','Gle','',1,'Computer Science','Junior',0,0,0,0,NULL,NULL,0,0),('heggens','B00765098','heggens@berea.edu','(859)985-5555','Scott','Heggen','',0,NULL,NULL,1,1,0,0,NULL,NULL,0,0),('hoerstl','B00791233','hoerstl@berea.edu','(555)555-9999','Lawrence','Hoerst','',1,'Computer Science','Senior',0,0,0,0,NULL,NULL,0,0),('khatts','B00759107','khatts@berea.edu','(555)555-5555','Sreynit','Khatt','',1,'Computer Science','Senior',0,0,0,0,NULL,1,0,1),('lamichhanes2','B00733993','lamichhanes2@berea.edu','(555)555-5555','Sandesh','Lamichhane','',1,'Computer and Information Science','Junior',0,0,0,0,NULL,NULL,0,0),('makindeo','B00791326','makindeo@berea.edu','(555)555-5555','Oluwagbayi','Makinde','',1,'Computer Science','Senior',0,0,0,0,NULL,NULL,0,0),('michels','B00781963','michels@berea.edu','(555)555-9999','Stevenson','Michel','',1,'Computer Science','Senior',0,0,0,0,NULL,NULL,0,0),('mupotsal','B00741640','mupotsal@berea.edu','(859)463-1159','Liberty','Mupotsa','',1,NULL,NULL,0,0,0,1,NULL,NULL,0,0),('neillz','B00751864','neillz@berea.edu','(555)985-1234','Zach','Neill','',1,'Psychology','Sophomore',0,0,0,1,NULL,0,0,0),('partont','B00751360','partont@berea.edu','(859)433-1559','Tyler','Parton','',1,'Computer Science','Senior',0,0,0,0,NULL,NULL,0,0),('qasema','B00000000','qasema@berea.edu','8599723821','Ala','Qasem','',0,NULL,NULL,1,1,1,0,NULL,NULL,0,0),('ramsayb2','B00763721','ramsayb2@berea.edu','(555)555-5555','Brian','Ramsay','',0,NULL,NULL,0,1,1,0,'Diary',NULL,0,0),('stettnera2','B00719955','stettnera2@berea.edu','(555)555-5555','Anderson','Stettner','',0,NULL,NULL,0,1,1,0,NULL,NULL,0,0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-05 16:47:22
