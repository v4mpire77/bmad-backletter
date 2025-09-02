'use client'

/*
 * Authentication Context Provider
 * 
 * Provides authentication state and methods throughout the application.
 * Follows Context Engineering Framework standards for consistency and maintainability.
 * 
 * Features:
 * - User session management
 * - Authentication state tracking
 * - Sign up/in/out functionality
 * - Password reset handling
 * 
 * Performance Targets:
 * - Auth state changes: < 100ms
 * - Sign in/up operations: < 1s
 */

import { createContext, useContext, useEffect, useState } from 'react'
import { User, Session, AuthChangeEvent } from '@supabase/supabase-js'
import { createSupabaseClient } from '@/lib/supabase'

interface AuthContextType {
  user: User | null
  session: Session | null
  loading: boolean
  signUp: (email: string, password: string, metadata?: object) => Promise<any>
  signIn: (email: string, password: string) => Promise<any>
  signOut: () => Promise<any>
  resetPassword: (email: string) => Promise<any>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [session, setSession] = useState<Session | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Only initialize Supabase on the client side
    if (typeof window === 'undefined') {
      setLoading(false)
      return
    }

    try {
      const supabase = createSupabaseClient()
      
      // Get initial session
      const getSession = async () => {
        const { data: { session } } = await supabase.auth.getSession()
        setSession(session)
        setUser(session?.user ?? null)
        setLoading(false)
      }

      getSession()

      // Listen for auth changes
      const { data: { subscription } } = supabase.auth.onAuthStateChange(
        async (event: AuthChangeEvent, session: Session | null) => {
          setSession(session)
          setUser(session?.user ?? null)
          setLoading(false)
        }
      )

      return () => subscription.unsubscribe()
    } catch (error) {
      console.warn('Supabase not available:', error)
      setLoading(false)
    }
  }, [])

  const signUp = async (email: string, password: string, metadata?: object) => {
    const startTime = performance.now()
    try {
      const supabase = createSupabaseClient()
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: metadata,
        },
      })
      const duration = performance.now() - startTime
      console.debug(`Sign up operation completed in ${duration}ms`)
      return { data, error }
    } catch (e) {
      const duration = performance.now() - startTime
      console.error(`Sign up failed after ${duration}ms:`, e)
      return { data: null, error: e as Error }
    }
  }

  const signIn = async (email: string, password: string) => {
    const startTime = performance.now()
    try {
      const supabase = createSupabaseClient()
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      })
      const duration = performance.now() - startTime
      console.debug(`Sign in operation completed in ${duration}ms`)
      return { data, error }
    } catch (e) {
      const duration = performance.now() - startTime
      console.error(`Sign in failed after ${duration}ms:`, e)
      return { data: null, error: e as Error }
    }
  }

  const signOut = async () => {
    const startTime = performance.now()
    try {
      const supabase = createSupabaseClient()
      const { error } = await supabase.auth.signOut()
      const duration = performance.now() - startTime
      console.debug(`Sign out operation completed in ${duration}ms`)
      return { error }
    } catch (e) {
      const duration = performance.now() - startTime
      console.error(`Sign out failed after ${duration}ms:`, e)
      return { error: e as Error }
    }
  }

  const resetPassword = async (email: string) => {
    const startTime = performance.now()
    try {
      const supabase = createSupabaseClient()
      const { data, error } = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: `${window.location.origin}/auth/reset-password`,
      })
      const duration = performance.now() - startTime
      console.debug(`Password reset operation completed in ${duration}ms`)
      return { data, error }
    } catch (e) {
      const duration = performance.now() - startTime
      console.error(`Password reset failed after ${duration}ms:`, e)
      return { data: null, error: e as Error }
    }
  }

  const value = {
    user,
    session,
    loading,
    signUp,
    signIn,
    signOut,
    resetPassword,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
