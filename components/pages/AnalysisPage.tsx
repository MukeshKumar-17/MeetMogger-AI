import React, { useState, useCallback } from 'react';
import type { AnalysisResult } from '../../types';
import { analyzeCallTranscript } from '../../services/geminiService';
import TranscriptInput from '../TranscriptInput';
import AnalysisDisplay from '../AnalysisDisplay';
import Loader from '../Loader';

const AnalysisPage: React.FC = () => {
  const [transcript, setTranscript] = useState<string>('');
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const sampleTranscript = `Distributor: Thanks for joining today. Before we dive in, I want to highlight recurring stock shortages in the southwest region—they’re really slowing us down.
Vendor: I hear you. We’ve had similar feedback from others and are looking at optimizing the supply chain. Could you specify which SKUs are affected most?
Distributor: Mostly health and wellness products. Also, our training team still hasn’t received the updated product manuals.
Vendor: Apologies for that. I’ll ensure the new documentation is resent today. Anything else holding back your sales?
Distributor: Yes, we’re struggling to access co-marketing funds for Q4 campaigns. The application portal seems buggy.
Vendor: That’s on our radar—we’re working with IT on a fix. I can escalate your access to the marketing lead after this call.
Distributor: Appreciate it. For next month, it’d help if we could schedule a technical workshop, especially for the new AI-powered offerings.
Vendor: Absolutely, I’ll coordinate with our solution engineers and come back with dates. Is mid-October reasonable?
Distributor: That would be perfect. One last thing: end-customer feedback suggests our service response times could be faster.
Vendor: Thanks for flagging it. I’ll set up a review with our support team and include you on the tracking thread. Anything else urgent?
Distributor: That covers my big topics. Thanks for being proactive—this is exactly the follow-up we need.
Vendor: Likewise, thanks for the clear feedback. I’ll send detailed action items by end of day.`;

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
    <main className="space-y-6 font-content">
      <TranscriptInput
        value={transcript}
        onChange={(e) => setTranscript(e.target.value)}
        onAnalyze={handleAnalyze}
        onLoadSample={loadSample}
        isLoading={isLoading}
      />

      {error && (
        <div className="bg-gradient-to-b from-red-900/50 via-red-950/50 to-black/80 border border-red-700 text-red-200 px-4 py-3 rounded-lg text-center backdrop-blur-sm" role="alert">
          <strong className="font-bold">Error: </strong>
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      {isLoading && <Loader />}

      {analysisResult && (
        <AnalysisDisplay result={analysisResult} />
      )}
    </main>
  );
}

export default AnalysisPage;