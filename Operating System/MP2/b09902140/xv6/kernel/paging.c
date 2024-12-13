#include "param.h"
#include "types.h"
#include "memlayout.h"
#include "riscv.h"
#include "spinlock.h"
#include "defs.h"
#include "proc.h"

/* NTU OS 2022 */
/* Page fault handler */
int handle_pgfault() {
  /* Find the address that caused the fault */
   struct proc *p = myproc();
   uint64 va=PGROUNDDOWN(r_stval());
   pte_t* pte=walk(p->pagetable,va,0);
   if(*pte & PTE_S)
   {
      uint64 blockno = PTE2BLOCKNO(*pte);
      char *mem = kalloc();
      memset(mem, 0, PGSIZE);
      if(mappages(p->pagetable, va, PGSIZE, (uint64)mem, PTE_U | PTE_R | PTE_W | PTE_X) != 0){
          kfree(mem);
          return 0;
      }
      begin_op();
      read_page_from_disk(ROOTDEV, (char* )mem, blockno);
      bfree_page(ROOTDEV,blockno);
      *pte = PA2PTE(mem) | PTE_FLAGS(*pte);
      end_op();
    }
    else
    {
      struct proc *p = myproc();
      char *mem = kalloc();
      memset(mem, 0, PGSIZE);
      if(mappages(p->pagetable, va, PGSIZE, (uint64)mem, PTE_U | PTE_R | PTE_W | PTE_X) != 0){
          kfree(mem);
          return 0;
      }
    }
    return 1;
}
