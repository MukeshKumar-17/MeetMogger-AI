import React, { useState } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Auth from './components/Auth';
import Navbar from './components/Navbar';
import MatrixRain from './components/MatrixRain';
import HomePage from './components/pages/HomePage';
import AnalysisPage from './components/pages/AnalysisPage';
import ProfilePage from './components/pages/ProfilePage';
import ContactPage from './components/pages/ContactPage';

export type Page = 'home' | 'analyze' | 'profile' | 'contact';

const AppContent: React.FC = () => {
  const { user, logout, isLoading } = useAuth();
  const [currentPage, setCurrentPage] = useState<Page>('home');

  const handleSignOut = () => {
    logout();
    setCurrentPage('home');
  };
  
  const handleLoginSuccess = () => {
    // After login, direct to the main feature, the analysis page.
    setCurrentPage('analyze');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-white"></div>
      </div>
    );
  }
  
  const renderContent = () => {
    const protectedPages: Page[] = ['analyze', 'profile'];
    
    // If user is not logged in and tries to access a protected page, show the login form.
    if (!user && protectedPages.includes(currentPage)) {
      return <Auth onLoginSuccess={handleLoginSuccess} />;
    }

    switch (currentPage) {
      case 'home':
        return <HomePage onNavigate={(page) => setCurrentPage(page)} />;
      case 'analyze':
        return <AnalysisPage />;
      case 'profile':
        return <ProfilePage />;
      case 'contact':
        return <ContactPage />;
      default:
        return <HomePage onNavigate={(page) => setCurrentPage(page)} />;
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center">
      <MatrixRain />
      <Navbar
        isLoggedIn={!!user}
        onSignOut={handleSignOut}
        currentPage={currentPage}
        onNavigate={setCurrentPage}
      />
      
      <div className="w-full max-w-4xl z-10 relative pt-24 pb-8 px-4 sm:px-6 lg:px-8">
        {renderContent()}
      </div>
    </div>
  );
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
};

export default App;