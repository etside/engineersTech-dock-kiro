#!/bin/bash
# QUICK DEPLOYMENT GUIDE
# Copy-paste commands to deploy Kiro Dock to GitHub

## STEP 1: Verify Local Setup
git status
git log --oneline

## STEP 2: Configure Git (first time only)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

## STEP 3: Create GitHub Repository
# 1. Go to https://github.com/new
# 2. Repository name: engineersTech-dock-kiro
# 3. Visibility: Public
# 4. License: MIT (select from template)
# 5. Click "Create repository"

## STEP 4: Add Remote and Push
# Replace YOUR_USERNAME with your GitHub username
GITHUB_USERNAME="YOUR_USERNAME"
REPO_URL="https://github.com/${GITHUB_USERNAME}/engineersTech-dock-kiro.git"

git remote add origin "$REPO_URL"
git branch -M main
git push -u origin main

## STEP 5: Create Release
# Option A: Using GitHub Web (Easiest)
# 1. Go to https://github.com/YOUR_USERNAME/engineersTech-dock-kiro/releases
# 2. Click "Create a new release"
# 3. Tag: v1.0.0
# 4. Title: Kiro Dock v1.0.0 - Initial Release
# 5. Description: Copy from CHANGELOG.md
# 6. Click "Publish release"

# Option B: Using GitHub CLI
# gh release create v1.0.0 \
#   --title "Kiro Dock v1.0.0 - Initial Release" \
#   --notes-file CHANGELOG.md \
#   --latest

## STEP 6: Configure Repository
# 1. Go to https://github.com/YOUR_USERNAME/engineersTech-dock-kiro
# 2. Click "About" (right sidebar) → gear icon
# 3. Add description: "🚀 Animated desktop dock powered by Kiro CLI"
# 4. Add topics: python, pyqt6, desktop-app, kiro-cli, animated-agent
# 5. Enable "Discussions"

## STEP 7: Share & Promote
# Twitter/X:
# 🚀 Introducing Kiro Dock v1.0.0 - Animated AI Desktop Agent
# 
# Features:
# ✨ Multiple positions (bottom, top, center, corners)
# 💬 Built-in Kiro CLI chat
# 🎨 Custom animations & icons
# 🎮 Draggable interface
# 
# GitHub: https://github.com/YOUR_USERNAME/engineersTech-dock-kiro
# #Python #PyQt6 #AI

## VERIFY DEPLOYMENT
# 1. Visit your repo: https://github.com/YOUR_USERNAME/engineersTech-dock-kiro
# 2. Click Releases - should see v1.0.0
# 3. Click Actions - should see CI workflow
# 4. Share link with friends!

echo "✅ Quick reference complete!"
echo "📖 See DEPLOYMENT.md for detailed instructions"
