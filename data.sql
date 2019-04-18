CREATE TABLE IF NOT EXISTS 'user'(
    'user_id' VARCHAR(6) PRIMARY KEY,
    'user_name' VARCHAR(32) NOT NULL,
    'password' VARCHAR(24) NOT NULL,
    'privilidge' CHAR(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS 'admin'(
    'admin_id' VARCHAR(6) PRIMARY KEY,
    'admin_name' VARCHAR(32) NOT NULL,
    'privilidge' CHAR(1) NOT NULL,
    FOREIGN KEY(admin_id) REFERENCES user(user_id))
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS 'book'(
    'isbn' VARCHAR(13) PRIMARY KEY, 
	'book_name' VARCHAR(64), 
	'author' VARCHAR(64), 
	'press' VARCHAR(32), 
	'class_name' VARCHAR(64), 
	PRIMARY KEY (isbn)
);

CREATE TABLE IF NOT EXISTS 'librarycard'(
	'card_id' VARCHAR(8) PRIMARY KEY, 
	'name' VARCHAR(32), 
	'sex' VARCHAR(2), 
	'telephone' VARCHAR(11), 
	'enroll_date' DATE NOT NULL, 
	'valid_date' DATE NOT NULL, 
	'loss' BOOLEAN,
	'debt' BOOLEAN
    FOREIGN KEY(card_id) REFERENCES user(user_id))
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS 'inventory'(
    'barcode' VARCHAR(6) PRIMARY KEY, 
	'isbn' VARCHAR(13) REFERENCES book(isbn), 
	'storage_date' DATE, 
	'location' VARCHAR(32), 
	'status' BOOLEAN, 
	'admin' VARCHAR(6) REFERENCES admin(admin_id), 
);

CREATE TABLE IF NOT EXISTS 'readbook'(
    'operation_id' INTEGER PRIMARY KEY AUTO_INCREMENT, 
	'barcode' VARCHAR(6) REFERENCES inventory(barcode), 
	'card_id' VARCHAR(8) REFERENCES librarycard(card_id), 
    'borrow_user' VARCHAR(6), REFERENCES user(user_id),
	'start_date' DATE, 
	'end_date' DATE, 
	'due_date' DATE
);

