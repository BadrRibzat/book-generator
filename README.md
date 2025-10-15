# Book Generator SaaS

A credit-card-free, open-source SaaS platform that generates **complete, publish-ready digital books** (15–30 pages + professional cover) in PDF format using AI. Built for creators, educators, and indie publishers who want high-quality, niche-targeted books in seconds — with zero upfront cost.

> 🚀 **No bank account or payment method required** — built entirely with free-tier tools.

---

## ✨ Features

- **Niche-Optimized Content**: Choose from 15 evergreen sub-niches across 5 domains:
  - 📚 Language & Kids (e.g., personalized learning stories)
  - 💻 Technology & AI (e.g., no-code guides, AI ethics)
  - 🥑 Nutrition & Wellness (e.g., keto cookbooks, mental health nutrition)
  - 🧘 Meditation (e.g., anxiety workbooks, gratitude journals)
  - 💪 Home Workout (e.g., desk yoga, bodyweight plans)
- **Auto-Generated Titles**: Market-optimized titles for better discoverability.
- **Professional Covers**: 3 AI-assisted cover options per book (template-based).
- **Complete PDF Output**: Interior + cover merged into one downloadable file.
- **User Dashboard**: View, regenerate, or delete your book history.

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 4.2 + Django REST Framework
- **Database**: SQLite (dev) → MongoDB Atlas (free tier, no credit card)
- **AI**: Groq API (Llama 3.1 8B, free tier)
- **Async**: Django-Q (no Redis required)
- **PDF**: WeasyPrint (HTML/CSS → print-ready PDF)

### Frontend (Planned)
- Vue 3 + TypeScript + Tailwind CSS + DaisyUI

### Deployment (Planned)
- Backend: Render (free tier)
- Frontend: Vercel / Netlify
- Storage: Cloudflare R2 (free tier, no card)

---

## 🚦 Current Status

✅ Backend project initialized  
✅ User, Book, and Cover apps created  
✅ Groq API integration verified (`llama-3.1-8b-instant`)  
✅ Environment and dependency management ready  
✅ MIT Licensed  

> 🔜 Next: User authentication, book generation pipeline, and cover designer.

---

## 🧪 Test Groq Connection

```bash
cd backend
python test_groq.py
# Expected: "✅ Groq API connection successful!"

📜 License
MIT © 2025 Badr Ribzat


---

### ✅ Next Steps

Run these commands to commit and push:

```bash
# Add README
echo "# Book Generator SaaS

A credit-card-free, open-source SaaS platform that generates **complete, publish-ready digital books** (15–30 pages + professional cover) in PDF format using AI. Built for creators, educators, and indie publishers who want high-quality, niche-targeted books in seconds — with zero upfront cost.

> 🚀 **No bank account or payment method required** — built entirely with free-tier tools.

---

## ✨ Features

- **Niche-Optimized Content**: Choose from 15 evergreen sub-niches across 5 domains:
  - 📚 Language & Kids (e.g., personalized learning stories)
  - 💻 Technology & AI (e.g., no-code guides, AI ethics)
  - 🥑 Nutrition & Wellness (e.g., keto cookbooks, mental health nutrition)
  - 🧘 Meditation (e.g., anxiety workbooks, gratitude journals)
  - 💪 Home Workout (e.g., desk yoga, bodyweight plans)
- **Auto-Generated Titles**: Market-optimized titles for better discoverability.
- **Professional Covers**: 3 AI-assisted cover options per book (template-based).
- **Complete PDF Output**: Interior + cover merged into one downloadable file.
- **User Dashboard**: View, regenerate, or delete your book history.

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 4.2 + Django REST Framework
- **Database**: SQLite (dev) → MongoDB Atlas (free tier, no credit card)
- **AI**: Groq API (Llama 3.1 8B, free tier)
- **Async**: Django-Q (no Redis required)
- **PDF**: WeasyPrint (HTML/CSS → print-ready PDF)

### Frontend (Planned)
- Vue 3 + TypeScript + Tailwind CSS + DaisyUI

### Deployment (Planned)
- Backend: Render (free tier)
- Frontend: Vercel / Netlify
- Storage: Cloudflare R2 (free tier, no card)

---

## 🚦 Current Status

✅ Backend project initialized  
✅ User, Book, and Cover apps created  
✅ Groq API integration verified (\`llama-3.1-8b-instant\`)  
✅ Environment and dependency management ready  
✅ MIT Licensed  

> 🔜 Next: User authentication, book generation pipeline, and cover designer.

---

## 🧪 Test Groq Connection

\`\`\`bash
cd backend
python test_groq.py
# Expected: "✅ Groq API connection successful!"
\`\`\`

---

## 📜 License

MIT © 2025 [Badr Ribzat](https://github.com/BadrRibzat)
" > README.md

