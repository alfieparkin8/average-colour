from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import os

def most_prominent_color(image_path, k=1):
    img = Image.open(image_path)
    img = img.convert("RGB")
    img_array = np.array(img).reshape((-1, 3))

    # Perform k-means clustering to find the most prominent color
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(img_array)

    # Get the most prominent color
    prominent_color = np.uint8(kmeans.cluster_centers_[0])

    return tuple(prominent_color)

def apply_most_prominent_color(image_path, output_folder, relative_path):
    try:
        # Get the most prominent color for the input image
        prominent_color = most_prominent_color(image_path)

        # Create an output image with the same size as the input
        img = Image.open(image_path)
        img = img.convert("RGB")
        new_image = Image.new("RGB", img.size, prominent_color)

        # Save the output image in the corresponding subdirectory with the same name as the input
        output_subfolder = os.path.join(output_folder, os.path.dirname(relative_path))
        os.makedirs(output_subfolder, exist_ok=True)
        output_path = os.path.join(output_subfolder, os.path.basename(image_path))
        new_image.save(output_path)

        return output_path
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None

def main():
    # Path to the directory containing your images
    images_directory = "images"
    
    # Output folder
    output_folder = "output"

    # Get a list of image files in the directory and its subdirectories
    image_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(images_directory) for f in filenames if f.endswith(('.jpg', '.jpeg', '.png'))]

    if not image_files:
        print("No image files found in the directory.")
        return

    # Apply the most prominent color to each image in the directory and its subdirectories
    successful_count = 0
    for i, image_path in enumerate(image_files):
        relative_path = os.path.relpath(image_path, images_directory)
        output_path = apply_most_prominent_color(image_path, output_folder, relative_path)
        if output_path is not None:
            successful_count += 1
            print(f"Processed image {i + 1}/{len(image_files)} - Output saved to: {output_path}")

    print(f"Processed {successful_count} out of {len(image_files)} images.")

if __name__ == "__main__":
    main()
