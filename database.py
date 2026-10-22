import psycopg2


def get_db_connection():
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database="degree_verification",
        user="postgres"
    )

    return connection


def save_certificate(data, certificate_hash):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO certificates
        (
            student_name,
            degree,
            institution,
            graduation_year,
            credential_id,
            certificate_hash,
            verification_status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)

        ON CONFLICT (credential_id)
        DO UPDATE SET
            student_name = EXCLUDED.student_name,
            degree = EXCLUDED.degree,
            institution = EXCLUDED.institution,
            graduation_year = EXCLUDED.graduation_year,
            certificate_hash = EXCLUDED.certificate_hash

        RETURNING id;
    """

    cursor.execute(
        query,
        (
            data["student_name"],
            data["degree"],
            data["institution"],
            data["graduation_year"],
            data["credential_id"],
            certificate_hash,
            "PENDING"
        )
    )

    certificate_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return certificate_id