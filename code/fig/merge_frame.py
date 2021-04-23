import imageio
import glob
import re
import os

png_filenames = glob.glob(r"*.png")
png_filenames.sort()
buf=[]
for png_file in png_filenames:
    buf.append(png_file)

print(buf)

frames = []
for image_name in buf:
    frames.append(imageio.imread(image_name))
# Save them as frames into a gif
imageio.mimsave('sw.mp4', frames, 'MP4')


