import { createClient } from '@supabase/supabase-js';

// IMPORTANT: 
// 1. Go to your Supabase project dashboard.
// 2. Navigate to Project Settings > API.
// 3. Find your Project URL and the `anon` public key.
// 4. Replace the placeholder strings below with your actual credentials.

// FIX: Explicitly type supabaseUrl as string to avoid a TypeScript error where the inferred literal type makes the comparison against the placeholder string impossible.
const supabaseUrl: string = 'https://kjwhgvdehxuzbdrxjzbx.supabase.co'; 
const supabaseAnonKey: string = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtqd2hndmRlaHh1emJkcnhqemJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg5MjUwODIsImV4cCI6MjA3NDUwMTA4Mn0.ibcMwTsKmcfLJFVARk_lb3T3w0KCh65a4lWf8HVl1dI'; 

if (!supabaseUrl || supabaseUrl === 'YOUR_SUPABASE_URL') {
  console.error("Supabase URL is not configured. Please update lib/supabaseClient.ts");
}

if (!supabaseAnonKey || supabaseAnonKey === 'YOUR_SUPABASE_ANON_KEY') {
  console.error("Supabase Anon Key is not configured. Please update lib/supabaseClient.ts");
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);