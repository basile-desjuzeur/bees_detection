import os
import wget
from tqdm import tqdm
import asyncio
import argparse

argparser = argparse.ArgumentParser()

argparser.add_argument(
    '-i', '--input',
    help='Input file',
    required=True)

args = argparser.add_argument(
    '-o', '--output',
    help='Output folder',
    required=True)


def background(f):
	def wrapped(*args, **kwargs):
		return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)
		
	return wrapped
	
@background
def get_image(image_url, target_dest):
	wget.download(image_url, target_dest)
	return


def download_images(input_file, output_folder):

	# Create output folder
	if not os.path.exists(output_folder):
		os.mkdir(output_folder)


	# Load CSV of selected pictures : #taxon_id	#photo_id #extension
	with open(input_file, newline='') as csvfile:
		lines = csvfile.read().split("\n")
		for i,row in enumerate(tqdm(lines)):
			data = row.split(',')
			if i > 0 and len(data) > 2:
				taxon_name = data[0]
				taxon_id = data[1]
				photo_id = data[2]
				extension = data[3]
			
				if not os.path.exists(output_folder + taxon_name):
					os.mkdir(output_folder + taxon_name)
					
				image_url = f"https://inaturalist-open-data.s3.amazonaws.com/photos/{photo_id}/medium.{extension}"
				target_dest = os.path.join(output_folder, taxon_name, f"{photo_id}.{extension}")
				get_image(image_url, target_dest)


if __name__ == "__main__":
	args = argparser.parse_args()
	download_images(args.input, args.output)