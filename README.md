# 🚀 GitHub Webhook Receiver

A Flask-based webhook receiver that captures GitHub repository events and displays them in an elegant dashboard.

## 🌟 Features

- **Real-time GitHub event tracking** (Push, Pull Request, Merge)
- **Beautiful dashboard UI** with auto-refresh
- **MongoDB storage** for event persistence
- **RESTful API** for event retrieval
- **Responsive design** for mobile and desktop

## 📋 Prerequisites

- Python 3.7+
- MongoDB Atlas account (or local MongoDB)
- GitHub repository for webhook testing

## 🛠️ Setup

### 1. Clone and Setup Environment

```bash
# Create virtual environment
pip install virtualenv
virtualenv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/github_events?retryWrites=true&w=majority
```

### 3. Run the Application

```bash
python run.py
```

The application will start on `http://127.0.0.1:5000`

## 🔗 Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/webhook/` | Dashboard UI |
| `POST` | `/webhook/receiver` | GitHub webhook endpoint |
| `GET` | `/webhook/events` | All events API |
| `GET` | `/webhook/events/latest` | Recent events API |

## ⚙️ GitHub Webhook Setup

1. Go to your GitHub repository
2. Navigate to **Settings** → **Webhooks**
3. Click **"Add webhook"**
4. Set the payload URL to: `http://your-domain/webhook/receiver`
5. Select **"application/json"** as content type
6. Choose individual events:
   - ✅ **Pushes**
   - ✅ **Pull requests**
7. Click **"Add webhook"**

### 🌐 For Local Development

Use [ngrok](https://ngrok.com/) to expose your local server:

```bash
# Install ngrok and run
ngrok http 5000

# Use the HTTPS URL in GitHub webhook settings
# Example: https://abc123.ngrok.io/webhook/receiver
```

## 📊 Dashboard

Visit `http://127.0.0.1:5000/webhook/` to view the elegant dashboard featuring:

- **Event cards** with color-coded types
- **Real-time updates** (auto-refresh every 30s)
- **Event details** including author, branch, and timestamp
- **Responsive design** for all devices

## 🎯 Event Types Supported

| Event | Description | Display Color |
|-------|-------------|---------------|
| **Push** | Code pushed to repository | 🟢 Green |
| **Pull Request** | New pull request opened | 🔵 Blue |
| **Merge** | Pull request merged | 🟣 Purple |

## 🗂️ Project Structure

```
github-webhook-receiver/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── extensions.py        # MongoDB setup
│   └── webhook/
│       └── routes.py        # Webhook routes
├── templates/
│   └── index.html          # Dashboard UI
├── .env                    # Environment variables
├── requirements.txt        # Dependencies
├── run.py                 # Application entry point
└── README.md              # This file
```

## 🚀 Production Deployment

For production environments:

```bash
# Use Gunicorn instead of Flask dev server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 🛡️ Security Notes

- Never commit `.env` files to version control
- Use environment variables for sensitive data
- Consider implementing webhook signature verification for production use

## 📝 API Response Examples

### Event Object Structure
```json
{
  "type": "push",
  "message": "\"username\" pushed to \"main\" on 3rd July 2025 - 2:30 PM UTC",
  "timestamp": "3rd July 2025 - 2:30 PM UTC",
  "author": "username",
  "branch": "main",
  "created_at": "2025-07-03T14:30:00Z"
}
```

