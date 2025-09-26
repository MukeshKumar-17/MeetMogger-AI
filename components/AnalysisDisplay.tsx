import React from 'react';
import type { AnalysisResult } from '../types';
import { ClipboardIcon } from './icons/ClipboardIcon';
import { SentimentIcon } from './icons/SentimentIcon';
import { ProblemIcon } from './icons/ProblemIcon';
import { SolutionIcon } from './icons/SolutionIcon';
import { ActionIcon } from './icons/ActionIcon';
import { SummaryIcon } from './icons/SummaryIcon';

interface AnalysisDisplayProps {
  result: AnalysisResult;
}

const AnalysisSection: React.FC<{ title: string; icon: React.ReactNode; children: React.ReactNode }> = ({ title, icon, children }) => (
    <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-6 shadow-lg">
        <h2 className="text-xl font-bold text-gray-200 mb-4 flex items-center">
            <span className="mr-3 text-gray-400">{icon}</span>
            {title}
        </h2>
        <div className="text-gray-300 space-y-2">{children}</div>
    </div>
);


const AnalysisDisplay: React.FC<AnalysisDisplayProps> = ({ result }) => {
    const sentimentColor = 
        result.sentiment.polarity === 'Positive' ? 'text-green-400' :
        result.sentiment.polarity === 'Negative' ? 'text-red-400' : 'text-yellow-400';

  return (
    <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <AnalysisSection title="Call Theme" icon={<ClipboardIcon />}>
                <p className="font-semibold text-lg text-gray-100">{result.theme.classification}</p>
                <p className="text-gray-400">{result.theme.reasoning}</p>
            </AnalysisSection>
             <AnalysisSection title="Sentiment Analysis" icon={<SentimentIcon />}>
                <p><strong>Polarity:</strong> <span className={`font-bold ${sentimentColor}`}>{result.sentiment.polarity}</span></p>
                <div className="flex flex-wrap gap-2 pt-1">
                    {result.sentiment.tones.map((tone, index) => (
                        <span key={index} className="bg-gray-700 text-gray-300 text-xs font-medium px-2.5 py-1 rounded-full">{tone}</span>
                    ))}
                </div>
            </AnalysisSection>
        </div>

      <AnalysisSection title="Problems Identified" icon={<ProblemIcon />}>
        {result.problems.length > 0 ? (
          <ul className="list-disc list-inside space-y-2">
            {result.problems.map((item, index) => <li key={index}>{item}</li>)}
          </ul>
        ) : (
          <p className="text-gray-500 italic">No specific problems were identified.</p>
        )}
      </AnalysisSection>

      <AnalysisSection title="Solutions Proposed" icon={<SolutionIcon />}>
        {result.solutions.length > 0 ? (
          <ul className="list-disc list-inside space-y-2">
            {result.solutions.map((item, index) => <li key={index}>{item}</li>)}
          </ul>
        ) : (
          <p className="text-gray-500 italic">No specific solutions were proposed.</p>
        )}
      </AnalysisSection>

      <AnalysisSection title="Action Items" icon={<ActionIcon />}>
        {result.actionItems.length > 0 ? (
          <ul className="list-disc list-inside space-y-2">
            {result.actionItems.map((item, index) => <li key={index}>{item}</li>)}
          </ul>
        ) : (
          <p className="text-gray-500 italic">No action items were assigned.</p>
        )}
      </AnalysisSection>

      <AnalysisSection title="Executive Summary" icon={<SummaryIcon />}>
        <p className="leading-relaxed">{result.summary}</p>
      </AnalysisSection>
    </div>
  );
};

export default AnalysisDisplay;