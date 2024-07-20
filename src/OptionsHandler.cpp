#include "OptionsHandler.h"

po::variables_map OptionsHandler::parseOptions(int argc, char *argv[])
{
    po::options_description desc("Allowed options");
    desc.add_options()
        ("help,h", "produce help message")
        ("directory,d", po::value<std::string>()->required(), "root directory")
        ("list-files", po::value<StringList>()->multitoken(), "list of specific files to process (relative to root directory)")
        ("extensions,e", po::value<StringList>()->multitoken(), "file extensions to include (if not specified, all files are included)")
        ("exclude-extensions,E", po::value<StringList>()->multitoken(), "file extensions to exclude (takes priority over --extensions)")
        ("exclude-dirs,x", po::value<StringList>()->multitoken(), "directories to exclude")
        ("exclude-files,f", po::value<StringList>()->multitoken(), "files to exclude")
        ("unlimited", "process files of any size")
        ("allow-binary-files", "allow binary files to be processed")
        ("diff", "print all files diff (if available)")
        ("output,o", po::value<std::string>()->default_value("output.md"), "output file");

    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);

    if (vm.count("help"))
    {
        std::cout << desc << "\n";
        exit(0);
    }

    po::notify(vm);

    if (vm.count("list-files"))
    {
        if (vm.count("extensions") || vm.count("exclude-extensions") ||
            vm.count("exclude-dirs") || vm.count("exclude-files"))
        {
            throw po::error("--list-files cannot be used with other file selection options");
        }
    }

    if (vm.count("diff"))
    {
        #ifdef _WIN32
        if (system("git --version > NUL 2>&1") != 0)
        #else
        if (system("git --version > /dev/null 2>&1") != 0)
        #endif
        {
            throw po::error("Git is required for --diff option.");
        }
    }

    return vm;
}