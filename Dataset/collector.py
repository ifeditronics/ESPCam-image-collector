import cv2
import numpy as np
import requests
import os

# ======================================================
# CONFIGURATION
# ======================================================

ESP32_IP = "192.168.137.153"

PREVIEW_URL = f"http://{ESP32_IP}/preview"
CAPTURE_URL = f"http://{ESP32_IP}/capture"

DATASET = [

    ("recyclable", "Bottle Cap", 25),
    ("recyclable", "Pure Water Nylon", 25),

    ("non_recyclable", "Gala Wrapper", 17),
    ("non_recyclable", "Biscuit Wrapper", 17),
    ("non_recyclable", "Chocolate Wrapper", 16),

]

# ======================================================

ROOT = "dataset"

os.makedirs(ROOT, exist_ok=True)

for c in ["recyclable", "non_recyclable"]:
    os.makedirs(os.path.join(ROOT, c), exist_ok=True)

current = 0

recyclable_count = 0
non_count = 0

print("="*60)
print("SMART BIN DATASET COLLECTOR")
print("="*60)
print("SPACE = Capture")
print("ESC   = Quit")
print("="*60)

while current < len(DATASET):

    category, object_name, target = DATASET[current]

    print()
    print("="*50)
    print(f"Current Object : {object_name}")
    print(f"Target Images  : {target}")
    print("="*50)

    captured = 0

    while captured < target:

        try:

            r = requests.get(PREVIEW_URL, timeout=5)

            img = np.asarray(bytearray(r.content), dtype=np.uint8)

            frame = cv2.imdecode(img, cv2.IMREAD_COLOR)

            if frame is None:
                continue

        except Exception as e:
            print(e)
            continue

        display = frame.copy()

        cv2.putText(display,
                    category.upper(),
                    (10,25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,0),
                    2)

        cv2.putText(display,
                    object_name,
                    (10,55),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255,255,0),
                    2)

        cv2.putText(display,
                    f"{captured}/{target}",
                    (10,90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,0,255),
                    2)

        cv2.putText(display,
                    "SPACE = Capture",
                    (10,120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255,255,255),
                    2)

        cv2.imshow("Dataset Collector", display)

        key = cv2.waitKey(1) & 0xFF

        if key == 27:
            cv2.destroyAllWindows()
            quit()

        if key == 32:

            print("Capturing...")

            r = requests.get(CAPTURE_URL, timeout=10)

            img = np.asarray(bytearray(r.content), dtype=np.uint8)

            frame = cv2.imdecode(img, cv2.IMREAD_COLOR)

            if frame is None:
                print("Capture Failed")
                continue

            if category == "recyclable":

                recyclable_count += 1

                filename = os.path.join(
                    ROOT,
                    category,
                    f"recyclable_{recyclable_count:03d}.jpg"
                )

            else:

                non_count += 1

                filename = os.path.join(
                    ROOT,
                    category,
                    f"non_recyclable_{non_count:03d}.jpg"
                )

            cv2.imwrite(filename, frame)

            print("Saved:", filename)

            captured += 1

    print()
    print(f"✓ {object_name} COMPLETE")

    current += 1

    if current < len(DATASET):
        input("\nChange object then press ENTER...")

cv2.destroyAllWindows()

print()
print("="*60)
print("DATASET COMPLETE")
print("="*60)
print(f"Recyclable Images     : {recyclable_count}")
print(f"Non-Recyclable Images : {non_count}")
print("="*60)