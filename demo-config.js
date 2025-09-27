// Demo configuration for GitHub Pages
// This file provides mock data when running in demo mode

export const DEMO_MODE = true;

export const DEMO_USERS = [
  {
    id: 'demo-user-1',
    email: 'demo@meetmogger.ai',
    name: 'Demo User',
    password: 'demo123'
  }
];

export const DEMO_ANALYSIS = {
  theme: {
    classification: "Customer Support Inquiry",
    reasoning: "The conversation involves a customer seeking help with a technical issue and billing question."
  },
  sentiment: {
    polarity: "Neutral",
    tones: ["Helpful", "Professional", "Concerned"]
  },
  problems: [
    "Unable to access account dashboard",
    "Billing discrepancy on monthly statement",
    "Previous support ticket not resolved"
  ],
  solutions: [
    "Reset password and verify account access",
    "Review billing history and provide detailed breakdown",
    "Escalate to senior support team for resolution"
  ],
  actionItems: [
    "Send password reset email within 2 hours",
    "Provide billing statement by end of day",
    "Assign dedicated support agent for follow-up",
    "Schedule callback for tomorrow morning"
  ],
  summary: "Customer contacted support regarding account access issues and billing concerns. The representative provided immediate assistance with password reset and committed to resolving the billing discrepancy. A follow-up call was scheduled to ensure complete resolution of all issues."
};

export const DEMO_TRANSCRIPTS = [
  "Hi, I'm having trouble logging into my account. I've tried resetting my password but I'm still getting an error message. Also, I noticed a charge on my bill that doesn't look right. Can you help me with both of these issues?",
  "Thank you for calling customer support. I understand you're experiencing login issues and have a billing concern. Let me help you with both. First, let's get you back into your account, and then we'll review your billing statement together.",
  "I really appreciate your help. I've been trying to resolve this for days and I'm getting frustrated. The billing issue is particularly concerning because I don't recognize this charge.",
  "I completely understand your frustration, and I'm here to help resolve both issues today. Let me start by sending you a password reset email, and then we'll go through your billing statement line by line to identify that charge."
];
