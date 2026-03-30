import React, { useState, useRef } from 'react';
import { User } from 'lucide-react';

const HomePage = ({ onNavigate, user, onSignOut }) => {
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const containerRef = useRef(null);

  const handleMouseMove = (e) => {
    if (containerRef.current) {
      const rect = containerRef.current.getBoundingClientRect();
      setMousePosition({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top,
      });
    }
  };

  const handleSignOut = () => {
    setShowProfileMenu(false);
    onSignOut();
  };

  const handleGoToDashboard = () => {
    if (user) {
      onNavigate('dashboard');
    }
  };

  return (
    <div
      ref={containerRef}
      onMouseMove={handleMouseMove}
      className="relative w-full h-screen bg-black overflow-hidden flex items-center justify-center"
    >
      {/* Hover Chroma Background Effect */}
      <div
        className="absolute pointer-events-none"
        style={{
          left: `${mousePosition.x}px`,
          top: `${mousePosition.y}px`,
          width: '300px',
          height: '300px',
          transform: 'translate(-50%, -50%)',
          background: `radial-gradient(circle, rgba(249, 115, 22, 0.3) 0%, rgba(249, 115, 22, 0.15) 30%, transparent 70%)`,
          filter: 'blur(40px)',
          willChange: 'transform',
        }}
      />

      {/* Profile Icon - Top Right */}
      <div className="absolute top-8 right-8 z-50">
        <button
          onClick={() => setShowProfileMenu(!showProfileMenu)}
          className="w-12 h-12 bg-gray-800 hover:bg-gray-700 rounded-full flex items-center justify-center border border-gray-700 transition-all"
        >
          <User className="w-6 h-6 text-gray-300" />
        </button>

        {/* Profile Dropdown Menu */}
        {showProfileMenu && (
          <div className="absolute top-16 right-0 bg-[#1a1a1a] border border-gray-700 rounded-lg shadow-lg w-48 z-50">
            {user ? (
              <>
                <div className="px-4 py-3 border-b border-gray-700">
                  <p className="text-xs text-gray-500 uppercase">Logged in as</p>
                  <p className="text-sm font-semibold text-gray-100">{user.username}</p>
                </div>
                <button
                  onClick={() => setShowProfileMenu(false)}
                  className="w-full text-left px-4 py-3 hover:bg-gray-900 text-gray-100 text-sm font-medium border-b border-gray-700 transition-all"
                >
                  Edit Profile
                </button>
                <button
                  onClick={handleSignOut}
                  className="w-full text-left px-4 py-3 hover:bg-gray-900 text-red-400 text-sm font-medium transition-all"
                >
                  Sign Out
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={() => {
                    onNavigate('login');
                    setShowProfileMenu(false);
                  }}
                  className="w-full text-left px-4 py-3 hover:bg-gray-900 text-gray-100 text-sm font-medium border-b border-gray-700 transition-all"
                >
                  Login
                </button>
                <button
                  onClick={() => {
                    onNavigate('signup');
                    setShowProfileMenu(false);
                  }}
                  className="w-full text-left px-4 py-3 hover:bg-gray-900 text-gray-100 text-sm font-medium transition-all"
                >
                  Sign Up
                </button>
              </>
            )}
          </div>
        )}
      </div>

      {/* Center Content */}
      <div className="text-center z-10">
        <div className="flex items-center justify-center gap-3 mb-6">
          <div className="w-16 h-16 bg-orange-500 rounded-xl flex items-center justify-center font-bold text-2xl text-black">
            V
          </div>
        </div>
        <h1 className="text-5xl font-bold text-white mb-4 tracking-tight">
          Virtual Trading Sim
        </h1>
        <p className="text-gray-400 text-lg mb-8">
          Practice trading with real-time market data
        </p>
        
        {/* Begin Button - Only show if user is logged in */}
        {user && (
          <button
            onClick={handleGoToDashboard}
            className="bg-orange-500 hover:bg-orange-600 text-black font-bold py-3 px-8 rounded-lg transition-all text-lg"
          >
            Begin
          </button>
        )}
      </div>
    </div>
  );
};

export default HomePage;
