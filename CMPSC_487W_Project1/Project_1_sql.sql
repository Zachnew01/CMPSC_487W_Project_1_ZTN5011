CREATE DATABASE sunlabaccesssystem;

USE sublabaccesssystem;

CREATE TABLE sysUsers (
	id VARCHAR(9) PRIMARY KEY,
	type VARCHAR(20),
	isActive BOOL
);

CREATE TABLE accesses (
	aID VARCHAR(9),
	aTime DATETIME,
	isValid BOOL,
	FOREIGN KEY (aID) REFERENCES sysUsers(id)
);