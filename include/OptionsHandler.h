#pragma once

#include "CommonIncludes.h"

class OptionsHandler {
public:
    static po::variables_map parseOptions(int argc, char* argv[]);
};