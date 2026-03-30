from auth_service import supabase, get_profile

def buy_stock(user_id: str, ticker: str, shares: int, current_price: float):
    """
    Logic:
    1. Fetch current cash_balance from 'profiles'
    2. Calculate total_cost (shares * current_price)
    3. If cash_balance >= total_cost:
       - Update profiles (subtract cash)
       - Update/Insert holdings (dont need to track old share price since considered in old average)
    avg price = (old average x shares + current share price x shares ) / total shares
    """

    try:
        current_balance = get_profile(user_id)["cash_balance"]
        trade_cost = shares * current_price
        new_balance = current_balance - trade_cost

        if (new_balance >= 0):
            update_balance = supabase.table("profiles").update({"cash_balance": new_balance}).eq("id", user_id).execute()

            holding_exist = supabase.table("holdings").select("*").eq("user_id", user_id).eq("ticker", ticker).execute()
            new_average_price = current_price
            new_shares = shares
            
            #if holding already exist, update avg price, otherwise create new holding
            if (len(holding_exist.data) > 0):
                holding = holding_exist.data[0]
                old_average = holding["average_price"]
                old_shares = holding["shares"]
                new_shares = shares + old_shares
                new_average_price = ((old_average * old_shares) + (current_price * shares)) / new_shares

            new_data = {"user_id": user_id, "ticker": ticker, "shares": new_shares, "average_price": new_average_price}
            update_holdings = supabase.table("holdings").upsert(new_data, on_conflict="user_id, ticker").execute()
            return {"sucess": True, "Details": "holdings updated"}
        return {"sucess": False, "Details": "Insufficient Funds"}
    except Exception as e:
        print(f"Error executing trade: {e}")
        return {"Success": False, "Detail": "Server Error. Please try again later."}

def sell_stock(user_id: str, ticker: str, shares_to_sell: int, current_price: float):
    """
    logic: 
    check if user_id has any shares of ticker.
    calc value (current_price x shares)
    add value to balance
    delete holdings
    """
    try:
        holding_exist = supabase.table("holdings").select("*").eq("user_id", user_id).eq("ticker", ticker).execute()

        old_shares = holding_exist.data[0]["shares"]

        if (shares_to_sell > old_shares or shares_to_sell <= 0):
            return {"Success": False, "Detail": f"You can sell anywhere from 1 to {old_shares} shares"}
        
        new_shares = old_shares - shares_to_sell
        current_balance = get_profile(user_id)["cash_balance"]
        trade_cost = shares_to_sell * current_price
        new_balance = current_balance + trade_cost  

        update_balance = supabase.table("profiles").update({"cash_balance": new_balance}).eq("user_id", user_id).execute()

        if (new_shares == 0): #sell all, delete holding
            delete_holding = supabase.table("holdings").delete().eq("user_id", user_id).eq("ticker", ticker).execute()
            return({"Sucess": True, "Detail": "Holding Deleted, Balance Updated"})

        else: #partial sell, update shares
            update_shares = supabase.table("holdings").update({"shares": new_shares}).eq("user_id", user_id).eq("ticker", ticker).execute()
            return({"Sucess": True, "Detail": "Shares Updated, Balance Updated"})
    except Exception as e:
        print(f"Error executing trade: {e}")
        return {"Success": False, "Detail": "Server Error. Please try again later."}
        
#def calculate_performance(user_id: str):
