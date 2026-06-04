## AI Marketing Post Generator

Full‑stack demo app that turns a short product brief into ready‑to‑use marketing copy.

- **Frontend**: Vue 3 (Composition API) + Vite, mobile‑first, dark mode, toasts, copy/export
- **Backend**: FastAPI + SQLite + SQLModel, OpenAI / Gemini AI integration

### Folder structure

- `backend/`
  - `app/main.py` – FastAPI app entrypoint
  - `app/api/routes.py` – `/api/generate`, `/api/history`, `/api/history/{id}`
  - `app/core/config.py` – settings and env variables
  - `app/db/session.py` – SQLite engine and session
  - `app/models/history.py` – generated history table
  - `app/schemas/generation.py` – request/response schemas
  - `app/services/ai_generator.py` – OpenAI / Gemini prompt + call
  - `.env.example` – example environment configuration
  - `requirements.txt` – backend Python dependencies
- `frontend/`
  - `src/main.ts` – Vue entry
  - `src/router/index.ts` – Home / Generate / History routes
  - `src/App.vue` – layout shell, nav, dark‑mode toggle, toasts
  - `src/pages/HomePage.vue` – intro page
  - `src/pages/GeneratePage.vue` – main generator with validation
  - `src/pages/HistoryPage.vue` – history list and deletion
  - `src/components/GenerateForm.vue` – form + API integration
  - `src/components/ResultCard.vue` – output with copy/export
  - `src/components/LoadingSpinner.vue` – loading state
  - `src/components/DarkModeToggle.vue` – dark mode
  - `src/components/ToastContainer.vue` – toast notifications
  - `src/services/api.ts` – axios client

---

## Backend – FastAPI

### 1. Create and activate virtual environment

From `backend/`:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in:

```bash
cp .env.example .env
```

Important keys:

- **`DATABASE_URL`** – usually `sqlite:///./ai_marketing.db`
- **`AI_PROVIDER`** – `openai` or `gemini`
- **OpenAI**
  - `OPENAI_API_KEY`
  - `OPENAI_MODEL` (e.g. `gpt-4o-mini`)
- **Gemini**
  - `GEMINI_API_KEY`
  - `GEMINI_MODEL` (e.g. `gemini-1.5-flash`)
- **`BACKEND_CORS_ORIGINS`** – set to your frontend origin (e.g. `http://localhost:5173` or your Vercel URL)

### 4. Run the backend locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at:

- `http://localhost:8000/api/generate`
- `http://localhost:8000/api/history`
- `http://localhost:8000/api/history/{id}`

Interactive docs:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

### REST API overview

- **POST `/api/generate`**
  - Body:

    ```json
    {
      "product_name": "EcoGlow LED Desk Lamp",
      "product_description": "Energy‑efficient lamp with adjustable arm and warm/cool light modes.",
      "target_audience": "Remote workers who care about eye comfort and modern design",
      "platform_type": "Instagram"
    }
    ```

  - Response:

    ```json
    {
      "id": 1,
      "caption": "...",
      "short_ad_text": "...",
      "hashtags": ["#marketing", "#sale"],
      "email_subject": "...",
      "cta": "Buy now",
      "created_at": "2026-05-27T06:00:00.000000Z"
    }
    ```

- **GET `/api/history`**

  - Response:

    ```json
    {
      "items": [
        {
          "id": 1,
          "product_name": "...",
          "product_description": "...",
          "target_audience": "...",
          "platform_type": "Facebook",
          "caption": "...",
          "short_ad_text": "...",
          "hashtags": ["#x", "#y"],
          "email_subject": "...",
          "cta": "...",
          "created_at": "..."
        }
      ]
    }
    ```

- **DELETE `/api/history/{id}`**
  - Deletes a stored history item. Returns status `204 No Content` on success.

---

## Frontend – Vue 3 + Vite

### 1. Install dependencies

From `frontend/`:

```bash
cd frontend
npm install
```

### 2. Configure API base URL

Create `.env` in `frontend/`:

```bash
VITE_API_BASE_URL=http://localhost:8000/api
```

Later, change this to your deployed backend URL (Render) when you go live.

### 3. Run the frontend locally

```bash
npm run dev
```

The app runs at `http://localhost:5173`.

### Frontend features

- **Home Page**
  - Overview of the tool and quick links to generate or view history.
- **Generate Page**
  - Validated form for:
    - Product name
    - Product description
    - Target audience
    - Platform type (Facebook, TikTok, Instagram)
  - Uses axios to call `POST /api/generate`
  - Loading spinner while waiting for AI
  - Toast notifications on success/error
  - Display:
    - Marketing caption
    - Short advertisement text
    - Hashtags
    - Email subject
    - Call to action
  - **Bonus**
    - Dark mode toggle
    - Copy buttons for each field
    - Copy all
    - Export result to `.txt`
- **History Page**
  - Fetches data from `GET /api/history`
  - Shows previous generations with metadata
  - `DELETE /api/history/{id}` to remove an item

---

## Deployment

### Backend on Render

1. Push this repo to GitHub.
2. In Render:
   - Create a **New Web Service**.
   - Connect your repository.
   - Select the `backend` folder as the root if prompted, or set:
     - **Build command**: `pip install -r backend/requirements.txt`
     - **Start command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - Use a Python environment (3.11+).
3. Add environment variables in Render:

   - `DATABASE_URL=sqlite:///./ai_marketing.db`
   - `AI_PROVIDER=openai` (or `gemini`)
   - `OPENAI_API_KEY=...` and `OPENAI_MODEL=...` (if using OpenAI)
   - `GEMINI_API_KEY=...` and `GEMINI_MODEL=...` (if using Gemini)
   - `BACKEND_CORS_ORIGINS=https://your-frontend-domain.vercel.app`

4. Deploy. Note the public URL, e.g. `https://ai-marketing-api.onrender.com`.

Check the docs at `https://ai-marketing-api.onrender.com/docs`.

### Frontend on Vercel

1. Push the repo to GitHub (same repo as backend is fine).
2. In Vercel:
   - **New Project** → Import the repository.
   - Set **Root Directory** to `frontend/`.
   - Build settings:
     - **Framework**: Vite
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`
3. Add environment variable:

   - `VITE_API_BASE_URL=https://your-backend-url.onrender.com/api`

4. Deploy.

After deployment:

- Visit your Vercel URL (`https://ai-marketing-frontend.vercel.app`).
- The frontend will call the Render backend using `VITE_API_BASE_URL`.

---

## Notes and customization

- **Switching AI provider**
  - Change `AI_PROVIDER` in backend `.env` to `openai` or `gemini`.
  - Ensure corresponding API keys and models are set.
- **Styling**
  - All base styles live in `frontend/src/styles/base.css`. You can easily tweak colors and spacing there.
- **Validation**
  - Simple, beginner‑friendly validation is implemented in `GenerateForm.vue`. You can extend it or replace it with a validation library later if needed.

This project is intentionally small and readable so beginners can understand both the FastAPI backend and Vue 3 frontend end‑to‑end.
