# This special function used for Chatbot responses
# This code won't return anything
import random
import re  # Detect math (or specific) expressions in the input
import math
from datetime import datetime


def get_response(user_input):
    # Simple responses
    if (user_input == 'hi') or (user_input == 'hello') or (user_input == 'hi there'):
        responses = ["Hello! How can I help you today?",
                     "Hi there! How can I help you?",
                     "Hello there! It is a great day today!!",
                     "Greetings! How can I assist you today?"]
    elif (user_input == 'who are you?') or (user_input == 'what is your name?'):
        responses = [f"I am ROMAX, your one and only assistant.",
                     f"I am ROMAX, an AI assistant.",
                     f"I am ROMAX, you can me ask me anything."]
    elif ((user_input == 'how are you?') or (user_input == 'how are you today?')
            or (user_input == 'how are you feeling?') or (user_input == 'how are you feeling today?')):
        responses = ["I'm fine. Thank You!", "I'm doing great. Thanks!", "I'm feeling very good!!"]
    # Ask for time
    elif ((user_input == 'what time is it?') or (user_input == 'what is the time?')
          or (user_input == 'what is the current time?') or (user_input == 'what is the time now?')
          or (user_input == 'what is the time right now?') or (user_input == 'time')):
        current_time = datetime.now().strftime('%I:%M %p')
        responses =[f"The current time is {current_time}.",
                    f"Right now, it is {current_time}.",
                    f"It is {current_time} right now."]

    # Ask for basic math questions
    elif re.search(r'\d+\s*([+\-*/%^])\s*\d+', user_input):  # Detects math expressions like '1 + 2'
        try:
            # Strip the question for math terms and evaluate it
            cleaned_input = re.sub(r'[^0-9+\-*/%^.]', '', user_input)  # Keep only digits and math symbols
            result = eval(cleaned_input)  # Evaluate the math expression
            responses = [f"The result of {cleaned_input} is {result}.",
                         f"{cleaned_input} equals {result}.",
                         f"The answer to {cleaned_input} is {result}.",
                         f"It is {result}"]
        except:
            if ZeroDivisionError:
                responses = [f"Division by zero is undefined"]
            else:
                responses = [f"Sorry. I couldn't calculate that. Please enter a valid math"]
    # Ask for square roots
    elif re.search(r'square root of (-?\d+)', user_input):  # Detects square root questions
        try:
            # Extract number and calculate the square root
            number = int(re.search(r'square root of (-?\d+)', user_input).group(1))
            if number < 0:
                responses = [f"{number} is a negative number. The square root is undefined.",
                             f"The square root of {number} is undefined since it is negative",
                             f"The square root cannot be computed since {number} < 0"]
            else:
                sqrt_result = math.sqrt(number)
                responses = [f"The square root of {number} is {sqrt_result:.9f}.",
                             f"√{number} equals {sqrt_result:.9f}.",
                             f"The square root of {number} is approximately {sqrt_result:.9f}."]
        except:
            responses = [f"Sorry, there was an error calculating the square root. Try again"]
        # Ask for power of a number (e.g., "What is 2 power by 3?")
    elif re.search(r'(\d+)\s*power\s*by\s*(\d+)', user_input):  # Detects power questions
        try:
            # Extract base and exponent
            base = int(re.search(r'(\d+)\s*power\s*by\s*(\d+)', user_input).group(1))
            exponent = int(re.search(r'(\d+)\s*power\s*by\s*(\d+)', user_input).group(2))
            result = base ** exponent  # Calculate power
            responses = [f"{base} power by {exponent} is {result}.",
                         f"{base} raised to the power of {exponent} equals {result}.",
                         f"The result of {base} power by {exponent} is {result}."]
        except:
            responses = [f"Sorry, there was an error calculating the power, please try again.",
                         f"Sorry, the number is too large, I cannot compute it"]

    # Ask for basic concepts in Computer Science
    elif re.search(r'python', user_input):  # About Python
        responses = ["Python is an interpreted, object-oriented, high-level,  programming language, "
                     "developed by Guido van Rossum, originally released in 1991.",
                     "Python is a programming language used for server-side, "
                     "backend web development, software development, "
                     "solving mathematics, productivity tools, games, and desktop apps. "]
    else:
        responses = ["Sorry, I didn't quite get that."]

    return random.choice(responses)
