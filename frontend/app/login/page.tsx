'use client';

import { useState } from 'react';
import { ArrowRight, Lock, Mail, User } from 'lucide-react';
import NetworkBackground from '@/components/NetworkBackground';
import Link from 'next/link';

export default function LoginPage() {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Real auth integration would go here
    console.log(isRegister ? 'Registering' : 'Logging in', { email, password });
  };

  return (
    <div className="relative min-h-screen w-full flex items-center justify-center overflow-hidden font-sans text-gray-800">
      {/* ── BACKGROUND ANIMATION ── */}
      <NetworkBackground />

      {/* ── FOREGROUND UI ── */}
      <main className="relative z-10 w-full max-w-md p-6">
        
        {/* Glassmorphism Card */}
        <div className="bg-white/60 backdrop-blur-xl border border-white/50 rounded-3xl shadow-[0_8px_32px_rgb(0,0,0,0.05)] p-8 md:p-10 transform transition-all hover:shadow-[0_16px_40px_rgb(0,0,0,0.08)]">
          
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-br from-purple-100 to-blue-50 text-indigo-500 mb-4 shadow-sm border border-white">
               <SparklesIcon />
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-gray-900">
              Almatti AI Workforce
            </h1>
            <p className="text-sm text-gray-500 mt-2 font-medium">
              {isRegister ? 'Create an account to access the cluster' : 'Sign in to your intelligence dashboard'}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Email */}
            <div className="space-y-1">
              <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider pl-1">Email</label>
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400 group-focus-within:text-purple-500 transition-colors">
                  <Mail size={18} />
                </div>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-white/80 border border-gray-200 text-gray-800 rounded-xl pl-10 pr-4 py-3 text-sm focus:ring-4 focus:ring-purple-500/10 focus:border-purple-300 outline-none transition-all shadow-sm"
                  placeholder="you@company.com"
                  required
                />
              </div>
            </div>

            {/* Password */}
            <div className="space-y-1">
              <div className="flex justify-between items-center pl-1">
                <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Password</label>
                {!isRegister && <a href="#" className="text-xs text-purple-600 hover:text-purple-700 font-medium">Forgot?</a>}
              </div>
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400 group-focus-within:text-purple-500 transition-colors">
                  <Lock size={18} />
                </div>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-white/80 border border-gray-200 text-gray-800 rounded-xl pl-10 pr-4 py-3 text-sm focus:ring-4 focus:ring-purple-500/10 focus:border-purple-300 outline-none transition-all shadow-sm"
                  placeholder="••••••••"
                  required
                />
              </div>
            </div>

            {/* Confirm Password (Register Only) */}
            {isRegister && (
              <div className="space-y-1 animate-in slide-in-from-top-2 fade-in duration-300">
                <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider pl-1">Confirm Password</label>
                <div className="relative group">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400 group-focus-within:text-purple-500 transition-colors">
                    <Lock size={18} />
                  </div>
                  <input
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full bg-white/80 border border-gray-200 text-gray-800 rounded-xl pl-10 pr-4 py-3 text-sm focus:ring-4 focus:ring-purple-500/10 focus:border-purple-300 outline-none transition-all shadow-sm"
                    placeholder="••••••••"
                    required={isRegister}
                  />
                </div>
              </div>
            )}

            {/* Submit Button */}
            <Link href="/" className="block mt-6">
              <button
                type="button" 
                className="w-full bg-gradient-to-r from-gray-900 to-black hover:from-gray-800 hover:to-gray-900 text-white py-3.5 rounded-xl font-semibold text-sm flex justify-center items-center gap-2 shadow-[0_4px_14px_0_rgba(0,0,0,0.1)] hover:shadow-[0_6px_20px_0_rgba(0,0,0,0.15)] hover:-translate-y-[1px] transition-all"
              >
                {isRegister ? 'Create Account' : 'Access Dashboard'}
                <ArrowRight size={16} />
              </button>
            </Link>
          </form>

          {/* Toggle Register/Login */}
          <div className="mt-8 text-center">
            <p className="text-sm text-gray-500">
              {isRegister ? 'Already have an account?' : "Don't have an account?"}{' '}
              <button
                onClick={() => setIsRegister(!isRegister)}
                className="font-semibold text-purple-600 hover:text-purple-800 transition-colors underline-offset-4 hover:underline"
              >
                {isRegister ? 'Log in' : 'Register now'}
              </button>
            </p>
          </div>

        </div>
      </main>
    </div>
  );
}

function SparklesIcon() {
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>
      <path d="M5 3v4"/>
      <path d="M19 17v4"/>
      <path d="M3 5h4"/>
      <path d="M17 19h4"/>
    </svg>
  );
}
