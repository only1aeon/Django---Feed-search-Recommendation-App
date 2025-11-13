# Live-Social Recommendation & Hybrid Search Application

This repo includes:
- Django web app (feed + search)
- FAISS (sharded) vector search integration
- ASR lattice utilities (WhisperX hooks / stubs)
- Cross-encoder re-ranker (sentence-transformers / CrossEncoder)
- Docker + docker-compose for local dev

Quickstart (dev):
1. Copy `.env.dev.example` -> `.env.dev` and edit DB/Redis settings.
2. docker-compose up --build
3. python manage.py migrate
4. python manage.py createsuperuser
5. python manage.py index_videos
6. Use `/api/search?q=...` and `/api/recommend` endpoints.
