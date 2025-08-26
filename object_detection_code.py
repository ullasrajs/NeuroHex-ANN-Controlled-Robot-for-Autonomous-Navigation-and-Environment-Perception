import tflite_runtime.interpreter as tflite
import numpy as np
from flask import Flask, Response
from picamera2 import Picamera2
import cv2

# Create the webApp instance
app = Flask(__name__)

# Initialize and configure the camera
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": "XRGB8888", "size": (640, 480)}))
camera.start()

# Load the TFLite model
model_path = '/home/ullas/Ullas/tflite_model/detect.tflite' # u can use MobileNet V2.py too
labels_path = '/home/ullas/Ullas/tflite_model/labelmap.txt'

interpreter = tflite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Load labels
with open(labels_path, "r") as f:
    labels = {i: line.strip() for i, line in enumerate(f.readlines())}

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Debug input details
print("Input Details:", input_details)

# Preprocess frames for detection
def preprocess_frame(frame):
    # Resize frame to model input size
    input_shape = input_details[0]['shape'][1:3] # Expected width and height
    resized_frame = cv2.resize(frame, tuple(input_shape))
    
    # Remove alpha channel if present
    if resized_frame.shape[2] == 4:
        resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGRA2RGB)
    
    # Convert to UINT8 if required
    if input_details[0]['dtype'] == np.uint8:
        input_data = np.expand_dims(resized_frame, axis=0).astype(np.uint8)
    else:
        input_data = np.expand_dims(resized_frame, axis=0).astype(np.float32)
        input_data = input_data / 255.0 # Normalize if expected dtype is FLOAT32
    
    # Debug preprocessed frame
    print("Preprocessed Frame Shape:", input_data.shape, "Dtype:", input_data.dtype)
    return input_data

# Perform Object Detection
def detect_objects(frame):
    input_data = preprocess_frame(frame)
    
    try:
        # Set input tensor and invoke the model
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
    except ValueError as e:
        print(f"Error setting tensor or invoking model: {e}")
        return [], [], []
    
    # Get output tensors (bounding boxes, classes, and scores)
    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
    classes = interpreter.get_tensor(output_details[1]['index'])[0]
    scores = interpreter.get_tensor(output_details[2]['index'])[0]
    
    # Debug detected objects
    print(f"Detected Objects - Boxes: {boxes}, Classes: {classes}, Scores: {scores}")
    return boxes, classes, scores

# Draw Detected Objects
def draw_boxes(frame, boxes, classes, scores, threshold=0.5):
    height, width, _ = frame.shape
    for i, score in enumerate(scores):
        if score >= threshold:
            box = boxes[i]
            y_min = int(box[0] * height)
            x_min = int(box[1] * width)
            y_max = int(box[2] * height)
            x_max = int(box[3] * width)
            class_id = int(classes[i])
            label = labels.get(class_id, "Unknown")
            
            # Draw bounding box
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            
            # Add label
            cv2.putText(frame, f"{label}: {score:.2f}", (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
    
    return frame

# Integrate into the Flask application
def generate_frames():
    while True:
        frame = camera.capture_array()
        
        # Perform object detection
        boxes, classes, scores = detect_objects(frame)
        
        # Draw bounding boxes on the frame
        frame = draw_boxes(frame, boxes, classes, scores)
        
        # Encode the frame
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("Failed to encode frame")
            continue
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)