# 🌿 HerSpace — A Safe Digital Sanctuary for Women

**HerSpace** is a digital wellness platform designed to support women emotionally, spiritually, and practically. It combines thoughtful UX, emotional intelligence, and backend power to provide a healing space for reflection, self-awareness, and empowerment.

> *“Sometimes, you don’t need to be fixed — you just need to be heard.”*

---

## ✨ Why HerSpace?

HerSpace isn’t just another productivity tool. It’s a sanctuary.  
A place where women can check in with their emotions, process their thoughts, track their rituals, and feel supported — especially in motherhood and burnout.

---

## 📦 Project Scope

### ✅ MVP Features

- [x] **User Auth**: JWT-based registration, login, and refresh
- [x] **Daily Mood Check-ins**: One per day, stored and analyzed
- [x] **Private Journaling**: Create, filter, and search journal entries
- [x] **Daily Task Flow**: Tasks for body, work, and soul
- [x] **Ritual Library**: Meditations, affirmations, and journaling prompts
- [x] **AI Assistant (DAGI)**: GPT-based empathetic AI assistant placeholder
- [x] **Admin Panel**: Manage rituals, wisdom messages, and user data
- [x] **API Documentation**: Swagger/OpenAPI interactive docs

---

## 🌸 Extended Features (Post-MVP)

### 🧘‍♀️ Emotional & Ritual Tracking

- ✅ Ritual Usage Tracker: Track which rituals users try, with mood before/after
- ✅ Effectiveness Rating (1-5 scale)
- ✅ Optional notes and insights
- ✅ Personal usage stats and history view

### ✉️ Wisdom Message System

- ✅ Personalized delivery of motivational messages
- ✅ Categories: comfort, power, reflection, grounding
- ✅ Fully manageable via Django admin

### 👩‍👧 Motherhood Support Space

- ✅ Journaling for mothers
- ✅ Childcare routines
- ✅ Motherhood-specific resources and emotional support tools

### 📊 Analytics

- ✅ Mood analytics: mood trends, daily distribution
- ✅ Task completion insights
- ✅ Journal usage patterns
- ✅ Insight model for user behavior (for future personalization)

### 🧑‍🤝‍🧑 Community Features

- ✅ Anonymous & non-anonymous community posting
- ✅ Support / celebration / gratitude categories
- ✅ Commenting and reactions (❤️ 🤗 🙏)
- ✅ Post moderation logic included

### 🔔 Notifications

- ✅ Scheduled and real-time notifications
- ✅ User preferences for reminders
- ✅ Statistics per notification type

---

## 🛠️ Tech Stack

| Layer             | Tech                              |
|------------------|-----------------------------------|
| **Backend**       | Django, Django REST Framework     |
| **Database**      | PostgreSQL                        |
| **Authentication**| JWT (djangorestframework-simplejwt) |
| **AI Integration**| OpenAI GPT (DAGI assistant)       |
| **Documentation** | Swagger / drf-spectacular         |
| **Deployment**    | Render, Railway (TBD)             |
| **Future Frontend**| Vue.js / Next.js (TBD)            |

---

## 🔐 Security Features

- ✅ JWT Auth with refresh
- ✅ API Rate Limiting (throttling)
- ✅ CORS and security headers
- ✅ Anonymous post protection
- ✅ .env file excluded from Git via `.gitignore`
- ✅ Ready for production security configuration

---

## 🔗 API Overview

### Authentication
- `POST /api/token/` – Login
- `POST /api/token/refresh/` – Refresh access token
- `POST /api/users/register/` – Register new user

### Journaling & Mood
- `GET/POST /api/journal/journal-entries/`
- `GET/POST /api/journal/mood-checkins/`
- `GET/POST /api/journal/daily-tasks/`
- `GET /api/journal/rituals/`  
- `POST /api/journal/dagi-ai/` – DAGI assistant (placeholder)

### Ritual Usage
- `POST /api/wellness/rituals/track/` – Track ritual and mood
- `GET /api/wellness/rituals/history/` – Ritual history with insights

### Wisdom Messages
- `GET /api/wisdom/messages/` – Fetch personalized messages

### Motherhood
- `GET/POST /api/motherhood/routines/`
- `GET/POST /api/motherhood/journal/`
- `GET /api/motherhood/resources/`
- `GET /api/motherhood/support-groups/`

### Analytics
- `GET /api/analytics/mood/`
- `GET /api/analytics/tasks/`
- `GET /api/analytics/journal/`
- `GET /api/analytics/insights/`

### Community
- `GET/POST /api/community/posts/`
- `GET/POST /api/community/posts/{id}/comments/`
- `POST /api/community/posts/{id}/reactions/`

### Notifications
- `GET /api/notifications/`
- `PATCH /api/notifications/preferences/`
- `POST /api/notifications/create/`
- `GET /api/notifications/stats/`

---

## 📂 Project Structure (Apps)

- `users` – Registration, auth, profiles
- `journal` – Journaling, moods, tasks, rituals, DAGI assistant
- `motherhood` – Motherhood-specific journaling and resources
- `community` – Anonymous and public posting
- `analytics` – Mood/task/journal usage insights
- `notifications` – Alerts, reminders, preferences
- `wisdom` – Custom motivational message system

---

## 🚀 Status & Next Steps

HerSpace backend is **complete and production-ready**.

### ✅ Done:
- Functional API with 6 structured Django apps
- Complete CRUD, validation, and security
- Admin panel for all core models
- Thorough testing with Postman
- Fully documented API with Swagger

### 🧩 Next Steps:
- [ ] Frontend development (Vue / Next.js)
- [ ] DAGI AI assistant (GPT-4o integration)
- [ ] User-facing dashboards and insights
- [ ] Stripe/TBC payment integration (optional)
- [ ] Cloud deployment (Render / Railway)

---

## 💬 Want to Collaborate?

Whether you’re a frontend dev, designer, AI researcher, or just excited about women-centered tech — feel free to fork, raise issues, or contribute!

---

## 🫶 Created with Heart

Built by **Benz** — a mother, creator, and developer on a mission to build soulful, safe, and smart digital spaces for women.

---

> _HerSpace isn’t just code. It’s a daily ritual, a mirror, and a companion for women’s emotional journey._  
