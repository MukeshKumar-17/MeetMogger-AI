import React from 'react';

interface TranscriptInputProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  onAnalyze: () => void;
  onLoadSample: () => void;
  isLoading: boolean;
}

const TranscriptInput: React.FC<TranscriptInputProps> = ({ value, onChange, onAnalyze, onLoadSample, isLoading }) => {
  return (
    <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-4 shadow-lg">
      <div className="flex justify-between items-center mb-2">
        <label htmlFor="transcript" className="font-bold text-lg text-gray-300">
          Call Transcript
        </label>
        <button
          onClick={onLoadSample}
          disabled={isLoading}
          className="text-sm text-gray-400 hover:text-white transition-colors disabled:opacity-50"
        >
          Load Sample
        </button>
      </div>
      <textarea
        id="transcript"
        value={value}
        onChange={onChange}
        placeholder="Paste your call transcript here..."
        className="w-full h-60 p-3 bg-gray-900 border border-gray-600 rounded-md focus:ring-2 focus:ring-gray-500 focus:outline-none transition-shadow text-gray-200 resize-y"
        disabled={isLoading}
      />
      <button
        onClick={onAnalyze}
        disabled={isLoading}
        className="mt-4 w-full bg-gradient-to-b from-gray-600 via-gray-700 to-gray-800 text-white font-bold py-3 px-4 rounded-lg shadow-lg border border-gray-600 hover:from-gray-500 hover:to-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-900 focus:ring-gray-500 active:translate-y-px transition-all duration-200 ease-in-out disabled:from-gray-800 disabled:to-gray-800 disabled:shadow-none disabled:border-gray-700 disabled:text-gray-500 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
      >
        {isLoading ? (
          <>
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>Analyzing...</span>
          </>
        ) : (
          <span>Analyze Call</span>
        )}
      </button>
    </div>
  );
};

export default TranscriptInput;