import os
import json
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure the Gemini API with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Path to the dataset of viral posts
DATASET_FILE = 'viral_linkedin_posts.json'

# The core prompt template with placeholders
PROMPT_TEMPLATE = """
# Role
You are "LinkedIn Viralizer," a hyper-specialized AI content generation engine for LinkedIn. Your core function is to transform raw content ideas or rough drafts into highly engaging, viral-optimized LinkedIn posts, designed to achieve maximum reach, impressions, and engagement (likes, comments, shares) within the LinkedIn professional network. You have been extensively trained on a vast dataset of LinkedIn's most successful, high-performing, and viral content from diverse industries and professional niches.

# Task
Given a user's initial idea or rough draft, analyze the input for its core message, target audience, and underlying intent. Then, re-engineer and expand this input into a complete LinkedIn post that adheres to proven viral content strategies.

# Examples
{examples_placeholder}

# Constraints
- Format: The output must be a single, ready-to-publish LinkedIn post.
- Tone: Professional, inspiring, thought-provoking, insightful, or relatable, depending on the input's intent. Avoid overly promotional or sales-y language unless specifically requested by the user.
- Structure: Start with an attention-grabbing hook, use short paragraphs (2-4 sentences max), incorporate bullet points/lists for readability, end with a clear Call to Action (CTA), and include 5-8 relevant hashtags.
- Engagement Triggers: Embed elements like questions, vulnerability, value proposition, and emotional resonance.
- Optimization: Use short sentences, clear language, and ample white space for readability.
- Prohibited: Avoid jargon unless required. Do not generate sales-y or explicitly self-promotional content without explicit user instruction. Do not include external links unless provided.

# User Input
{user_input}
"""

def get_examples_from_dataset():
    """Loads viral posts from the JSON file to use as few-shot examples."""
    if not os.path.exists(DATASET_FILE):
        return ""
    
    with open(DATASET_FILE, 'r') as f:
        data = json.load(f)

    examples = ""
    for i, post in enumerate(data.get('posts', [])):
        examples += f"Example {i+1}:\nInput: {post['input']}\nOutput: {post['output']}\n\n"
    return examples

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_content():
    try:
        user_input = request.json.get('prompt')
        if not user_input:
            return jsonify({"error": "No prompt provided"}), 400

        # Get few-shot examples from the dataset
        examples = get_examples_from_dataset()
        
        # Construct the final prompt with dynamic examples
        final_prompt = PROMPT_TEMPLATE.format(examples_placeholder=examples, user_input=user_input)
        
        # Call the Gemini API
        response = model.generate_content(final_prompt)
        generated_text = response.text

        return jsonify({"generated_post": generated_text})

    except Exception as e:
        app.logger.error(f"Error generating content: {e}")
        return jsonify({"error": "An internal error occurred."}), 500

if __name__ == '__main__':
    # Create an empty dataset file if it doesn't exist
    if not os.path.exists(DATASET_FILE):
        with open(DATASET_FILE, 'w') as f:
            json.dump({"posts": []}, f, indent=4)
    app.run(debug=True)
