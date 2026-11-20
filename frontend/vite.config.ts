import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// The backend runs on :8000 (cd backend && .venv/Scripts/python -m uvicorn qalqon.api:app --port 8000).
// The dev server proxies /api to it, including the SSE live feed.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true },
    },
  },
  preview: {
    port: 4173,
    proxy: {
      '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true },
    },
  },
})
