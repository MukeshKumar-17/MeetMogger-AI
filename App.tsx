import React, { useState, useCallback } from 'react';
import type { AnalysisResult } from './types';
import { analyzeCallTranscript } from './services/geminiService';
import TranscriptInput from './components/TranscriptInput';
import AnalysisDisplay from './components/AnalysisDisplay';
import Loader from './components/Loader';

const App: React.FC = () => {
  const [transcript, setTranscript] = useState<string>('');
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  const sampleTranscript = `Agent: Thank you for calling Tech Support, this is Alex. How can I help you today?
Customer: Hi Alex, my name is Sarah. I'm having a serious issue with my internet connection. It's been dropping every 5 minutes for the past two hours. I can't get any work done.
Agent: I'm very sorry to hear that, Sarah. That sounds incredibly frustrating. I can definitely help you with that. Can you please provide me with your account number?
Customer: Yes, it's 555-1234.
Agent: Thank you. I'm looking at your connection status now... I see some intermittent signal loss. It looks like there might be an issue with the local node. A few of your neighbors are experiencing similar problems.
Customer: Oh, so it's not just me? That's a relief, I guess. What's the solution?
Agent: We have a maintenance team scheduled to work on the node. The first step is for you to try a full power cycle of your modem. Unplug it for 60 seconds and then plug it back in. This often resolves the immediate issue by forcing a new connection.
Customer: Okay, I can do that right now.
(Pause)
Customer: Alright, I've plugged it back in. The lights are blinking.
Agent: Great. Let me check the signal from my end... It looks much stronger now! The connection seems stable. We will still have the team check the node to prevent this from happening again. I will schedule a follow-up call with you tomorrow to confirm everything is still working perfectly.
Customer: Wow, that's great. Thank you so much for the quick help, Alex.
Agent: You're very welcome, Sarah. Is there anything else I can assist you with today?
Customer: No, that's all. Thanks again.
Agent: Have a great day!`;


  const handleAnalyze = useCallback(async () => {
    if (!transcript.trim()) {
      setError("Please enter a transcript to analyze.");
      return;
    }
    setIsLoading(true);
    setError(null);
    setAnalysisResult(null);

    try {
      const result = await analyzeCallTranscript(transcript);
      setAnalysisResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An unknown error occurred.");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, [transcript]);

  const loadSample = () => {
    setTranscript(sampleTranscript);
    setError(null);
    setAnalysisResult(null);
  }

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 font-sans flex flex-col items-center p-4 sm:p-6 lg:p-8">
      <div className="w-full max-w-4xl">
        <header className="text-center mb-8">
          <h1 className="text-4xl sm:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-gray-300 via-gray-400 to-gray-500">
            MeetMogger AI
          </h1>
        </header>

        <main className="space-y-6">
          <TranscriptInput
            value={transcript}
            onChange={(e) => setTranscript(e.target.value)}
            onAnalyze={handleAnalyze}
            onLoadSample={loadSample}
            isLoading={isLoading}
          />

          {error && (
            <div className="bg-red-900/50 border border-red-700 text-red-300 px-4 py-3 rounded-lg text-center" role="alert">
              <strong className="font-bold">Error: </strong>
              <span className="block sm:inline">{error}</span>
            </div>
          )}

          {isLoading && <Loader />}

          {analysisResult && (
            <div className="animate-fade-in">
              <AnalysisDisplay result={analysisResult} />
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default App;