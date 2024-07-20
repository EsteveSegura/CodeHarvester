#include "CodeHarvester.h"

CodeHarvester::CodeHarvester(const po::variables_map &vm)
    : rootDir(vm["directory"].as<std::string>()),
      outputFile(vm["output"].as<std::string>()),
      isListFilesMode(vm.count("list-files") > 0),
      unlimitedSize(vm.count("unlimited") > 0),
      allowBinaryFiles(vm.count("allow-binary-files") > 0)
{
    isDiff = false;
    
    if (isListFilesMode)
    {
        listFiles = vm["list-files"].as<StringList>();
        if (vm.count("diff"))
            isDiff = true;
    }
    else
    {
        if (vm.count("extensions"))
            extensions = vm["extensions"].as<StringList>();
        if (vm.count("exclude-extensions"))
            excludeExtensions = vm["exclude-extensions"].as<StringList>();
        if (vm.count("exclude-dirs"))
            excludeDirs = vm["exclude-dirs"].as<StringList>();
        if (vm.count("exclude-files"))
            excludeFiles = vm["exclude-files"].as<StringList>();
        if (vm.count("diff"))
            isDiff = true;
    }
}

void CodeHarvester::run()
{
    output.open(outputFile);
    if (!output.is_open())
    {
        std::cerr << "Failed to open output file." << std::endl;
        return;
    }

    output << "# Project Structure\n\n";

    if (isListFilesMode)
    {
        processListFilesMode();
    }
    else
    {
        processNormalMode();
    }

    output.close();
}

void CodeHarvester::processListFilesMode()
{
    PathList relevantPaths;
    for (const auto &relativeFilePath : listFiles)
    {
        fs::path fullPath = fs::absolute(fs::path(rootDir) / relativeFilePath).lexically_normal();
        if (fs::exists(fullPath) && fs::is_regular_file(fullPath))
        {
            relevantPaths.push_back(fullPath);
        }
    }
    DirectoryProcessor::processDirectory(rootDir, output, extensions, excludeExtensions,
                                         excludeDirs, excludeFiles, "", &relevantPaths);

    output << "\n# File Contents\n\n";

    for (const auto &relativeFilePath : listFiles)
    {
        fs::path fullPath = fs::absolute(fs::path(rootDir) / relativeFilePath).lexically_normal();
        if (fs::exists(fullPath) && fs::is_regular_file(fullPath))
        {
            FileProcessor::processFile(fullPath, rootDir, output, unlimitedSize, allowBinaryFiles, isDiff);
        }
        else
        {
            output << "## Error: File not found or not a regular file: " << fullPath.string() << "\n\n";
        }
    }
}

void CodeHarvester::processNormalMode()
{
    DirectoryProcessor::processDirectory(rootDir, output, extensions, excludeExtensions, excludeDirs, excludeFiles);

    output << "\n# File Contents\n\n";

    for (const auto &entry : fs::recursive_directory_iterator(rootDir))
    {
        if (fs::is_regular_file(entry) &&
            FileProcessor::shouldProcess(entry, extensions, excludeExtensions, excludeFiles) &&
            DirectoryProcessor::shouldProcess(entry.path().parent_path(), excludeDirs))
        {
            FileProcessor::processFile(entry, rootDir, output, unlimitedSize, allowBinaryFiles, isDiff);
        }
    }
}