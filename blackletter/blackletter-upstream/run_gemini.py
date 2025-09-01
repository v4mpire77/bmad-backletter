
import os
from dotenv import load_dotenv
import google.generativeai as genai

def main():
	# Load environment variables from .env file
	load_dotenv()
	api_key = os.getenv("GEMINI_API_KEY")
	if not api_key:
		raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")

	try:
		genai.configure(api_key=api_key)
		model = genai.GenerativeModel('gemini-1.5-flash')
		response = model.generate_content("Tell me a fun fact about the Python programming language.")
		print(response.text)
	except Exception as e:
		print(f"An error occurred: {e}")

if __name__ == "__main__":
	main()
