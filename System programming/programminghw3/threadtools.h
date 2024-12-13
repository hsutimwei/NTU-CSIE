#include <stdio.h>
#include <stdlib.h>
#include <setjmp.h>
#include <signal.h>
#include <unistd.h>

extern int timeslice, switchmode;

typedef struct TCB_NODE *TCB_ptr;
typedef struct TCB_NODE{
    jmp_buf  Environment;
    int      Thread_id;
    TCB_ptr  Next;
    TCB_ptr  Prev;
    int i, N;
    int w, x, y, z;
} TCB;

extern jmp_buf MAIN, SCHEDULER;
extern TCB_ptr Head;
extern TCB_ptr Current;
extern TCB_ptr Work;
extern sigset_t base_mask, waiting_mask, tstp_mask, alrm_mask;

void sighandler(int signo);
void scheduler();

// Call function in the argument that is passed in
#define ThreadCreate(function, thread_id, number)                                         \
{                                                                                         \
	/* Please fill this code section. */	                                              \
    function(thread_id,number);											                  \
}

// Build up TCB_NODE for each function, insert it into circular linked-list
#define ThreadInit(thread_id, number)                                                     \
{                                                                                         \
	/* Please fill this code section. */												  \
    if(Head==NULL)                                                                        \
    {                                                                                     \
         Head=(TCB_ptr)malloc(sizeof(TCB));                                               \
         Current=Head;                                                                    \
         Head->Thread_id=thread_id;                                                       \
         Head->Next=Head;                                                                 \
         Head->Prev=Head;                                                                 \
         Current=Head;                                                                    \
    }                                                                                     \
    else                                                                                  \
    {                                                                                     \
        Work=(TCB_ptr)malloc(sizeof(TCB));                                                \
        Work->Thread_id=thread_id;                                                        \
        Work->Prev=Current;                                                               \
        Work->Next=Current->Next;                                                         \
        Current->Next->Prev=Work;                                                         \
        Current->Next=Work;                                                               \
        Current=Work;                                                                     \
                                                                                          \
    }                                                                                     \
    Current->N=0;                                                                 \
    Current->z=number;                                                               \
    Current->i=0;                                                                         \
}

// Call this while a thread is terminated
#define ThreadExit()                                                                      \
{                                                                                         \
	/* Please fill this code section. */                                                  \
    longjmp(SCHEDULER,2);												                  \
}
//ThreadYield想法:task每做一次iteration就ThreadYield，然後跳到scheduler去排，再跳回來。
// Decided whether to "context switch" based on the switchmode argument passed in main.c
#define ThreadYield()                                                                     \
{                                                                                         \
	/* Please fill this code section. */												  \
    int env=setjmp(Current->Environment);                                          \
    if(env==0)                                                                            \
    {                                                                                     \
       if(switchmode==0)                                                                  \
       longjmp(SCHEDULER, 1);                                                             \
       else                                                                               \
       {                                                                                  \
            sigpending(&waiting_mask);                                                    \
            if(sigismember(&waiting_mask, SIGTSTP))                                       \
            {                                                                             \
                sigsuspend(&alrm_mask);                                                   \
            }                                                                             \
            else if(sigismember(&waiting_mask, SIGALRM))                                  \
            {                                                                             \
                sigsuspend(&tstp_mask);                                                   \
            }                                                                             \
       }                                                                                  \
    }                                                                                     \
}                                                                                         
