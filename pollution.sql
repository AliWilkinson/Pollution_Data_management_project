-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema pollution-db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `pollution-db` ;

-- -----------------------------------------------------
-- Schema pollution-db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pollution-db` DEFAULT CHARACTER SET utf8 ;
USE `pollution-db` ;

-- -----------------------------------------------------
-- Table `pollution-db`.`Site`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pollution-db`.`Site` (
  `Site_ID` INT NOT NULL,
  `Location` VARCHAR(50) NULL,
  `Geo_Point_2d` VARCHAR(50) NULL,
  PRIMARY KEY (`Site_ID`),
  UNIQUE INDEX `Site_ID_UNIQUE` (`Site_ID` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pollution-db`.`Readings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pollution-db`.`Readings` (
  `Reading_ID` INT NOT NULL AUTO_INCREMENT,
  `Site_ID` INT NOT NULL,
  `Date_Time` DATETIME NULL,
  `NOx` FLOAT NULL,
  `NO2` FLOAT NULL,
  `NO` FLOAT NULL,
  `PM10` FLOAT NULL,
  `NVPM10` FLOAT NULL,
  `VPM10` FLOAT NULL,
  `NVPM2.5` FLOAT NULL,
  `PM2.5` FLOAT NULL,
  `VPM2.5` FLOAT NULL,
  `CO` FLOAT NULL,
  `O3` FLOAT NULL,
  `SO2` FLOAT NULL,
  `Temperature` REAL NULL,
  `Relative_Humidity` FLOAT NULL,
  `Air_Pressure` FLOAT NULL,
  `Date_Start` DATETIME NULL,
  `Date_End` DATETIME NULL,
  `Current` TINYINT NULL,
  `Instrument_Type` VARCHAR(45) NULL,
  PRIMARY KEY (`Reading_ID`),
  UNIQUE INDEX `Reading_ID_UNIQUE` (`Reading_ID` ASC),
  INDEX `fk_Readings_Site_idx` (`Site_ID` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pollution-db`.`Schema`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pollution-db`.`Schema` (
  `Measure` VARCHAR(35) NOT NULL,
  `Description` VARCHAR(65) NULL,
  `Unit` VARCHAR(10) NULL,
  PRIMARY KEY (`Measure`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
