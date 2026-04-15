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
        profile = get_profile(user_id)
        if not profile:
            return {"Success": False, "Detail": "User profile not found"}
        
        current_balance = profile.get("cash_balance", 0)
        trade_cost = shares * current_price
        new_balance = current_balance - trade_cost

        if new_balance < 0:
            return {"Success": False, "Detail": "Insufficient Funds"}
        
        # Update the user's cash balance
        update_balance = supabase.table("profiles").update({"cash_balance": new_balance}).eq("id", user_id).execute()

        # Check if holding already exists
        holding_exist = supabase.table("holdings").select("*").eq("user_id", user_id).eq("ticker", ticker).execute()
        new_average_price = current_price
        new_shares = shares
        
        # If holding already exists, calculate new average price
        if holding_exist.data and len(holding_exist.data) > 0:
            holding = holding_exist.data[0]
            old_average = holding["average_price"]
            old_shares = holding["shares"]
            new_shares = shares + old_shares
            new_average_price = ((old_average * old_shares) + (current_price * shares)) / new_shares
            
            # Update existing holding
            update_holdings = supabase.table("holdings").update({
                "shares": new_shares, 
                "average_price": new_average_price
            }).eq("user_id", user_id).eq("ticker", ticker).execute()
        else:
            # Insert new holding
            insert_holdings = supabase.table("holdings").insert({
                "user_id": user_id, 
                "ticker": ticker, 
                "shares": new_shares, 
                "average_price": new_average_price
            }).execute()
        
        return {"Success": True, "Detail": "Holdings updated successfully"}
    except Exception as e:
        print(f"Error executing buy trade: {e}")
        return {"Success": False, "Detail": f"Server Error: {str(e)}"}

def sell_stock(user_id: str, ticker: str, shares_to_sell: int, current_price: float):
    """
    logic: 
    check if user_id has any shares of ticker.
    calc value (current_price x shares)
    add value to balance
    delete holdings or update shares
    """
    try:
        holding_exist = supabase.table("holdings").select("*").eq("user_id", user_id).eq("ticker", ticker).execute()

        if not holding_exist.data or len(holding_exist.data) == 0:
            return {"Success": False, "Detail": f"You don't own any shares of {ticker}"}
        
        old_shares = holding_exist.data[0]["shares"]

        if shares_to_sell > old_shares or shares_to_sell <= 0:
            return {"Success": False, "Detail": f"You can sell anywhere from 1 to {old_shares} shares"}
        
        new_shares = old_shares - shares_to_sell
        profile = get_profile(user_id)
        if not profile:
            return {"Success": False, "Detail": "User profile not found"}
        
        current_balance = profile.get("cash_balance", 0)
        trade_proceeds = shares_to_sell * current_price
        new_balance = current_balance + trade_proceeds  

        # Update user's cash balance
        update_balance = supabase.table("profiles").update({"cash_balance": new_balance}).eq("id", user_id).execute()

        if new_shares == 0:
            # Sell all shares - delete the holding
            delete_holding = supabase.table("holdings").delete().eq("user_id", user_id).eq("ticker", ticker).execute()
            return {"Success": True, "Detail": "Holding deleted, balance updated"}
        else:
            # Partial sell - update shares count
            update_shares = supabase.table("holdings").update({"shares": new_shares}).eq("user_id", user_id).eq("ticker", ticker).execute()
            return {"Success": True, "Detail": "Shares updated, balance updated"}
    except Exception as e:
        print(f"Error executing sell trade: {e}")
        return {"Success": False, "Detail": f"Server Error: {str(e)}"}
        
#def calculate_performance(user_id: str):
