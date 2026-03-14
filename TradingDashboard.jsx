import React, { useState } from 'react';
import { Search, User, TrendingUp, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

// Mock data for the graph
const data = [
  { time: '09:00', price: 3800 }, { time: '10:00', price: 3850 },
  { time: '11:00', price: 3820 }, { time: '12:00', price: 3880 },
  { time: '13:00', price: 3860 }, { time: '14:00', price: 3920 },
  { time: '15:00', price: 3900 },
];

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('Trade');

  return (
    <div className="min-h-screen bg-[#0f0f0f] text-gray-100 p-4 font-sans">
      {/* HEADER SECTION */}
      <header className="flex items-center justify-between mb-8 px-2">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-orange-500 rounded-lg flex items-center justify-center font-bold text-black">V</div>
          <h1 className="text-xl font-semibold tracking-tight">Virtual Trading Sim</h1>
        </div>

        {/* TOP MIDDLE TABS */}
        <nav className="flex bg-[#1a1a1a] rounded-full p-1 border border-gray-800">
          {['Home', 'Trade', 'Portfolio', 'Activity'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-6 py-1.5 rounded-full text-sm transition-all ${
                activeTab === tab ? 'bg-orange-500/20 text-orange-500 border border-orange-500/30' : 'text-gray-400 hover:text-white'
              }`}
            >
              {tab}
            </button>
          ))}
        </nav>

        <div className="flex items-center gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
            <input 
              type="text" 
              placeholder="Search stocks..." 
              className="bg-[#1a1a1a] border border-gray-800 rounded-lg py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-orange-500 w-64"
            />
          </div>
          <div className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center border border-gray-700">
            <User className="w-6 h-6 text-gray-400" />
          </div>
        </div>
      </header>

      {/* MAIN CONTENT GRID */}
      <div className="grid grid-cols-12 gap-6">
        
        {/* LEFT: GRAPH SECTION */}
        <div className="col-span-8 space-y-6">
          <div className="bg-[#141414] border border-gray-800 rounded-2xl p-6 h-[450px]">
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-2xl font-bold">ETH / USD</h2>
                <div className="flex items-center gap-2 text-green-500">
                  <span className="text-lg font-medium">$3,900.25</span>
                  <ArrowUpRight className="w-4 h-4" />
                  <span className="text-sm">+0.9%</span>
                </div>
              </div>
              <div className="flex gap-2">
                {['1H', '1D', '1W', '1M', '1Y'].map(t => (
                  <button key={t} className="px-3 py-1 bg-gray-800 rounded text-xs hover:bg-gray-700">{t}</button>
                ))}
              </div>
            </div>
            
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data}>
                  <defs>
                    <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#f97316" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#f97316" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <Area type="monotone" dataKey="price" stroke="#f97316" fillOpacity={1} fill="url(#colorPrice)" strokeWidth={2} />
                  <Tooltip contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333' }} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* PERFORMANCE FOOTER (P/L Calculation) */}
          <div className="bg-[#141414] border border-gray-800 rounded-2xl p-6 flex justify-between items-center">
            <div>
              <p className="text-gray-500 text-xs uppercase tracking-wider mb-1">Portfolio Value</p>
              <h3 className="text-xl font-bold">$12,450.75</h3>
            </div>
            <div className="text-right">
              <p className="text-gray-500 text-xs uppercase tracking-wider mb-1">Unrealized P/L</p>
              <h3 className="text-xl font-bold text-green-500">+$850.50 (7.3%)</h3>
            </div>
          </div>
        </div>

        {/* RIGHT: BUY/SELL CONTROLS */}
        <div className="col-span-4 space-y-6">
          <div className="bg-[#141414] border border-gray-800 rounded-2xl p-6">
            <div className="flex bg-gray-900 rounded-lg p-1 mb-6">
              <button className="flex-1 py-2 text-sm font-medium bg-gray-800 rounded-md shadow-sm">Limit</button>
              <button className="flex-1 py-2 text-sm font-medium text-gray-500">Market</button>
            </div>

            <div className="space-y-4">
              <div className="flex gap-2">
                <button className="flex-1 bg-green-600 hover:bg-green-500 text-white font-bold py-3 rounded-xl transition-colors">BUY</button>
                <button className="flex-1 bg-red-600/20 text-red-500 border border-red-500/30 hover:bg-red-600/30 font-bold py-3 rounded-xl transition-colors">SELL</button>
              </div>

              <div className="space-y-2">
                <label className="text-xs text-gray-500">Price</label>
                <input type="text" value="$3,900.25" readOnly className="w-full bg-gray-900 border border-gray-800 rounded-lg p-3 text-sm focus:outline-none" />
              </div>

              <div className="space-y-2">
                <label className="text-xs text-gray-500">Amount</label>
                <input type="number" placeholder="0.00" className="w-full bg-gray-900 border border-gray-800 rounded-lg p-3 text-sm focus:outline-none focus:border-orange-500" />
              </div>

              <button className="w-full bg-orange-500 hover:bg-orange-600 text-black font-bold py-4 rounded-xl mt-4 transition-all uppercase tracking-widest text-sm">
                Confirm Trade
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default Dashboard;