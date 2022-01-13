#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TRUE 1
#define FALSE 0
typedef int BOOL;

/* Program to illustrate insertion into, and deletion from a linked list
 * using triple ref technique.
 *
 * Note that the "tracer" has a content type of "ref ref THING" or "THING **",
 * which means that the memory location of "tracer" itself is  one "ref" higher
 * i.e.  "ref ref ref THING" or "***THING" in C.
 *
 * tracer is used to locate a place in the list. And, by using casts, to singly
 * or doubly dereference it, one can inspect the contents of either the current
 * element or the next element along.
 *
 * The nice part is tthat although the insertThing and removeThing functions
 * using this technique will generally be handling something in the middle of a
 * list, but the functions are also robust against the special cases:
 *
 * 1) inserting/deleting to/from a null list
 * 2) inserting/deleting to/from a single-member list
 * 3) inserting/deleting  at the end of a list
 * 4) inserting/deleting at the front of a list
 *
 * All of the above place with no need for additional "special case" coding. The
 * timely detection of NULL and the updating (if needed) of the pointer to the
 * start of the list happen quite automatically.
 *
 * Use is made, in the functions below, of the commonplace C shorthand of "while
 * (*tracer)" rather than the more general "while (*tracer != NULL)". But do be
 * clear that this short-cut relies on boolean values being represented as 0 and
 * 1 and the NULL pointer as 0. It's possible to envisage exotic C
 * implementations where this might not be the case.
 *
 * NOTE: this is a tutorial. The insertion and deletion functions have been
 * deliberately constructed so as to deliver "void". This is to illustrate that
 * they do not need to deliver a formal THING * result for the purpose of
 * updating the list head.
 *
 * Instead, the content of the incoming formal parameter called "head" points at
 * the global variable "start" gets updated, automatically and correctly, in all
 * special cases where "insert at front of the list" takes place.
 *
 * So, it is not necessary for the functions to deliver back a traditional
 * THING* pointer to the new list head -- to enable update to be done manually
 * in a separate operation. However it is easy to alter the result, if this is
 * required for some reason. The "return" statements in these procedures would
 * then need to be replaced by "return *head" */

typedef struct _thing {

  char *item;
  struct _thing *next;
} THING;

THING *start = NULL;

// create new list element of type THING from the supplied text string

THING *newElement(char *text) {

  THING *newP;
  newP = (THING *)malloc(sizeof(THING));
  newP->item = (char *)malloc(strlen(text) + 1);
  strcpy(newP->item, text);
  newP->next = NULL;

  return newP;
}

// Inset a new element into a singly-linked list
// NOTE: Duplicate entries are nto checked for

void insertThing(THING **head, THING *newP) {

  THING **tracer = head;

  while ((*tracer) && strcmp((*tracer)->item, newP->item) < 1) {

    tracer = &(*tracer)->next;
  }

  newP->next = *tracer;
  *tracer = newP;
}

// Delete first element on list whose item field matches the given text
// NOTE: delete requests for elements not in the list are silently ignored

void removeThing(THING **head, char *text) {

  BOOL present = FALSE;
  THING *old;
  THING **tracer = head;

  while ((*tracer) && !(present = (strcmp(text, (*tracer)->item) == 0))) {

    tracer = &(*tracer)->next;

    if (present) {

      old = *tracer;
      *tracer = (*tracer)->next;
      free(old->item); // free off space used by text string
      free(old);       // free up remainder of list element
    }
  }
}

void printList(THING **head) {

  THING **tracer = head;
  while (*tracer) {

    printf("%s \n", (*tracer)->item);
    tracer = &(*tracer)->next;
  }
}

int main(int argc, char *argv[]) {
  insertThing(&start, newElement("Chips"));
  insertThing(&start, newElement("Wine"));
  insertThing(&start, newElement("Burgers"));
  insertThing(&start, newElement("Beer"));
  insertThing(&start, newElement("Pizza"));
  insertThing(&start, newElement("Zucchini"));
  insertThing(&start, newElement("Burgers"));
  insertThing(&start, newElement("Slaw"));

  printf("\nINITIAL LIST\n");
  printList(&start);

  removeThing(&start, "Pizza");
  removeThing(&start, "Zucchini");
  removeThing(&start, "Burgers");
  
  printf("\nALTERED LIST\n");
  printList(&start);
  return 0;
}
