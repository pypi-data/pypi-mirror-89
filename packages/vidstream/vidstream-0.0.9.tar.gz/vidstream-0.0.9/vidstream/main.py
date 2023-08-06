from streaming import VideoClient
from streaming import CameraClient
from streaming import ScreenShareClient

#client1 = ScreenShareClient('localhost', 9090)
client2 = VideoClient('localhost', 9090, "test.m4v")
#client3 = VideoClient('localhost', 9090)

client2.start_stream()