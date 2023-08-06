### SIMPLE IMAGE DOWNLOADER
import httpx
from PIL import Image
import argparse
import os
import sys
from io import BytesIO

class JPGDL:
    # MAIN DOWNLOADER FUNCTION
    @staticmethod
    def jpeg_download(download_url, filename, output_folder=os.getcwd()):
        """
        Download an IMAGE with a JPEG output.

        download_url => Url link of the image file.
        filename => Filename to be downloaded.
        output_folder => Where to store the image. Defaults to current directory.
        """

        img_file = f"{filename}.jpg" # filename
        output_file = os.path.join(output_folder, img_file) # output file dir

        # check if the filename exists in the directory
        if os.path.exists(output_folder + img_file):
            print(f"\n  ![Err] Filename `{img_file}` already exists at folder `{output_folder}`.")
            sys.exit(1) # exit the app

        file = ''
        # start download
        try:
            print(f"\n  Downloading Image: `{img_file}` from > {download_url}")
            file = httpx.get(download_url, timeout=None)
        except httpx.ConnectError:
            print(f"\n  ![NetErr] The download url doesn't seem to exist or you are not connected to the internet.")
            sys.exit(1)

        # try to convert the content to jpeg
        try:
            print("\n  Converting image to JPEG...")
            image = Image.open(BytesIO(file.content)).convert("RGB")
            image.save(output_file, "jpeg") # save as jpeg
        except Exception:
            print("\n  ![ConvErr] There was a problem while trying to save and convert the image to JPEG.")
            sys.exit(1)

        # print done message
        print(f"\n  Image has been successfully downloaded.\n\tSaved to => {output_file}")


# this will only run when it is called from the command line
if __name__ == '__main__':
    # Initiate the parser
    parser = argparse.ArgumentParser()

    # set parser arguments
    parser.add_argument("-u", "--url", help="Download url / the link of the image. It must start with `https://` or `http://`", required=True, type=str)
    parser.add_argument("-f", '--filename', help="Set filename of the image. Do not add `.jpg`", required=True, type=str)
    parser.add_argument("-o", '--output', help="Where to store the image. Default is the current directory", type=str)

    # check if there are arguments specified
    # based from: https://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()


    # check and get each argument
    if args.url and args.filename:
        JPGDL.jpeg_download(download_url=args.url, filename=args.filename) # download the image with the handler