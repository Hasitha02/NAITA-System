CREATE DATABASE IF NOT EXISTS NAITA;

USE NAITA;

CREATE TABLE IF NOT EXISTS CreateAccount (
fname VARCHAR(255) NOT NULL,
lname VARCHAR(255) NOT NULL,
username VARCHAR(255) NOT NULL,
email VARCHAR(255) PRIMARY KEY,
password CHAR(60) NOT NULL
);


CREATE TABLE IF NOT EXISTS CBTSD(
    category VARCHAR(255),
    district VARCHAR(255),
    dateOfRegistration VARCHAR(255),
    indexNumber VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    fullName VARCHAR(255),
    dateofBirth VARCHAR(255),
    gender VARCHAR(255),
    NIC VARCHAR(255),
    telephoneNumber VARCHAR(20),
    NAITAIDnumber VARCHAR(255),
    dropOut VARCHAR(255),
    dropOutDate VARCHAR(255),
    addressNo VARCHAR(255),
    addressFLine VARCHAR(255),
    addressLLine VARCHAR(255),
    nameofEstablishment VARCHAR(255),
    establishmentType VARCHAR(255),
    establishmentAddressDivision VARCHAR(255),
    establishmentAddressDistrict VARCHAR(255),
    establishmentTelephone VARCHAR(20),
    DSDivision VARCHAR(255),
    establishmentCode VARCHAR(255),
    sectorName VARCHAR(255),
    trade VARCHAR(255),
    tradeCode VARCHAR(255),
    mode VARCHAR(255),
    NVQLevel VARCHAR(255),
    inspectorName VARCHAR(255),
    commencementDate VARCHAR(255),
    scheduleDateCompletion VARCHAR(255),
    signatureTM VARCHAR(255),
    remark VARCHAR(255)
);



CREATE TABLE IF NOT EXISTS EBTSD(
    category VARCHAR(255),
    district VARCHAR(255),
    dateOfRegistration VARCHAR(255),
    indexNumber VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    fullName VARCHAR(255),
    dateofBirth VARCHAR(255),
    gender VARCHAR(255),
    NIC VARCHAR(255),
    telephoneNumber VARCHAR(20),
    NAITAIDnumber VARCHAR(255),
    dropOut VARCHAR(255),
    dropOutDate VARCHAR(255),
    addressNo VARCHAR(255),
    addressFLine VARCHAR(255),
    addressLLine VARCHAR(255),
    nameofEstablishment VARCHAR(255),
    establishmentType VARCHAR(255),
    establishmentAddressDivision VARCHAR(255),
    establishmentAddressDistrict VARCHAR(255),
    establishmentTelephone VARCHAR(20),
    DSDivision VARCHAR(255),
    establishmentCode VARCHAR(255),
    sectorName VARCHAR(255),
    trade VARCHAR(255),
    tradeCode VARCHAR(255),
    mode VARCHAR(255),
    NVQLevel VARCHAR(255),
    inspectorName VARCHAR(255),
    commencementDate VARCHAR(255),
    scheduleDateCompletion VARCHAR(255),
    signatureTM VARCHAR(255),
    remark VARCHAR(255)
);
select * from CreateAccount;

select * from EBTSD;

show databases;

select * from CBTSD;