import psycopg2
from django.conf import settings

class NewsMapper:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )

    def get_all_news(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM news")
                all_news = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching news: {e}")
            all_news = []
        finally:
            self.connection.close()

        return all_news

    def get_news_by_id(self, news_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM news WHERE id = %s", [news_id])
                news = cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching news: {e}")
        finally:
            self.connection.close()

        return news

    def create_news(self, title, description, date):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO news ("title", "description", "date")
                VALUES (%s, %s, %s)
                RETURNING id
                """, (title, description, date)
            )
            news_id = cursor.fetchone()[0]
        self.connection.commit()
        return news_id

    def update_news(self, news_id, title, description, date):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE news
                    SET "title" = %s, "description" = %s, "date" = %s, "updatedAt" = NOW()
                    WHERE id = %s
                    """, (title, description, date, news_id)
                )
                if cursor.rowcount == 0:
                    return {"success": False, "message": "News not found"}
            self.connection.commit()
            return {"success": True, "message": "News updated successfully"}
        except psycopg2.Error as e:
            print(f"Error updating news: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}

    def delete_news(self, news_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM news WHERE id = %s", [news_id])
                if cursor.rowcount == 0:
                    return {"success": False, "message": "News not found"}
            self.connection.commit()
            return {"success": True, "message": "News deleted successfully"}
        except psycopg2.Error as e:
            print(f"Error deleting news: {e}")
            return {"success": False, "message": f"Database error: {str(e)}"}
