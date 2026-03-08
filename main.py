from auth_service import sign_up, login

if __name__ == "__main__":
    try: 
        user_email = "eastoneng282@gmail.com"
        user_pw = "abc123"
        user_username = "eqston"

        #result = sign_up(user_email, user_pw, user_username)
        result = login(user_email, user_pw)

        if result.user:
            print(f"Sucess! User logged in with id: {result.user.id}")
        else:
            print("Login failed")
    except Exception as e:
        print(f"Error: {e}")