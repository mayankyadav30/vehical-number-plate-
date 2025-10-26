import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load the image
image = cv2.imread('car_image.jpg.jpg')

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Display the grayscale image
cv2.imshow('Grayscale Image', gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Apply Canny Edge Detection
edges = cv2.Canny(gray_image, 100, 200)

# Display the edges image
cv2.imshow('Edges Image', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Step 2: Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Just for checking: print how many shapes (contours) were found
print(f"Number of contours found: {len(contours)}")

# Step 3: Check for 4-sided shapes (rectangles)
for contour in contours:
    epsilon = 0.04 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
        area = cv2.contourArea(contour)

        if area > 1000 and w > h:
            aspect_ratio = w / h
            if 1.5 < aspect_ratio < 8:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                plate_img = image[y:y + h, x:x + w]
                print("Number plate found and cropped")
                break
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

text = pytesseract.image_to_string(plate_img)
print("Detected Plate Text:", text.strip())


# Show the final image with the rectangle
cv2.imshow('Detected Plate', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

if 'plate_img' in locals():
    cv2.imshow("Cropped Plate", plate_img)
    cv2.imwrite("cropped_plate.jpg", plate_img)

    # 🔽 Add this block to improve OCR
    gray_plate = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    _, thresh_plate = cv2.threshold(gray_plate, 150, 255, cv2.THRESH_BINARY)

    # Optional: view what Tesseract sees
    cv2.imshow("Thresholded Plate", thresh_plate)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 🔍 OCR to read text
    text = pytesseract.image_to_string(thresh_plate, config='--psm 8')
    print("Detected Plate Text:", text.strip())

else:
    print("Plate not detected")

# Show the cropped number plate if found
if 'plate_img' in locals():
    cv2.imshow("Cropped Plate", plate_img)
    cv2.imwrite("cropped_plate.jpg", plate_img)
else:
    print("Plate not detected")

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if 'plate_img' in locals():
    # OCR the cropped image
    plate_text = pytesseract.image_to_string(plate_img, config='--psm 7')
    print("Detected Number Plate Text:", plate_text.strip())

    # Optional: save to a text file
    with open("plate_text_output.txt", "w") as f:
        f.write(plate_text.strip())
else:
    print("No number plate image found.")
