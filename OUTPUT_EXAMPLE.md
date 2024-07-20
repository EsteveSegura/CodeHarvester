# Project Structure

```plaintext
/project/
  src/
    main.cpp
    util.cpp
  include/
    util.h
  CMakeLists.txt
```

# File Contents

## /path/to/project/src/main.cpp

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
```

## /path/to/project/src/main.cpp <- Changes present in this file

```diff
diff --git a/src/main.cpp b/src/main.cpp
index e69de29..d95f3ad 100644
--- a/src/main.cpp
+++ b/src/main.cpp
@@ -1,4 +1,4 @@
 #include <iostream>
 
 int main() {
-    std::cout << "Hello, World!" << std::endl;
+    std::cout << "Hello, CodeHarvester!" << std::endl;
     return 0;
 }
```

## /path/to/project/src/util.cpp

```cpp
#include "util.h"

void doSomething() {
    // Implementation
}
```

## /path/to/project/include/util.h

```h
#pragma once

void doSomething();
```
