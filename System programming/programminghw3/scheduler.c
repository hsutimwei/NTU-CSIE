#include "threadtools.h"

/*
1) You should state the signal you received by: printf('TSTP signal caught!\n') or printf('ALRM signal caught!\n')
2) If you receive SIGALRM, you should reset alarm() by timeslice argument passed in ./main
3) You should longjmp(SCHEDULER,1) once you're done.
*/
void sighandler(int signo){
	
	sigprocmask(SIG_SETMASK, &base_mask, NULL);
	if(signo==SIGALRM)
	{
		printf("ALRM signal caught!\n");
		alarm(timeslice);
	}
	else if(signo==SIGTSTP)
	{
		printf("TSTP signal caught!\n");
	}
	longjmp(SCHEDULER, 1);
}

/*
1) You are stronly adviced to make 
	setjmp(SCHEDULER) = 1 for ThreadYield() case
	setjmp(SCHEDULER) = 2 for ThreadExit() case
2) Please point the Current TCB_ptr to correct TCB_NODE
3) Please maintain the circular linked-list here
*/
void scheduler(){
	/* Please fill this code section. */
	int check=setjmp(SCHEDULER);
    
	if(check==0)//initial by main
	{
       Current = Head;
	   longjmp(Current->Environment,1);
	}
	else if(check==1) //ThreadYield
	{        
         Current = Current->Next;
	}
	else if(check==2)//ThreadExit
	{
         if(Current->Next==Current)
		  longjmp(MAIN,1);//執行完了
         else
		 {
			 Current->Next->Prev=Current->Prev;
			 Current->Prev->Next=Current->Next;
			 Current=Current->Next;
		 }
		 
	}
	

		longjmp(Current->Environment,1);

		
	
}