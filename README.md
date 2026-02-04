# 🤖 AI Integrated Dynamic Quiz Application

## 📌 Project Overview
This project is an **AI-based dynamic quiz web application** developed using **HTML, CSS, Bootstrap, JavaScript, and Flask/Django**. Users can log in, enter a topic, choose a difficulty level (Easy, Medium, Hard), and generate quizzes dynamically using AI. The application evaluates answers, calculates scores, and stores quiz history in a database.

---

## 🔗 Project Links
- **GitHub Repository:**  
  https://github.com/your-username/ai-dynamic-quiz-app

- **Live Demo (Deployed App):**  
  https://your-app-name.onrender.com  
  *(or Railway / PythonAnywhere / AWS)*

---

## ✨ Features
- User authentication (Login / Signup)
- AI-based quiz generation (topic-based)
- Difficulty levels: Easy, Medium, Hard
- Automatic score evaluation
- Quiz history per user
- Admin dashboard for monitoring users and results
- Responsive UI using Bootstrap

---

## 🛠️ Technologies Used

### Frontend
- HTML  
- CSS  
- Bootstrap  
- JavaScript  

### Backend
- Flask / Django (Python)

### Database
- SQLite (development)
- MySQL (production-ready)

### AI Integration
- OpenAI (GPT-4 / GPT-4 Mini)

---

## 🔄 Application Flow
1. User registers or logs in  
2. User enters quiz topic and selects difficulty  
3. Backend sends request to AI for question generation  
4. 10 MCQs are displayed to the user  
5. User submits answers  
6. Backend evaluates responses and calculates score  
7. Result and correct answers are displayed  
8. Quiz history is saved and linked to the logged-in user  

---

## 🗄️ Database Structure
- **Users Table**
  - Stores user details and role (user/admin)
- **Quiz Results Table**
  - Stores topic, score, date, and user reference

Admins can view all users and quiz attempts, while users can only access their own history.

---

## 🔐 User Roles
- **User:** Attempt quizzes and view personal history  
- **Admin:** View all users, quiz results, and performance data  

---

## 🚀 Future Enhancements
- Timer-based quizzes
- Leaderboard
- Detailed analytics
- Email notifications
- More AI customization

---

## 📦 Deployment
The project is suitable for deployment on:
- Render
- Railway
- PythonAnywhere
- AWS / VPS

---

## 👨‍💻 Author
Built as a full-stack learning project focusing on **AI integration, backend logic, authentication, and database design**.
