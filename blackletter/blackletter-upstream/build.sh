#!/bin/bash

# Build script for Blackletter Systems on Render
echo "🚀 Building Blackletter Systems..."

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "📦 Installing dependencies..."
npm ci

# Build the application
echo "🔨 Building Next.js application..."
npm run build

# Verify build output
echo "✅ Build completed!"
echo "📁 Build output directory: ./out"
echo "📊 Build size:"
du -sh ./out

# List build contents
echo "📋 Build contents:"
ls -la ./out

echo "🎉 Build ready for Render deployment!"
