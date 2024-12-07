import cv2
import os
import matplotlib.pyplot as plt

from Face_Detection import detect_face
from Emoji_Swap import swap_emoji, detect_emotion
from Hair_Detection import readHairColor

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
#turn off FER/tensorflow debug msgs

# Paths to images and emojis
image_paths = {'Data/AngryMan.jpg', 'Data/jim.jpg', 'Data/crying_stock_photo.png', 'Data/GingerMan.jpg'}

for image_path in image_paths:
    # Load the image
    image = cv2.imread(image_path)
    image_filename = os.path.basename(image_path)
    print(image_filename)

    # Check if the image was loaded successfully
    if image is None:
        print("Error loading image. Please check the image path and file.")
        exit()
    
    # TODO: Make image resizing dynamic, for some reason, not very robust when I tried making it dynamic
    # Resize the image if needed 
    scale_percent = 25 if(image_path == 'Data/Tiger_Woods.jpeg') else 100 # Adjust this value
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    image_resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    
    # Convert the resized image to RGB as Mediapipe requires
    image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)

    emotion = detect_emotion(image_rgb.copy())
    angle, x_max, x_min, y_max, y_min = detect_face(image_rgb.copy(), image_resized, width, height)
    image_emoji = swap_emoji(image_resized.copy(), emotion, angle, x_max, x_min, y_max, y_min)
    hair_color = readHairColor(image_filename)
    print(hair_color)

    # Display the final image
    side_by_side = cv2.hconcat([image_resized, image_emoji])
    cv2.imshow('Emoji Face Swap', side_by_side)
    cv2.moveWindow('Emoji Face Swap', 0, 200)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    plt.imshow(cv2.cvtColor(image_emoji, cv2.COLOR_BGR2RGB))
    output_filename = 'final_'+ image_filename 
    plt.savefig(f'output/{output_filename}')

