import React, { useState } from 'react';

const ContactPage: React.FC = () => {
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    // Simulate network request
    setTimeout(() => {
        setLoading(false);
        setSubmitted(true);
    }, 1000);
  };

  if (submitted) {
    return (
      <div className="animate-fade-in-up">
        <div className="w-full max-w-lg mx-auto bg-gradient-to-b from-white/10 via-black/60 to-black/90 border border-white/20 rounded-xl p-8 shadow-lg backdrop-blur-sm text-center">
           <h2 className="text-3xl font-bold text-white mb-4">
            Thank You!
          </h2>
          <p className="text-gray-300">Your message has been sent. We'll get back to you shortly.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="animate-fade-in-up">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-lg mx-auto bg-gradient-to-b from-white/10 via-black/60 to-black/90 border border-white/20 rounded-xl p-8 shadow-lg backdrop-blur-sm"
      >
        <h2 className="text-3xl font-bold text-center text-white mb-6">
          Contact Us
        </h2>
        <div className="space-y-4">
          <div>
            <label htmlFor="name" className="sr-only">Name</label>
            <input type="text" id="name" placeholder="Your Name" required disabled={loading} className="w-full p-3 bg-black/50 border border-gray-700/60 rounded-md focus:ring-2 focus:ring-gray-400 focus:outline-none transition-shadow text-white placeholder-gray-400" />
          </div>
          <div>
            <label htmlFor="email" className="sr-only">Email</label>
            <input type="email" id="email" placeholder="Your Email" required disabled={loading} className="w-full p-3 bg-black/50 border border-gray-700/60 rounded-md focus:ring-2 focus:ring-gray-400 focus:outline-none transition-shadow text-white placeholder-gray-400" />
          </div>
          <div>
            <label htmlFor="message" className="sr-only">Message</label>
            <textarea id="message" placeholder="Your Message..." rows={5} required disabled={loading} className="w-full p-3 bg-black/50 border border-gray-700/60 rounded-md focus:ring-2 focus:ring-gray-400 focus:outline-none transition-shadow text-white placeholder-gray-400 resize-y"></textarea>
          </div>
        </div>
        <button
            type="submit"
            disabled={loading}
            className="mt-6 w-full bg-gradient-to-b from-gray-800/80 via-gray-900/80 to-black text-white font-bold py-3 px-4 rounded-lg shadow-lg border border-gray-700/80 hover:from-gray-700 hover:to-gray-800 active:translate-y-px transition-all duration-200 ease-in-out disabled:from-gray-900 disabled:to-black disabled:shadow-none disabled:border-gray-800 disabled:text-gray-600 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
        >
          {loading ? (
            <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Sending...</span>
            </>
          ) : (
            <span>Send Message</span>
          )}
        </button>
      </form>
    </div>
  );
};

export default ContactPage;
