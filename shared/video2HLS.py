# import ffmpeg
#
#
# def convert_to_hls(video_path, output_directory):
#     output_path = f"{output_directory}/output.m3u8"
#
#     try:
#         input_file = ffmpeg.input(video_path)
#
#         ffmpeg.output(input_file, output_path, format='hls', start_number=0).run()
#
#         print("Conversion to HLS format completed successfully.")
#         print(f"Output HLS playlist file: {output_path}")
#
#     except ffmpeg.Error as e:
#         print(f"An error occurred during the conversion: {e.stderr}")
#
#
# # Example usage
# video_path = '/home/ibrohimjon/Desktop/New Folder/VideoTest/v.mp4'
# output_directory = '/home/ibrohimjon/Desktop/pythonProject/'
#
# convert_to_hls(video_path, output_directory)
