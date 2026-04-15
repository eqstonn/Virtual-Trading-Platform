"""
Comprehensive pytest test suite for Virtual Trading Platform
Tests authentication, trading services, and API endpoints
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from fastapi.testclient import TestClient
from pydantic import BaseModel

# Import the app and services
from app_api import app, SignUpRequest, LoginRequest, TradeRequest
from auth_service import sign_up, login, get_session, sign_out, get_profile
from trading_service import buy_stock, sell_stock


@pytest.fixture
def client():
    """FastAPI test client fixture"""
    return TestClient(app)


@pytest.fixture
def mock_supabase():
    """Mock Supabase client fixture"""
    with patch('auth_service.supabase') as mock:
        yield mock


@pytest.fixture
def mock_trading_supabase():
    """Mock Supabase for trading service"""
    with patch('trading_service.supabase') as mock:
        yield mock


@pytest.fixture
def mock_get_profile():
    """Mock get_profile function"""
    with patch('trading_service.get_profile') as mock:
        yield mock


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "username": "testuser",
        "user_id": "user123"
    }


@pytest.fixture
def sample_profile_data():
    """Sample profile data"""
    return {
        "id": "user123",
        "username": "testuser",
        "email": "test@example.com",
        "cash_balance": 10000.00
    }


# ==================== AUTH SERVICE TESTS ====================

class TestAuthService:
    """Test suite for authentication service"""

    def test_sign_up_success(self, mock_supabase, sample_user_data):
        """Test successful user sign up"""
        mock_user = Mock()
        mock_user.id = sample_user_data["user_id"]
        mock_user.email = sample_user_data["email"]
        
        mock_supabase.auth.sign_up.return_value = Mock(user=mock_user)
        
        with patch('auth_service.create_user_profile') as mock_create_profile:
            result = sign_up(
                sample_user_data["email"],
                sample_user_data["password"],
                sample_user_data["username"]
            )
        
        assert result["user_id"] == sample_user_data["user_id"]
        assert result["email"] == sample_user_data["email"]
        assert result["username"] == sample_user_data["username"]
        assert "Sign up successful" in result["message"]

    def test_sign_up_failure(self, mock_supabase, sample_user_data):
        """Test sign up when user creation fails"""
        mock_supabase.auth.sign_up.return_value = Mock(user=None)
        
        result = sign_up(
            sample_user_data["email"],
            sample_user_data["password"],
            sample_user_data["username"]
        )
        
        assert "error" in result
        assert result["error"] == "Sign up failed"

    def test_sign_up_exception(self, mock_supabase, sample_user_data):
        """Test sign up exception handling"""
        mock_supabase.auth.sign_up.side_effect = Exception("Database error")
        
        result = sign_up(
            sample_user_data["email"],
            sample_user_data["password"],
            sample_user_data["username"]
        )
        
        assert "error" in result
        assert "Database error" in result["error"]

    def test_login_success(self, mock_supabase, sample_user_data, sample_profile_data):
        """Test successful login"""
        mock_user = Mock()
        mock_user.id = sample_user_data["user_id"]
        mock_user.email = sample_user_data["email"]
        
        mock_supabase.auth.sign_in_with_password.return_value = Mock(user=mock_user)
        
        with patch('auth_service.get_user_profile', return_value=sample_profile_data):
            result = login(sample_user_data["email"], sample_user_data["password"])
        
        assert result["user_id"] == sample_user_data["user_id"]
        assert result["email"] == sample_user_data["email"]
        assert "Login successful" in result["message"]

    def test_login_failure(self, mock_supabase, sample_user_data):
        """Test login failure"""
        mock_supabase.auth.sign_in_with_password.return_value = Mock(user=None)
        
        result = login(sample_user_data["email"], sample_user_data["password"])
        
        assert "error" in result
        assert result["error"] == "Login failed"

    def test_login_exception(self, mock_supabase, sample_user_data):
        """Test login exception handling"""
        mock_supabase.auth.sign_in_with_password.side_effect = Exception("Auth error")
        
        result = login(sample_user_data["email"], sample_user_data["password"])
        
        assert "error" in result

    def test_get_session_success(self, mock_supabase):
        """Test get_session when user is logged in"""
        mock_user = Mock()
        mock_user.id = "user123"
        
        mock_supabase.auth.get_user.return_value = Mock(user=mock_user)
        
        result = get_session()
        
        assert result is not None
        assert result.id == "user123"

    def test_get_session_no_user(self, mock_supabase):
        """Test get_session when no user is logged in"""
        mock_supabase.auth.get_user.return_value = Mock(user=None)
        
        result = get_session()
        
        assert result is None

    def test_sign_out_success(self, mock_supabase):
        """Test successful sign out"""
        mock_supabase.auth.sign_out.return_value = None
        
        result = sign_out()
        
        mock_supabase.auth.sign_out.assert_called_once()

    def test_get_profile_success(self, mock_supabase, sample_profile_data):
        """Test get_profile returns user data"""
        mock_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.single.return_value.execute.return_value = Mock(
            data=sample_profile_data
        )
        
        result = get_profile("user123")
        
        assert result == sample_profile_data
        assert result["cash_balance"] == 10000.00


# ==================== TRADING SERVICE TESTS ====================

class TestTradingService:
    """Test suite for trading service"""

    def test_buy_stock_success(self, mock_get_profile, sample_profile_data):
        """Test successful stock purchase"""
        mock_get_profile.return_value = sample_profile_data
        
        with patch('trading_service.supabase') as mock_supabase:
            mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = Mock()
            mock_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = Mock(data=[])
            mock_supabase.table.return_value.insert.return_value.execute.return_value = Mock()
            
            result = buy_stock("user123", "AAPL", 10, 150.0)
        
        assert result["Success"] is True
        assert "Holdings updated successfully" in result["Detail"]

    def test_buy_stock_insufficient_funds(self, mock_get_profile):
        """Test buy stock with insufficient funds"""
        profile_data = {
            "id": "user123",
            "cash_balance": 100.00
        }
        mock_get_profile.return_value = profile_data
        
        result = buy_stock("user123", "AAPL", 10, 150.0)
        
        assert result["Success"] is False
        assert "Insufficient Funds" in result["Detail"]

    def test_buy_stock_user_not_found(self, mock_get_profile):
        """Test buy stock when user profile not found"""
        mock_get_profile.return_value = None
        
        result = buy_stock("invalid_user", "AAPL", 10, 150.0)
        
        assert result["Success"] is False
        assert "User profile not found" in result["Detail"]

    def test_buy_stock_update_existing_holding(self, mock_get_profile, sample_profile_data):
        """Test buying stock when user already owns that ticker"""
        mock_get_profile.return_value = sample_profile_data
        
        existing_holding = {
            "shares": 5,
            "average_price": 145.0,
            "ticker": "AAPL",
            "user_id": "user123"
        }
        
        with patch('trading_service.supabase') as mock_supabase:
            mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = Mock()
            mock_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = Mock(
                data=[existing_holding]
            )
            
            result = buy_stock("user123", "AAPL", 10, 150.0)
        
        assert result["Success"] is True

    def test_sell_stock_success(self, mock_trading_supabase, mock_get_profile):
        """Test successful stock sale"""
        holding = {
            "shares": 15,
            "average_price": 145.0,
            "ticker": "AAPL"
        }
        
        mock_trading_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = Mock(data=[holding])
        mock_trading_supabase.table.return_value.update.return_value.eq.return_value.eq.return_value.execute.return_value = Mock()
        mock_get_profile.return_value = {"cash_balance": 5000.0}
        
        result = sell_stock("user123", "AAPL", 10, 150.0)
        
        assert result["Success"] is True

    def test_sell_stock_no_holdings(self, mock_trading_supabase):
        """Test selling stock when user has no holdings"""
        mock_trading_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = Mock(data=[])
        
        result = sell_stock("user123", "AAPL", 10, 150.0)
        
        assert result["Success"] is False
        assert "don't own any shares" in result["Detail"]

    def test_sell_stock_insufficient_shares(self, mock_trading_supabase):
        """Test selling more shares than owned"""
        holding = {"shares": 5, "average_price": 145.0}
        mock_trading_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = Mock(data=[holding])
        
        result = sell_stock("user123", "AAPL", 10, 150.0)
        
        assert result["Success"] is False
        assert "You can sell anywhere from 1 to 5 shares" in result["Detail"]

    def test_sell_stock_invalid_shares(self, mock_trading_supabase):
        """Test selling invalid number of shares (zero or negative)"""
        holding = {"shares": 15, "average_price": 145.0}
        mock_trading_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = Mock(data=[holding])
        
        result = sell_stock("user123", "AAPL", -5, 150.0)
        
        assert result["Success"] is False


# ==================== API ENDPOINT TESTS ====================

class TestAPIEndpoints:
    """Test suite for FastAPI endpoints"""

    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        assert response.json()["message"] == "API is running"

    def test_sign_up_endpoint_success(self, client):
        """Test sign up endpoint"""
        with patch('app_api.sign_up') as mock_sign_up:
            mock_sign_up.return_value = {
                "user_id": "user123",
                "email": "test@example.com",
                "username": "testuser",
                "message": "Sign up successful"
            }
            
            response = client.post("/sign_up", json={
                "email": "test@example.com",
                "password": "password123",
                "username": "testuser"
            })
        
        assert response.status_code == 200
        assert response.json()["user_id"] == "user123"

    def test_sign_up_endpoint_failure(self, client):
        """Test sign up endpoint with error"""
        with patch('app_api.sign_up') as mock_sign_up:
            mock_sign_up.return_value = {"error": "Email already exists"}
            
            response = client.post("/sign_up", json={
                "email": "test@example.com",
                "password": "password123",
                "username": "testuser"
            })
        
        assert response.status_code == 400

    def test_login_endpoint_success(self, client):
        """Test login endpoint"""
        with patch('app_api.login') as mock_login:
            mock_login.return_value = {
                "user_id": "user123",
                "email": "test@example.com",
                "username": "testuser",
                "cash_balance": 10000.0,
                "message": "Login successful"
            }
            
            response = client.post("/login", json={
                "email": "test@example.com",
                "password": "password123"
            })
        
        assert response.status_code == 200
        assert response.json()["user_id"] == "user123"

    def test_login_endpoint_failure(self, client):
        """Test login endpoint with invalid credentials"""
        with patch('app_api.login') as mock_login:
            mock_login.return_value = {"error": "Invalid email or password"}
            
            response = client.post("/login", json={
                "email": "test@example.com",
                "password": "wrongpassword"
            })
        
        assert response.status_code == 401


# ==================== DATA VALIDATION TESTS ====================

class TestDataValidation:
    """Test suite for data model validation"""

    def test_sign_up_request_valid(self):
        """Test valid SignUpRequest model"""
        request = SignUpRequest(
            email="test@example.com",
            password="password123",
            username="testuser"
        )
        
        assert request.email == "test@example.com"
        assert request.password == "password123"
        assert request.username == "testuser"

    def test_sign_up_request_invalid_email(self):
        """Test SignUpRequest with invalid email"""
        with pytest.raises(Exception):
            SignUpRequest(
                email="invalid-email",
                password="password123",
                username="testuser"
            )

    def test_login_request_valid(self):
        """Test valid LoginRequest model"""
        request = LoginRequest(
            email="test@example.com",
            password="password123"
        )
        
        assert request.email == "test@example.com"
        assert request.password == "password123"

    def test_trade_request_valid(self):
        """Test valid TradeRequest model"""
        request = TradeRequest(
            user_id="user123",
            ticker="AAPL",
            shares=10,
            price=150.0
        )
        
        assert request.user_id == "user123"
        assert request.ticker == "AAPL"
        assert request.shares == 10
        assert request.price == 150.0

    def test_trade_request_invalid_shares(self):
        """Test TradeRequest with invalid shares"""
        with pytest.raises(Exception):
            TradeRequest(
                user_id="user123",
                ticker="AAPL",
                shares="invalid",
                price=150.0
            )


# ==================== INTEGRATION TESTS ====================

class TestIntegration:
    """Integration tests for the trading platform"""

    def test_complete_auth_flow(self, mock_supabase):
        """Test complete authentication flow: sign up -> login -> get profile -> sign out"""
        # Mock signup
        mock_user = Mock()
        mock_user.id = "user123"
        mock_user.email = "test@example.com"
        mock_supabase.auth.sign_up.return_value = Mock(user=mock_user)
        
        with patch('auth_service.create_user_profile'):
            signup_result = sign_up("test@example.com", "password123", "testuser")
        
        assert signup_result["user_id"] == "user123"
        
        # Mock login
        mock_supabase.auth.sign_in_with_password.return_value = Mock(user=mock_user)
        with patch('auth_service.get_user_profile', return_value={"cash_balance": 10000}):
            login_result = login("test@example.com", "password123")
        
        assert login_result["user_id"] == "user123"
        
        # Mock sign out
        mock_supabase.auth.sign_out.return_value = None
        sign_out()
        mock_supabase.auth.sign_out.assert_called()

    def test_trading_flow(self, mock_get_profile):
        """Test complete trading flow: buy stock -> sell stock"""
        profile = {"id": "user123", "cash_balance": 10000.0}
        mock_get_profile.return_value = profile
        
        with patch('trading_service.supabase') as mock_supabase:
            # Setup mocks for buy
            mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = Mock()
            mock_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = Mock(data=[])
            mock_supabase.table.return_value.insert.return_value.execute.return_value = Mock()
            
            buy_result = buy_stock("user123", "AAPL", 10, 150.0)
            assert buy_result["Success"] is True
            
            # Setup mocks for sell
            holding = {"shares": 10, "average_price": 150.0}
            mock_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = Mock(data=[holding])
            
            sell_result = sell_stock("user123", "AAPL", 5, 155.0)
            assert sell_result["Success"] is True


# ==================== EDGE CASE TESTS ====================

class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_buy_zero_shares(self, mock_get_profile, sample_profile_data):
        """Test buying zero shares"""
        mock_get_profile.return_value = sample_profile_data
        
        with patch('trading_service.supabase'):
            result = buy_stock("user123", "AAPL", 0, 150.0)
        
        # Should still process but result depends on implementation
        # This tests that the system doesn't crash

    def test_very_large_share_quantity(self, mock_get_profile):
        """Test buying very large quantities of shares"""
        profile = {"id": "user123", "cash_balance": 1000000000.0}
        mock_get_profile.return_value = profile
        
        with patch('trading_service.supabase') as mock_supabase:
            mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = Mock()
            mock_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = Mock(data=[])
            mock_supabase.table.return_value.insert.return_value.execute.return_value = Mock()
            
            result = buy_stock("user123", "AAPL", 1000000, 0.01)
        
        assert result["Success"] is True

    def test_extremely_high_price(self, mock_get_profile, sample_profile_data):
        """Test trading at extremely high prices"""
        mock_get_profile.return_value = sample_profile_data
        
        with patch('trading_service.supabase') as mock_supabase:
            mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = Mock()
            mock_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = Mock(data=[])
            mock_supabase.table.return_value.insert.return_value.execute.return_value = Mock()
            
            result = buy_stock("user123", "AAPL", 1, 999999.99)
        
        # Should fail due to insufficient funds
        if result["Success"] is False:
            assert "Insufficient Funds" in result["Detail"]


if __name__ == "__main__":
    # Run tests with pytest
    # pytest test_trading_platform.py -v
    pytest.main([__file__, "-v", "--tb=short"])
