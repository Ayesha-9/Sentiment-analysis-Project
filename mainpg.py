import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import nltk
import re
import string
import sys
from tkinter import Text

# Custom Text widget to redirect stdout
class OutputText(Text):
    def write(self, txt):
        self.insert(tk.END, txt)
        self.see(tk.END)  # Auto-scroll to the end

# Function to display file content in the text widget
def display_file_content(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    text_widget.delete(1.0, END)  # Clear previous content
    text_widget.insert(1.0, content)

# Function to handle file selection
def select_file():
    filetypes = (
        ('CSV files', '*.csv'),
        ('All files', '*.*')
    )
    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes
    )
    if filename:
        display_file_content(filename)
        global selected_filename
        selected_filename = filename

# Function to plot total users by year
def total_user():
    global selected_filename
    if selected_filename:
        df = pd.read_csv(selected_filename)
        if 'tweet_created' in df.columns:
            df['tweet_created'] = pd.to_datetime(df['tweet_created'], format="%m/%d/%Y %H:%M", errors='coerce')
            df['Year'] = df['tweet_created'].dt.year
            year_counts = df['Year'].value_counts().sort_index()
            
            plt.figure(figsize=(10, 6))
            year_counts.plot(kind='bar', color='skyblue')
            plt.title('Number of Users by Year')
            plt.xlabel('Year')
            plt.ylabel('Number of Users')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showwarning('Warning', "No 'tweet_created' column found.")
    else:
        messagebox.showwarning('Warning', "No file selected.")

def analyse():
    # Redirect stdout to text_widget
    sys.stdout = text_widget

    global selected_filename
    if selected_filename:
        data = pd.read_csv(selected_filename)
        # Rename the text column to 'tweet' if it exists
        if 'text' in data.columns:
            data.rename(columns={'text': 'tweet'}, inplace=True)
        else:
            print("No 'text' column found.")
            return
        
        text_widget.delete(1.0, END)  # Clear previous content

        nltk.download('stopwords')
        nltk.download('vader_lexicon')
        stemmer = nltk.SnowballStemmer("english")
        from nltk.corpus import stopwords
        stopword = set(stopwords.words('english'))

        def clean(text):
            text = str(text).lower()
            text = re.sub(r'\[.*?\]', '', text)
            text = re.sub(r'https?://\S+|www\.\S+', '', text)
            text = re.sub(r'<.*?>+', '', text)
            text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
            text = re.sub(r'\n', '', text)
            text = re.sub(r'\w*\d\w*', '', text)
            text = [word for word in text.split(' ') if word not in stopword]
            text = " ".join(text)
            text = [stemmer.stem(word) for word in text.split(' ')]
            text = " ".join(text)
            return text

        data['cleaned_tweet'] = data['tweet'].apply(clean)

        text_widget.insert(END, "First five rows of the Original dataset:\n")
        text_widget.insert(END, data[['tweet', 'cleaned_tweet']].head().to_string() + "\n\n")

        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        sentiments = SentimentIntensityAnalyzer()
        data["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in data["cleaned_tweet"]]
        data["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in data["cleaned_tweet"]]
        data["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data["cleaned_tweet"]]

        text_widget.insert(END, "First five rows of cleaned dataset with sentiment scores:\n")
        text_widget.insert(END, data[['cleaned_tweet']].head().to_string() + "\n\n")
        text_widget.insert(END, data[['Positive', 'Negative', 'Neutral']].head().to_string() + "\n\n")

        x = sum(data["Positive"])
        y = sum(data["Negative"])
        z = sum(data["Neutral"])

        def sentiment_score(a, b, c):
            if (a > b) and (a > c):
                return "Positive 😊"
            elif (b > a) and (b > c):
                return "Negative 😠"
            else:
                return "Neutral 🙂"

        result = sentiment_score(x, y, z)
        text_widget.insert(END, f"Sentiment Analysis Result:\n{result}\n\n")
        text_widget.insert(END, f"Positive: {x:.3f}\nNegative: {y:.3f}\nNeutral: {z:.3f}\n")

        pos.set(f"{x:.3f} 😊")
        neg.set(f"{y:.3f} 😠")
        neu.set(f"{z:.3f} 🙂")

    else:
        print("No file selected.")



# Function to handle quitting the application
def qit():
    res = messagebox.askquestion('Quit', 'Are you sure you want to quit?')
    if res == 'yes':
        root.destroy()

# Create the root window
root = tk.Tk()
root.title('Sentiment Analysis Tool')
root.configure(bg='sky blue')

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size and position to full screen
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Create a heading for the application
heading_label = tk.Label(root, text="Sentiment Analysis", font=("Times new roman", 24, "bold"), bg='sky blue', fg='white')
heading_label.place(x=78, y=10)

# Create a container frame for left-side boxes and image
left_frame = tk.Frame(root, bg='sky blue')
left_frame.place(x=10, y=60, width=440, height=screen_height-70)  # Adjust height as needed

# Define variables for sentiment scores
pos = StringVar()
neg = StringVar()
neu = StringVar()

# Creating a photoimage object to use image
photo = PhotoImage(file=r"E:\NFUL- Project SA-ml\t.png")

# Resize the image to fit the window size
resized_photo = photo.subsample(2, 2)

# Image label on the left side
image_label = Label(left_frame, image=resized_photo, bg='sky blue')
image_label.pack(pady=20)

# Create a frame for sentiment scores on the left side
scores_frame = tk.Frame(left_frame, bg='sky blue', padx=10, pady=10)
scores_frame.pack(pady=20)

# Sentiment score frames and labels
frame_config = {'bd': 2, 'relief': "solid", 'padx': 10, 'pady': 10}
label_config = {'font': ("Arial", 12, "bold")}

positive_frame = tk.Frame(scores_frame, bg="#D4EDDA", **frame_config)
positive_frame.grid(row=0, column=0, padx=5, pady=5, sticky='w')
positive_label = tk.Label(positive_frame, text="POSITIVE: 😊", bg="#D4EDDA", **label_config)
positive_label.pack()
positive_score_label = tk.Label(positive_frame, textvariable=pos, font=("Arial", 14), bg="#D4EDDA")
positive_score_label.pack()

negative_frame = tk.Frame(scores_frame, bg="#F8D7DA", **frame_config)
negative_frame.grid(row=0, column=1, padx=5, pady=5, sticky='w')
negative_label = tk.Label(negative_frame, text="NEGATIVE: 🙁", bg="#F8D7DA", **label_config)
negative_label.pack()
negative_score_label = tk.Label(negative_frame, textvariable=neg, font=("Arial", 14), bg="#F8D7DA")
negative_score_label.pack()

neutral_frame = tk.Frame(scores_frame, bg="#FFD700", **frame_config)
neutral_frame.grid(row=0, column=2, padx=5, pady=5, sticky='w')
neutral_label = tk.Label(neutral_frame, text="NEUTRAL: 😐", bg="#FFD700", **label_config)
neutral_label.pack()
neutral_score_label = tk.Label(neutral_frame, textvariable=neu, font=("Arial", 14), bg="#FFD700")
neutral_score_label.pack()

# Create the text widget to display file content and analysis results
text_widget = OutputText(root, wrap="none", bg='white', font=("Arial", 12))
text_widget.place(x=470, y=3, relwidth=0.68, relheight=0.8)

# Buttons Frame
buttons_frame = tk.Frame(root, bg='sky blue')
buttons_frame.place(x=650, rely=0.85, width=screen_width-330, height=0.1*screen_height)

# Open File Button
open_button = tk.Button(buttons_frame, text='Select a File', command=select_file, bg='#d81159', fg='white', font=("Arial", 12))
open_button.grid(row=0, column=0, padx=10, pady=10)

# Analyse Button
analyse_button = tk.Button(buttons_frame, text='Analyse', command=analyse, bg='#218380', fg='white', font=("Arial", 12))
analyse_button.grid(row=0, column=1, padx=10, pady=10)

# Total Users Button
total_users_button = tk.Button(buttons_frame, text='Total Users', command=total_user, bg='#d81159', fg='white', font=("Arial", 12))
total_users_button.grid(row=0, column=2, padx=10, pady=10)

# Quit Button
quit_button = tk.Button(buttons_frame, text='Quit', command=qit, bg='red', fg='white', font=("Arial", 12))
quit_button.grid(row=0, column=3, padx=10, pady=10)

# Set initial sentiment scores
pos.set("0.0 😊")
neg.set("0.0 🙁")
neu.set("0.0 😐")

# Run the application
root.mainloop()
