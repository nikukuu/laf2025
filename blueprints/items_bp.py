from flask import Blueprint, render_template, request, jsonify
import mysql.connector

items_bp = Blueprint('items', __name__, template_folder='../templates')

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='3y7pu.h.filess.io',
            user='laf2025_couplewent',
            password='b4db8ac094f3b4f08e3e97af326b0ec0ed2bf217',
            database='laf2025_couplewent',
            port='3307'
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

@items_bp.route('/items', methods=['GET'])
def items():
    query = request.args.get('query', '')  # Get the search query from the request
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        if query:  # If there's a search query
            search_query = f"%{query}%"
            cursor.execute(
                "SELECT * FROM items WHERE status='published' AND (id LIKE %s OR item_name LIKE %s OR description LIKE %s OR location LIKE %s)",
                (search_query, search_query, search_query, search_query)
            )
        else:  # No query, fetch all items
            cursor.execute("SELECT * FROM items WHERE status='published'")

        # Fetch the items
        items = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        items = []
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the database connection

    return render_template('items.html', items=items)

@items_bp.route('/items/search', methods=['GET'])
def search_items():
    query = request.args.get('query', '')  # Get the search query
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        if query:  # If there's a search query
            search_query = f"%{query}%"
            cursor.execute(
                "SELECT * FROM items WHERE status='published' AND (id LIKE %s OR item_name LIKE %s OR description LIKE %s OR location LIKE %s)",
                (search_query, search_query, search_query, search_query)
            )
        else:  # No query, fetch all items
            cursor.execute("SELECT * FROM items WHERE status='published'")

        items = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        items = []
    finally:
        cursor.close()
        connection.close()

    return jsonify({'items': items})  # Return items as JSON
