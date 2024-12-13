CC = gcc
CXX = g++
INCLUDE_OPENCV = `pkg-config --cflags --libs opencv4`
LINK_PTHREAD = -lpthread

CLIENT = client.cpp
SERVER = server.cpp
OPEN_CV = openCV.cpp
PTHREAD = pthread.cpp
CLI = client
SER = server
CV = openCV
PTH = pthread
CDIR = client_dir
SDIR = server_dir
all: server client haha
  
server: $(SERVER)
	$(CXX) $(SERVER) -o $(SER) $(INCLUDE_OPENCV)
client: $(CLIENT)
	$(CXX) $(CLIENT) -o $(CLI) $(INCLUDE_OPENCV) 


.PHONY: clean

clean:
	rm $(CLI) $(SER)
haha:
	rm -rf $(CDIR) $(SDIR)

eee:
	cp video.mpg server_dir/admin/
	cp file.txt client_dir/
	cp aaa.txt server_dir/admin/
	cp ooh.mpg client_dir/
	cp ooh.mpg server_dir/alice/

dif:
	diff server_dir/admin client_dir -s

diff:
	diff server_dir/admin/video.mpg client_dir/video.mpg -s
