import React from 'react';

const Loader: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center p-8 bg-gray-800/50 border border-gray-700 rounded-xl">
      <div className="w-12 h-12 border-4 border-gray-400 border-t-transparent rounded-full animate-spin"></div>
      <p className="mt-4 text-gray-300 text-lg">Analyzing transcript, please wait...</p>
    </div>
  );
};

export default Loader;