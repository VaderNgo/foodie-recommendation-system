# 🍽️ **Foodie Recommendation System** 🍽️  
A robust **Flask-based Recommendation System** that helps users discover **Dishes** and **Restaurants** they will love! Powered by **Collaborative Filtering** and integrated with PostgreSQL for efficient data management.  

![Python](https://img.shields.io/badge/Python-3.9-blue?style=flat-square&logo=python) 
![Flask](https://img.shields.io/badge/Flask-2.0.1-black?style=flat-square&logo=flask)  
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=flat-square&logo=postgresql) 
![Numpy](https://img.shields.io/badge/Numpy-Matrix%20Operations-013243?style=flat-square&logo=numpy)  
![Gunicorn](https://img.shields.io/badge/Gunicorn-Server-green?style=flat-square&logo=gunicorn)  
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?style=flat-square&logo=docker)  
![Railway](https://img.shields.io/badge/Railway-Deployment-444?style=flat-square&logo=railway)

---

## 🚀 **Project Overview**
The **Foodie Recommendation System** allows users to get personalized **dish** and **restaurant recommendations** based on user ratings. Built using collaborative filtering algorithms, the system calculates user-item similarities and generates suggestions.

### Key Features:
✅ **Collaborative Filtering** for personalized recommendations.  
✅ API endpoints for both **Dishes** and **Restaurants**.  
✅ Flask-based RESTful API architecture.  
✅ PostgreSQL integration for scalable storage.  
✅ Ready-to-deploy with Docker & Railway.  

---

## 🛠️ **Technologies Used**
| Technology         | Description                           |
|---------------------|---------------------------------------|
| **Python**         | Core backend logic and calculations. |
| **Flask**          | Lightweight web framework for APIs.  |
| **PostgreSQL**     | Database for storing user, dishes, and reviews data. |
| **NumPy**          | Matrix operations for collaborative filtering. |
| **Gunicorn**       | Production server for Flask app.     |
| **Docker**         | Containerization for easy deployment. |
| **Railway**        | Hosting and environment management.  |

---

## ⚙️ **Setup Instructions**

### Prerequisites:
- Python 3.9+
- Docker & Docker Compose
- PostgreSQL

### 1. **Clone the Repository**
```bash
git clone https://github.com/your-username/foodie-recommendation.git
cd foodie-recommendation
```

### 2. **Set Up Environment Variables**  
Create a `.env` file in the root directory and add:
```dotenv
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=your_postgres_host
POSTGRES_PORT=5432
POSTGRES_DATABASE=your_db_name
FOODIE_DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
```

### 3. **Build and Run Docker Container**
```bash
docker-compose up --build
```
- App will run on: **`http://localhost:5000`**

---

## 🔑 **API Endpoints**

### **Test Endpoint**
```http
GET /
```
**Response:**
```json
{"hello": "world"}
```

### **Get Models Data**
```http
GET /models
```

### **Recommended Dishes**
```http
GET /recommended-dishes?userId=<user_id>&n=<number_of_recommendations>
```
**Response:** A list of recommended **Dish IDs**.

### **Recommended Restaurants**
```http
GET /recommended-restaurants?userId=<user_id>&n=<number_of_recommendations>
```
**Response:** A list of recommended **Restaurant IDs**.

---

## 🧪 **Testing the Project**
1. Populate the PostgreSQL database with mock data for `AspNetUsers`, `Dishes`, `DishReview`, `Restaurants`, and `RestaurantReviews`.  
2. Test the API endpoints using tools like **Postman** or **curl**.  
3. Example:
```bash
curl "http://localhost:5000/recommended-dishes?userId=123&n=5"
```

---

## 🛦️ **Deployment**
The project is pre-configured for deployment using **Railway** or other cloud platforms supporting Docker. Update your environment variables and trigger the build pipeline.

---

## 🏅 **Badges**
![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=flat-square&logo=github)  
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)  
![Status](https://img.shields.io/badge/Status-Production-ready-brightgreen?style=flat-square)  

---

## 💡 **Future Improvements**
- Add support for **content-based recommendations**.  
- Improve recommendation accuracy with hybrid models.  
- Add **user authentication** and **feedback system**.  

---

## 🤝 **Contributing**
We welcome contributions! To get started:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Submit a Pull Request.

---

## 📄 **License**
This project is licensed under the **MIT License**.

---

## 👨‍💻 **Author**
- **Ngo Duc Loc**  
  [![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=flat-square&logo=linkedin)]([https://www.linkedin.com/in/your-profile](https://www.linkedin.com/in/ngoducloc/))  

---

🎉 **Thank you for exploring the Foodie Recommendation System!** 🎉  
