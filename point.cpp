#include <iostream>
#include <vector>

using namespace std;


void copy_fct(vector<int>& v) {
  
  std::cout << v << std::endl;
}

int main (int argc, char *argv[])
{
 
  vector<int> v{1,2,3,4};
  copy_fct(v);
  return 0;
}
