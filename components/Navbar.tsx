import React from 'react';
import type { Page } from '../../App';

interface NavbarProps {
  isLoggedIn: boolean;
  onSignOut: () => void;
  currentPage: Page;
  onNavigate: (page: Page) => void;
}

const NavLink: React.FC<{
  page: Page;
  currentPage: Page;
  onNavigate: (page: Page) => void;
  children: React.ReactNode;
}> = ({ page, currentPage, onNavigate, children }) => {
  const isActive = currentPage === page;
  return (
    <button
      onClick={() => onNavigate(page)}
      className={`font-semibold transition-colors text-base ${isActive ? 'text-white' : 'text-gray-400 hover:text-white'}`}
    >
      {children}
    </button>
  );
};


const Navbar: React.FC<NavbarProps> = ({ isLoggedIn, onSignOut, currentPage, onNavigate }) => {
  return (
    <nav className="w-full py-5 z-20 fixed top-0 bg-gradient-to-b from-white/5 via-black/30 to-black/60 backdrop-blur-xl border-b border-white/10">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-[1fr_auto_1fr] items-center gap-8">
        {/* Left Aligned Links */}
        <div className="flex justify-start items-center space-x-6">
            <NavLink page="home" currentPage={currentPage} onNavigate={onNavigate}>Home</NavLink>
            {isLoggedIn && (
              <>
                <NavLink page="analyze" currentPage={currentPage} onNavigate={onNavigate}>Analyze</NavLink>
                <NavLink page="profile" currentPage={currentPage} onNavigate={onNavigate}>Profile</NavLink>
              </>
            )}
            <NavLink page="contact" currentPage={currentPage} onNavigate={onNavigate}>Contact</NavLink>
        </div>

        {/* Centered Title */}
        <div className="text-center px-4">
            <h1 className="text-3xl sm:text-4xl font-extrabold font-title whitespace-nowrap">
              MeetMogger AI
            </h1>
        </div>

        {/* Right Aligned Sign Out Button */}
        <div className="flex justify-end">
          {isLoggedIn && (
            <button
              onClick={onSignOut}
              className="bg-gray-800/80 hover:bg-gray-700/80 text-white font-bold py-2 px-4 rounded-lg text-sm border border-gray-700/80 transition-colors"
            >
              Sign Out
            </button>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;