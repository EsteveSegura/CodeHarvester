#pragma once

#include "CommonIncludes.h"

class FileProcessor {
public:
    static bool isBinaryFile(const fs::path& path);
    static bool isFileTooLarge(const fs::path& path, const std::uintmax_t maxSize = 10 * 1024 * 1024);
    static bool shouldProcess(const fs::path& path, const StringList& extensions, 
                              const StringList& excludeExtensions, const StringList& excludeFiles);
    static void processFile(const fs::path& path, const fs::path& rootDir, std::ofstream& output, bool unlimitedSize, bool allowBinaryFiles, bool isDiff);
};