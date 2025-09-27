import React from 'react';
import type { AnalysisResult } from '../types';
import { ClipboardIcon } from './icons/ClipboardIcon';
import { SentimentIcon } from './icons/SentimentIcon';
import { ProblemIcon } from './icons/ProblemIcon';
import { SolutionIcon } from './icons/SolutionIcon';
import { ActionIcon } from './icons/ActionIcon';
import { SummaryIcon } from './icons/SummaryIcon';
import { DownloadIcon } from './icons/DownloadIcon';

interface AnalysisDisplayProps {
  result: AnalysisResult;
}

const AnalysisDisplay: React.FC<AnalysisDisplayProps> = ({ result }) => {
  const handleDownloadActionItems = () => {
    const jsonString = `data:text/json;charset=utf-8,${encodeURIComponent(
      JSON.stringify({ actionItems: result.actionItems }, null, 2)
    )}`;
    const link = document.createElement('a');
    link.href = jsonString;
    link.download = 'action_items.json';
    link.click();
  };

  interface CardProps {
    icon: React.ReactNode;
    title: string;
    children: React.ReactNode;
    className?: string;
    style?: React.CSSProperties;
  }

  const Card: React.FC<CardProps> = ({ icon, title, children, className = '', style }) => (
    <div
      className={`bg-gradient-to-b from-white/10 via-black/60 to-black/90 border border-white/20 rounded-xl shadow-lg overflow-hidden backdrop-blur-sm ${className}`}
      style={style}
    >
      <div className="p-4 bg-black/50 flex items-center space-x-3 border-b border-gray-800/60">
        <div className="text-gray-400">{icon}</div>
        <h3 className="text-xl font-bold text-gray-100">{title}</h3>
      </div>
      <div className="p-4 text-white">
        {children}
      </div>
    </div>
  );
  
  interface ListCardProps {
    icon: React.ReactNode;
    title: string;
    items: string[];
    className?: string;
    style?: React.CSSProperties;
  }

  const ListCard: React.FC<ListCardProps> = ({ icon, title, items, className, style }) => {
    if (!items || items.length === 0) return null;
    return (
      <Card icon={icon} title={title} className={className} style={style}>
        <ul className="space-y-2 list-disc list-inside">
          {items.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </Card>
    );
  };
  
  const getSentimentContainerClasses = () => {
    switch (result.sentiment.polarity) {
      case 'Positive':
        return 'bg-gradient-to-br from-green-900/40 to-black/60 border-green-800/50';
      case 'Negative':
        return 'bg-gradient-to-br from-red-900/40 to-black/60 border-red-800/50';
      default:
        return 'bg-gradient-to-br from-gray-800/40 to-black/60 border-gray-700/50';
    }
  };

  const getSentimentPillClasses = () => {
    switch (result.sentiment.polarity) {
        case 'Positive': return 'bg-green-900/70 text-green-200';
        case 'Negative': return 'bg-red-900/70 text-red-200';
        default: return 'bg-gray-800/70 text-gray-300';
    }
  };

  const animationClass = "opacity-0 animate-fade-in-up will-change-transform-opacity";
  let visibleChildIndex = 0;

  return (
    <div className="space-y-6">
      <Card 
        icon={<ClipboardIcon />} 
        title="Call Theme"
        className={animationClass}
        style={{ animationDelay: `${visibleChildIndex++ * 100}ms` }}
      >
        <h4 className="font-bold text-lg text-gray-100 mb-1">{result.theme.classification}</h4>
        <p className="text-gray-300">{result.theme.reasoning}</p>
      </Card>

      <Card
        icon={<SentimentIcon />}
        title="Sentiment Analysis"
        className={animationClass}
        style={{ animationDelay: `${visibleChildIndex++ * 100}ms` }}
      >
        <div className={`p-4 rounded-lg border ${getSentimentContainerClasses()}`}>
          <div className="flex items-center justify-between">
            <h4 className="font-bold text-lg">Overall Sentiment</h4>
            <span className={`px-3 py-1 text-sm font-semibold rounded-full ${getSentimentPillClasses()}`}>
              {result.sentiment.polarity}
            </span>
          </div>
          {result.sentiment.tones && result.sentiment.tones.length > 0 && (
            <div className="mt-3">
              <h5 className="font-semibold text-sm mb-2 text-gray-200">Detected Tones:</h5>
              <div className="flex flex-wrap gap-2">
                {result.sentiment.tones.map((tone, index) => (
                  <span key={index} className="bg-black/50 text-gray-200 text-xs font-medium px-2.5 py-1 rounded-full border border-gray-800/60">
                    {tone}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </Card>

      {result.problems && result.problems.length > 0 && (
        <ListCard
          icon={<ProblemIcon />}
          title="Identified Problems"
          items={result.problems}
          className={animationClass}
          style={{ animationDelay: `${visibleChildIndex++ * 100}ms` }}
        />
      )}

      {result.solutions && result.solutions.length > 0 && (
        <ListCard
          icon={<SolutionIcon />}
          title="Proposed Solutions"
          items={result.solutions}
          className={animationClass}
          style={{ animationDelay: `${visibleChildIndex++ * 100}ms` }}
        />
      )}
      
      {result.actionItems && result.actionItems.length > 0 && (
        <Card
          icon={<ActionIcon />}
          title="Action Items"
          className={animationClass}
          style={{ animationDelay: `${visibleChildIndex++ * 100}ms` }}
        >
          <div className="flex flex-col">
            <ul className="space-y-2 list-disc list-inside mb-4">
              {result.actionItems.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
            <button
              onClick={handleDownloadActionItems}
              className="self-end flex items-center gap-2 text-sm bg-gray-900/50 hover:bg-gray-800/80 text-white font-semibold py-2 px-3 rounded-lg transition-colors border border-gray-700/50"
              aria-label="Download action items as JSON"
            >
              <DownloadIcon />
              Download as JSON
            </button>
          </div>
        </Card>
      )}

      <Card
        icon={<SummaryIcon />}
        title="Conversation Summary"
        className={animationClass}
        style={{ animationDelay: `${visibleChildIndex++ * 100}ms` }}
      >
        <p className="whitespace-pre-wrap">{result.summary}</p>
      </Card>
    </div>
  );
};

export default AnalysisDisplay;