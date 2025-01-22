import cv2
from deepface import DeepFace
import time
from module.utils import my_function

def detect_emotions_from_video(
    video_source=0,
    process_every_nth_frame=3,
    max_resolution=(320, 240),
    duration_threshold=1,
    min_display_time=0.01
):
    #video capture
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print("Error: Unable to open video source.")
        return
    #frame dimensions for efficient processing
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, max_resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, max_resolution[1])
    frame_count = 0
    processed_frames = 0
    start_time = time.time()
    #dictionary
    emotion_count = {
        "happy": 0,
        "sad": 0,
        "angry": 0,
        "surprise": 0,
        "fear": 0,
        "disgust": 0,
        "neutral": 0
    }
    current_emotion = None
    emotion_start_time = None
    last_displayed_emotion = None
    last_display_time = None
    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video or unable to capture frame.")
            break
        frame_count += 1
        # Skip frames to reduce processing load
        if frame_count % process_every_nth_frame != 0:
            continue
        resized_frame = cv2.resize(frame, (max_resolution[0], max_resolution[1]))
        # Analyze emotions
        try:
            analysis = DeepFace.analyze(resized_frame, actions=['emotion'], enforce_detection=False)
            dominant_emotion = analysis[0]['dominant_emotion']

            if current_emotion == dominant_emotion:
                if emotion_start_time is None:
                    emotion_start_time = time.time()
                elapsed_time = time.time() - emotion_start_time
                # Increment the count if the emotion persists for the threshold duration
                if elapsed_time >= duration_threshold:
                    emotion_count[dominant_emotion] += 1
                    emotion_start_time = time.time()  # Reset timer
                    print(f"Emotion '{dominant_emotion}' persisted for {elapsed_time:.2f} seconds. Incremented count.")
            else:
                current_emotion = dominant_emotion
                emotion_start_time = time.time()
                elapsed_time = 0 
            elapsed_display_time = time.time() - (last_display_time if last_display_time else 0)
            if elapsed_display_time >= min_display_time:
                # Update displayed emotion if it's more than the 10 ms
                last_displayed_emotion = dominant_emotion
                last_display_time = time.time()
            cv2.putText(
                resized_frame,
                f"Emotion: {last_displayed_emotion}",(10, 30),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2,cv2.LINE_AA)
            print("\nEmotion Counts:")
            for emotion, count in emotion_count.items():
                print(f"{emotion.capitalize()}: {count}", end=' | ')
            print("\n")
        except Exception as e:
            print(f"Error analyzing frame: {e}")
        processed_frames += 1
        # Display emotion detection on screen
        cv2.imshow("Emotion Detection - Webcam", resized_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    # Processing status
    total_elapsed_time = time.time() - start_time
    print(f"Total frames captured: {frame_count}")
    print(f"Total frames processed: {processed_frames}")
    print(f"Processing time: {total_elapsed_time:.2f} seconds")
    # Final emotion counts
      # Final emotion counts
    print("\nFinal Emotion Counts (incremented if emotion persists for more than 1 second):")
    for emotion, count in emotion_count.items():
        print(f"{emotion}: {count}")
    # Find the most frequent emotion
    most_common_emotion = max(emotion_count, key=emotion_count.get)
    most_common_count = emotion_count[most_common_emotion]
    # Print the most common emotion
    print(f"\nThe emotion that occurred the most is '{most_common_emotion}' with a count of {most_common_count}.")


# Video input 
detect_emotions_from_video(f"{my_function()}")


