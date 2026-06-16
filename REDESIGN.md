# NeuralBase Redesign Instructions

## Goal
Redesign NeuralBase into a professional AI Resource Hub with white background, clean minimalis design.

## Design Requirements
1. Background: WHITE (#ffffff), NOT dark/hacker theme
2. Accent: black-gray (#111, #555, #888)
3. Typography: Inter (body) + JetBrains Mono (code)
4. Cards with shadow + hover effect
5. Navigation: Home, Providers, Free Resources, Tools, Edukasi, FAQ
6. Search bar (Ctrl+K)
7. Footer with copyright
8. Responsive design

## Providers (21 total)
Include ALL these providers with Name, Model, Pricing, Context Window, Free Tier:
1. OpenAI - GPT-5, GPT-5 mini, o3/o4
2. Anthropic - Claude Opus 4.8, Sonnet 4.6, Haiku 4.5
3. Google Gemini - Gemini 2.5 Pro/Flash
4. DeepSeek - V4 Pro, V4 Flash (cheapest)
5. Mistral - Large 3, Medium, Small
6. Meta Llama 4 - Scout 109B, Maverick 400B
7. Groq - Llama 4 Scout (FREE tier)
8. Cohere - Command R+, Command R
9. Perplexity - Sonar Pro
10. MiniMax - M2.7
11. Kimi (Moonshot) - K2.6
12. Zhipu AI - GLM-5, GLM-5.1
13. Qwen (Alibaba) - Qwen3 235B
14. OpenRouter - 300+ models
15. Together AI - Llama, Mistral
16. Fireworks AI - Llama, Mixtral
17. HuggingFace - Free inference
18. xAI - Grok 4.20
19. Amazon Bedrock
20. Azure OpenAI
21. Ollama - Local FREE

## Free Resources (15)
HuggingFace, Google Colab, Kaggle, Ollama, LM Studio, Nvidia NIM, Modal.com, Vercel AI SDK, Vast.ai, Lightning AI, RunPod, Paperspace, Replicate, Together AI, Groq Cloud

## Tools (10)
ChatGPT, Claude, Gemini, Copilot, Cursor, Bolt.new, v0.dev, Windsurf, Replit Agent, Poe

## Edukasi (12 articles)
1. Prompt Engineering Fundamentals
2. Memahami Context Window
3. Fine-tuning vs RAG
4. AI Safety & Responsible Use
5. Local LLM: Ollama & LM Studio
6. API Integration Guide
7. Cost Optimization Strategies
8. Multi-Model Strategy
9. RAG Architecture
10. AI Agent Frameworks
11. VPS Deployment Guide (Hermes Agent tutorial - full 8 steps)
12. Free AI Resources Cheat Sheet

## FAQ (15)
All common LLM questions in Indonesian

## Technical
- Flask app at /var/www/neuralbase/app.py
- SQLite DB at neuralbase.db
- Jinja2 templates in /templates/
- Static files in /static/
- Service: neuralbase.service
- Domain: neuralbase.ucel.my.id

## Task
1. Rewrite ALL templates with clean white design
2. Update app.py with all routes
3. Update seed.py with ALL data above
4. Make provider names clickable links
5. Add "Last Updated" to all tables
6. Fix truncated text
7. Render markdown in tutorial/article pages
8. Restart service: systemctl restart neuralbase
