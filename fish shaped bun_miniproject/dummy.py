import pymysql
import random
from faker import Faker

# Faker 객체 생성
fake = Faker()

# 데이터베이스 연결 설정
connection = pymysql.connect(
    host='localhost',
    user='root',  # 사용자 이름
    password='0000',  # 비밀번호
    database='fish_shaped_bun_shop',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with connection.cursor() as cursor:
        # 더미 사용자 데이터 삽입
        for _ in range(50):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            password = fake.password()
            address = fake.address()
            contact = fake.phone_number()
            is_active = random.choice([True, False])
            is_staff = random.choice([True, False])
            is_orderable = random.choice([True, False])
            gender = random.choice([True, False])  # 남성/여성 랜덤 선택 (True: 남성, False: 여성)

            cursor.execute("""
                INSERT INTO users (first_name, last_name, email, password, address, contact, is_active, is_staff, is_orderable, gender)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (first_name, last_name, email, password, address, contact, is_active, is_staff, is_orderable, gender))

        # 더미 원재료 데이터 삽입
        raw_materials = [
            ('Flour', 1.76),           # 밀가루
            ('Sugar', 2.00),           # 설탕
            ('Yeast', 0.50),           # 이스트
            ('Red Bean Paste', 4.50),  # 팥소
            ('Chocolate', 28.00),      # 초콜릿
            ('Cream', 4.50),           # 크림
            ('Avocado', 11.40),        # 아보카도
            ('Milk', 1.20),            # 우유
            ('Baking Powder', 0.80),   # 베이킹 파우더
            ('Chicken Breast', 5.00),  # 통안심
            ('Salt', 0.30),            # 소금
            ('Butter', 2.50)           # 버터
        ]
        for name, price in raw_materials:
            cursor.execute("""
                INSERT INTO raw_materials (name, price)
                VALUES (%s, %s)
            """, (name, price))

        # 더미 재고 데이터 삽입
        cursor.execute("SELECT id FROM raw_materials")
        raw_material_ids = [row['id'] for row in cursor.fetchall()]
        for raw_material_id in raw_material_ids:
            quantity = random.randint(50, 200)
            cursor.execute("""
                INSERT INTO stocks (raw_material_id, quantity)
                VALUES (%s, %s)
            """, (raw_material_id, quantity))

        # 더미 제품 데이터 삽입
        products = [
            ('Fish Bun', 'A delicious fish-shaped bun.', 3.00),
            ('Red Bean Bun', 'Sweet bun filled with red bean paste.', 2.50),
            ('Chocolate Bun', 'Decadent chocolate-filled bun.', 3.50),
            ('Avocado Bun', 'Fresh avocado-filled bun.', 5.50),
            ('Beef Wellington Bun', '신선한 안심이 들어간 붕어빵', 9.99)
        ]
        for name, description, price in products:
            cursor.execute("""
                INSERT INTO products (name, description, price)
                VALUES (%s, %s, %s)
            """, (name, description, price))

        # 더미 판매 기록 데이터 삽입
        cursor.execute("SELECT id FROM users")
        user_ids = [row['id'] for row in cursor.fetchall()]
        cursor.execute("SELECT id FROM products")
        product_ids = [row['id'] for row in cursor.fetchall()]

        for user_id in user_ids:
            created_at = fake.date_time_this_year()
            cursor.execute("""
                INSERT INTO sales_records (user_id, created_at)
                VALUES (%s, %s)
            """, (user_id, created_at))

            sales_record_id = cursor.lastrowid
            for _ in range(random.randint(1, 3)):  # 1~3개의 상품을 추가
                product_id = random.choice(product_ids)
                quantity = random.randint(1, 5)
                cursor.execute("""
                    INSERT INTO sales_items (sales_record_id, product_id, quantity)
                    VALUES (%s, %s, %s)
                """, (sales_record_id, product_id, quantity))

        # **Stocks 테이블 업데이트 이력 삽입**
        cursor.execute("SELECT id FROM raw_materials")
        raw_material_ids = [row['id'] for row in cursor.fetchall()]

        for _ in range(20):  # 20개의 재고 업데이트 이력 추가
            raw_material_id = random.choice(raw_material_ids)
            change_quantity = random.randint(-10, 20)  # 재고 증가 또는 감소
            change_type = random.choice(["IN", "OUT", "RETURNED", "DISCARDED"])  # 입고, 출고, 반품, 폐기
            change_date = fake.date_time_this_year()

            # daily_records 테이블에 삽입
            cursor.execute("""
                INSERT INTO daily_records (stock_id, change_quantity, change_type, change_date)
                VALUES ((SELECT id FROM stocks WHERE raw_material_id = %s), %s, %s, %s)
            """, (raw_material_id, change_quantity, change_type, change_date))

            # stocks 테이블 업데이트 (수량 변경)
            cursor.execute("""
                UPDATE stocks
                SET quantity = quantity + %s, last_updated = %s
                WHERE raw_material_id = %s
            """, (change_quantity, change_date, raw_material_id))

        # **daily_records 테이블에 하루 판매 기록 삽입**
        for _ in range(20):  # 20개의 일별 판매 기록 추가
            date = fake.date_this_year()  # 랜덤 날짜 생성

            # daily_records 테이블에 change_date만 삽입
            cursor.execute("""
                INSERT INTO daily_records (change_date)
                VALUES (%s)
            """, (date,))


        # 변경 사항 커밋
        connection.commit()
finally:
    connection.close()
