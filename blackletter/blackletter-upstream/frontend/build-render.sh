#!/bin/bash

# Build script for Render deployment
echo "🚀 Building Blackletter Systems for Render..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf .next out

# Install dependencies
echo "📦 Installing dependencies..."
npm ci --only=production

# Build the application
echo "🔨 Building application..."
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
