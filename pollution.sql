-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Pollution-er
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `Pollution-er` ;

-- -----------------------------------------------------
-- Schema Pollution-er
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Pollution-er` DEFAULT CHARACTER SET utf8 ;
USE `Pollution-er` ;

-- -----------------------------------------------------
-- Table `Pollution-er`.`Stations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Pollution-er`.`Stations` (
  `stationid` INT NOT NULL,
  `location` VARCHAR(47) NULL,
  `geo_point_2d` VARCHAR(47) NULL,
  PRIMARY KEY (`stationid`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Pollution-er`.`readings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Pollution-er`.`readings` (
  `readingid` INT NOT NULL,
  `datetime` DATETIME NULL,
  `nox` FLOAT NULL,
  `no2` FLOAT NULL,
  `no` FLOAT NULL,
  `pm 10` FLOAT NULL,
  `nvpm 10` FLOAT NULL,
  `vpm 10` FLOAT NULL,
  `mvpm 2.5` FLOAT NULL,
  `pm 2.5` FLOAT NULL,
  `vpm 2.5` FLOAT NULL,
  `co` FLOAT NULL,
  `o3` FLOAT NULL,
  `so2` FLOAT NULL,
  `temperature` REAL NULL,
  `rh` INT NULL,
  `airpressure` INT NULL,
  `datestart` DATETIME NULL,
  `dateend` DATETIME NULL,
  `current` TEXT(5) NULL,
  `instrumenttype` VARCHAR(34) NULL,
  `stationid-fk` INT NULL,
  PRIMARY KEY (`readingid`),
  INDEX `stationid_idx` (`stationid-fk` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Pollution-er`.`schema`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Pollution-er`.`schema` (
  `measure` VARCHAR(34) NOT NULL,
  `description` VARCHAR(66) NULL,
  `unit` VARCHAR(25) NULL,
  PRIMARY KEY (`measure`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
