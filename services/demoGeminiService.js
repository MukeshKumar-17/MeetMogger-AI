import { DEMO_ANALYSIS, DEMO_TRANSCRIPTS } from '../demo-config.js';

export const analyzeCallTranscript = async (transcript) => {
  try {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Return demo analysis with some randomization
    const analysis = { ...DEMO_ANALYSIS };
    
    // Add some variation to make it feel more realistic
    const variations = [
      {
        theme: {
          classification: "Technical Support Request",
          reasoning: "The conversation involves technical troubleshooting and system access issues."
        }
      },
      {
        theme: {
          classification: "Billing Inquiry",
          reasoning: "The customer is seeking clarification about charges and payment issues."
        }
      },
      {
        theme: {
          classification: "Product Information Request",
          reasoning: "The customer is asking about features and capabilities of the service."
        }
      }
    ];
    
    const randomVariation = variations[Math.floor(Math.random() * variations.length)];
    analysis.theme = randomVariation.theme;
    
    // Add some random sentiment variations
    const sentimentOptions = [
      { polarity: "Positive", tones: ["Satisfied", "Helpful", "Grateful"] },
      { polarity: "Neutral", tones: ["Professional", "Informative", "Calm"] },
      { polarity: "Negative", tones: ["Frustrated", "Concerned", "Impatient"] }
    ];
    
    const randomSentiment = sentimentOptions[Math.floor(Math.random() * sentimentOptions.length)];
    analysis.sentiment = randomSentiment;
    
    // Add some variation to problems and solutions
    const problemVariations = [
      "Account access issues",
      "Payment processing error",
      "Feature not working as expected",
      "Data synchronization problem",
      "User interface confusion"
    ];
    
    const solutionVariations = [
      "Clear step-by-step troubleshooting guide",
      "Account verification process",
      "Feature demonstration and training",
      "Technical support escalation",
      "Alternative solution provided"
    ];
    
    // Randomly select some problems and solutions
    const numProblems = Math.floor(Math.random() * 3) + 1;
    const numSolutions = Math.floor(Math.random() * 3) + 1;
    
    analysis.problems = problemVariations
      .sort(() => 0.5 - Math.random())
      .slice(0, numProblems);
      
    analysis.solutions = solutionVariations
      .sort(() => 0.5 - Math.random())
      .slice(0, numSolutions);
    
    // Update summary to reflect the variations
    analysis.summary = `Customer contacted support regarding ${analysis.theme.classification.toLowerCase()}. The conversation involved ${analysis.sentiment.polarity.toLowerCase()} sentiment with ${analysis.problems.length} identified issues and ${analysis.solutions.length} proposed solutions. The representative provided comprehensive assistance and scheduled appropriate follow-up actions.`;
    
    return analysis;
    
  } catch (error) {
    console.error("Demo analysis error:", error);
    throw new Error("Demo analysis failed. Please try again.");
  }
};
