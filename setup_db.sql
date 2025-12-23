CREATE DATABASE setup_db;
USE setup_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    reset_token VARCHAR(255),
    reset_token_expires DATETIME
);

SHOW TABLES;
DESCRIBE users;
SELECT * FROM users;