CREATE DATABASE IF NOT EXISTS fish_shaped_bun_shop;

USE fish_shaped_bun_shop;

DROP TABLE IF EXISTS sales_items;
DROP TABLE IF EXISTS sales_records;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS order_records;
DROP TABLE IF EXISTS daily_records;
DROP TABLE IF EXISTS stocks;
DROP TABLE IF EXISTS raw_materials;
DROP TABLE IF EXISTS users;

CREATE TABLE users(
	id INT AUTO_INCREMENT PRIMARY KEY, -- 인덱싱
	first_name VARCHAR(50), -- 이름
	last_name VARCHAR(20) NOT NULL, -- 성
	email VARCHAR(50) NOT NULL UNIQUE, -- 이메일
	password VARCHAR(255) NOT NULL, -- 비밀번호
	address VARCHAR(255), -- 주소
	contact VARCHAR(50), -- 전화번호
	gender BOOLEAN NOT NULL, -- 성별
	is_active BOOLEAN NOT NULL DEFAULT TRUE, -- 활성화된 계정인지 확인하는 컬럼
	is_staff BOOLEAN NOT NULL DEFAULT FALSE, -- 직원인지 확인하는 컬럼
	is_orderable BOOLEAN NOT NULL DEFAULT FALSE -- 주문 권한이 있는지 확인하는 컬럼
);

CREATE TABLE raw_materials (
	id INT AUTO_INCREMENT PRIMARY KEY, -- 인덱싱
	name VARCHAR(50) NOT NULL, -- 원재료 이름
	price DECIMAL(10, 2) NOT NULL -- 원재료 가격
);

CREATE TABLE stocks(
	id INT AUTO_INCREMENT PRIMARY KEY, -- 인덱싱
	raw_material_id INT NOT NULL, -- 원재료 id
	quantity INT NOT NULL, -- 수량
	last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 마지막 업데이트 시간
	FOREIGN KEY (raw_material_id) REFERENCES raw_materials(id)
);

CREATE TABLE daily_records(
	id INT AUTO_INCREMENT PRIMARY KEY, -- 인덱싱
	stock_id INT,-- stocks 테이블의 id
	change_quantity INT, -- 변경된 수량
	change_type ENUM('IN', 'OUT', 'RETURNED', 'DISCARDED'), -- 입고(IN) 출고(OUT) 반품(RETURNED) 폐기(DISCARDED)
	change_date DATETIME DEFAULT CURRENT_TIMESTAMP, -- 변경된 시간
	FOREIGN KEY (stock_id) REFERENCES stocks(id)
);

CREATE TABLE order_records(
	id INT AUTO_INCREMENT PRIMARY KEY, -- 인덱싱
	user_id INT, -- users 테이블의 id
	change_date DATETIME DEFAULT CURRENT_TIMESTAMP, -- 변경된 시간
	raw_material_id INT, -- raw_material 테이블의 id
	quantity INT NOT NULL, -- 수량
	FOREIGN KEY (user_id) REFERENCES users(id),
	FOREIGN KEY (raw_material_id) REFERENCES raw_materials(id)
);

CREATE TABLE products(
	id INT AUTO_INCREMENT PRIMARY KEY, -- 인덱싱
	name VARCHAR(50) NOT NULL, -- 상품 이름
	description TEXT, -- 상품 설명
	price DECIMAL(7, 2) NOT NULL -- 상품 가격
);

CREATE TABLE sales_records(
	id INT AUTO_INCREMENT PRIMARY KEY, -- 인덱싱
	user_id INT, -- users 테이블의 id
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- 생성 시간
	FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE sales_items(
	id INT AUTO_INCREMENT PRIMARY KEY, -- 인덱싱
	sales_record_id INT, -- sales_records의 id
	product_id INT, -- products의 id
	quantity INT NOT NULL, -- 수량
	FOREIGN KEY (sales_record_id) REFERENCES sales_records(id),
	FOREIGN KEY (product_id) REFERENCES products(id)
);
