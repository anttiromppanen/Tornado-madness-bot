import os
import time
import threading
import pyautogui
import keyboard
import random

# Function to take screenshots
def take_screenshot(interval, stop_event):
    # Create a directory for screenshots if it doesn't exist
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    while not stop_event.is_set():
        # Take screenshot
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        screenshot = pyautogui.screenshot()

        # Random num for file name
        file_text = "random"
        rand_num = random.randint(1, 1000000)

        screenshot.save(f"screenshots/screenshot_{file_text}_{rand_num}_{timestamp}.png")

        # Wait for the specified interval
        stop_event.wait(interval)

# Main function
def main():
    # Ask for the interval between screenshots
    interval = float(input("Enter the interval between screenshots (in seconds): "))
    
    # Create a stop event for the screenshot thread
    stop_event = threading.Event()
    
    # Sleep for 3 seconds
    # Loop for 3 seconds
    time.sleep(3)

    for i in range(3, 0, -1):
        print(f"Starting in {i} seconds...")
        time.sleep(1)

    # Create and start the screenshot thread
    screenshot_thread = threading.Thread(target=take_screenshot, args=(interval, stop_event))
    screenshot_thread.start()

    print("Screenshot program started. Press 'q' to quit.")

    # Listen for keyboard input to quit the program
    keyboard.wait("q")

    # Set the stop event to end the screenshot thread
    stop_event.set()

    # Wait for the screenshot thread to finish
    screenshot_thread.join()

    print("Program ended.")

if __name__ == "__main__":
    main()