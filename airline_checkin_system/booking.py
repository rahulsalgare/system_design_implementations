import threading
import psycopg2
from airline_checkin_system.db_setup.db_config import DB_PARAMS


def book_seat(user_id):
    connection = psycopg2.connect(**DB_PARAMS)
    cursor = connection.cursor()
    try:
        """
        If we do not provide FOR UPDATE (exclusive lock), then threads won't wait for the other thread to complete
        accessing the same row and modifying that same row by the multiple threads
        FOR update acquires an exclusive lock on the row, any other thread trying to modify the same row has to wait
        after the first thread releases the lock the other thread can acquire it.
        Also when other thread acquires the lock, it re-evaluates the SELECT query, 
        in that case if first user had got seat with user_id NULL, after he writes user_id with some value,
        the other thread wont get the same row since that rows user_id is not NULL anymore.
        
        Lock is released when the transaction is commmited. in this case connection.commit()
        """
        cursor.execute("SELECT seat_id FROM seats WHERE user_id IS NULL ORDER BY seat_id LIMIT 1 FOR UPDATE;")
        seat = cursor.fetchone()[0]
        cursor.execute(f"UPDATE seats SET user_id={user_id} WHERE seat_id={seat}")
    except Exception as e:
        print(f"Error booking seat for user {user_id}: {e}")
    finally:
        connection.commit()
        connection.close()


def book_seats_for_all_users():
    threads = []
    for user_id in range(1, 121):
        thread = threading.Thread(target=book_seat, args=(user_id,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def display_seats():
    """
    Display seats in nice table format.
    """
    connection = psycopg2.connect(**DB_PARAMS)
    cursor = connection.cursor()

    cursor.execute("SELECT seat, user_id FROM seats ORDER BY seat;")
    seat_data = cursor.fetchall()

    seat_layout = [['.' for _ in range(20)] for _ in range(6)]

    for seat, user_id in seat_data:
        row = seat.split('-')[1].strip()
        col = int(seat.split('-')[0]) - 1

        row_ind = ord(row) - ord('A')  # calculate row index (A=0, B=1, ...)
        seat_layout[row_ind][col] = 'X' if user_id is not None else '.'

    for row in seat_layout:
        print(" ".join(row))
        if row == 2:
            print()

    connection.close()


if __name__ == '__main__':
    book_seats_for_all_users()
    display_seats()
