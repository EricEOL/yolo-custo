from flask import Flask, request, jsonify
import os
from evidences_processor import process_video

app = Flask(__name__)

# Define the directory to save uploaded files
UPLOAD_FOLDER = 'uploaded_videos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/video_evidence_processor', methods=['POST'])
def video_evidence_processor():
    # Get the uploaded file
    file = request.files['video_evidence']
    
    # Define the path to save the file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    # Save the file to the specified path
    file.save(file_path)
    
    output_file_path = os.path.join(UPLOAD_FOLDER, 'processed_' + file.filename)

    process_video(file_path)
    
    # Respond with a JSON message
    return jsonify({"message": "Received!", "data": file.filename}), 200

if __name__ == '__main__':
    app.run(debug=True)