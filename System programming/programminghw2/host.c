/********************************************************************************************
*                                       
*                              
*                            
*                              
********************************************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <sys/wait.h>
#define _GNU_SOURCE

char* m="-m";
char* l="-l";
char* d="-d";
char* n="-n";

void fork2child(int depth, int lucky, int id , int player1, int player2, int* f2r, int* f2w, int * t2r, int* t2w)
{
         
    if(pipe(f2r)<0)
       fprintf(stderr, "f2r pipe error\n");

    if(pipe(f2w)<0)
       fprintf(stderr, "f2w pipe error\n");

    if(pipe(t2r)<0)
       fprintf(stderr, "t2r pipe error\n");
    
    if(pipe(t2w)<0)
       fprintf(stderr, "t2w pipe error\n");

    int pid1 = fork();
    int pid2=1;
    if(pid1<0)
    {
        fprintf(stderr, "fork error\n");
    }
    else if(pid1 == 0)//first child
    {    
         close(f2r[0]);
         close(f2w[1]);
         dup2(f2r[1],1);
         close(f2r[1]);
         dup2(f2w[0],0);
         close(f2w[0]);
    }
    else
    {
         pid2 = fork();//second child

         if(pid2<0)
         fprintf(stderr, "fork error\n");

         if(pid2==0)
         {
             close(t2r[0]);
             close(t2w[1]);
             dup2(t2r[1],1);
             close(t2r[1]);
             dup2(t2w[0],0);
             close(t2w[0]);
         }
    }
        char charid[10],charlucky[10],chardepth[10],charplayer1[10],charplayer2[10];
        sprintf(charid, "%d", id);
        sprintf(charlucky, "%d", lucky);
        depth++;
        sprintf(chardepth, "%d", depth);
        sprintf(charplayer1, "%d", player1);
        sprintf(charplayer2, "%d", player2);
        if(depth <= 2 && (pid1==0 || pid2==0))  
            execl("./host","./host", "-m", charid, "-d", chardepth , "-l", charlucky, NULL);
        else if(depth == 3 && (pid1==0 || pid2==0))
          if(pid1==0)
          {
            //fprintf(stderr, "to player %d\n",player1);
            execl("./player","./player", "-n", charplayer1, NULL);
            fprintf(stderr, "????\n");

          }
          else
          { 

            //fprintf(stderr, "to player %d\n",player2);
            execl("./player","./player", "-n", charplayer2, NULL);
            fprintf(stderr, "xxxx\n");
          }
        //parent

        close(f2r[1]);
        close(f2w[0]);
        close(t2r[1]);
        close(t2w[0]);
    
}

int  main(int argc, char *argv[])
{   
    if(argc != 7)
    {
        fprintf(stderr, "Wrong number of argument\n");
        exit(1);
    }

    int depth=-20;
    int id=-20;
    int lucky=-20;
    
    //讀進來
  
    if(!strcmp(argv[1],m))
       id=atoi(argv[2]);

    if(!strcmp(argv[3],m))
        id=atoi(argv[4]);

    if(!strcmp(argv[5],m))
        id=atoi(argv[6]);

    if(!strcmp(argv[1],l))
        lucky=atoi(argv[2]);

    if(!strcmp(argv[3],l))
        lucky=atoi(argv[4]);

    if(!strcmp(argv[5],l))
        lucky=atoi(argv[6]);

    if(!strcmp(argv[1],d))
        depth=atoi(argv[2]);

    if(!strcmp(argv[3],d))
        depth=atoi(argv[4]);

    if(!strcmp(argv[5],d))
        depth=atoi(argv[6]);
    
    if(id > 10 || id < 1 || depth < 0 || depth > 2 || lucky < 0 || lucky > 1000)
        {
            fprintf(stderr, "Umm... something error\n");
            exit(1);
        }

    
    int f2r[2],f2w[2],t2r[2],t2w[2];

    if(depth == 0)//root
    {      char buf[1024];
           fork2child(depth, lucky, id, 0, 0 , f2r , f2w, t2r, t2w);
           sprintf(buf, "fifo_%d.tmp", id);

           int readsys;
        
           if((readsys=open(buf,O_RDONLY))<0)
           fprintf(stderr, "%s open error",buf);

           int writesys;

           if((writesys=open("fifo_0.tmp", O_WRONLY))<0)
           fprintf(stderr, "fifo_0.tmp open error");

           int player[8];
           FILE  *f2 = fdopen(f2r[0], "r"),*t2 = fdopen(t2r[0], "r");
           int a;
           int cnt=0;
           while(1)
           {   //fprintf(stderr, "cggggcc\n");
              //sleep(2);
              memset(buf,0,1024);
              if(read(readsys, buf, sizeof(buf))<=0)
                  continue;
               //fprintf(stderr, "host %d buf %d: %s\n",id,cnt, buf);
               cnt++;
              //fprintf(stderr, "cgg\n");
              sscanf(buf, "%d%d%d%d%d%d%d%d", &player[0], &player[1], &player[2], &player[3], &player[4], &player[5], &player[6], &player[7]);
              //fprintf(stderr, "depth 0 player: %d %d %d %d %d %d %d %d\n", player[0], player[1], player[2], player[3], player[4], player[5], player[6], player[7]);
              sprintf(buf, "%d %d %d %d\n", player[0], player[1], player[2], player[3]);
              write(f2w[1], buf, strlen(buf));
              sprintf(buf, "%d %d %d %d\n", player[4], player[5], player[6], player[7]);
              write(t2w[1], buf, strlen(buf));
              
              //memset(buf,0,1024);
              
              if(player[0]==-1 || player[1]==-1 || player[2]==-1 || player[3]==-1 || player[4]==-1 || player[5]==-1 || player[6]==-1 || player[7]==-1 || player[8]==-1)
              break;
              
              int score[20]={0};

              int iid=2,guess=3,iid2=4,guess2=5;
              char buf0[1024];
              for(int i=0;i<10;i++)
              {  
                fscanf(f2,"%d%d",&iid,&guess);
                fscanf(t2,"%d%d",&iid2,&guess2);
                
                    if(abs(lucky-guess)<abs(lucky-guess2))
                    {
                      a=iid;
                      score[a]+=10;
                    }
                    else if(abs(lucky-guess)>abs(lucky-guess2))
                    {
                      a=iid2;
                      score[a]+=10;
                    }
                    else if((abs(lucky-guess)==abs(lucky-guess2)))
                    {
                        a=iid<iid2? iid:iid2;
                        score[a]+=10;
                    }
                //fprintf(stderr, "%d depth 0 pair %d %d %d %d winner: %d\n",i,iid,guess,iid2,guess2,a);
              }
              char buff[1024];
              sprintf(buff, "%d\n%d %d\n%d %d\n%d %d\n%d %d\n%d %d\n%d %d\n%d %d\n%d %d\n", id,player[0], score[player[0]], player[1], score[player[1]], player[2], score[player[2]], player[3], score[player[3]], player[4], score[player[4]], player[5], score[player[5]], player[6], score[player[6]], player[7], score[player[7]]);
              write(writesys, buff, strlen(buff));
              //fprintf(stderr, " final score: %s\n",buff);
           }
           int status;
           wait(&status);
           wait(&status);
           close(f2r[0]);
           close(t2r[0]);
           close(f2w[1]);
           close(t2w[1]);
           exit(0);
    }
    else if(depth == 1)//first child
    {      char buf[1024];
           fork2child(depth, lucky, id, 0, 0 , f2r , f2w, t2r, t2w);
           int player[4];
           int a;
           FILE  *f2 = fdopen(f2r[0], "r"),*t2 = fdopen(t2r[0], "r");
           while(1)
           {  
              scanf("%d %d %d %d",&player[0],&player[1],&player[2],&player[3]);
              //fprintf(stderr, "depth 1 player: %d %d %d %d\n", player[0], player[1], player[2], player[3]);
              sprintf(buf, "%d %d\n", player[0], player[1]);
              write(f2w[1], buf, strlen(buf));
              sprintf(buf, "%d %d\n", player[2], player[3]);
              write(t2w[1], buf, strlen(buf));
              
              if(player[0]==-1)
              break;

              int iid,guess,iid2,guess2;
              char buf1[1024];
              for(int i=0;i<10;i++)
              { 
                
                fscanf(f2,"%d%d",&iid,&guess);
                fscanf(t2,"%d%d",&iid2,&guess2);
                
                if(abs(lucky-guess)<abs(lucky-guess2))
                sprintf(buf,"%d %d\n", iid, guess);
                else if(abs(lucky-guess)>abs(lucky-guess2))
                sprintf(buf,"%d %d\n", iid2, guess2);
                else if(abs(lucky-guess)==abs(lucky-guess2))
                {
                      if(iid<iid2)
                      sprintf(buf,"%d %d\n", iid, guess);
                      else
                      sprintf(buf,"%d %d\n", iid2, guess2);
                }
                //fprintf(stderr, "%d depth 1 pair %d %d %d %d winner: %s\n",i,iid,guess,iid2,guess2,buf);

                   write(1, buf, strlen(buf));
                }
           }
           int status;
           wait(&status);
           wait(&status);
           close(f2r[0]);
           close(t2r[0]);
           close(f2w[1]);
           close(t2w[1]);
           exit(0);
    }
    else if(depth == 2)
    {
          
           char buf[1024];
           //fprintf(stderr, "cggggcc \n");
           int player[2];
           int a;
           while(1)
           {  
              scanf("%d%d",&player[0],&player[1]);

                //fprintf(stderr, "depth 2 player: %d %d\n", player[0], player[1]);
              if(player[0]==-1)
              break;
              
              fork2child(depth, lucky, id, player[0], player[1] , f2r , f2w, t2r, t2w);
              FILE *f2 = fdopen(f2r[0], "r"), *t2 = fdopen(t2r[0], "r");

              int iid,guess,iid2,guess2;
              char buf2[1024];
              for(int i=0;i<10;i++)
              {
                fscanf(f2,"%d%d",&iid,&guess);
                fscanf(t2,"%d%d",&iid2,&guess2);

                if(abs(lucky-guess)<abs(lucky-guess2))
                sprintf(buf,"%d %d\n", iid, guess);
                else if(abs(lucky-guess)>abs(lucky-guess2))
                sprintf(buf,"%d %d\n", iid2, guess2);
                else if(abs(lucky-guess)==abs(lucky-guess2))
                {
                    if(iid<iid2)
                    sprintf(buf,"%d %d\n", iid, guess);
                    else
                    sprintf(buf,"%d %d\n", iid2, guess2);
                }
                //fprintf(stderr, "%d depth 2 pair %d %d %d %d winner: %s",i,iid,guess,iid2,guess2,buf);
                write(1, buf, strlen(buf));
                fsync(1);
              }
              int status;
              wait(&status);
              wait(&status);
              close(f2r[0]);
              close(t2r[0]);
              close(f2w[1]);
              close(t2w[1]);
              
           }
           

           
    }
    return 0;
}

 

      

