import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface AuthProps {
  onLoginSuccess: () => void;
}

const Auth: React.FC<AuthProps> = ({ onLoginSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [isLogin, setIsLogin] = useState(true);
  const { login, register } = useAuth();

  const handleAuth = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      let result;
      if (isLogin) {
        result = await login(email, password);
      } else {
        if (!name.trim()) {
          setError('Name is required for registration');
          setLoading(false);
          return;
        }
        result = await register(name, email, password);
      }

      if (result.success) {
        onLoginSuccess();
      } else {
        setError(result.message);
      }
    } catch (error) {
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center font-content">
      <div className="w-full max-w-md bg-gradient-to-b from-white/10 via-black/60 to-black/90 border border-white/20 rounded-xl p-8 shadow-lg backdrop-blur-sm">
        <h2 className="text-2xl font-bold text-center text-white mb-2">
          {isLogin ? 'Sign In' : 'Create Account'}
        </h2>
        <p className="text-center text-gray-300 mb-6">
          {isLogin ? 'Enter your credentials to sign in.' : 'Create a new account to get started.'}
        </p>
        
        <form onSubmit={handleAuth} className="space-y-4">
          {!isLogin && (
            <div>
              <label htmlFor="name" className="sr-only">Name</label>
              <input
                id="name"
                className="w-full p-3 bg-black/50 border border-gray-700/60 rounded-md focus:ring-2 focus:ring-gray-400 focus:outline-none transition-shadow text-white placeholder-gray-400"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Your Name"
                required={!isLogin}
                disabled={loading}
              />
            </div>
          )}
          
          <div>
            <label htmlFor="email" className="sr-only">Email</label>
            <input
              id="email"
              className="w-full p-3 bg-black/50 border border-gray-700/60 rounded-md focus:ring-2 focus:ring-gray-400 focus:outline-none transition-shadow text-white placeholder-gray-400"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
              required
              disabled={loading}
            />
          </div>
          
          <div>
            <label htmlFor="password" className="sr-only">Password</label>
            <input
              id="password"
              className="w-full p-3 bg-black/50 border border-gray-700/60 rounded-md focus:ring-2 focus:ring-gray-400 focus:outline-none transition-shadow text-white placeholder-gray-400"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password (min 6 characters)"
              required
              disabled={loading}
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-b from-gray-800/80 via-gray-900/80 to-black text-white font-bold py-3 px-4 rounded-lg shadow-lg border border-gray-700/80 hover:from-gray-700 hover:to-gray-800 active:translate-y-px transition-all duration-200 ease-in-out disabled:from-gray-900 disabled:to-black disabled:shadow-none disabled:border-gray-800 disabled:text-gray-600 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>{isLogin ? 'Signing In...' : 'Creating Account...'}</span>
              </>
            ) : (
              <span>{isLogin ? 'Sign In' : 'Create Account'}</span>
            )}
          </button>
        </form>
        
        <div className="mt-4 text-center">
          <button
            type="button"
            onClick={() => {
              setIsLogin(!isLogin);
              setError('');
              setEmail('');
              setPassword('');
              setName('');
            }}
            className="text-gray-400 hover:text-white transition-colors text-sm"
          >
            {isLogin ? "Don't have an account? Sign up" : "Already have an account? Sign in"}
          </button>
        </div>
        
        {error && <p className="mt-4 text-center text-red-400">{error}</p>}
      </div>
    </div>
  );
};

export default Auth;
