from auth_service import sign_up, login, get_session, sign_out, get_profile

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

        profile_data = get_profile(result.user.id)
        if profile_data:
            print(f"[SUCCESS] Profile found!")
            print(f" > Username: {profile_data['username']}")
            print(f" > Balance:  ${profile_data['cash_balance']:,.2f}")

        result2 = get_session()
        if result2:
            print(f"Sucess! {result.user.id} is logged in currently")
        
        sign_out()
        result2 = get_session()
        if result2 is None:
            print(f"Sucess! {result.user.id} is logged out currently")

    except Exception as e:
        print(f"Error: {e}")