#pragma once

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <filesystem>
#include <algorithm>
#include <boost/program_options.hpp>

namespace fs = std::filesystem;
namespace po = boost::program_options;

using PathList = std::vector<fs::path>;
using StringList = std::vector<std::string>;