import psycopg2
from faker import Faker
import random

fake = Faker()

conn_params = {
    'dbname': 'testdb',
    'user': 'postgres',
    'password': '12345678',
    'host': 'localhost',
    'port': 5432
}

def get_connection():
    return psycopg2.connect(**conn_params)

def fill_buildings(conn):
    with conn.cursor() as cur:
        for _ in range(10):
            city = fake.city()
            street = fake.street_name()
            house_number = random.randint(1, 100)
            apartment_number = random.randint(1, 100)
            width = round(random.uniform(10.0, 100.0), 2)
            longitude = round(random.uniform(-180.0, 180.0), 6)

            cur.execute("""
                INSERT INTO buildings (city, street, house_number, apartment_number, width, longitude)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (city, street, house_number, apartment_number, width, longitude))
        conn.commit()

def fill_organizations(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM buildings")
        building_ids = [row[0] for row in cur.fetchall()]
        for building_id in building_ids:
            name = fake.company()
            phone = fake.phone_number()

            cur.execute("""
                INSERT INTO organizations (name, phone, building_id)
                VALUES (%s, %s, %s)
            """, (name, phone, building_id))
        conn.commit()

def fill_activitys(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM organizations")
        organization_ids = [row[0] for row in cur.fetchall()]

        for _ in range(10):
            name = fake.word()
            organization_id = random.choice(organization_ids)

            cur.execute("""
                INSERT INTO activitys (name, organization_id)
                VALUES (%s, %s)
            """, (name, organization_id))
        conn.commit()

def fill_categorys(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM activitys")
        activity_ids = [row[0] for row in cur.fetchall()]

        for _ in range(10):
            name = fake.word()
            activity_id = random.choice(activity_ids)

            cur.execute("""
                INSERT INTO categorys (name, activity_id)
                VALUES (%s, %s)
            """, (name, activity_id))
        conn.commit()

def fill_products(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM categorys")
        category_ids = [row[0] for row in cur.fetchall()]

        for _ in range(10):
            name = fake.word()
            category_id = random.choice(category_ids)

            cur.execute("""
                INSERT INTO products (name, category_id)
                VALUES (%s, %s)
            """, (name, category_id))
        conn.commit()

def main():
    conn = get_connection()
    try:
        fill_buildings(conn)
        fill_organizations(conn)
        fill_activitys(conn)
        fill_categorys(conn)
        fill_products(conn)
    finally:
        conn.close()

if __name__ == "__main__":
    main()