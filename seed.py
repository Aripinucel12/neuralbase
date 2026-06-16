#!/usr/bin/env python3
"""Seed database with real AI data."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from models import init_db, Provider, Resource, Tool, Education, FAQ, AdminUser
from werkzeug.security import generate_password_hash
from config import Config


def seed():
    init_db()

    # ── Create admin user ──
    if not AdminUser.get_by_username(Config.ADMIN_USERNAME):
        AdminUser.create(Config.ADMIN_USERNAME, generate_password_hash(Config.ADMIN_PASSWORD))
        print("✅ Admin user created")

    # ── LLM Providers ──
    providers = [
        {
            'name': 'OpenAI', 'slug': 'openai',
            'website_url': 'https://openai.com',
            'description': 'OpenAI adalah perusahaan AI research yang mengembangkan GPT series. Model terbaru mereka (GPT-4o, o3) merupakan salah satu yang paling powerful untuk berbagai task.',
            'pricing_in': '$2.50', 'pricing_out': '$10.00', 'context_window': '128K',
            'strengths': 'Multimodal (text, image, audio), function calling sangat bagus, ecosystem terbesar, API paling stabil',
            'weaknesses': 'Harga relatif mahal, rate limit ketat di free tier, kadang overly cautious',
            'free_tier': '$5 credit on signup',
            'sort_order': 1, 'last_updated': '2026-06-17'
        },
        {
            'name': 'Anthropic', 'slug': 'anthropic',
            'website_url': 'https://anthropic.com',
            'description': 'Anthropic mengembangkan Claude — AI assistant yang fokus pada safety dan helpfulness. Claude Sonnet dan Opus adalah model flagship mereka.',
            'pricing_in': '$3.00', 'pricing_out': '$15.00', 'context_window': '200K',
            'strengths': 'Context window sangat besar (200K), coding sangat bagus, nuanced reasoning, artifacts feature',
            'weaknesses': 'Tidak support image generation, agak mahal, rate limit di tier rendah',
            'free_tier': 'Free tier available',
            'sort_order': 2, 'last_updated': '2026-06-17'
        },
        {
            'name': 'Google', 'slug': 'google',
            'website_url': 'https://ai.google.dev',
            'description': 'Google mengembangkan Gemini series — model multimodal yang powerful. Gemini 2.5 Pro dan Flash menawarkan harga yang sangat kompetitif.',
            'pricing_in': '$1.25', 'pricing_out': '$5.00', 'context_window': '1M',
            'strengths': 'Context window terbesar (1M tokens), harga murah, multimodal, grounding with Google Search',
            'weaknesses': 'Kadang hallucinate, API kadang tidak stabil, less mature ecosystem',
            'free_tier': 'Free tier generous',
            'sort_order': 3, 'last_updated': '2026-06-17'
        },
        {
            'name': 'Meta (Llama)', 'slug': 'meta-llama',
            'website_url': 'https://llama.meta.com',
            'description': 'Meta mengembangkan Llama — open source LLM yang bisa di-self-host. Llama 4 Scout dan Maverick tersedia secara gratis.',
            'pricing_in': 'Gratis (self-host)', 'pricing_out': 'Gratis (self-host)', 'context_window': '128K',
            'strengths': 'Open source, bisa self-host, community besar, banyak fine-tuned variants',
            'weaknesses': 'Butuh GPU untuk self-host, kualitas di bawah proprietary models untuk beberapa task',
            'free_tier': 'Fully open source',
            'sort_order': 4, 'last_updated': '2026-06-17'
        },
        {
            'name': 'Mistral', 'slug': 'mistral',
            'website_url': 'https://mistral.ai',
            'description': 'Mistral AI adalah perusahaan Prancis yang mengembangkan efficient LLMs. Model mereka terkenal karena performa yang bagus dengan harga yang kompetitif.',
            'pricing_in': '$0.25', 'pricing_out': '$0.25', 'context_window': '128K',
            'strengths': 'Harga sangat murah, open weight models, cepat, good multilingual support',
            'weaknesses': 'Kurang powerful dibanding GPT-4/Claude untuk complex reasoning, smaller ecosystem',
            'free_tier': 'Free tier available',
            'sort_order': 5, 'last_updated': '2026-06-17'
        },
        {
            'name': 'DeepSeek', 'slug': 'deepseek',
            'website_url': 'https://deepseek.com',
            'description': 'DeepSeek adalah AI lab dari China yang mengembangkan model open source yang sangat kompetitif. DeepSeek-V3 dan R1 mengejutkan industry dengan performanya.',
            'pricing_in': '$0.27', 'pricing_out': '$1.10', 'context_window': '128K',
            'strengths': 'Sangat murah, reasoning bagus (R1), open source, competitive with top models',
            'weaknesses': 'Kadang sensor topik sensitif, latency lebih tinggi, support terbatas',
            'free_tier': 'Free API credits',
            'sort_order': 6, 'last_updated': '2026-06-17'
        },
        {
            'name': 'xAI (Grok)', 'slug': 'xai',
            'website_url': 'https://x.ai',
            'description': 'xAI (Elon Musk) mengembangkan Grok — AI yang terintegrasi dengan X/Twitter. Grok 3 dan 4 menawarkan real-time information access.',
            'pricing_in': '$3.00', 'pricing_out': '$15.00', 'context_window': '128K',
            'strengths': 'Real-time info dari X, less censored, humor/personality, multimodal',
            'weaknesses': 'Relatively new, smaller ecosystem, tied to X platform',
            'free_tier': 'Limited free on X',
            'sort_order': 7, 'last_updated': '2026-06-17'
        },
        {
            'name': 'Alibaba (Qwen)', 'slug': 'qwen',
            'website_url': 'https://qwen.ai',
            'description': 'Qwen dikembangkan oleh Alibaba Cloud. Model ini sangat populer di Asia dan menawarkan performa yang bagus untuk harga yang terjangkau.',
            'pricing_in': '$0.15', 'pricing_out': '$0.60', 'context_window': '128K',
            'strengths': 'Sangat murah, multilingual bagus, open source, coding bagus',
            'weaknesses': 'Kurang dikenal di Barat, support Bahasa Indonesia terbatas',
            'free_tier': 'Free tier available',
            'sort_order': 8, 'last_updated': '2026-06-17'
        },
        {
            'name': 'Groq', 'slug': 'groq',
            'website_url': 'https://groq.com',
            'description': 'Groq menggunakan LPU (Language Processing Unit) hardware untuk inference ultra-cepat. Mereka host model open source seperti Llama dan Mistral dengan kecepatan hingga 750 tokens/detik.',
            'pricing_in': '$0.05', 'pricing_out': '$0.08', 'context_window': '128K',
            'strengths': 'Inference tercepat di industry, harga sangat murah, free tier generous, support banyak model open source',
            'weaknesses': 'Hanya inference (tidak bisa training), pilihan model terbatas, tidak ada custom fine-tuning',
            'free_tier': 'Free tier available',
            'sort_order': 9, 'last_updated': '2026-06-17'
        },
        {
            'name': 'Cohere', 'slug': 'cohere',
            'website_url': 'https://cohere.com',
            'description': 'Cohere fokus pada enterprise AI dengan model Command R+. Mereka unggul dalam RAG (Retrieval Augmented Generation) dan multilingual tasks untuk kebutuhan bisnis.',
            'pricing_in': '$0.15', 'pricing_out': '$0.60', 'context_window': '128K',
            'strengths': 'Sangat bagus untuk RAG, enterprise-ready, multilingual 100+ bahasa, grounding akurat',
            'weaknesses': 'Kurang cocok untuk creative tasks, ecosystem lebih kecil, kurang dikenal developer',
            'free_tier': 'Free trial available',
            'sort_order': 10, 'last_updated': '2026-06-17'
        },
        {
            'name': 'Perplexity', 'slug': 'perplexity',
            'website_url': 'https://perplexity.ai',
            'description': 'Perplexity adalah AI-powered search engine yang memberikan jawaban dengan sumber sitasi. Mereka menggabungkan LLM dengan real-time web search untuk hasil yang akurat.',
            'pricing_in': '$0.20', 'pricing_out': '$1.00', 'context_window': '128K',
            'strengths': 'Jawaban dengan sumber sitasi, real-time web search, sangat bagus untuk research, UI intuitif',
            'weaknesses': 'Hanya untuk search/Q&A (tidak untuk generation), API terbatas, free tier dibatasi',
            'free_tier': 'Free tier with limits',
            'sort_order': 11, 'last_updated': '2026-06-17'
        },
        {
            'name': 'Together AI', 'slug': 'together-ai',
            'website_url': 'https://together.ai',
            'description': 'Together AI menyediakan platform untuk menjalankan dan fine-tune open source models. Mereka menawarkan akses ke Llama, Mistral, dan banyak model lainnya dengan harga kompetitif.',
            'pricing_in': '$0.10', 'pricing_out': '$0.10', 'context_window': '128K',
            'strengths': 'Fine-tuning support, banyak pilihan open source models, harga murah, $5 free credit',
            'weaknesses': 'Kurang stabil dibanding provider besar, dokumentasi kurang lengkap, support terbatas',
            'free_tier': '$5 free credit',
            'sort_order': 12, 'last_updated': '2026-06-17'
        },
        {
            'name': 'Fireworks AI', 'slug': 'fireworks-ai',
            'website_url': 'https://fireworks.ai',
            'description': 'Fireworks AI menawarkan inference cepat untuk open source models. Mereka fokus pada kecepatan dan efisiensi dengan teknologi proprietary mereka.',
            'pricing_in': '$0.10', 'pricing_out': '$0.10', 'context_window': '128K',
            'strengths': 'Inference sangat cepat, harga murah, support function calling, good for production',
            'weaknesses': 'Kurang dikenal, pilihan model lebih sedikit, dokumentasi terbatas',
            'free_tier': 'Free tier available',
            'sort_order': 13, 'last_updated': '2026-06-17'
        },
        {
            'name': 'Moonshot AI', 'slug': 'moonshot-ai',
            'website_url': 'https://moonshot.cn',
            'description': 'Moonshot AI (Kimi) adalah AI lab dari China yang mengembangkan model dengan context window sangat panjang. Kimi Chat mendukung hingga 2M tokens context.',
            'pricing_in': '$0.30', 'pricing_out': '$1.20', 'context_window': '2M',
            'strengths': 'Context window sangat besar (2M tokens), bagus untuk dokumen panjang, multilingual',
            'weaknesses': 'Tersedia terutama untuk pasar China, API terbatas di luar China, kurang dikenal global',
            'free_tier': 'Free tier available',
            'sort_order': 14, 'last_updated': '2026-06-17'
        },
        {
            'name': 'Zhipu AI (GLM)', 'slug': 'zhipu-ai',
            'website_url': 'https://zhipuai.cn',
            'description': 'Zhipu AI mengembangkan GLM (General Language Model) series. Mereka adalah salah satu AI lab terkemuka di China dengan model yang kompetitif.',
            'pricing_in': '$0.35', 'pricing_out': '$1.40', 'context_window': '128K',
            'strengths': 'Model kuat untuk bahasa China, multimodal support, good API documentation, competitive pricing',
            'weaknesses': 'Fokus pada pasar China, kurang optimal untuk bahasa lain, akses internasional terbatas',
            'free_tier': 'Free credits for new users',
            'sort_order': 15, 'last_updated': '2026-06-17'
        },
        {
            'name': 'Amazon Bedrock', 'slug': 'amazon-bedrock',
            'website_url': 'https://aws.amazon.com/bedrock',
            'description': 'Amazon Bedrock adalah managed service dari AWS untuk mengakses berbagai foundation models (Claude, Llama, Mistral, dll) melalui satu API terpadu.',
            'pricing_in': 'Varies by model', 'pricing_out': 'Varies by model', 'context_window': 'Varies',
            'strengths': 'Akses ke banyak model dalam satu API, terintegrasi dengan AWS ecosystem, enterprise-grade security, scalable',
            'weaknesses': 'Harga lebih mahal dari direct API, setup kompleks, vendor lock-in ke AWS',
            'free_tier': 'Free tier with limits',
            'sort_order': 16, 'last_updated': '2026-06-17'
        },
        {
            'name': 'Azure AI', 'slug': 'azure-ai',
            'website_url': 'https://azure.microsoft.com/en-us/products/ai-services',
            'description': 'Azure AI dari Microsoft menyediakan akses ke OpenAI models (GPT-4o, o3) dan berbagai model lain melalui platform cloud Azure yang enterprise-ready.',
            'pricing_in': 'Varies by model', 'pricing_out': 'Varies by model', 'context_window': 'Varies',
            'strengths': 'Akses eksklusif ke OpenAI models, enterprise compliance, terintegrasi dengan Microsoft 365, SLA terjamin',
            'weaknesses': 'Mahal, kompleks untuk pemula, vendor lock-in ke Azure, rate limit bervariasi',
            'free_tier': '$200 credit for new accounts',
            'sort_order': 17, 'last_updated': '2026-06-17'
        },
        {
            'name': 'Baidu (ERNIE)', 'slug': 'baidu-ernie',
            'website_url': 'https://yiyan.baidu.com',
            'description': 'Baidu mengembangkan ERNIE (Enhanced Representation through Knowledge Integration) — model LLM terkemuka di China. ERNIE 4.0 adalah model flagship mereka.',
            'pricing_in': '$0.20', 'pricing_out': '$0.80', 'context_window': '128K',
            'strengths': 'Sangat kuat untuk bahasa China, terintegrasi dengan Baidu ecosystem, harga kompetitif, multimodal',
            'weaknesses': 'Kurang optimal untuk bahasa lain, akses internasional terbatas, kurang transparan',
            'free_tier': 'Free tier available',
            'sort_order': 18, 'last_updated': '2026-06-17'
        },
        {
            'name': '01.AI (Yi)', 'slug': '01ai-yi',
            'website_url': 'https://01.ai',
            'description': '01.AI didirikan oleh Kai-Fu Lee dan mengembangkan Yi series models. Yi-1.5 dan Yi-Lightning menawarkan performa yang sangat bagus untuk harga yang terjangkau.',
            'pricing_in': '$0.10', 'pricing_out': '$0.40', 'context_window': '200K',
            'strengths': 'Harga sangat murah, context window besar (200K), open source, performa bagus untuk harganya',
            'weaknesses': 'Relatif baru, kurang dikenal di Barat, ecosystem kecil, support terbatas',
            'free_tier': 'Free credits available',
            'sort_order': 19, 'last_updated': '2026-06-17'
        },
        {
            'name': 'Stability AI', 'slug': 'stability-ai',
            'website_url': 'https://stability.ai',
            'description': 'Stability AI dikenal dengan Stable Diffusion untuk image generation. Mereka juga mengembangkan LLM open source seperti StableLM dan Stable Code.',
            'pricing_in': '$0.10', 'pricing_out': '$0.10', 'context_window': '64K',
            'strengths': 'Leader di image generation (Stable Diffusion), open source, model ringan untuk edge deployment',
            'weaknesses': 'LLM kurang powerful dibanding kompetitor, fokus utama di image bukan text, finansial tidak stabil',
            'free_tier': 'Free tier for images',
            'sort_order': 20, 'last_updated': '2026-06-17'
        },
        {
            'name': 'Cerebras', 'slug': 'cerebras',
            'website_url': 'https://cerebras.ai',
            'description': 'Cerebras mengembangkan wafer-scale chip khusus untuk AI training dan inference. Mereka menawarkan inference super cepat dengan teknologi hardware unik mereka.',
            'pricing_in': '$0.10', 'pricing_out': '$0.10', 'context_window': '128K',
            'strengths': 'Inference sangat cepat dengan custom hardware, harga kompetitif, good for high-throughput applications',
            'weaknesses': 'Pilihan model terbatas, kurang dikenal, fokus pada enterprise, hardware dependency',
            'free_tier': 'Free tier available',
            'sort_order': 21, 'last_updated': '2026-06-17'
        },
    ]

    for p in providers:
        if not Provider.get_by_slug(p['slug']):
            Provider.create(p)
    print(f"✅ {len(providers)} providers seeded")

    # ── Free Resources ──
    resources = [
        {
            'name': 'Google Colab', 'slug': 'google-colab', 'category': 'gpu',
            'description': 'Platform Jupyter notebook gratis dari Google dengan akses GPU (T4). Cocok untuk belajar ML/AI dan menjalankan model.',
            'url': 'https://colab.research.google.com',
            'free_details': 'Free T4 GPU, 12GB RAM',
            'sort_order': 1
        },
        {
            'name': 'Hugging Face', 'slug': 'hugging-face', 'category': 'api',
            'description': 'Platform terbesar untuk ML models, datasets, dan spaces. Bisa deploy model gratis dan akses ribuan model open source.',
            'url': 'https://huggingface.co',
            'free_details': 'Free inference API, free Spaces',
            'sort_order': 2
        },
        {
            'name': 'Kaggle', 'slug': 'kaggle', 'category': 'gpu',
            'description': 'Platform data science dari Google dengan free GPU notebooks, datasets, dan competitions.',
            'url': 'https://kaggle.com',
            'free_details': 'Free GPU 30hrs/week',
            'sort_order': 3
        },
        {
            'name': 'Railway', 'slug': 'railway', 'category': 'vps',
            'description': 'Platform PaaS untuk deploy aplikasi. Free tier memberikan $5 credit per bulan untuk hosting apps.',
            'url': 'https://railway.app',
            'free_details': '$5/month free credit',
            'sort_order': 4
        },
        {
            'name': 'Vercel', 'slug': 'vercel', 'category': 'vps',
            'description': 'Platform hosting untuk frontend dan fullstack apps. Deploy Next.js, React, dan static sites secara gratis.',
            'url': 'https://vercel.com',
            'free_details': 'Free tier for hobby',
            'sort_order': 5
        },
        {
            'name': 'Fly.io', 'slug': 'fly-io', 'category': 'vps',
            'description': 'Platform untuk deploy apps dekat dengan user. Free tier termasuk 3 shared VMs dan 160GB bandwidth.',
            'url': 'https://fly.io',
            'free_details': '3 free VMs, 160GB bandwidth',
            'sort_order': 6
        },
        {
            'name': 'OpenRouter', 'slug': 'openrouter', 'category': 'api',
            'description': 'Unified API untuk akses 100+ LLMs dari berbagai provider. Banyak model yang tersedia secara gratis.',
            'url': 'https://openrouter.ai',
            'free_details': 'Free models available',
            'sort_order': 7
        },
        {
            'name': 'Together AI', 'slug': 'together-ai', 'category': 'api',
            'description': 'Platform untuk menjalankan open source AI models. Free credit untuk memulai dan harga yang kompetitif.',
            'url': 'https://together.ai',
            'free_details': '$5 free credit',
            'sort_order': 8
        },
        {
            'name': 'Groq', 'slug': 'groq', 'category': 'api',
            'description': 'Platform inference ultra-cepat menggunakan LPU hardware. Free tier tersedia untuk akses berbagai open source models.',
            'url': 'https://groq.com',
            'free_details': 'Free tier available',
            'sort_order': 9
        },
    ]

    for r in resources:
        if not Resource.get_by_slug(r['slug']):
            Resource.create(r)
    print(f"✅ {len(resources)} resources seeded")

    # ── AI Tools ──
    tools = [
        {
            'name': 'Cursor', 'slug': 'cursor', 'category': 'coding',
            'description': 'AI-powered code editor berbasis VS Code. Bisa generate, edit, dan debug code dengan AI. Sangat powerful untuk development.',
            'url': 'https://cursor.sh',
            'pricing': 'Free / $20/mo Pro',
            'rating': 4.8,
            'sort_order': 1
        },
        {
            'name': 'GitHub Copilot', 'slug': 'github-copilot', 'category': 'coding',
            'description': 'AI pair programmer dari GitHub. Auto-complete code, generate functions, dan explain code langsung di IDE.',
            'url': 'https://github.com/features/copilot',
            'pricing': '$10/mo',
            'rating': 4.5,
            'sort_order': 2
        },
        {
            'name': 'ChatGPT', 'slug': 'chatgpt', 'category': 'chat',
            'description': 'AI chatbot dari OpenAI yang paling populer. Bisa untuk coding, writing, analysis, dan banyak lagi.',
            'url': 'https://chat.openai.com',
            'pricing': 'Free / $20/mo Plus',
            'rating': 4.7,
            'sort_order': 3
        },
        {
            'name': 'Claude', 'slug': 'claude', 'category': 'chat',
            'description': 'AI assistant dari Anthropic dengan context window sangat besar. Sangat bagus untuk coding, analysis, dan creative writing.',
            'url': 'https://claude.ai',
            'pricing': 'Free / $20/mo Pro',
            'rating': 4.8,
            'sort_order': 4
        },
        {
            'name': 'Midjourney', 'slug': 'midjourney', 'category': 'image',
            'description': 'AI image generator terbaik untuk menghasilkan gambar berkualitas tinggi dari text prompt.',
            'url': 'https://midjourney.com',
            'pricing': '$10/mo Basic',
            'rating': 4.9,
            'sort_order': 5
        },
        {
            'name': 'DALL-E 3', 'slug': 'dall-e-3', 'category': 'image',
            'description': 'AI image generator dari OpenAI. Terintegrasi dengan ChatGPT, sangat mudah digunakan.',
            'url': 'https://openai.com/dall-e-3',
            'pricing': 'Included in ChatGPT Plus',
            'rating': 4.5,
            'sort_order': 6
        },
        {
            'name': 'Perplexity', 'slug': 'perplexity', 'category': 'chat',
            'description': 'AI search engine yang memberikan jawaban dengan sumber. Lebih akurat untuk research dibanding chatbot biasa.',
            'url': 'https://perplexity.ai',
            'pricing': 'Free / $20/mo Pro',
            'rating': 4.6,
            'sort_order': 7
        },
        {
            'name': 'Notion AI', 'slug': 'notion-ai', 'category': 'writing',
            'description': 'AI writing assistant terintegrasi dengan Notion. Bisa summarize, translate, generate content, dan organize notes.',
            'url': 'https://notion.so',
            'pricing': 'Free / $10/mo',
            'rating': 4.3,
            'sort_order': 8
        },
    ]

    for t in tools:
        if not Tool.get_by_slug(t['slug']):
            Tool.create(t)
    print(f"✅ {len(tools)} tools seeded")

    # ── Education ──
    education = [
        {
            'title': 'Apa itu LLM (Large Language Model)?',
            'slug': 'apa-itu-llm',
            'category': 'llm',
            'content': '''LLM (Large Language Model) adalah jenis AI model yang dilatih dengan dataset text yang sangat besar untuk memahami dan menghasilkan bahasa manusia.

Contoh LLM yang terkenal:
• GPT-4o (OpenAI)
• Claude (Anthropic)
• Gemini (Google)
• Llama (Meta)
• Mistral (Mistral AI)

Bagaimana LLM Bekerja:
1. Training: Model dilatih dengan jutaan dokumen dari internet
2. Fine-tuning: Model disesuaikan untuk task tertentu
3. RLHF: Model dioptimasi berdasarkan feedback manusia
4. Inference: Model menghasilkan response berdasarkan input

LLM bisa digunakan untuk:
• Chatbot dan virtual assistant
• Code generation dan debugging
• Content writing dan translation
• Data analysis dan summarization
• Dan banyak lagi!''',
            'last_updated': '2026-06-17'
        },
        {
            'title': 'Prompt Engineering: Cara Efektif Berinteraksi dengan AI',
            'slug': 'prompt-engineering',
            'category': 'prompt-engineering',
            'content': '''Prompt engineering adalah seni dan sains dalam menulis instruksi yang efektif untuk AI.

Tips Prompt Engineering:

1. Be Specific
❌ "Tulis artikel tentang AI"
✅ "Tulis artikel 500 kata tentang cara menggunakan LLM untuk pemula, dengan contoh praktis"

2. Give Context
❌ "Buatkan kode Python"
✅ "Buatkan fungsi Python untuk fetch data dari API, handle errors, dan return JSON. Gunakan requests library."

3. Use Examples
Berikan contoh input/output yang diinginkan agar AI lebih akurat.

4. Break Down Tasks
Untuk task kompleks, pecah menjadi langkah-langkah kecil.

5. Specify Format
Tentukan format output yang diinginkan (JSON, markdown, table, dll).

6. Iterasi
Jika hasil kurang bagus, refine prompt dan coba lagi.

7. Use System Prompts
Gunakan system prompt untuk mengatur behavior AI secara konsisten.

8. Chain of Thought
Minta AI untuk "berpikir step by step" untuk reasoning tasks.''',
            'last_updated': '2026-06-17'
        },
        {
            'title': 'Cara Menggunakan API LLM',
            'slug': 'cara-menggunakan-api-llm',
            'category': 'api',
            'content': '''Tutorial cara menggunakan API LLM untuk membangun aplikasi AI.

Step 1: Pilih Provider
• OpenAI API - paling populer
• Anthropic API - bagus untuk coding
• Google AI Studio - gratis untuk testing

Step 2: Dapatkan API Key
Daftar di website provider dan buat API key.

Step 3: Install Library
Python: pip install openai

Step 4: Buat Request

Contoh dengan Python:
```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Apa itu AI?"}
    ]
)

print(response.choices[0].message.content)
```

Step 5: Handle Responses
Parse response, handle errors, dan implement retry logic.

Tips:
• Simpan API key di environment variable
• Implement rate limiting
• Cache responses untuk menghemat cost
• Monitor usage dan set budget alerts''',
            'last_updated': '2026-06-17'
        },
        {
            'title': 'Context Windows: Memahami Batas Memori LLM',
            'slug': 'context-windows',
            'category': 'llm',
            'content': '''Context window adalah jumlah token maksimal yang bisa diproses oleh LLM dalam satu percakapan.

Apa itu Token?
Token adalah unit terkecil yang diproses LLM. 1 token ≈ 4 karakter bahasa Inggris ≈ 0.75 kata. Untuk bahasa Indonesia, 1 token ≈ 2-3 karakter.

Context Window Berbagai Provider:
• Google Gemini: 1M tokens (terbesar)
• Moonshot Kimi: 2M tokens
• Anthropic Claude: 200K tokens
• OpenAI GPT-4o: 128K tokens
• Mistral: 128K tokens

Mengapa Context Window Penting?
1. Dokumen Panjang: Bisa memproses buku, kodebase, atau dokumen hukum sekaligus
2. Percakapan Panjang: Chat bisa lebih lama tanpa "lupa" konteks sebelumnya
3. RAG: Bisa memasukkan lebih banyak referensi ke dalam prompt

Tips Menggunakan Context Window:
• Jangan buang token untuk hal yang tidak perlu
• Gunakan system prompt yang efisien
• Compress informasi yang berulang
• Pertimbangkan cost — token lebih banyak = lebih mahal

Cara Menghitung Cost:
Cost = (input tokens × harga input) + (output tokens × harga output)
Contoh: 10K input tokens × $3/1M + 2K output tokens × $15/1M = $0.03 + $0.03 = $0.06 per request''',
            'last_updated': '2026-06-17'
        },
        {
            'title': 'Fine-tuning vs RAG: Kapan Menggunakan yang Mana?',
            'slug': 'fine-tuning-vs-rag',
            'category': 'llm',
            'content': '''Fine-tuning dan RAG (Retrieval Augmented Generation) adalah dua pendekatan utama untuk meng-customize LLM.

FINE-TUNING
Fine-tuning melatih ulang model dengan data khusus Anda.

Kapan menggunakan fine-tuning:
• Butuh output dengan format/spesifik yang konsisten
• Punya dataset besar (>1000 contoh)
• Butuh model yang "paham" domain tertentu
• Ingin mengurangi hallucination untuk topik spesifik

Kelebihan:
+ Output lebih konsisten
+ Lebih cepat (tidak perlu retrieve data)
+ Bisa "mengubah" personality model

Kekurangan:
- Mahal (butuh GPU untuk training)
- Butuh banyak data berkualitas
- Sulit di-update (harus retrain)
- Bisa overfitting

RAG (Retrieval Augmented Generation)
RAG mengambil informasi dari database/dokumen eksternal dan memasukkannya ke prompt.

Kapan menggunakan RAG:
• Data sering berubah (pricing, inventory, news)
• Butuh sumber yang bisa diverifikasi
• Ingin mengurangi hallucination
• Data terlalu besar untuk context window

Kelebihan:
+ Mudah di-update (tinggal update database)
+ Lebih murah (tidak perlu training)
+ Bisa sitasi sumber
+ Data selalu fresh

Kekurangan:
- Quality tergantung retrieval
- Lebih lambat (perlu retrieve dulu)
- Butuh infrastructure tambahan (vector database)

Rekomendasi:
• Mulai dengan RAG — lebih mudah dan murah
• Gunakan fine-tuning hanya jika RAG tidak cukup
• Bisa juga kombinasi keduanya (RAG + fine-tuned model)''',
            'last_updated': '2026-06-17'
        },
        {
            'title': 'Multi-modal AI: Lebih dari Sekadar Text',
            'slug': 'multi-modal-ai',
            'category': 'llm',
            'content': '''Multi-modal AI adalah model yang bisa memproses dan menghasilkan berbagai jenis input: text, gambar, audio, dan video.

Jenis Multi-modal AI:

1. Vision-Language Models (VLM)
• GPT-4o: Bisa analisis gambar, OCR, describe images
• Claude: Bisa baca dokumen, charts, screenshots
• Gemini: Native multimodal, proses text+image+audio+video

2. Image Generation
• DALL-E 3 (OpenAI): Text-to-image
• Stable Diffusion (Stability AI): Open source image generation
• Midjourney: Kualitas terbaik untuk artistic images

3. Audio Models
• Whisper (OpenAI): Speech-to-text sangat akurat
• ElevenLabs: Text-to-speech dengan suara natural
• Suno: AI music generation

4. Video Models
• Sora (OpenAI): Text-to-video
• Runway: Video generation dan editing
• Pika: AI video generation

Contoh Penggunaan Multi-modal:
• Upload foto makanan → dapat resep
• Upload screenshot code → dapat penjelasan
• Upload dokumen → dapat summary
• Describe gambar → generate image

Tips Menggunakan Multi-modal AI:
• Berikan instruksi yang jelas tentang apa yang ingin Anda ketahui
• Gunakan high-quality images untuk hasil terbaik
• Kombinasikan text dan image untuk konteks yang lebih kaya
• Perhatikan cost — image processing lebih mahal dari text''',
            'last_updated': '2026-06-17'
        },
        {
            'title': 'AI Safety dan Responsible AI',
            'slug': 'ai-safety',
            'category': 'general',
            'content': '''AI Safety adalah bidang yang memastikan AI dikembangkan dan digunakan dengan aman dan bertanggung jawab.

Mengapa AI Safety Penting?
1. Hallucination: AI kadang menghasilkan informasi salah dengan sangat meyakinkan
2. Bias: AI bisa mewarisi bias dari data training
3. Privacy: AI bisa secara tidak sengaja mengungkap data sensitif
4. Misuse: AI bisa digunakan untuk hal negatif (scams, deepfakes, dll)

Prinsip Responsible AI:
1. Transparency: Harus jelas kapan sesuatu dibuat oleh AI
2. Fairness: AI harus adil untuk semua kelompok
3. Privacy: Data user harus dilindungi
4. Accountability: Harus ada yang bertanggung jawab atas output AI
5. Safety: AI harus diuji sebelum digunakan

Tips Menggunakan AI dengan Aman:
• Selalu verifikasi informasi penting dari AI
• Jangan masukkan data sensitif ke public AI services
• Gunakan AI sebagai asisten, bukan pengganti keputusan manusia
• Pahami batasan model yang Anda gunakan
• Report output yang berbahaya atau tidak akurat

AI Safety di Berbagai Provider:
• Anthropic: Constitutional AI, fokus pada safety
• OpenAI: Safety team besar, red teaming
• Google: Responsible AI practices
• Meta: Open source dengan safety guidelines''',
            'last_updated': '2026-06-17'
        },
        {
            'title': 'Membangun Aplikasi AI dari Nol',
            'slug': 'membangun-aplikasi-ai',
            'category': 'api',
            'content': '''Panduan langkah demi langkah untuk membangun aplikasi menggunakan AI.

Step 1: Tentukan Use Case
• Apa masalah yang ingin Anda selesaikan?
• Apakah LLM adalah solusi yang tepat?
• Siapa target user Anda?

Step 2: Pilih Tech Stack
Backend: Python (Flask/FastAPI) atau Node.js
Frontend: React, Next.js, atau vanilla HTML/CSS
Database: SQLite (simple), PostgreSQL (production)
AI: OpenAI API, Anthropic API, atau open source

Step 3: Design Architecture
• Frontend → Backend → AI API → Database
• Tambahkan caching untuk menghemat cost
• Implement rate limiting untuk mencegah abuse
• Gunakan queue untuk request yang berat

Step 4: Implementasi Dasar
```python
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json['message']
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_msg}]
    )
    return jsonify({"reply": response.choices[0].message.content})
```

Step 5: Tambahkan Features
• User authentication
• Chat history
• Streaming responses
• Error handling
• Usage tracking

Step 6: Deploy
• Vercel/Netlify untuk frontend
• Railway/Fly.io untuk backend
• Environment variables untuk API keys
• HTTPS wajib untuk production

Tips:
• Mulai dari MVP, iterasi berdasarkan feedback
• Monitor cost API Anda
• Implement retry logic untuk API calls
• Cache response yang sering diminta
• Gunakan streaming untuk UX yang lebih baik''',
            'last_updated': '2026-06-17'
        },
        {
            'title': 'Token dan Pricing: Menghitung Biaya LLM',
            'slug': 'token-dan-pricing',
            'category': 'llm',
            'content': '''Memahami token dan pricing adalah kunci untuk mengelola biaya penggunaan LLM.

Apa itu Token?
Token adalah unit terkecil yang diproses oleh LLM. Model tidak membaca kata, tapi token.

Contoh Tokenization:
• "Hello world" = 2 tokens
• "Artificial intelligence" = 3 tokens
• "ChatGPT" = 2-3 tokens
• Bahasa Indonesia biasanya lebih banyak token per kata

Cara Menghitung Biaya:
Formula: (input tokens × harga input per token) + (output tokens × harga output per token)

Contoh Perhitungan:
Misal Anda menggunakan GPT-4o ($2.50/1M input, $10/1M output)
• Input: 5,000 tokens = 5,000 × $0.0000025 = $0.0125
• Output: 1,000 tokens = 1,000 × $0.00001 = $0.01
• Total per request: $0.0225

Tips Menghemat Biaya:
1. Gunakan model yang tepat — tidak perlu GPT-4o untuk task sederhana
2. Compress prompt — hilangkan informasi yang tidak perlu
3. Cache responses — simpan jawaban yang sering diminta
4. Set max_tokens — batasi output yang dihasilkan
5. Gunakan batch API — lebih murah dari real-time API
6. Monitor usage — set budget alerts

Perbandingan Harga (per 1M tokens):
Murah: DeepSeek ($0.27), Groq ($0.05), Mistral ($0.25)
Sedang: GPT-4o ($2.50), Gemini Pro ($1.25)
Mahal: Claude Opus ($15), GPT-4 Turbo ($10)

Kapan Gunakan Model Mahal?
• Complex reasoning dan analysis
• Coding yang sangat kompleks
• Task yang butuh akurasi tinggi
• Dokumen panjang dengan konteks penting''',
            'last_updated': '2026-06-17'
        },
        {
            'title': 'API Key Security: Melindungi Akses AI Anda',
            'slug': 'api-key-security',
            'category': 'api',
            'content': '''API key adalah kunci akses ke layanan AI. Jika bocor, orang lain bisa menggunakan quota Anda.

Mengapa API Key Security Penting?
• API key yang bocor = tagihan tak terduga
• Bisa disalahgunakan untuk aktivitas ilegal
• Account bisa di-ban oleh provider
• Data Anda bisa diakses orang lain

Best Practices:

1. Jangan Hardcode API Key
❌ api_key = "sk-abc123..."  # DI KODE
✅ api_key = os.environ.get("OPENAI_API_KEY")  # DI ENV VAR

2. Gunakan Environment Variables
# .env file (JANGAN commit ke git)
OPENAI_API_KEY=sk-abc123...

# .gitignore
.env

3. Buat API Key Terpisah per Environment
• Development: key dengan limit kecil
• Staging: key terpisah
• Production: key dengan limit dan monitoring

4. Set Usage Limits
• Monthly budget limit
• Rate limit per minute/hour
• Alert jika usage abnormal

5. Rotate API Key Secara Berkala
• Buat key baru
• Update semua aplikasi
• Hapus key lama

6. Monitor Usage
• Cek dashboard provider secara berkala
• Set up alerts untuk usage tinggi
• Log semua API calls

7. Gunakan Proxy/API Gateway
• Centralize API key management
• Tambahkan authentication layer
• Monitor dan log semua requests

Tanda-tanda API Key Bocor:
• Usage tiba-tiba naik drastis
• Tagihan tidak wajar
• Ada request dari IP yang tidak dikenal
• Provider mengirim warning email

Jika API Key Bocor:
1. Revoke key SEGERA di dashboard provider
2. Buat key baru
3. Cek tagihan dan dispute jika perlu
4. Audit code untuk menemukan kebocoran
5. Implement security practices di atas''',
            'last_updated': '2026-06-17'
        },
        {
            'title': 'Tutorial Lengkap: Setup Hermes AI Agent dari VPS Baru',
            'slug': 'setup-hermes-ai-agent',
            'category': 'agent',
            'content': '''Panduan lengkap membangun AI Agent yang terhubung ke Telegram menggunakan Hermes Agent — dari VPS kosong sampai bot aktif.

## Apa itu Hermes Agent?

Hermes Agent adalah open-source AI agent framework yang memungkinkan Anda menjalankan AI assistant yang terhubung ke berbagai platform (Telegram, Discord, WhatsApp). Agent bisa browsing web, menjalankan script, mengelola cron jobs, dan banyak lagi.

## Prasyarat

- VPS Ubuntu 22.04+ (minimal 1GB RAM, 2GB direkomendasikan)
- Telegram Bot Token (dari @BotFather)
- API Key dari LLM provider (OpenAI, Anthropic, Google, dll)
- Domain (opsional, untuk webhook)

## Step 1: Siapkan VPS

Update system dan install dependencies:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git python3 python3-pip python3-venv nodejs npm
```

Install Node.js v20+ (wajib):

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
node --version  # Pastikan v20+
```

## Step 2: Install Hermes Agent

```bash
npm install -g hermes-agent
hermes --version
```

Atau dari source:

```bash
git clone https://github.com/nousresearch/hermes-agent.git
cd hermes-agent
npm install
npm link
```

## Step 3: Buat Telegram Bot

1. Buka Telegram, cari @BotFather
2. Kirim /newbot
3. Ikuti instruksi (nama bot + username)
4. Simpan token yang diberikan (format: 123456789:ABCdefGHI...)

## Step 4: Konfigurasi Hermes

Buat config file:

```bash
mkdir -p ~/.hermes
hermes setup
```

Atau buat manual di ~/.hermes/config.yaml:

```yaml
telegram:
  bot_token: "YOUR_TELEGRAM_BOT_TOKEN"

agent:
  model:
    default: "gpt-4o"
  temperature: 0.7

providers:
  openai:
    api_key: "YOUR_API_KEY"
```

Model yang bisa digunakan:
- OpenAI: gpt-4o, gpt-4o-mini, o3, o4-mini
- Anthropic: claude-sonnet-4, claude-haiku-3.5
- Google: gemini-2.5-pro, gemini-2.5-flash
- DeepSeek: deepseek-chat, deepseek-reasoner
- Custom: any OpenAI-compatible API

## Step 5: Jalankan Gateway

```bash
hermes gateway
```

Untuk menjalankan sebagai service (recommended):

```bash
sudo tee /etc/systemd/system/hermes-gateway.service << 'EOF'
[Unit]
Description=Hermes AI Gateway
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root
ExecStart=/usr/bin/node /usr/lib/node_modules/hermes-agent/cli.js gateway
Restart=always
RestartSec=5
MemoryMax=512M
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable hermes-gateway
sudo systemctl start hermes-gateway
```

Cek status:

```bash
sudo systemctl status hermes-gateway
```

## Step 6: Test Bot

1. Buka Telegram
2. Cari bot Anda (username yang dibuat di Step 3)
3. Kirim /start
4. Kirim pesan test: "Halo, siapa kamu?"

Jika bot merespons = setup berhasil!

## Command Dasar Hermes

```bash
# Gateway management
hermes gateway              # Start gateway
hermes gateway restart      # Restart
hermes gateway stop         # Stop
hermes gateway status       # Cek status

# Config management
hermes config set model.default gpt-4o    # Ganti model
hermes config get model.default            # Lihat config
hermes config set temperature 0.7          # Set temperature

# Skill management
hermes skills list          # Lihat semua skills
hermes skills install <name>  # Install skill

# Cron jobs
hermes cron list            # Lihat cron jobs
hermes cron create "prompt" --schedule "0 9 * * *"  # Buat cron

# Session management
hermes sessions list        # Lihat session aktif
hermes sessions clear       # Clear session
```

## Step 7: Tambah AI Gateway (Opsional)

Anda bisa menambah AI gateway seperti OmniRoute untuk routing model:

```bash
npm install -g omniroute
omniroute
```

OmniRoute berjalan di port 20128 dan bisa diakses via dashboard.

## Step 8: Setup Caddy Reverse Proxy (Opsional)

Untuk akses HTTPS ke dashboard:

```bash
sudo apt install -y caddy
```

Edit /etc/caddy/Caddyfile:

```
dashboard.yourdomain.com {
    reverse_proxy localhost:20128
}
```

```bash
sudo systemctl restart caddy
```

## Tips & Best Practices

1. **Memory Management**: Set memory_char_limit ke 5000000 di config.yaml untuk memory yang lebih besar
2. **Skills**: Install skills yang relevan untuk task Anda (crypto, security, productivity)
3. **Cron Jobs**: Gunakan cron untuk automation (daily reports, monitoring, dll)
4. **Multiple Providers**: Setup fallback providers untuk uptime yang lebih baik
5. **Security**: Jangan share API key, gunakan environment variables
6. **Monitoring**: Cek logs secara berkala dengan `journalctl -u hermes-gateway -f`

## Troubleshooting

- Bot tidak merespons: Cek `systemctl status hermes-gateway`
- API error: Cek API key dan quota provider
- Memory issue: Tambah swap atau upgrade VPS
- Gateway crash: Cek logs dengan `journalctl -u hermes-gateway --no-pager -n 50'

## Links

- GitHub: https://github.com/nousresearch/hermes-agent
- Docs: https://hermes-agent.nousresearch.com/docs
- Skills: https://www.skills.sh/''',
            'excerpt': 'Tutorial lengkap setup Hermes AI Agent dari VPS kosong sampai bot Telegram aktif. Termasuk konfigurasi, commands, dan best practices.',
            'read_time': '15 menit',
            'last_updated': '2026-06-17'
        },
    ]

    for e in education:
        if not Education.get_by_slug(e['slug']):
            Education.create(e)
    print(f"✅ {len(education)} education articles seeded")

    # ── FAQ ──
    faqs = [
        {
            'question': 'Apa itu NeuralBase?',
            'answer': 'NeuralBase adalah AI Resource Hub yang menyediakan informasi lengkap tentang LLM providers, free resources (VPS, API, GPU), AI tools, dan edukasi tentang artificial intelligence.',
            'sort_order': 1, 'last_updated': '2026-06-17'
        },
        {
            'question': 'Apakah semua informasi di NeuralBase gratis?',
            'answer': 'Ya! NeuralBase adalah platform gratis. Semua informasi tentang providers, resources, tools, dan edukasi bisa diakses tanpa biaya.',
            'sort_order': 2, 'last_updated': '2026-06-17'
        },
        {
            'question': 'Bagaimana cara mendapatkan free API credits?',
            'answer': 'Banyak provider yang menawarkan free credits: OpenAI ($5), Google (generous free tier), Hugging Face (free inference API), OpenRouter (free models), Groq (free tier), dan lainnya. Cek halaman Free Resources untuk info lengkap.',
            'sort_order': 3, 'last_updated': '2026-06-17'
        },
        {
            'question': 'LLM mana yang terbaik untuk coding?',
            'answer': 'Untuk coding, rekomendasi kami: 1) Claude (Anthropic) — sangat bagus untuk complex coding, 2) GPT-4o (OpenAI) — versatile dan reliable, 3) Cursor — AI-powered code editor yang sangat powerful. Pilih tergantung kebutuhan dan budget Anda.',
            'sort_order': 4, 'last_updated': '2026-06-17'
        },
        {
            'question': 'Bisakah saya self-host LLM?',
            'answer': 'Ya! Model open source seperti Llama (Meta), Mistral, dan Qwen bisa di-self-host. Anda butuh GPU yang cukup (minimal 8GB VRAM untuk model kecil). Google Colab dan Kaggle menyediakan free GPU untuk testing.',
            'sort_order': 5, 'last_updated': '2026-06-17'
        },
        {
            'question': 'Bagaimana cara mulai belajar AI?',
            'answer': 'Mulai dari: 1) Pahami dasar Python, 2) Pelajari cara menggunakan API LLM, 3) Praktik prompt engineering, 4) Eksperimen dengan free tools, 5) Baca artikel edukasi di halaman Edukasi kami.',
            'sort_order': 6, 'last_updated': '2026-06-17'
        },
        {
            'question': 'Apa itu token dan bagaimana cara menghitung biaya LLM?',
            'answer': 'Token adalah unit terkecil yang diproses LLM. 1 token ≈ 4 karakter bahasa Inggris. Biaya dihitung berdasarkan jumlah input dan output tokens. Contoh: GPT-4o berharga $2.50 per 1M input tokens dan $10 per 1M output tokens. Baca artikel "Token dan Pricing" di halaman Edukasi untuk penjelasan lengkap.',
            'sort_order': 7, 'last_updated': '2026-06-17'
        },
        {
            'question': 'Apa bedanya fine-tuning dan RAG?',
            'answer': 'Fine-tuning melatih ulang model dengan data khusus Anda — cocok untuk format output yang konsisten. RAG (Retrieval Augmented Generation) mengambil informasi dari database eksternal — cocok untuk data yang sering berubah. Mulai dengan RAG karena lebih mudah dan murah.',
            'sort_order': 8, 'last_updated': '2026-06-17'
        },
        {
            'question': 'Bagaimana cara memilih LLM provider yang tepat?',
            'answer': 'Pertimbangkan: 1) Budget — DeepSeek/Groq paling murah, Claude/GPT-4o paling powerful, 2) Use case — coding? Claude. Research? Perplexity. Image? DALL-E/Midjourney, 3) Context window — Gemini 1M, Claude 200K, 4) Free tier — Google dan Groq paling generous. Coba beberapa provider dan bandingkan hasilnya.',
            'sort_order': 9, 'last_updated': '2026-06-17'
        },
        {
            'question': 'Apakah aman menggunakan API key?',
            'answer': 'API key aman selama Anda: 1) Tidak hardcode di source code, 2) Gunakan environment variables, 3) Set usage limits, 4) Monitor usage secara berkala, 5) Jangan share key ke orang lain. Baca artikel "API Key Security" di halaman Edukasi untuk panduan lengkap.',
            'sort_order': 10, 'last_updated': '2026-06-17'
        },
        {
            'question': 'Apa itu context window dan mengapa penting?',
            'answer': 'Context window adalah jumlah token maksimal yang bisa diproses LLM dalam satu percakapan. Semakin besar, semakin banyak informasi yang bisa diproses sekaligus. Gemini (1M) terbesar, diikuti Claude (200K) dan GPT-4o (128K). Penting untuk dokumen panjang dan percakapan panjang.',
            'sort_order': 11, 'last_updated': '2026-06-17'
        },
        {
            'question': 'Apa itu rate limit dan bagaimana mengatasinya?',
            'answer': 'Rate limit adalah batas jumlah request yang bisa Anda buat dalam periode waktu tertentu. Setiap provider punya limit berbeda. Cara mengatasinya: 1) Implement retry with exponential backoff, 2) Cache responses, 3) Gunakan queue untuk batch processing, 4) Upgrade tier jika perlu.',
            'sort_order': 12, 'last_updated': '2026-06-17'
        },
        {
            'question': 'Open source vs proprietary LLM — mana yang lebih baik?',
            'answer': 'Open source (Llama, Mistral, Qwen): Gratis, bisa self-host, bisa fine-tune, lebih transparan. Proprietary (GPT-4o, Claude, Gemini): Lebih powerful, mudah digunakan, support resmi. Gunakan open source untuk kontrol penuh dan cost saving, proprietary untuk kualitas terbaik dan kemudahan.',
            'sort_order': 13, 'last_updated': '2026-06-17'
        },
        {
            'question': 'Bisakah LLM menggantikan programmer?',
            'answer': 'Belum dan mungkin tidak akan sepenuhnya. LLM sangat bagus untuk: boilerplate code, debugging, learning, dan prototyping. Tapi masih butuh manusia untuk: system design, architecture decisions, understanding business requirements, dan code review. LLM adalah tool yang powerful, bukan pengganti.',
            'sort_order': 14, 'last_updated': '2026-06-17'
        },
        {
            'question': 'Bagaimana cara mengurangi hallucination dari LLM?',
            'answer': 'Hallucination adalah ketika LLM menghasilkan informasi salah dengan meyakinkan. Cara mengurangi: 1) Gunakan RAG untuk memberikan sumber yang valid, 2) Minta AI untuk sitasi, 3) Gunakan model yang lebih besar, 4) Berikan konteks yang spesifik, 5) Selalu verifikasi informasi penting, 6) Gunakan temperature rendah (0-0.3).',
            'sort_order': 15, 'last_updated': '2026-06-17'
        },
    ]

    if not FAQ.get_by_id(1):  # Only seed if empty
        for f in faqs:
            FAQ.create(f)
    print(f"✅ {len(faqs)} FAQs seeded")

    print("\n🎉 Database seeding complete!")


if __name__ == '__main__':
    seed()
