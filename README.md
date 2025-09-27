# MeetMogger AI 🚀

A powerful AI-powered call transcript analysis tool that provides deep insights from customer conversations. Analyze themes, sentiment, and extract actionable items to drive your business forward.

## 🌐 Live Demo

**Try it now!** [View Live Demo](https://pandiharshan.github.io/MeetMogger-AI/)

**Demo Credentials:**
- Email: `demo@meetmogger.ai`
- Password: `demo123`

*Note: The live demo uses mock data and doesn't require a backend server or API keys.*

## ✨ Features

- **🔐 User Authentication**: Secure MongoDB-based user registration and login
- **🎯 Theme Classification**: Automatically categorize calls by their primary topic
- **😊 Sentiment Analysis**: Understand customer mood and tone
- **📋 Actionable Extraction**: Extract problems, solutions, and action items
- **🎨 Modern UI**: Beautiful, responsive interface with dark theme
- **⚡ Real-time Analysis**: Instant AI-powered insights

## 🛠️ Tech Stack

- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS
- **Backend**: Node.js, Express.js
- **Database**: MongoDB with Mongoose
- **Authentication**: JWT tokens, bcryptjs
- **AI**: Google Gemini API
- **Styling**: Tailwind CSS with custom animations

## 📋 Prerequisites

Before running this project, make sure you have:

- **Node.js** (v18 or higher)
- **MongoDB** (local installation or MongoDB Atlas)
- **Google Gemini API Key**

## 🎮 Demo Mode

The application includes a **Demo Mode** that works without any backend setup:

- **No MongoDB required** - Uses mock authentication
- **No API keys needed** - Uses simulated AI responses
- **Instant setup** - Just clone and run
- **Full functionality** - Experience all features

To enable demo mode, the application automatically detects when running on GitHub Pages and switches to demo mode.

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Pandiharshan/MeetMogger-AI.git
cd MeetMogger-AI
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Environment Setup

Create a `.env` file in the root directory:

```bash
# Gemini AI API Key
GEMINI_API_KEY=your_actual_gemini_api_key_here

# MongoDB Connection String
MONGODB_URI=mongodb://localhost:27017/meetmogger-ai

# JWT Secret for authentication
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production

# Server Port
PORT=3001
```

### 4. Start MongoDB

**Option A: Local MongoDB**
```bash
# Make sure MongoDB service is running
# On Windows: MongoDB should start automatically
# On macOS: brew services start mongodb-community
# On Linux: sudo systemctl start mongod
```

**Option B: MongoDB Atlas**
- Create a free account at [MongoDB Atlas](https://www.mongodb.com/atlas)
- Create a cluster and get your connection string
- Replace `MONGODB_URI` in `.env` with your Atlas connection string

### 5. Run the Application

**Terminal 1 - Start Backend Server:**
```bash
npm run server
```

**Terminal 2 - Start Frontend:**
```bash
npm run dev
```

### 6. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:3001
- **Health Check**: http://localhost:3001/api/health

## 📱 Usage

### 1. Create Account
- Click "Get Started" on the homepage
- Click "Don't have an account? Sign up"
- Fill in your details and create an account

### 2. Login
- Use your credentials to sign in
- You'll be redirected to the analysis page

### 3. Analyze Call Transcripts
- Paste your call transcript in the input field
- Click "Analyze" to get AI-powered insights
- View detailed analysis including:
  - Theme classification
  - Sentiment analysis
  - Problems and solutions
  - Action items
  - Summary

## 🔧 Available Scripts

```bash
# Development
npm run dev          # Start frontend development server
npm run server       # Start backend server
npm run build        # Build for production
npm run preview      # Preview production build

# Database
npm run test-mongodb # Test MongoDB connection
```

## 🗄️ Database Schema

### User Model
```javascript
{
  email: String (unique, required)
  password: String (hashed, required)
  name: String (required)
  createdAt: Date
  updatedAt: Date
}
```

## 🔐 Authentication

The application uses JWT tokens for authentication:
- Tokens expire after 7 days
- Passwords are hashed using bcryptjs
- User sessions are stored in localStorage

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Health Check
- `GET /api/health` - Server health status

## 🐛 Troubleshooting

### Common Issues

**1. MongoDB Connection Error**
```bash
# Check if MongoDB is running
# Windows: Check Services for "MongoDB"
# macOS: brew services list | grep mongodb
# Linux: sudo systemctl status mongod
```

**2. Port Already in Use**
```bash
# Kill process using port 3001
# Windows: netstat -ano | findstr :3001
# macOS/Linux: lsof -ti:3001 | xargs kill -9
```

**3. Environment Variables Not Loading**
- Make sure `.env` file is in the root directory
- Restart both server and frontend after changing `.env`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Pandi Harshan K** - [@Pandiharshan](https://github.com/Pandiharshan)
- **Mukesh Kumar** - [@MukeshKumar-17](https://github.com/MukeshKumar-17)

## 🙏 Acknowledgments

- Google Gemini AI for powerful language analysis
- MongoDB for reliable data storage
- React and Vite for the amazing development experience
- Tailwind CSS for beautiful styling

---

**⭐ Star this repository if you found it helpful!**
