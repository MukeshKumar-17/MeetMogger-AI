import React from 'react';

const Loader: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center p-8 bg-gradient-to-b from-white/10 via-black/60 to-black/90 border border-white/20 rounded-xl backdrop-blur-sm">
      <div className="w-12 h-12 border-4 border-white border-t-transparent rounded-full animate-spin"></div>
      <p className="mt-4 text-white text-lg">Analyzing transcript, please wait...</p>
    </div>
  );
};

export default Loader;