import requests
import time
import json
import argparse
import os

class InstagramScraper:
    def __init__(self, session_id=None):
        self.session = requests.Session()
        self.session_id = session_id
        if session_id:
            self.session.cookies.set('sessionid', session_id)
        self.base_url = "https://www.instagram.com"

    def login(self):
        """Login to Instagram using the provided session ID."""
        url = f"{self.base_url}/accounts/login/ajax/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"{self.base_url}/accounts/login/",
        }

        response = self.session.get(url, headers=headers)
        if response.status_code == 200 and "authenticated" in response.text:
            print("Login successful!")
            return True
        else:
            print("Login failed. Please check your session ID.")
            return False

    def get_followers(self, username, num_users=100):
        """Retrieve followers of the target username."""
        url = f"{self.base_url}/{username}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        }

        response = self.session.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching data for {username}. Status code: {response.status_code}")
            return []

        # Example data structure for followers (you should replace this with real scraping logic)
        user_data = [{"username": f"user{i}", "full_name": f"Full Name {i}", "phone_number": None} for i in range(num_users)]
        return user_data

    def save_user_data(self, user_data, filename):
        """Save scraped user data to a JSON file."""
        with open(filename, 'w') as file:
            json.dump(user_data, file, indent=4)

    def load_user_data(self, filename):
        """Load user data from a JSON file."""
        if not os.path.exists(filename):
            print("File not found.")
            return []
        with open(filename, 'r') as file:
            return json.load(file)
        
    def search_by_phone(self, phone_number, user_data):
        """Search user data for a specific phone number."""
        for user in user_data:
            if user.get('phone_number') == phone_number:
                return user
        return None

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Instagram Scraper - Scrape followers and search by phone number.")
    
    parser.add_argument('--session_id', type=str, required=True, help="Your Instagram session ID.")
    parser.add_argument('--target_username', type=str, required=True, help="Instagram username of the target account to scrape.")
    parser.add_argument('--num_users', type=int, default=100, help="Number of followers to scrape.")
    parser.add_argument('--filename', type=str, default="user_data.json", help="File to save scraped user data.")
    parser.add_argument('--search_phone', type=str, help="Phone number to search for in the scraped data.")
    parser.add_argument('--delay', type=int, default=3, help="Delay between requests in seconds to avoid rate limiting.")
    
    args = parser.parse_args()
    
    # Initialize scraper
    scraper = InstagramScraper(session_id=args.session_id)

    # Attempt login
    if scraper.login():
        print(f"Starting to scrape followers of {args.target_username}...")

        # Scrape the user's followers
        user_data = scraper.get_followers(args.target_username, args.num_users)
        
        if user_data:
            # Save scraped data to a file
            scraper.save_user_data(user_data, args.filename)
            print(f"Scraped {len(user_data)} users. Data saved to {args.filename}.")
            
            # Optionally, search for a phone number
            if args.search_phone:
                print(f"Searching for phone number: {args.search_phone}...")
                result = scraper.search_by_phone(args.search_phone, user_data)
                
                if result:
                    print("User found:")
                    print(json.dumps(result, indent=4))
                else:
                    print("No user found with that phone number.")
        
        else:
            print(f"Failed to scrape any followers for {args.target_username}.")
    
    else:
        print("Login failed. Please verify your session ID.")
    
    print("Done.")

if __name__ == "__main__":
    main()

