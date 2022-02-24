from config import ConnectionDB

db = ConnectionDB

class AuthByToken:
    """ Authorise a connection and making changes with a token given. """
    def auth_by_token(token):
        conn = db.connection
        cursor = conn.cursor()
        cursor.execute(f"Select username, password, token from users where token = '{token}'")
        users = cursor.fetchall()
        try:
            for user in users:
                if token in user[2]:
                    return True, 'Successfully logged in.', 200
        except Exception as e:
            print(e)
            return "User not found, try again", 423

if __name__ == '__main__':
    AuthByToken()