import { GoogleGenAI, Type } from '@google/genai';
import type { AnalysisResult } from '../types';

// Initialize the Google Gemini API client.
// The API key is automatically sourced from the environment.
const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

// Define the exact JSON structure we expect from the Gemini API.
// This ensures the AI's response is always in a predictable, parseable format.
const analysisSchema = {
  type: Type.OBJECT,
  properties: {
    theme: {
      type: Type.OBJECT,
      description: 'Classification of the call\'s main topic and reasoning.',
      properties: {
        classification: {
          type: Type.STRING,
          description: 'A short, descriptive category for the call (e.g., "Internet Connection Issue", "Billing Inquiry").',
        },
        reasoning: {
          type: Type.STRING,
          description: 'A brief explanation for why this classification was chosen.',
        },
      },
      required: ['classification', 'reasoning'],
    },
    sentiment: {
      type: Type.OBJECT,
      description: 'Analysis of the overall sentiment and emotional tones in the conversation.',
      properties: {
        polarity: {
          type: Type.STRING,
          description: 'The dominant sentiment of the call.',
          enum: ['Positive', 'Negative', 'Neutral'],
        },
        tones: {
          type: Type.ARRAY,
          description: 'A list of emotional tones detected (e.g., "Frustrated", "Relieved", "Helpful").',
          items: { type: Type.STRING },
        },
      },
      required: ['polarity', 'tones'],
    },
    problems: {
      type: Type.ARRAY,
      description: 'A list of specific problems or issues mentioned by the customer.',
      items: { type: Type.STRING },
    },
    solutions: {
      type: Type.ARRAY,
      description: 'A list of solutions or fixes proposed by the agent.',
      items: { type: Type.STRING },
    },
    actionItems: {
      type: Type.ARRAY,
      description: 'A list of concrete next steps or follow-ups for either the agent or customer.',
      items: { type: Type.STRING },
    },
    summary: {
      type: Type.STRING,
      description: 'A concise, one-paragraph summary of the entire conversation from start to finish.',
    },
  },
  required: ['theme', 'sentiment', 'problems', 'solutions', 'actionItems', 'summary'],
};

export const analyzeCallTranscript = async (transcript: string): Promise<AnalysisResult> => {
  try {
    const prompt = `
      Analyze the following transcribed call conversation.
      Based on the content, provide a detailed analysis covering the call's theme, sentiment,
      identified problems, proposed solutions, any action items, and a final summary.
      Adhere strictly to the provided JSON schema for your response.

      Transcript to analyze:
      ---
      ${transcript}
      ---
    `;

    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
      config: {
        responseMimeType: 'application/json',
        responseSchema: analysisSchema,
      },
    });

    const jsonText = response.text;
    if (!jsonText) {
      throw new Error("Received an empty response from the Gemini API.");
    }

    // The response is already guaranteed to be a JSON string due to the config.
    const result = JSON.parse(jsonText);
    
    return result as AnalysisResult;

  } catch (error) {
    console.error("Error analyzing transcript with Gemini API:", error);
    const errorMessage = error instanceof Error ? error.message : "An unknown error occurred. Check the console for details.";
    throw new Error(`Failed to get analysis from Gemini API. ${errorMessage}`);
  }
};
