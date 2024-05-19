-- MySQL Script generated by MySQL Workbench
-- Thu May 16 17:11:50 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`temporada`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`temporada` (
  `ano` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ano`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`equipe`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`equipe` (
  `equipe` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`equipe`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`jogos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`jogos` (
  `id` INT NOT NULL,
  `placar_casa` INT NULL,
  `placar_visitante` INT NULL,
  `data` DATETIME NULL,
  `round` INT NULL,
  `stage` INT NULL,
  `ano` VARCHAR(45) NOT NULL,
  `equipe_casa` VARCHAR(45) NOT NULL,
  `equipe_visitante` VARCHAR(45) NOT NULL,
  `estatisticas_casa` JSON NULL,
  `estatisticas_visitantes` JSON NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_jogos_temporada_idx` (`ano` ASC),
  INDEX `fk_jogos_equipe1_idx` (`equipe_casa` ASC),
  INDEX `fk_jogos_equipe2_idx` (`equipe_visitante` ASC),
  CONSTRAINT `fk_jogos_temporada`
    FOREIGN KEY (`ano`)
    REFERENCES `mydb`.`temporada` (`ano`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_jogos_equipe1`
    FOREIGN KEY (`equipe_casa`)
    REFERENCES `mydb`.`equipe` (`equipe`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_jogos_equipe2`
    FOREIGN KEY (`equipe_visitante`)
    REFERENCES `mydb`.`equipe` (`equipe`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
