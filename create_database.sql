CREATE DATABASE book_management_system_db;
CREATE USER book_management_system_user;
GRANT ALL PRIVILEGES ON book_management_system_db.* TO book_management_system_user@'localhost' IDENTIFIED BY 'test_password';
FLUSH PRIVILEGES;
EXIT;