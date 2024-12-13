#include<stdio.h>
#include<stdlib.h>
#include <malloc.h>
#include <pthread.h>

int a,b,c;

int neighbours(char** life, int i, int j)
{
  int countn = 0;
  if(j-1 >= 0)
  {
     if (i-1 >= 0)
     {
        if (life[i-1][j-1] == 1)
          countn++;
     }

     if(life[i][j-1] == 1)
        countn++;
  
     if (i+1 < a)
     {
        if(life[i+1][j-1] == 1)
          countn++;
     }
  }
  

  if (i-1 >= 0)
  {
    if(life[i-1][j] == 1)
      countn++;
  }
  
  if (i+1 < a)
  {
    if(life[i+1][j] == 1)
      countn++;
  }
  
  if(j+1 < b)
  {
     if (i-1 >= 0)
     {
        if (life[i-1][j+1] == 1)
          countn++;
     }

     if(life[i][j+1] == 1)
        countn++;
  
     if (i+1 < b)
     {
        if(life[i+1][j+1] == 1)
          countn++;
     }

   }

  return countn;
}

int main(int argc, char ** argv)
{

  int threadnum=atoi(argv[2]);

  char input[100],output[100];

  strncpy(input,argv[3]+2,strlen(argv[3])-2);
  strncpy(output,argv[4]+2,strlen(argv[4])-2);

	FILE *fp = fopen(input, "r");

  fscanf(fp, "%d%d%d", &a, &b, &c);

  char (*life)[b] = (char(*)[b])malloc(a*b*sizeof(char));

  int (*count)[b] = (int(*)[b])malloc(a*b*sizeof(int));

  int d=0;
	while(!feof(fp))
	{
		fscanf(fp, "%s", life[d]);
    d++;
	}
	fclose(fp);

  for (int epoch = 0; epoch<c; epoch++)
  {
    for (int i = 0; i < a; i++)
    {
      for (int j = 0; j < b; j++)
      {
        count[i][j] = neighbours((char **)life,i,j);
      }
    }

    for (int i = 0; i < a; i++)
    {
      for (int j = 0; j < b; j++)
      {
        if ( life[i][j] >= 1 )
        {
          if (count[i][j] <= 1 || count[i][j] >=4)
            life[i][j] = 0;
        }
        else
          if (count[i][j] == 3)
            life[i][j] = 1;
      }
    }
    
  }
  FILE *fpo = fopen(output, "r");
  for (int i = 0; i < a; i++)
    {
      fprintf(fpo,"%s", life[i]);
    }

  return 0;
}

