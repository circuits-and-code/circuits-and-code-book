from PIL import Image
import os
import argparse
from cairosvg import svg2png


def crop_image(input_path, output_path):
    # Open the image file
    with Image.open(input_path) as img:
        # Convert image to RGBA to handle transparency if needed
        img = img.convert("RGBA")

        # Get the bounding box of the non-white area
        bbox = img.getbbox()

        if bbox:
            # Crop the image to the bounding box
            cropped_img = img.crop(bbox)

            # Save the cropped image
            cropped_img.save(output_path)
            print(f"Image successfully cropped and saved to {output_path}")
        else:
            print("No content found in the image to crop.")


def convert_svg_to_png(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Search for all .svg files in the input directory
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".svg"):
                svg_path = os.path.join(root, file)
                png_filename = os.path.splitext(file)[0] + ".png"
                temp_png_path = os.path.join(output_dir, f"temp_{png_filename}")
                final_png_path = os.path.join(output_dir, png_filename)

                # Convert SVG to PNG
                try:
                    print(f"Converting: {svg_path} -> {temp_png_path}")
                    with open(svg_path, "rb") as svg_file:
                        svg_data = svg_file.read()
                        svg2png(
                            bytestring=svg_data,
                            write_to=temp_png_path,
                            output_width=1024,
                            output_height=1024,
                        )

                    # Crop the PNG after conversion
                    crop_image(temp_png_path, final_png_path)

                    # Remove the temporary uncropped PNG
                    os.remove(temp_png_path)

                    print(f"Successfully converted and cropped: {final_png_path}")
                except Exception as e:
                    print(f"Failed to convert {svg_path}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert SVG images to PNG format.")
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Path to the directory containing SVG files.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Path to the output directory where PNG files will be saved.",
    )

    args = parser.parse_args()

    input_directory = args.input_dir
    output_directory = args.output_dir

    convert_svg_to_png(input_directory, output_directory)
