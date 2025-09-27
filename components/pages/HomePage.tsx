import React from 'react';
import type { Page } from '../../../App';

interface HomePageProps {
  onNavigate: (page: Page) => void;
}

const HomePage: React.FC<HomePageProps> = ({ onNavigate }) => {
  return (
    <div className="text-center space-y-12 animate-fade-in-up">
      <div className="bg-gradient-to-b from-white/10 via-black/60 to-black/90 border border-white/20 rounded-xl p-8 shadow-lg backdrop-blur-sm">
        <h1 className="text-4xl sm:text-5xl font-extrabold text-white mb-4">
          Unlock Insights from Every Conversation
        </h1>
        <p className="max-w-2xl mx-auto text-lg text-gray-300 mb-8">
          MeetMogger AI analyzes your call transcripts to provide deep insights instantly.
          Classify themes, gauge sentiment, and extract actionable items to drive your business forward.
        </p>
        <button
          onClick={() => onNavigate('analyze')}
          className="bg-gradient-to-b from-gray-800/80 via-gray-900/80 to-black text-white font-bold py-3 px-8 rounded-lg shadow-lg border border-gray-700/80 hover:from-gray-700 hover:to-gray-800 active:translate-y-px transition-all duration-200 ease-in-out text-lg"
        >
          Get Started
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <FeatureCard title="Theme Classification" description="Automatically categorize calls by their primary topic for better trend analysis." />
        <FeatureCard title="Sentiment Analysis" description="Understand customer mood and tone to improve service and identify at-risk clients." />
        <FeatureCard title="Actionable Extraction" description="Never miss a follow-up. We pull out problems, solutions, and action items for you." />
      </div>
    </div>
  );
};

interface FeatureCardProps {
  title: string;
  description: string;
}

const FeatureCard: React.FC<FeatureCardProps> = ({ title, description }) => (
  <div className="bg-gradient-to-b from-white/10 via-black/60 to-black/90 border border-white/20 rounded-xl p-6 shadow-lg backdrop-blur-sm h-full">
    <h3 className="text-xl font-bold mb-2 text-white">{title}</h3>
    <p className="text-gray-300">{description}</p>
  </div>
);

export default HomePage;
