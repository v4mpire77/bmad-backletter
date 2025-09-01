import { createClient, type SupabaseClient } from '@supabase/supabase-js'

// Only create the client if environment variables are available
let supabase: SupabaseClient | null = null

if (typeof window !== 'undefined' && process.env.NEXT_PUBLIC_SUPABASE_URL && process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY) {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL.trim()
  const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY.trim()
  
  if (supabaseUrl && supabaseAnonKey) {
    supabase = createClient(supabaseUrl, supabaseAnonKey)
  }
}

// Export a function that returns the client or throws an error
export const getSupabaseClient = (): SupabaseClient => {
  if (!supabase) {
    throw new Error('Supabase client not initialized. Check environment variables.')
  }
  return supabase
}

// Export the client directly for backward compatibility (but it might be null)
export { supabase }


