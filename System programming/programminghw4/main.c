#include<stdio.h>
#include<stdlib.h>
#include <malloc.h>
#include <string.h>
#include <pthread.h>
#include <signal.h>
int a,b,c,size,remind,threadnum;
char ** life;
int ** count;
pthread_barrier_t stop;
int neighbours(int i, int j)
{
  int countn = 0;
  if(j-1 >= 0)
  {
     if (i-1 >= 0)
     {
        if (life[i-1][j-1] == 'O')
          countn++;
     }

     if(life[i][j-1] == 'O')
        countn++;
  
     if (i+1 < a)
     {
        if(life[i+1][j-1] == 'O')
          countn++;
     }
  }
  

  if (i-1 >= 0)
  {
    if(life[i-1][j] == 'O')
      countn++;
  }
  
  if (i+1 < a)
  {
    if(life[i+1][j] == 'O')
      countn++;
  }
  
  if(j+1 < b)
  {
     if (i-1 >= 0)
     {
        if (life[i-1][j+1] == 'O')
          countn++;
     }

     if(life[i][j+1] == 'O')
        countn++;
  
     if (i+1 < a)
     {
        if(life[i+1][j+1] == 'O')
          countn++;
     }

   }

  return countn;
}
void play(int start, int end, int id)
{   
    int k=0;
    while(k < c)
    {   
        int turei,turej,check;
        for(int i=start;i<=end;i++)
        {
               turei=i/b;
               turej=i%b;
            count[turei][turej]=neighbours(turei,turej);
            //printf("thread %d: now i is %d and point is (%d,%d) and check is %d\n",id,i,turei,turej,count[turei][turej]);
        }
            
        pthread_barrier_wait(&stop);
        //修改life
        //printf("bbbb\n");
        for(int i=start;i<=end;i++)
        {    
            turei=i/b;
            turej=i%b;
           //printf("point (%d,%d) now is %c and check is %d\n",turei,turej,life[turei][turej],count[turei][turej]);
            if(count[turei][turej]==3 && life[turei][turej]=='.')
                life[turei][turej]='O';
            else if(count[turei][turej]<2 && life[turei][turej]=='O')
                life[turei][turej]='.';
            else if(count[turei][turej]>3 && life[turei][turej]=='O')
                life[turei][turej]='.';
           //printf(" and then point (%d,%d) is %c now\n",turei,turej,life[turei][turej]);
        }
        pthread_barrier_wait(&stop);
        k++;
    }
    pthread_exit(NULL);
}
void* prepare(void* arg)
{  //printf("aaaaa\n");
   int id = *(int *)arg;
   int start=size*id;
   int end=start+size-1;
   if(id==threadnum-1)
      end+=remind;
    //printf("thread %d: %d ~ %d\n",id,start,end);
    play(start,end,id);
}
void sighandler(int signo)
{	
	
}
int  main(int argc, char * argv[])
{
   
    threadnum=atoi(argv[2]);

    char input[100],output[100];
    memset(input,'\0',sizeof(input));
    memset(output,'\0',sizeof(output));
    strncpy(input,argv[3]+2,strlen(argv[3])-2);
    strncpy(output,argv[4]+2,strlen(argv[4])-2);
  
    FILE *fp = fopen(input, "r");
    
    fscanf(fp, "%d%d%d", &a, &b, &c);
    //printf("%d %d %d\n",a,b,c);
    //printf("%s\n",input);
    //printf("%s\n",output);
    life = (char **) malloc(a*sizeof(char *));
    for (int i=0; i<a; i++)
      life[i] = (char *) malloc(b*sizeof(char));

    count = (int **) malloc(a*sizeof(int *));
    for (int i=0; i<a; i++)
      count[i] = (int *) malloc(b*sizeof(int));

    int d=0;
    while(!feof(fp))//read file
    {
    	fscanf(fp, "%s", life[d]);
        d++;
    }
    fclose(fp);

    
    pthread_barrier_init(&stop, NULL, threadnum);

    size=a*b/threadnum;
    remind=a*b%threadnum;
    pthread_t threadid[threadnum];
    
    for(int i=0;i<threadnum;i++)
    {     
          int *j= malloc(sizeof(int));
          *j=i;
          pthread_create(&threadid[i], NULL, prepare, j);
    }
    for(int i=0;i<threadnum;i++)
    {
          pthread_join(threadid[i],NULL);
    }
   
   
	
    FILE *fpo = fopen(output, "w");
    
    for (int i = 0; i < a; i++)//output
    {
        
        fprintf(fpo,"%s",life[i]);
        if(i!=a-1)
        fprintf(fpo,"\n");
    }

    pthread_barrier_destroy(&stop);
	  fclose(fpo);
   }
