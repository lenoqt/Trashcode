#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TRUE 1
#define FALSE 0
typedef int BOOL;

/* a set of routines to illustrate insertion into, and deletion from a linked
 * list using 'traditional' single-level pointer techniques. The routines for
 * deleting a list element, and for inserting at the fron of a list are
 * adapted from Kernighan and Pike's "The Practice of Programming" pp.46 et
 * seq. (Addison-Wesley 1999). The elements of the list are of type THING
 * where each THING is a structure in which the 'item' field holds a
 * string and the 'next' field holds a pointer to the next THING on the list.
 *
 * The techniques for adding a THING before the start of a list, or after the
 * end of a list, are two special cases that are straightforward enough.
 * However if the list elements are to be kept ordered alphabetically (say)
 * the insertion of a new element needs great care to ensure that the
 * NULL end-of-list marker does not get dereferenced.
 *
 * In summary the routines should be robust against:
 *
 * 1) inserting/deleting to/from an empty list
 * 2) inserting/deleting to/from a single-element list
 * 3) inserting/deleting at the end of a list
 * 4) inserting/deleting at the front of a list - with updating of the
 * pointer to the list head
 *
                    +-----+-----+          +-----+-----+          +-----+-----+
                    |     |     |          |     |     |          |     |     |
                    |BEER |NEXT +----+     |CHIPS|NEXT +----+     |WINE |NULL |
+--+-----+--+       +--+--+--+--+    |     +--+--+--+--+    |     +--+--+--+--+
|++|START|++|       |++|THING|++|    +---->+++|THING|++|    +---->+++|THING|++|
+--+--+--+--+       +--+--^--+--+          +--+-----+--+          +--+-----+--+
      |                   |
      +-------------------+
  * The general routine "addMiddle", supplied below, is general purpose but
  * it calls on "addFront" and "addEnd" in specific special cases. Note
  * carefully that it does allow for duplicate list elements.
  * TODO: Exercise -> modify addMiddle so that this duplication is NOT allowed.
*/

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

// delElement: remove from list the first instance of an element
// containing a given text string
// NOTE: delete requests for elements not in the list are silently ignored
THING *delElement(THING *head, char *text) {
  THING *p, *prev;
  prev = NULL;
  for (p = head; p != NULL; p = p->next) {
    if (strcmp(text, p->item) == 0) {
      if (prev == NULL)
        head = p->next;
      else
        prev->next = p->next;
      free(p->item); // free off the the string field
      free(p);       // remove rest of THING
      return head;
    }
    prev = p;
  }
}

/* addFront: add new THING to front of list
 * example usage: start = (addFront(start, newElement("burgers"))); */

THING *addFront(THING *head, THING *newP) {
  newP->next = head;
  return newP;
}

/* addEnd: add new THING to the end of a list
 * usage example: start = (addEnd(start, newElement("wine"))); */

THING *addEnd(THING *head, THING *newP) {
  THING *p2;
  if (head == NULL)
    return newP;
  // now find the end of list
  for (p2 = head; p2->next != NULL; p2 = p2->next)
    ;
  p2->next = newP;
  return head;
}

// addMiddle: add element into middle of a list of THINGs based on alphabetical
// order of the 'item' strings withing the THING structures

THING *addMiddle(THING *head, THING *newP) {
  BOOL found = FALSE;
  THING *p1, *p2;
  if (head == NULL) { // special case
    printf("Initial list was NULL\n");
    head = addFront(head, newP);
    return head;
  }
  // Main loop. Use p2 to remember previous p1

  p2 = p1 = head;
  while (!found) {

    if (found == strcmp(p1->item, newP->item) >= 1) {
      if (p1 == head) {
        printf("Adding at head\n");
        head = addFront(head, newP);
        return (head);
      } else { // general case - insert the item

        printf("General case entered\n");
        p2->next = newP;
        newP->next = p1;
        return head;
      }
    }
    // match not found before end of list so insert at end
    if (p1->next == NULL) {
      head = addEnd(head, newP);
      return (head);
    }
    // go round while loop one more time
    p2 = p1;
    p1 = p1->next;
  } // end of while
}

void printList(THING **head) {
  THING **tracer = head;
  while ((*tracer) != NULL) {
    printf("%s \n", (*tracer)->item);
    tracer = &(*tracer)->next;
  }
}

int main(int argc, char *argv[]) {
  start = addMiddle(start, newElement("BEER"));
  start = addMiddle(start, newElement("WINE"));
  printf("\nINITIAL LIST\n");
  printList(&start);
  delElement(start, "WINE");
  printf("\nALTERED LIST\n");
  printList(&start);
  return 0;
}
