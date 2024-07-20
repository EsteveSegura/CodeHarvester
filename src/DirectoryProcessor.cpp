#include "DirectoryProcessor.h"

bool DirectoryProcessor::shouldProcess(const fs::path &path, const StringList &excludeDirs)
{
    return std::none_of(excludeDirs.begin(), excludeDirs.end(),
                        [&path](const auto &excludeDir)
                        { return path.string().find(excludeDir) != std::string::npos; });
}

void DirectoryProcessor::processDirectory(const fs::path &path, std::ofstream &output, const StringList &extensions,
                                          const StringList &excludeExtensions, const StringList &excludeDirs,
                                          const StringList &excludeFiles, std::string prefix,
                                          const PathList *relevantPaths)
{
    if (!shouldProcess(path, excludeDirs) && !relevantPaths)
    {
        return;
    }

    bool shouldShow = !relevantPaths;
    PathList subRelevantPaths;

    if (relevantPaths)
    {
        for (const auto &relevantPath : *relevantPaths)
        {
            if (fs::relative(relevantPath, path).string().find("..") == std::string::npos)
            {
                shouldShow = true;
                if (relevantPath != path)
                {
                    subRelevantPaths.push_back(relevantPath);
                }
            }
        }
    }

    if (shouldShow)
    {
        output << prefix << path.filename().string() << "/\n";
    }

    std::vector<fs::directory_entry> entries;
    for (const auto &entry : fs::directory_iterator(path))
    {
        if (!relevantPaths || std::find(relevantPaths->begin(), relevantPaths->end(), entry.path()) != relevantPaths->end() ||
            std::any_of(relevantPaths->begin(), relevantPaths->end(), [&entry](const fs::path &p)
                        { return fs::relative(p, entry.path()).string().find("..") == std::string::npos; }))
        {
            entries.push_back(entry);
        }
    }

    std::sort(entries.begin(), entries.end(),
              [](const fs::directory_entry &a, const fs::directory_entry &b)
              {
                  return a.path().filename() < b.path().filename();
              });

    for (const auto &entry : entries)
    {
        if (fs::is_directory(entry))
        {
            processDirectory(entry, output, extensions, excludeExtensions, excludeDirs, excludeFiles,
                             prefix + "  ", relevantPaths ? &subRelevantPaths : nullptr);
        }
        else if (fs::is_regular_file(entry) &&
                 (FileProcessor::shouldProcess(entry, extensions, excludeExtensions, excludeFiles) || relevantPaths))
        {
            output << prefix << "  " << entry.path().filename().string() << "\n";
        }
    }
}