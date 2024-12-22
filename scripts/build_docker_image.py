import os
import argparse

IMAGE_NAME = "fw_hw_book_docker_img"


def main(args):
    # Build the Docker image
    os.system(f"docker build -t {IMAGE_NAME} .")

    if args.upload:
        # Upload the Docker image
        os.system(f"docker tag {IMAGE_NAME} {args.user}/{IMAGE_NAME}")
        os.system(f"docker push {args.user}/{IMAGE_NAME}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Docker Image")

    parser.add_argument(
        "--upload", action="store_true", help="Upload the image to the registry"
    )
    parser.add_argument("--user", type=str, help="Docker username", required=True)

    args = parser.parse_args()

    main(args)
