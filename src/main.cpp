#include "CommonIncludes.h"
#include "OptionsHandler.h"
#include "CodeHarvester.h"

int main(int argc, char* argv[]) {
    try {
        auto vm = OptionsHandler::parseOptions(argc, argv);
        CodeHarvester harvester(vm);
        harvester.run();
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
        return 1;
    }
    return 0;
}