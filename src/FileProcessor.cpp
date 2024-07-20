#include "FileProcessor.h"

bool FileProcessor::isBinaryFile(const fs::path &path)
{
    std::ifstream file(path, std::ios::binary);
    char buffer[1024];
    file.read(buffer, sizeof(buffer));
    std::streamsize readBytes = file.gcount();

    for (std::streamsize i = 0; i < readBytes; ++i)
    {
        if (static_cast<unsigned char>(buffer[i]) > 127)
        {
            return true;
        }
    }
    return false;
}

bool FileProcessor::isFileTooLarge(const fs::path &path, const std::uintmax_t maxSize)
{
    return fs::file_size(path) > maxSize;
}

bool FileProcessor::shouldProcess(const fs::path &path, const StringList &extensions,
                                  const StringList &excludeExtensions, const StringList &excludeFiles)
{
    std::string filename = path.filename().string();
    std::string extension = path.extension().string();

    if (std::find(excludeFiles.begin(), excludeFiles.end(), filename) != excludeFiles.end())
    {
        return false;
    }
    if (std::find(excludeExtensions.begin(), excludeExtensions.end(), extension) != excludeExtensions.end())
    {
        return false;
    }
    if (extensions.empty())
    {
        return true;
    }
    return std::find(extensions.begin(), extensions.end(), extension) != extensions.end();
}

void FileProcessor::processFile(const fs::path &path, const fs::path &rootDir, std::ofstream &output, bool unlimitedSize, bool allowBinaryFiles, bool isDiff)
{
    fs::path relativePath = fs::relative(path, rootDir);
    output << "## " << (rootDir / relativePath).string() << "\n\n";

    if (!unlimitedSize && isFileTooLarge(path))
    {
        output << "FILE_TOO_LARGE\n\n";
        return;
    }

    if (!allowBinaryFiles && isBinaryFile(path))
    {
        output << "BINARY_FILE\n\n";
        return;
    }

    std::string extension = path.extension().string();
    output << "```" << (extension.empty() ? "" : extension.substr(1)) << "\n";

    std::ifstream file(path);
    std::string line;
    while (std::getline(file, line))
    {
        output << line << "\n";
    }

    output << "```\n\n";

    if (isDiff)
    {
        std::string statusCommand = "git -C " + rootDir.string() + " status --porcelain " + relativePath.string();
        FILE* statusPipe = popen(statusCommand.c_str(), "r");
        if (!statusPipe)
        {
            output << "ERROR: Failed to run git status\n\n";
            return;
        }

        char statusBuffer[128];
        bool hasChanges = false;
        while (fgets(statusBuffer, sizeof(statusBuffer), statusPipe) != nullptr)
        {
            hasChanges = true;
            break;
        }
        pclose(statusPipe);

        if (hasChanges)
        {
            std::string diffCommand = "git -C " + rootDir.string() + " --no-pager diff " + relativePath.string();
            FILE* diffPipe = popen(diffCommand.c_str(), "r");
            if (!diffPipe)
            {
                output << "ERROR: Failed to run git diff\n\n";
                return;
            }

            output << "## " << (rootDir / relativePath).string() << " <- Changes present in this file\n\n";
            output << "```diff\n";
            char diffBuffer[128];
            while (fgets(diffBuffer, sizeof(diffBuffer), diffPipe) != nullptr)
            {
                output << diffBuffer;
            }
            pclose(diffPipe);
            output << "```\n\n";
        }
    }
}
