from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_pymongo import PyMongo
import pandas as pd
import openai
import requests
from datetime import datetime
import os
from config import Config
from dotenv import load_dotenv
load_dotenv()
import random


app = Flask(__name__)



# THE MOODEL SECTION OF THE PAGE 


routes_df = pd.read_csv('himachal_routes.csv')


app.secret_key = "super-secret-key"  # Required for session and flash messages

# --- MongoDB Setup ---
app.config["MONGO_URI"] = "mongodb://localhost:27017/redbus_clone"  # Local MongoDB URI
mongo = PyMongo(app)

# --- OpenAI API Key ---
openai.api_key = "1350a285c5e961566115d1868a8061084600253211dd599e536d1b6b69755bce"
# Load stop schedule CSV with error handling
try:
    stop_schedules = pd.read_csv('stop_schedule.csv')
except FileNotFoundError:
    print("Error: 'stop_schedule.csv' not found.")
    stop_schedules = pd.DataFrame(columns=['Stop', 'Departure Time'])

# Process function to match start and end bus schedules
def process_stop_schedules(start_stop, end_stop):
    if start_stop not in stop_schedules['Stop'].values or end_stop not in stop_schedules['Stop'].values:
        return []

    start_buses = stop_schedules[stop_schedules['Stop'] == start_stop]['Departure Time'].tolist()
    end_buses = stop_schedules[stop_schedules['Stop'] == end_stop]['Departure Time'].tolist()

    bus_schedules = []

    for start_entry in start_buses:
        for end_entry in end_buses:
            start_times = start_entry.split(', ')
            end_times = end_entry.split(', ')

            for start_time in start_times:
                try:
                    start_bus_id, start_arrival_time = start_time.split(': ')
                except ValueError:
                    continue  # skip malformed data

                for end_time in end_times:
                    try:
                        end_bus_id, end_arrival_time = end_time.split(': ')
                    except ValueError:
                        continue

                    if start_bus_id == end_bus_id:
                        bus_schedules.append({
                            'Bus ID': start_bus_id,
                            'Start Time': start_arrival_time,
                            'End Time': end_arrival_time
                        })
    return bus_schedules

# Route for filtering stops (AJAX search)
@app.route('/filter_stops', methods=['GET'])
def filter_stops():
    query = request.args.get('query', '')
    filtered_stops = stop_schedules[stop_schedules['Stop'].str.contains(query, case=False, na=False)]['Stop'].unique().tolist()
    return jsonify(filtered_stops)

# Main route to display the form and bus schedules
@app.route('/', methods=['GET', 'POST'])
# def index():
#     bus_schedules = []
#     start_stop = ''
#     end_stop = ''

#     if request.method == 'POST':
#         start_stop = request.form.get('start_stop')
#         end_stop = request.form.get('end_stop')

#         if start_stop and end_stop:
#             bus_schedules = process_stop_schedules(start_stop, end_stop)

#     return render_template('index.html', start_stop=start_stop, end_stop=end_stop, bus_schedules=bus_schedules)



def index():
    bus_schedules = []
    start_stop = ''
    end_stop = ''

    # Dummy default schedule options
    dummy_schedule_options = [
        [{'Bus ID': 'Bus101', 'Start Time': '08:00', 'End Time': '09:00'},
         {'Bus ID': 'Bus202', 'Start Time': '10:00', 'End Time': '11:30'}],
        [{'Bus ID': 'Bus303', 'Start Time': '07:15', 'End Time': '08:45'},
         {'Bus ID': 'Bus404', 'Start Time': '12:00', 'End Time': '13:15'}],
        [{'Bus ID': 'Bus505', 'Start Time': '09:30', 'End Time': '10:30'},
         {'Bus ID': 'Bus606', 'Start Time': '14:00', 'End Time': '15:20'}]
    ]
    default_schedules = random.choice(dummy_schedule_options)

    if request.method == 'POST':
        start_stop = request.form.get('start_stop')
        end_stop = request.form.get('end_stop')

        if start_stop and end_stop:
            bus_schedules = process_stop_schedules(start_stop, end_stop)

    return render_template(
        'index.html',
        start_stop=start_stop,
        end_stop=end_stop,
        bus_schedules=bus_schedules,
        default_schedules=default_schedules
    )


# --- Load Data Safely ---
# try:
#     stop_schedules = pd.read_csv('stop_schedule.csv')
# except FileNotFoundError:
#     stop_schedules = pd.DataFrame(columns=['Stop', 'Departure Time'])  # Fallback

# try:
#     routes = pd.read_csv('routes.csv')
# except FileNotFoundError:
#     routes = pd.DataFrame(columns=['Bus ID', 'Start Stop', 'End Stop'])  # Fallback

# try:
#     stops = pd.read_csv('stops.csv')
# except FileNotFoundError:
#     stops = pd.DataFrame(columns=['Stop', 'Location'])  # Fallback

# # --- Function to Process Stop Schedules ---
# def process_stop_schedules(start_stop, end_stop):
#     # Filter stops
#     start_buses = stop_schedules[stop_schedules['Stop'] == start_stop]['Departure Time'].tolist()
#     end_buses = stop_schedules[stop_schedules['Stop'] == end_stop]['Departure Time'].tolist()
    
#     bus_schedules = []
    
#     for start_entry in start_buses:
#         for end_entry in end_buses:
#             start_times = start_entry.split(', ')
#             end_times = end_entry.split(', ')
            
#             for start_time in start_times:
#                 try:
#                     start_bus_id, start_arrival_time = start_time.split(': ')
#                 except ValueError:
#                     continue  # Skip incorrectly formatted data
                
#                 for end_time in end_times:
#                     try:
#                         end_bus_id, end_arrival_time = end_time.split(': ')
#                     except ValueError:
#                         continue
                    
#                     if start_bus_id == end_bus_id:
#                         bus_schedules.append({
#                             'Bus ID': start_bus_id,
#                             'Start Time': start_arrival_time,
#                             'End Time': end_arrival_time
#                         })
    
#     return bus_schedules

# # Example Execution
# start_stop = 'A'
# end_stop = 'B'
# schedule = process_stop_schedules(start_stop, end_stop)
# print(schedule)
# # --- Routes ---


# app = Flask(__name__)

# # Load stop schedules safely
# try:
#     stop_schedules = pd.read_csv('stop_schedule.csv')
# except FileNotFoundError:
#     stop_schedules = pd.DataFrame(columns=['Stop'])  # Fallback empty DataFrame

# @app.route('/filter_stops', methods=['GET'])
# def filter_stops():
#     query = request.args.get('query', '')
    
#     if not query:  # Handle empty query gracefully
#         return jsonify({"error": "Query parameter is missing"}), 400
    
#     # Check if 'Stop' column exists to prevent errors
#     if 'Stop' not in stop_schedules.columns:
#         return jsonify({"error": "Stop column is missing in dataset"}), 500

#     # Filter stops safely
#     filtered_stops = stop_schedules[stop_schedules['Stop'].astype(str).str.contains(query, case=False, na=False)]['Stop'].unique().tolist()
    
#     return render_template({"bus.html": filtered_stops})


# @app.route('/all_urls')
# def all_urls():
#     routes = [rule.rule for rule in app.url_map.iter_rules() if "GET" in rule.methods and not rule.rule.startswith('/static')]
#     return render_template('all_urls.html', routes=sorted(routes))

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         start_stop = request.form['start_stop']
#         end_stop = request.form['end_stop']
#         bus_schedules = process_stop_schedules(start_stop, end_stop)

#         # Optional: Save to bookings
#         if 'user' in session:
#             mongo.db.bookings.insert_one({
#                 'user': session['user'],
#                 'start_stop': start_stop,
#                 'end_stop': end_stop,
#                 'buses': bus_schedules,
#                 'timestamp': datetime.utcnow()
#             })
        
#         # Return the rendered index page with schedules
#         return render_template('index.html', start_stop=start_stop, end_stop=end_stop, bus_schedules=bus_schedules)
    
#     return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html', par={"twitter_url": "https://twitter.com/example", "facebook_url": "https://facebook.com/example"})


@app.route('/bus')
def bus():
    return render_template('bus.html', par={"twitter_url": "https://twitter.com/example", "facebook_url": "https://facebook.com/example"})

@app.route('/map')
def map():
    return render_template('map.html', par={"twitter_url": "https://twitter.com/example", "facebook_url": "https://facebook.com/example"})

@app.route('/chatbot')
def chat():
    return render_template('chatbot.html', par={"twitter_url": "https://twitter.com/example", "facebook_url": "https://facebook.com/example"})

@app.route('/contact')
def contact():
    return render_template('contact.html', par={"twitter_url": "https://twitter.com/example", "facebook_url": "https://facebook.com/example"})

@app.route('/blogs')
def blogs():
    return render_template('blogs.html', par={"twitter_url": "https://twitter.com/example", "facebook_url": "https://facebook.com/example"})


@app.route('/adminpanel')
def adminpanel():
    return render_template('adminpanel.html', par={"twitter_url": "https://twitter.com/example", "facebook_url": "https://facebook.com/example"})


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash("Please log in to access the dashboard!", "danger")
        return redirect(url_for('login'))
    
    bookings = list(mongo.db.bookings.find({'user': session['user']}))
    return render_template('dashboard.html', bookings=bookings)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = mongo.db.users.find_one({'username': username, 'password': password})
        if user:
            session['user'] = username
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials, please try again.", "danger")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if mongo.db.users.find_one({'username': username}):
            flash("User already exists. Try logging in.", "warning")
            return redirect(url_for('login'))
        mongo.db.users.insert_one({'username': username, 'password': password})
        flash("Signup successful! You can now log in.", "success")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out!", "info")
    return render_template('home.html')

@app.route('/post/<string:post_slug>') 
def post(post_slug):
    return render_template('post.html', post_slug=post_slug)

@app.route('/success')
def success():
    return render_template('successMessage.html')

@app.route('/under_construction')
def under_construction():
    return render_template('undercons.html')

@app.route('/contributors')
def contributors():
    contributors_info = [
        {'name': 'Abhinav Kumar', 'email': 'abhinavkumar3375@gmail.com', 'description': 'Passionate coder.'},
        {'name': 'Hardik', 'email': 'HARDIK4376@gmail.com', 'description': 'Loves problem-solving.'},
        {'name': 'Muskan Sharma', 'email': 'muskanSharma5547@gmail.com', 'description': 'Creative developer.'},
        {'name': 'Muskan', 'email': 'muskan5547@gmail.com', 'description': 'Creative developer.'},
    ]
    return render_template('a.html', contributors=contributors_info)



@app.route('/chatbot_response', methods=['POST'])
def chatbot_response():
    try:
        user_message = request.json.get('message', '')
        if not user_message.strip():
            return jsonify({"response": "Please enter a message so I can assist you."})

        user_message_clean = user_message.strip().lower()

        from_districts = routes_df['From_District'].str.lower().str.strip().unique()
        to_districts = routes_df['To_District'].str.lower().str.strip().unique()
        all_districts = set(from_districts).union(set(to_districts))

        keywords_station_info = ['station', 'location', 'amenities', 'facilities', 'timings', 'where is', 'details']
        keywords_schedule = ['schedule', 'next bus', 'timing', 'bus time']

        # Check for station info queries first
        if any(k in user_message_clean for k in keywords_station_info):
            for idx, row in stations_df.iterrows():
                if row['Station'].lower() in user_message_clean or row['District'].lower() in user_message_clean:
                    response_text = (f"📍 Station: {row['Station']} ({row['District']})\n"
                                     f"Amenities: {row['Amenities']}\n"
                                     f"Location: https://maps.google.com/?q={row['Latitude']},{row['Longitude']}\n"
                                     f"More info: {row['Info_Link']}")
                    break
            else:
                response_text = "Sorry, I couldn't find information about that station. Please try with the exact station or district name."

            return jsonify({"response": response_text})

        # Extract districts mentioned
        mentioned = [d for d in all_districts if d in user_message_clean]

        if len(mentioned) < 2:
            if any(greet in user_message_clean for greet in ['hi', 'hello', 'hey']):
                response_text = ("Hi! I can help you find Himachal bus routes between districts. "
                                 "Try something like 'Route from Shimla to Mandi'.")
            else:
                response_text = ("Please mention two Himachal districts in your message like "
                                 "'Route from Shimla to Mandi' to get bus route information.")
            return jsonify({"response": response_text})

        from_district = mentioned[0]
        to_district = mentioned[1]

        # Find routes
        direct_route = routes_df[
            (routes_df['From_District'].str.lower().str.strip() == from_district) &
            (routes_df['To_District'].str.lower().str.strip() == to_district)
        ]

        reverse_route = routes_df[
            (routes_df['From_District'].str.lower().str.strip() == to_district) &
            (routes_df['To_District'].str.lower().str.strip() == from_district)
        ]

        def format_route(row, direction="forward"):
            stops = [s.strip() for s in row['Stops'].split(',')]
            if direction == "reverse":
                stops = list(reversed(stops))
            stops_str = " → ".join(stops)
            return (f"🚌 Route from {row['From_District']} to {row['To_District']}:\n"
                    f"Stops: {stops_str}\n"
                    f"Booking Link: {row['Booking_Link']}\n")

        response_text = ""

        if not direct_route.empty:
            for _, row in direct_route.iterrows():
                response_text += format_route(row, "forward") + "\n"
        elif not reverse_route.empty:
            for _, row in reverse_route.iterrows():
                response_text += format_route(row, "reverse") + "\n"
        else:
            response_text = f"Sorry, no direct route found between {from_district.title()} and {to_district.title()}."

        # Add live schedule info if requested
        if any(k in user_message_clean for k in keywords_schedule):
            live_schedule = get_live_bus_schedule(from_district, to_district)
            response_text += "\n\n🕒 Live Schedule:\n" + live_schedule

        # Log chat
        mongo.db.chatlogs.insert_one({
            'user': session.get('user', 'anonymous'),
            'message': user_message,
            'response': response_text,
            'timestamp': datetime.utcnow()
        })

        return jsonify({"response": response_text})

    except Exception as e:
        print("Error in chatbot_response:", e)
        fallback_reply = "Sorry, something went wrong. Please try again."
        try:
            mongo.db.chatlogs.insert_one({
                'user': session.get('user', 'anonymous'),
                'message': request.json.get('message', 'unknown'),
                'response': fallback_reply,
                'timestamp': datetime.utcnow()
            })
        except Exception as log_err:
            print("Mongo logging error:", log_err)
        return jsonify({"response": fallback_reply})

# --- Route to Submit Feedback using MongoDB ---
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        message = request.form.get('message')
        user = session.get('user', 'anonymous')
        
        mongo.db.feedbacks.insert_one({
            'user': user,
            'message': message,
            'timestamp': datetime.utcnow()
        })
        flash("Feedback submitted successfully!", "success")
        return redirect(url_for('home'))

# --- Optional: Route to View Feedbacks for All Users ---
@app.route('/view_feedbacks')
def view_feedbacks():
    feedbacks = list(mongo.db.feedbacks.find().sort('timestamp', -1))
    return render_template('feedbacks.html', feedbacks=feedbacks)

# --- Admin Feedback Dashboard ---
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user' not in session or session['user'] != 'admin':  # Check admin login
        flash("You must be an admin to view this page.", "danger")
        return redirect(url_for('login'))
    
    feedbacks = list(mongo.db.feedbacks.find().sort('timestamp', -1))
    return render_template('admin_dashboard.html', feedbacks=feedbacks)


# Example Flask route (simplified)


# Example station list — replace with your full dataset
all_stations = [
    "Shimla", "Mandi", "Bilaspur", "Sundernagar", "Kangra", "Palampur",
    "Baijnath", "Kullu", "Solan", "Hamirpur", "Nurpur", "Chamba"
]

@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('query', '').strip().lower()
    suggestions = []

    if query:
        suggestions = [
            station for station in all_stations
            if query in station.lower()
        ]
    # Limit suggestions to max 20 items
    suggestions = suggestions[:20]

    return jsonify({"suggestions": suggestions})



# --- Main Entry ---
if __name__ == '__main__':
    app.run(debug=True)
