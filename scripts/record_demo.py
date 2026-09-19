#!/usr/bin/env python3
"""
scripts/record_demo.py
A simple script to record a 3-minute video of the screen for the Devpost submission.
Uses mss for screen capture and cv2 for video encoding.
"""

import time
import cv2
import mss
import numpy as np

def record_screen(duration_seconds=180, output_file="devpost_demo.mp4", fps=20):
    print(f"Starting Devpost demo recording for {duration_seconds} seconds...")
    print(f"Output will be saved to: {output_file}")
    
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        width = monitor["width"]
        height = monitor["height"]
        
        # Use mp4v codec for cross-platform compatibility
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
        
        start_time = time.time()
        frames_recorded = 0
        
        try:
            while time.time() - start_time < duration_seconds:
                # Capture frame
                img = np.array(sct.grab(monitor))
                # Convert BGRA to BGR for OpenCV
                frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                out.write(frame)
                frames_recorded += 1
                
                # Sleep to maintain approximate FPS
                elapsed = time.time() - start_time
                expected_time = frames_recorded / fps
                sleep_time = expected_time - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
                if frames_recorded % (fps * 10) == 0:
                    remaining = int(duration_seconds - (time.time() - start_time))
                    print(f"Recording... {remaining} seconds remaining.")
                    
        except KeyboardInterrupt:
            print("\nRecording stopped manually.")
            
        finally:
            out.release()
            print(f"Recording complete! Saved to {output_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Record a demo video of the screen.")
    parser.add_argument("--duration", type=int, default=180, help="Duration in seconds")
    parser.add_argument("--out", type=str, default="devpost_demo.mp4", help="Output filename")
    parser.add_argument("--fps", type=int, default=20, help="Frames per second")
    args = parser.parse_args()
    
    record_screen(duration_seconds=args.duration, output_file=args.out, fps=args.fps)
