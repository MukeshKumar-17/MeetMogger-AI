import React from 'react';

const ProfilePage: React.FC = () => {
  return (
    <div className="animate-fade-in-up">
      <div className="w-full max-w-lg mx-auto bg-gradient-to-b from-white/10 via-black/60 to-black/90 border border-white/20 rounded-xl p-8 shadow-lg backdrop-blur-sm">
        <h2 className="text-3xl font-bold text-center text-white mb-6">
          My Profile
        </h2>
        <div className="space-y-4 text-lg">
          <div className="flex justify-between border-b border-gray-700/50 pb-2">
            <span className="font-semibold text-gray-300">Email:</span>
            <span className="text-white">admin@demo.com</span>
          </div>
          <div className="flex justify-between border-b border-gray-700/50 pb-2">
            <span className="font-semibold text-gray-300">Username:</span>
            <span className="text-white">Demo User</span>
          </div>
          <div className="flex justify-between">
            <span className="font-semibold text-gray-300">Plan:</span>
            <span className="text-white">Premium</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
