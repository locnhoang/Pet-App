
## Docker Instructions:
#To run the backend using Docker:  
#1. **Build the Docker image**  
  Make sure you're in the `backend/` folder and run: `docker build -t team23-backend .`.  
#2. **Run the Docker container**  
  `docker run -p 5004:5004 team23-backend`  
#3. **Access the backend**  
  #Open your browser and go to:  
  `http://localhost:5004`  

## Frontend Instructions

1. In the `backend/` directory:
   - Run `pip install -r requirements.txt`
   - Initialize the database: `python initialize_db.py`
   - Start the backend server: `python main.py`

2. In a second terminal, go to the `frontend/` directory:
   - Run `npm install`
   - Start the frontend server: `npm run dev`

3. Open your browser and visit:  
   `http://localhost:5173/`

4. Click the **Login** button in the navigation bar.  
   - Use the form to **sign up** with your name, email, and password  
   - Then enter the same email + password and click **Login**  
   - You should see: `"Login successful! User ID: ..."`
