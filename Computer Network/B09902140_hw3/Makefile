CC = g++
INCLUDE_OPENCV = `pkg-config --cflags --libs opencv4`
AGENT_SRC = agent.cpp
AGENT_EXEC = agent
SENDER_SRC = sender.cpp
SENDER_EXEC = sender
RECEIVER_SRC = receiver.cpp
RECEIVER_EXEC = receiver
all: agent sender receiver

agent: $(AGENT_SRC)
	$(CC) $(AGENT_SRC) -o $(AGENT_EXEC)

sender: $(SENDER_SRC)
	$(CC) $(SENDER_SRC) -lz -o $(SENDER_EXEC) $(INCLUDE_OPENCV)

receiver: $(RECEIVER_SRC)
	$(CC) $(RECEIVER_SRC) -lz -o $(RECEIVER_EXEC) $(INCLUDE_OPENCV)

cv: openCV.cpp
	g++ openCV.cpp -lz -o opencv $(INCLUDE_OPENCV)

.PHONY: clean

clean:
	rm sender receiver