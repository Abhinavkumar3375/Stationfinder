
This is a Flask web application that allows users to:

Search for bus routes between districts in Himachal Pradesh.

View stop-to-stop schedules.

Interact with a chatbot for route and station queries.

Manage bookings and user sessions.

Submit and view feedback (admin view enabled).

Explore bus schedules with live data and sample defaults.

🚀 Features
🔍 Bus Route Search between Himachal districts

💬 Chatbot Interface using OpenAI for route/station info

📅 Bus Schedules by stop-to-stop matching

🧑‍💼 User Authentication (Login/Signup)

📋 Admin Dashboard for feedback and chat logs

📄 Feedback Submission and Viewer

🧭 Interactive UI Pages: Map, Bus Info, Blogs, Dashboard, About

🔧 MongoDB Integration for storing users, feedback, chat logs, and bookings

🛠️ Tech Stack
Backend: Python (Flask)

Frontend: HTML, CSS, Jinja2 templates

Database: MongoDB

APIs: OpenAI GPT (for chatbot)

Data Handling: Pandas, CSV files

📂 Project Structure
bash
Copy
Edit
.
├── app.py                 # Main Flask application
├── himachal_routes.csv   # District-to-district route dataset
├── stop_schedule.csv     # Stop-wise bus timings
├── templates/            # HTML templates (Jinja2)
├── static/               # CSS, JS, and static assets
├── config.py             # Configuration file (API keys, etc.)
├── .env                  # Environment variables
🔧 Setup Instructions
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/yourusername/himachal-bus-app.git
cd himachal-bus-app
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Environment Setup
Create a .env file with your configuration:

env
Copy
Edit
OPENAI_API_KEY=your_openai_key
MONGO_URI=mongodb://localhost:27017/redbus_clone
4. Run the App
bash
Copy
Edit
python app.py
Visit http://127.0.0.1:5000 in your browser.

👤 Contributors
Abhinav Kumar - abhinavkumar3375@gmail.com

Hardik - HARDIK4376@gmail.com

Muskan Sharma - muskanSharma5547@gmail.com

Muskan - muskan5547@gmail.com

💡 Future Improvements
Add payment gateway for booking

Integrate live GPS tracking of buses

Expand dataset for more accurate scheduling

Add admin authentication and logs viewer

📃 License
This project is licensed under the MIT License. See LICENSE for more information.
