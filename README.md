# Weather Game Project

## **Concept**
The **Weather Game Project** is an interactive survival game that incorporates real-time weather data and multiplayer functionality. Players manage their survival stats such as health, hunger, and sanity while dealing with environmental challenges that are influenced by real-world weather conditions. The game aims to provide a unique blend of fitness, strategy, and engagement.

### **Key Features**
- **Dynamic Weather System**:
  - Integrates real-time weather data using a weather API.
  - Influences gameplay with conditions like rain, snow, and thunderstorms.

- **Multiplayer Rooms**:
  - Players can create and join game rooms.
  - Includes a chatbox for team communication.

- **Resource and Inventory Management**:
  - Players collect resources like wood and stone to craft tools.
  - Manages player inventory with items that influence survival.

- **Player Stats**:
  - Tracks health, hunger, and sanity over time, which are affected by gameplay and weather.

---

## **Current Status**
While significant progress has been made, several key issues prevent the project from functioning as intended. These issues are outlined below.

### **Known Issues**
1. **Backend Challenges**:
   - **WebSocket Errors**:
     - Flask-SocketIO raises `RuntimeError` when running with Werkzeug, requiring changes for compatibility with production-grade servers like `eventlet`.
   - **Missing Player States**:
     - When saving game data, `PlayerState` for certain users is not persisted correctly, causing save/load inconsistencies.
   - **Room and Resource Bugs**:
     - Some resources are missing critical `room_id` associations, resulting in database integrity errors.

2. **Frontend Challenges**:
   - **Incomplete Integration**:
     - The frontend has partial implementations for chat functionality and game stats but lacks full linkage to backend APIs.
   - **Game Interface Design**:
     - Visual elements like the chatbox and player stats are functional but require testing for dynamic updates.

3. **CI/CD and Docker Issues**:
   - **CodeQL and Dependabot**:
     - Automated security analysis and dependency updates are not yet configured.
   - **Docker Runtime**:
     - The current Docker setup results in Flask-SocketIO errors, preventing the app from running in containers without modifications.

4. **Deployment**:
   - The app is not yet deployed to AWS or any hosting platform.

---

## **How to Run the Project**

### **Requirements**
- **Python 3.9+**
- **PostgreSQL** (for database backend)
- **Docker** (for containerized environments)

### **Setup Instructions**

#### **1. Clone the Repository**
git clone https://github.com/Hussein-Alhajam/Weather-Game-Project.git
cd Weather-Game-Project

#### **2. Install Dependencies**
pip install -r backend/requirements.txt

#### **3. Run the Application**
python backend/app.py

#### **4. Build and Run Using Docker**
docker build -t weather-game .
docker run -p 5000:5000 weather-game


## **Project Roadmap**
Project Roadmap
Fix Backend Errors:

Address issues with PlayerState persistence and database integrity.
Enhance Frontend:

Complete the game interface and ensure smooth interaction with backend APIs.
Improve CI/CD:

Add CodeQL analysis and Dependabot for security and dependency management.
Deployment:

Deploy the app to AWS Elastic Beanstalk with proper SSL configuration

### **Credits**
1. `Hussein-Alhajam`, 100727390 
