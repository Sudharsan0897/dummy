CREATE DATABASE branch_db;
use branch_db;
CREATE TABLE branch(
    id INT AUTO_INCREMENT PRIMARY KEY,
    branch_name VARCHAR(100) NOT NULL,
    branch_code int(50) NOT NULL UNIQUE,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode int(20) NOT NULL,
    contact_person VARCHAR(100) NOT NULL,
    phone int(20) NOT NULL,
    email VARCHAR(100) NOT NULL
);
