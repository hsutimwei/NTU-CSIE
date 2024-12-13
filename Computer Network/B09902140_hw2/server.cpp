#include<stdio.h>
#include<sys/socket.h>
#include<arpa/inet.h>
#include<sys/ioctl.h>
#include<net/if.h>
#include<unistd.h> 
#include <signal.h>
#include <dirent.h>
#include<string.h>
#include<stdlib.h>
#include <sys/stat.h>
#include <vector>
#include <string>
#include <iostream>
#include "opencv2/opencv.hpp"
using namespace std;
using namespace cv;

#define BUFF_SIZE 1024
#define PORT 8787
#define ERR_EXIT(a){ perror(a); exit(1); }
/*
    怎麼測ip不是127.0.0.1
    可能某些client速度很慢其他正常
*/
fd_set truefds,tempfds;
int selectfd;
vector<string> blocklist;
void signal_handler(int a){
    FD_CLR(selectfd, &truefds);
    close(selectfd);
    printf("Close client socket [%d]\n",selectfd);
    return;
}

int syncwithrecv(char* buffer,int fd)
{
    bzero(buffer,sizeof(buffer));
    int byte=recv(fd, buffer,sizeof(buffer), 0);
    bzero(buffer,sizeof(buffer));
    if(byte<=0)
    {
        FD_CLR(fd, &truefds);
        close(fd);
        return 0;
    }
    return 1;
}

struct data
{
    char username[BUFF_SIZE];
    int fd;
    int size;
    FILE *fp;
};
struct player
{
    char username[BUFF_SIZE];
    int fd;
    VideoCapture cap;
    int width;
    int height;
    Mat server_img;
};
int main(int argc, char *argv[])
{
    signal(SIGPIPE, signal_handler);
    int server_sockfd, client_sockfd, write_byte;
    struct sockaddr_in server_addr, client_addr;
    int client_addr_len = sizeof(client_addr);
    char buffer[2 * BUFF_SIZE] = {};
    char buffer1[2 * BUFF_SIZE] = {};
    char message[BUFF_SIZE] = "Hello World from Server";
    
    // Get socket file descriptor
    if((server_sockfd = socket(AF_INET , SOCK_STREAM , 0)) < 0){
        ERR_EXIT("socket failed\n")
    }
    mkdir("server_dir",0777);
    int port=atoi(argv[1]);
    // Set server address information
    bzero(&server_addr, sizeof(server_addr)); // erase the data
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(port);
    
    // Bind the server file descriptor to the server address
    if(bind(server_sockfd, (struct sockaddr *)&server_addr , sizeof(server_addr)) < 0){
        ERR_EXIT("bind failed\n");
    }
        
    // Listen on the server file descriptor
    if(listen(server_sockfd , 10) < 0){
        ERR_EXIT("listen failed\n");
    }
    pthread_t tid;
    char username[BUFF_SIZE] = {};
    char u[2*BUFF_SIZE]={};
    char uu[4*BUFF_SIZE+10]={};
    // Accept the client and get client file descriptor
    
    FD_ZERO(&truefds);
    FD_SET(server_sockfd,&truefds);
    vector<struct data>putlist,getlist;
    vector<struct player>playlist;
    struct timeval timeout={0,0};
    struct data p;
    struct player pp;
    while(1)
    {   
        for(int i=0;i<playlist.size();i++)
        {   
            selectfd=playlist[i].fd;
            bzero(buffer,sizeof(buffer));
            playlist[i].cap >> playlist[i].server_img;
            int imgSize = playlist[i].server_img.total() * playlist[i].server_img.elemSize();
            
            sprintf(buffer,"%d",imgSize);
            send(playlist[i].fd,buffer, sizeof(buffer), 0);//傳image大小
            
            if(imgSize==0)
            {   
                bzero(buffer,sizeof(buffer));
                recv(playlist[i].fd, buffer,sizeof(buffer), 0);
                playlist[i].cap.release();
                playlist.erase(playlist.begin()+i);
                i--;
                continue;
            }

            if(syncwithrecv(buffer,playlist[i].fd)==0)
            {
                playlist[i].cap.release(); 
                playlist.erase(playlist.begin()+i);
                i--;
                continue;
            }

            char imgbuffer[imgSize];
            memcpy(imgbuffer, playlist[i].server_img.data, imgSize);
            int byte,j=0,check=0;
            while(imgSize>0)//傳image
            {   
		        byte = send(playlist[i].fd,imgbuffer+j, sizeof(imgbuffer)-j, 0);
                if(byte < 0)
                {   
                    playlist[i].cap.release(); 
                    playlist.erase(playlist.begin()+i);
                    i--;
                    check++;
                    break;
                }
                //memcpy(imgbuffer,imgbuffer+byte,sizeof(imgbuffer)-byte);
                imgSize -= byte;
                j+=byte;
            }
            
            bzero(buffer,sizeof(buffer));
            //printf("%ld %d %d aaa\n",strlen(buffer),getlist[i].fd,byte);
            
            byte = recv(playlist[i].fd, buffer,sizeof(buffer), 0);//確認已收到，得到waitkey回傳
            int c=atoi(buffer);
            send(playlist[i].fd,"hello", sizeof("hello"), 0);//總之同步一下
            //cout << imgSize<< '\n';
            if(byte <= 0 || c==27)
            {   
                if(!check)
                {   
                    playlist[i].cap.release(); 
                    playlist.erase(playlist.begin()+i);
                    i--; 
                }
                continue;
            }
            bzero(buffer,sizeof(buffer));
        }
        for(int i=0;i<getlist.size();i++)
        {
            selectfd=getlist[i].fd;
            bzero(buffer,sizeof(buffer));
		    int byte = fread(buffer, sizeof(char), sizeof(buffer), getlist[i].fp);
            if(byte < 0)
            {   
                fclose(getlist[i].fp);
                getlist.erase(getlist.begin()+i);
                i--;
                continue;
            }
            //printf("%ld %d aaa\n",strlen(buffer),getlist[i].fd);
            byte = send(getlist[i].fd, buffer, byte, 0);
            //printf("%ld %d %d aaa\n",strlen(buffer),getlist[i].fd,byte);
            if(byte < 0)
            {   
                fclose(getlist[i].fp);
                getlist.erase(getlist.begin()+i);
                i--;
                continue;
            } 
            getlist[i].size -= byte;
            if(getlist[i].size<=0)
            {
                fclose(getlist[i].fp);
                getlist.erase(getlist.begin()+i);
                i--;
            }
        }
        

        tempfds=truefds;
        int out=select(1024,&tempfds,NULL,NULL,&timeout);

        if(out==0)
            continue;
        
        for(selectfd=0; selectfd<1024; selectfd++)
        {
            if(FD_ISSET(selectfd,&tempfds))
            {   
                if(selectfd==server_sockfd)//建新連線
                {
                    client_sockfd = accept(server_sockfd, (struct sockaddr *)&client_addr, (socklen_t*)&client_addr_len);
                    FD_SET(client_sockfd, &truefds);
                    bzero((username), sizeof(username));
                    recv(client_sockfd, username, sizeof(username) - 1,0);
                    printf("Accept a new connection on socket [%d]. Login as %s.\n",client_sockfd,username);
                    sprintf(buffer,"server_dir/%s",username);
                    mkdir(buffer,0777);
                    bzero((buffer), sizeof(buffer));
                }
                else
                {   
                    int putt=0;
                    for(int i=0;i<putlist.size();i++)
                    {
                        if(selectfd==putlist[i].fd)
                        {   
                            bzero(buffer,sizeof(buffer));
		                    int byte = recv(putlist[i].fd, buffer, sizeof(buffer), 0);
                            if(byte <= 0)
                            {   
                                printf("Close client socket [%d]\n",selectfd);
                                FD_CLR(selectfd, &truefds);
                                close(selectfd);
                                fclose(putlist[i].fp);
                                putlist.erase(putlist.begin()+i);
                                i--;
                                putt++;
                                continue;
                            }   
                            //printf("%d %ld aa\n",byte,strlen(buffer));
		                    byte = fwrite(buffer, sizeof(char), byte, putlist[i].fp);
                            //printf("%d %ld aa\n",byte,strlen(buffer));
                            putlist[i].size -= byte;
                            if(putlist[i].size<=0)
                            {
                                fclose(putlist[i].fp);
                                putlist.erase(putlist.begin()+i);
                                i--;
                                bzero(buffer,sizeof(buffer));
                                send(selectfd, "hello", sizeof("hello"), 0);//同步
                                bzero((buffer), sizeof(buffer));
                                //printf("put finish\n");
                            }
                            putt++;
                        }
                        
                    }
                    if(putt>0)
                        continue;
                    
                    bzero((u), sizeof(u));
                    int readbytes=recv(selectfd, u, sizeof(u),0);//指令長度
                    if(readbytes <= 0)//如果fd斷線
                    {
                        FD_CLR(selectfd, &truefds);
                        close(selectfd);
                        printf("Close client socket [%d]\n",selectfd);
                        continue;
                    }
                    if(strlen(u)==0)
                        continue;
                    int size=atoi(u);//得到接下來指令的長度
                    //printf("指令長度是%s\n",u);
                    bzero(uu,sizeof(uu));
                    send(selectfd, "hello", sizeof("hello"), 0);//同步
                    int j=0;
                    while(size>0)//接收指令
                    {
                        bzero(u,sizeof(u));
                        int byte=recv(selectfd,uu+j,sizeof(uu)-j,0);
                        if(byte<=0)
                        {
                            printf("Close client socket [%d]\n",selectfd);
                            FD_CLR(selectfd, &truefds);
                            close(selectfd);
                        }
                        size-=byte;
                        j+=byte;
                    }
                    //printf("指令是%s這樣\n",uu);//確認指令是否正確
                    char *pch=strtok(uu," \n");//得到使用者和指令名稱
                    strcpy(p.username,pch);
                    strcpy(pp.username,pch);
                    pch=strtok(NULL," \n");
                    int cc=0;//確認blocklist
                    for(int i=0;i<blocklist.size();i++)//blocklist確認
                    {   
                        const char* c=blocklist[i].c_str();
                        if(strcmp(p.username,c)==0)
                        {
                            send(selectfd,"Permission denied.",sizeof("Permission denied."),0);
                            cc++;
                            break;
                        }
                    }
                    if(cc>0)//在blocklist所以continue
                        continue;
                    if(strcmp(pch,"ls")==0)
                    {   
                        bzero(buffer, sizeof(buffer));
                        sprintf(buffer,"./server_dir/%s",p.username);
                        DIR *dir =opendir(buffer);
                        struct dirent *ptr;
                        char lsname[200000]={};
                        bzero(buffer, sizeof(buffer));
                        bzero(lsname, sizeof(lsname));
                        while((ptr=readdir(dir)) != NULL)
                        {
                            if(strcmp(ptr->d_name,".") == 0 || strcmp(ptr->d_name,"..") == 0)
                                continue;
                            strcat(lsname, ptr->d_name);
                            strcat(lsname, "\n");
                            
                        }
                        closedir(dir);
                        size=strlen(lsname);
                        sprintf(buffer,"%d",size);
                        
                        int u=send(selectfd,buffer, sizeof(buffer), 0);//把結果的長度傳過去
                        if(u<0)
                            continue;
                        if(syncwithrecv(buffer,selectfd)==0)//同步
                            continue;
                        int j=0;
                        while(size>0)
                        {   
		                    int byte = send(selectfd,lsname+j, 2048, 0);
                            if(byte<0)
                                break;
                            size -= byte;
                            j+=byte;
                        }
                        bzero((buffer), sizeof(buffer));
                    }
                    else if(strcmp(pch,"play")==0)
                    {
                        bzero((buffer), sizeof(buffer));
                        sprintf(buffer,"./server_dir/%s",p.username);
                        DIR *dir =opendir(buffer);
                        struct dirent *ptr;
                        bzero((buffer), sizeof(buffer));
                        int flag = 0;
                        pch=strtok(NULL, " \n");
                        while((ptr = readdir(dir)) != NULL)
                        {
                            if(strcmp(pch, ptr->d_name) == 0)
                            {
                                flag = 1;
                                break;
                            }
                        }
                        //cout << pch << '\n';
                        char *pppch = strstr(pch,".mpg");
                        if(pppch==NULL && flag==1)
                            flag=2;
                        if(flag==1)
                        {   
                            
                            pp.fd=selectfd;
                            sprintf(buffer,"./server_dir/%s/%s",pp.username,pch);
                            VideoCapture cap(buffer);
                            pp.cap=cap;

                            sprintf(buffer,"Yes");
                            send(selectfd,buffer,sizeof(buffer),0); //傳yes
                            
                            bzero(buffer, sizeof(buffer));
                            recv(selectfd,buffer,sizeof(buffer),0);//同步

                            pp.width = cap.get(CAP_PROP_FRAME_WIDTH);
                            sprintf(buffer,"%d",pp.width);
                            send(selectfd,buffer,sizeof(buffer),0); //傳寬度

                            bzero(buffer, sizeof(buffer));
                            recv(selectfd,buffer,sizeof(buffer),0);//同步

                            pp.height = cap.get(CAP_PROP_FRAME_HEIGHT);
                            sprintf(buffer,"%d",pp.height);
                            send(selectfd,buffer,sizeof(buffer),0); //傳高度

                            bzero(buffer, sizeof(buffer));
                            recv(selectfd,buffer,sizeof(buffer),0);//同步
                            bzero(buffer, sizeof(buffer));

                            Mat server_img;
                            server_img = Mat::zeros(pp.height, pp.width, CV_8UC3);
                            pp.server_img=server_img;
                            if(!pp.server_img.isContinuous())
                            {
                                pp.server_img = pp.server_img.clone();
                            }
                            
                            
                            bzero((buffer), sizeof(buffer));
                            playlist.push_back(pp);
                        }
                        else if(flag==0)
                        {   
                            sprintf(buffer,"No");
                            send(selectfd,buffer,sizeof(buffer),0); 
                            bzero((buffer), sizeof(buffer));
                        }
                        else
                        {
                            sprintf(buffer,"Noo");
                            send(selectfd,buffer,sizeof(buffer),0); 
                            bzero((buffer), sizeof(buffer));
                        }
                    }
                    else if(strcmp(pch,"get")==0)
                    {
                        bzero((buffer), sizeof(buffer));
                        sprintf(buffer,"./server_dir/%s",p.username);
                        DIR *dir =opendir(buffer);
                        struct dirent *ptr;
                        bzero((buffer), sizeof(buffer));
                        int flag = 0;
                        pch=strtok(NULL, " \n");
                        while((ptr = readdir(dir)) != NULL)
                        {
                            if(strcmp(pch, ptr->d_name) == 0)
                            {
                                flag = 1;
                                break;
                            }
                        }
                        if(flag==1)
                        {
                            p.fd=selectfd;
                            sprintf(buffer,"./server_dir/%s/%s",p.username,pch);
                            FILE *fp = fopen(buffer, "r");
                            fseek(fp, 0, SEEK_END);
                            p.size = ftell(fp);
                            sprintf(buffer,"Yes %d",p.size);
                            send(selectfd,buffer,sizeof(buffer),0); 
                            bzero((buffer), sizeof(buffer));
                            fseek(fp, 0, SEEK_SET);
                            p.fp=fp;
                            if(syncwithrecv(buffer,selectfd)==0)
                            {
                                fclose(fp);
                                continue;
                            }
                            getlist.push_back(p);
                            
                        }
                        else
                        {   
                            sprintf(buffer,"No");
                            send(selectfd,buffer,sizeof(buffer),0); 
                            bzero((buffer), sizeof(buffer));
                        }
                    }
                    else if(strcmp(pch,"put")==0)
                    {   
                        p.fd=selectfd;//存fd
                        pch=strtok(NULL, " \n");//true or false
                        char* ppch=pch;
                        bzero(buffer,sizeof(buffer));
                        send(selectfd, "hello", sizeof("hello"), 0);//同步
                        pch=strtok(NULL, " \n");
                        if(strcmp(pch,"false")==0)
                            continue;
                        bzero((buffer), sizeof(buffer));
                        sprintf(buffer,"./server_dir/%s/%s",p.username,ppch);
                        //printf("%s\n",buffer);
                        FILE *fp = fopen(buffer, "w");
                        p.fp=fp;
                        pch=strtok(NULL, " \n");//檔案長度      
                        p.size=atoi(pch);
                        //printf("%d bb\n",p.size);
                        putlist.push_back(p);
                        
                        
                    }
                    else if(strcmp(pch,"ban")==0)
                    {   
                        
                        pch=strtok(NULL, " \n");
                        if(strcmp(p.username,"admin")==0)
                        {   
                            char large[200000]={};
                            while(pch!=NULL)
                            {
                                int cnt=0,i;
                        
                                for(i=0;i<blocklist.size();i++)
                                {   
                                    const char* c=blocklist[i].c_str();
                                    if(strcmp(pch,c)==0)
                                    {
                                        sprintf(buffer,"User %s is already on the blocklist!",pch);
                                        strcat(large,buffer);
                                        cnt++;
                                        break;
                                    }
                                }
                                if(strcmp(pch,"admin")==0)
                                {
                                    strcat(large,"You cannot ban yourself!");
                                }
                                else if(cnt==0)
                                {
                                    sprintf(buffer,"Ban %s successfully!",pch);
                                    strcat(large,buffer);
                                    string s(pch);
                            //cout << s << "\n";
                                    blocklist.push_back(s);
                                }
                            
                                pch=strtok(NULL, " \n");
                                if(pch!=NULL)
                                {
                                    strcat(large,"\n");
                                }
                            }
                            //cout << large << "\n";
                            size=strlen(large);
                            sprintf(buffer,"%d",size);
                            int u=send(selectfd,buffer,sizeof(buffer),0);//傳指令的長度
                            if(u<0)
                                continue;
                            if(syncwithrecv(buffer,selectfd)==0)
                            {
                                continue;
                            }
                            int j=0;
                            while(size>0)
                            {   
		                        int byte = send(selectfd,large+j, 2048, 0);
                                if(byte<0)
                                    break;
                                size -= byte;
                                j+=byte;
                            }
                            bzero((buffer), sizeof(buffer));
                    
                        }
                        else
                        {
                            send(selectfd,"Permission denied.",sizeof("Permission denied."),0);
                        }
                    }
                    else if(strcmp(pch,"unban")==0)
                    {   
                        
                        if(strcmp(p.username,"admin")==0)
                        {   
                            char large[200000]={};
                            pch=strtok(NULL, " \n");
                            while(pch!=NULL)
                            {
                                int cnt=0,i;
                        
                                for(i=0;i<blocklist.size();i++)
                                {   
                                    const char* c=blocklist[i].c_str();
                                    if(strcmp(pch,c)==0)
                                    {
                                        sprintf(buffer,"Successfully removed %s from the blocklist!",pch);
                                        strcat(large,buffer);
                                        blocklist.erase(blocklist.begin()+i);
                                        i--;
                                        cnt++;
                                        break;
                                    }
                                }
                                if(cnt==0)
                                {
                                    sprintf(buffer,"User %s is not on the blocklist!",pch);
                                    strcat(large,buffer);
                                }
                            
                                pch=strtok(NULL, " \n");
                                if(pch!=NULL)
                                {
                                    strcat(large,"\n");
                                }
                            }
                            //cout << buffer << "\n";
                            size=strlen(large);
                            sprintf(buffer,"%d",size);
                            int u=send(selectfd,buffer,sizeof(buffer),0);//傳指令的長度
                            if(u<0)
                                continue;
                            if(syncwithrecv(buffer,selectfd)==0)
                            {
                                continue;
                            }
                            int j=0;
                            while(size>0)
                            {   
		                        int byte = send(selectfd,large+j, 2048, 0);
                                if(byte<0)
                                    break;
                                size -= byte;
                                j+=byte;
                            }
                            bzero(buffer,sizeof(buffer));
                        }
                        else
                        {
                            send(selectfd,"Permission denied.",sizeof("Permission denied."),0);
                        }
                    }
                    else if(strcmp(pch,"blocklist")==0)
                    {   
                        char large[200000]={};
                        if(strcmp(p.username,"admin")==0)
                        {
                            for(int i=0;i<blocklist.size();i++)
                            {
                                const char* c=blocklist[i].c_str();
                                strcat(large,c);
                                strcat(large,"\n");

                            }
                            //printf("%s\n",large);
                            int size=strlen(large);
                            sprintf(buffer,"%d",size);
                            int u=send(selectfd,buffer,sizeof(buffer),0);//傳指令的長度
                            if(u<0)
                                continue;
                            if(syncwithrecv(buffer,selectfd)==0)//同步
                            {
                                continue;
                            }
                            while(size>0)
                            {   
                                strncpy(buffer,large,2048);
		                        int byte = send(selectfd,buffer, 2048, 0);
                                if(byte<0)
                                    break;
                                memcpy(large,large+byte,sizeof(large)-byte);
                                size -= byte;
                            }
                            bzero((buffer), sizeof(buffer));
                        }
                        else
                        {
                            send(selectfd,"Permission denied.",sizeof("Permission denied."),0);
                        }
                    }
                    else
                    {
                        send(selectfd,"Command not found.",sizeof("Command not found."),0);
                    }

            
        
                }
            


            }
        }
    }
    return 0;
}
