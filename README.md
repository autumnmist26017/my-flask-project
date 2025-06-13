# Audio Transcription & Sentiment Analysis Web App

A web application that transcribes audio files, performs speaker diarization, and analyzes sentiment for each speaker.

## Features

- Upload .wav audio files (up to 16MB)
- Specify the number of speakers (1-5)
- View transcription with speaker segmentation
- Sentiment analysis for each speaker's dialogue
- Download results as CSV
- Responsive design that works on desktop and mobile

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd audio_transcriber
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Use the interface to:
   - Upload a .wav file
   - Select the number of speakers
   - Click "Process Audio"
   - View the transcription and sentiment analysis
   - Download the results as CSV

## Deployment

### Local Deployment
For local use, simply run the application as described above.

### Cloud Deployment
To deploy this application to a cloud service like Heroku or PythonAnywhere:

1. Create a new app on your chosen platform
2. Add a `requirements.txt` file with all dependencies
3. Configure the platform to use `app.py` as the entry point
4. Deploy your code

## File Structure

```
audio_transcriber/
├── app.py                # Main application file
├── requirements.txt      # Python dependencies
├── static/              # Static files (CSS, JS, images)
│   ├── css/
│   └── js/
├── templates/           # HTML templates
│   └── index.html
└── uploads/             # Temporary file storage
```

## Dependencies

- Flask - Web framework
- Scraibe - Audio transcription
- pandas - Data manipulation
- vaderSentiment - Sentiment analysis
- matplotlib - Data visualization
- gunicorn - WSGI HTTP Server (for production)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Flask and Bootstrap 5
- Uses Scraibe for audio transcription
- VADER Sentiment Analysis for sentiment scoring
