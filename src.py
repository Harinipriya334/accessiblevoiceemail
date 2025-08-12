import speech_recognition as sr
import smtplib
import email
import imaplib
import pyglet
from gtts import gTTS
import pyttsx3
import os
import time
from email.message import EmailMessage

# Initialize recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Define a function to speak text
def talk(text):
    engine.say(text)
    engine.runAndWait()

# Play audio notifications
def play_audio(text, filename="audio.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    sound = pyglet.media.load(filename, streaming=False)
    sound.play()
    time.sleep(sound.duration)
    os.remove(filename)

# Logout email function
def logout_email():
    talk("Logging out of your email account.")
    print("Successfully logged out.")
    exit()

# Function to send an email
def send_mail(receiver, subject, message):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("harinipriya169@gmail.com", "uezy iwen sskd pkvr")  # Replace with your email and app password
        email_msg = EmailMessage()
        email_msg['From'] = "harinipriya169@gmail.com"
        email_msg['To'] = receiver
        email_msg['Subject'] = subject
        email_msg.set_content(message)
        server.send_message(email_msg)
        server.quit()
        talk("Your email has been sent successfully.")
    except Exception as e:
        talk("Sorry, I couldn't send the email.")
        print(f"Error: {e}")

def get_email_info():
    """Get email information and send an email."""
    contacts = {
        'nivi': 'srnive2004@gmail.com',
        'sabari': 'sabareas18@gmail.com',
        'customer': 'akalyaselvaraj14@gmail.com'
    }

# Function to get user input via voice
def get_info(prompt):
    talk(prompt)
    with sr.Microphone() as source:
        print(prompt)
        try:
            voice = listener.listen(source)
            info = listener.recognize_google(voice)
            print(f"You said: {info}")
            return info.lower()
        except sr.UnknownValueError:
            talk("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError as e:
            talk("Request error. Please check your internet connection.")
            print(f"Error: {e}")
            return ""

# Read emails function
def read_email():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login("harinipriya169@gmail.com", "uezy iwen sskd pkvr")  # Replace with your email and app password
        mail.select("inbox")
        status, messages = mail.search(None, 'UNSEEN')
        if status == "OK" and messages[0]:
            for num in messages[0].split():
                status, msg_data = mail.fetch(num, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        sender = email.utils.parseaddr(msg['From'])[1]
                        subject = msg['Subject']
                        talk(f"Unread email from {sender} with the subject {subject}")
                        print(f"Unread email from: {sender}\nSubject: {subject}")
            mail.logout()
        else:
            talk("You have no unread emails.")
    except Exception as e:
        talk("Sorry, I couldn't fetch your emails.")
        print(f"Error: {e}")

# Main menu
def main():
    while True:
        talk("Please select an option. Option 1: Send an email. Option 2: Check your inbox. Option 3: Read unread emails.")
        choice = get_info("What is your choice?")
        
        if "1" in choice or "send" in choice:
            try:
                receiver = get_info("Who do you want to send the email to?")
                subject = get_info("What is the subject?")
                message = get_info("What is the message?")
                send_mail(receiver, subject, message)
            except KeyError:
                talk("I couldn't find that contact. Please try again.")
        
        elif "2" in choice or "check" in choice:
            talk("Fetching the number of emails in your inbox.")
            read_email()

        elif "3" in choice or "read" in choice:
            read_email()

        else:
            talk("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
