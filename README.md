# LinkedIn Viralizer App

A full-stack web application that transforms user ideas into viral-optimized LinkedIn posts using Python Flask and the Gemini API.

## Features

- **AI-Powered Content Generation**: Uses Gemini 1.5 Flash API to create engaging LinkedIn posts
- **Few-Shot Learning**: Dynamically loads examples from `viral_linkedin_posts.json` to enhance generation quality
- **Simple Web Interface**: Clean, responsive UI built with Bootstrap
- **Easy Enhancement**: Add new viral post examples to the JSON file to improve the model

## Project Structure

```
linkedinGroupContentGenerator/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env                       # Environment variables (create this)
├── viral_linkedin_posts.json  # Few-shot learning examples
├── templates/
│   └── index.html             # Web interface
└── README.md                  # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY="your_actual_api_key_here"
   ```

### 3. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Open your browser and navigate to `http://localhost:5000`
2. Enter your content idea or rough draft in the text area
3. Click "Generate Viral Post"
4. Copy the generated LinkedIn post and use it on your profile

## Enhancing the Model

To improve the quality of generated posts, add new examples to `viral_linkedin_posts.json`:

```json
{
    "posts": [
        {
            "input": "Your input prompt here",
            "output": "The corresponding viral LinkedIn post here"
        }
    ]
}
```

The application automatically loads these examples and uses them for few-shot learning with the Gemini API.

## API Endpoints

- `GET /` - Serves the main web interface
- `POST /generate` - Generates LinkedIn content from user input
  - Request body: `{"prompt": "user input text"}`
  - Response: `{"generated_post": "generated content"}`

## Technical Details

- **Backend**: Flask (Python)
- **AI Model**: Gemini 1.5 Flash
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Few-Shot Learning**: Dynamic loading from JSON file
- **Error Handling**: Comprehensive error handling for API failures

## Troubleshooting

- **API Key Error**: Ensure your `.env` file contains the correct Gemini API key
- **Module Not Found**: Run `pip install -r requirements.txt` to install dependencies
- **Port Already in Use**: Change the port in `app.py` or kill the existing process

## License

This project is open source and available under the MIT License.
