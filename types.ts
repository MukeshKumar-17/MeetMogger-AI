
export interface AnalysisResult {
  theme: {
    classification: string;
    reasoning: string;
  };
  sentiment: {
    polarity: 'Positive' | 'Negative' | 'Neutral';
    tones: string[];
  };
  problems: string[];
  solutions: string[];
  actionItems: string[];
  summary: string;
}
