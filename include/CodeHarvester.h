#pragma once

#include "CommonIncludes.h"
#include "FileProcessor.h"
#include "DirectoryProcessor.h"

class CodeHarvester {
private:
    fs::path rootDir;
    StringList extensions;
    StringList excludeExtensions;
    StringList excludeDirs;
    StringList excludeFiles;
    StringList listFiles;
    fs::path outputFile;
    bool isListFilesMode;
    bool unlimitedSize;
    bool allowBinaryFiles;
    bool isDiff;

    std::ofstream output;

    void processListFilesMode();
    void processNormalMode();

public:
    CodeHarvester(const po::variables_map& vm);
    void run();
};