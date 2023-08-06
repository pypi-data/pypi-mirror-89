from os_file_stream_handler import file_stream_handler as fsh

src = "/Users/home/Google Drive/Remotes/Android/osfunapps_updates/Samsung/files/res/remotes/samsung_1/config.xml"
dst = "/Users/home/Google Drive/Remotes/Android/osfunapps_updates/Samsung/files/res/remotes/samsung_1/config2.json"
# fsh.compress_text_file_to_file(src, dst)
v = fsh.read_compressed_file(dst)