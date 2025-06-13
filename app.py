import os
from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import tempfile
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import re
from scraibe import Scraibe

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = os.urandom(24)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def transcribe_audio(file_path, language="english", num_speakers=1):
    """Transcribe audio file using Scraibe."""
    model = Scraibe()
    transcription = model.autotranscribe(file_path, language=language, num_speakers=num_speakers)
    return transcription

def parse_transcription_to_df(transcription_string):
    """Parse transcription string to DataFrame."""
    pattern = re.compile(r"^(SPEAKER_\d+)\s+\((\d{2}:\d{2}:\d{2})\s+;\s+(\d{2}:\d{2}:\d{2})\):\s*(.*)$")
    lines = transcription_string.strip().split('\n')
    data_rows = []

    for line in lines:
        match = pattern.match(line)
        if match:
            speaker, start_time, end_time, text = match.groups()
            data_rows.append({
                'speaker': speaker,
                'start_time': start_time,
                'end_time': end_time,
                'text': text.strip()
            })

    return pd.DataFrame(data_rows)

def analyze_sentiment(df):
    """Perform sentiment analysis on the transcription."""
    analyzer = SentimentIntensityAnalyzer()
    df['sentiment_score'] = df['text'].apply(
        lambda text: analyzer.polarity_scores(text)['compound']
    )
    return df

def generate_plot(df):
    """Generate sentiment analysis plot."""
    speaker_sentiment = df.groupby('speaker')['sentiment_score'].mean().sort_values()
    
    plt.figure(figsize=(10, 6))
    colors = ['g' if x > 0 else 'r' for x in speaker_sentiment.values]
    speaker_sentiment.plot(kind='barh', color=colors)
    
    plt.title('Overall Sentiment by Speaker')
    plt.xlabel('Average Sentiment Score (Compound)')
    plt.ylabel('Speaker')
    plt.axvline(x=0, color='k', linestyle='--')
    plt.tight_layout()
    
    # Save plot to a bytes buffer
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    
    return base64.b64encode(img.getvalue()).decode('utf-8')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and file.filename.endswith('.wav'):
        try:
            num_speakers = int(request.form.get('num_speakers', 1))
            
            # Save the file temporarily
            filename = secure_filename(file.filename)
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(temp_path)
            
            # Process the file
            transcription = transcribe_audio(temp_path, num_speakers=num_speakers)
            df = parse_transcription_to_df(str(transcription))
            df = analyze_sentiment(df)
            
            # Generate plot
            plot_data = generate_plot(df)
            
            # Save results to session
            results = {
                'transcription': df.to_dict(orient='records'),
                'speaker_sentiment': df.groupby('speaker')['sentiment_score'].mean().to_dict(),
                'plot_data': plot_data
            }
            
            # Clean up
            os.remove(temp_path)
            
            return jsonify(results)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file format. Please upload a .wav file'}), 400

@app.route('/download', methods=['POST'])
def download_csv():
    data = request.get_json()
    if not data or 'transcription' not in data:
        return jsonify({'error': 'No data to download'}), 400
        
    df = pd.DataFrame(data['transcription'])
    
    # Create CSV in memory
    csv_data = BytesIO()
    df.to_csv(csv_data, index=False)
    csv_data.seek(0)
    
    return send_file(
        csv_data,
        mimetype='text/csv',
        as_attachment=True,
        download_name='transcription_results.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)
