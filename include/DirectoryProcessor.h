#pragma once

#include "CommonIncludes.h"
#include "FileProcessor.h"

class DirectoryProcessor {
public:
    static bool shouldProcess(const fs::path& path, const StringList& excludeDirs);
    static void processDirectory(const fs::path& path, std::ofstream& output, const StringList& extensions, 
                                 const StringList& excludeExtensions, const StringList& excludeDirs, 
                                 const StringList& excludeFiles, std::string prefix = "", 
                                 const PathList* relevantPaths = nullptr);
};