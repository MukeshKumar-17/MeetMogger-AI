import React from 'react';

interface SentimentVisualizerProps {
  polarity: 'Positive' | 'Negative' | 'Neutral';
  tones: string[];
}

const SentimentVisualizer: React.FC<SentimentVisualizerProps> = ({ polarity, tones }) => {
  const getPolarityClasses = () => {
    switch (polarity) {
      case 'Positive':
        return 'bg-green-900/50 text-green-200 border-green-800';
      case 'Negative':
        return 'bg-red-900/50 text-red-200 border-red-800';
      case 'Neutral':
        return 'bg-gray-800/50 text-gray-200 border-gray-700';
      default:
        return 'bg-gray-800/50 text-gray-200 border-gray-700';
    }
  };

  return (
    <div className={`p-4 rounded-lg border ${getPolarityClasses()}`}>
      <div className="flex items-center justify-between">
        <h4 className="font-bold text-lg">Overall Sentiment</h4>
        <span className={`px-3 py-1 text-sm font-semibold rounded-full ${getPolarityClasses()}`}>
          {polarity}
        </span>
      </div>
      {tones && tones.length > 0 && (
        <div className="mt-3">
          <h5 className="font-semibold text-sm mb-2 text-gray-400">Detected Tones:</h5>
          <div className="flex flex-wrap gap-2">
            {tones.map((tone, index) => (
              <span key={index} className="bg-black/50 text-gray-300 text-xs font-medium px-2.5 py-1 rounded-full border border-gray-700">
                {tone}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SentimentVisualizer;