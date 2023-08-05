#include <string>
#include <exception>
#include "Geoid.hpp"

extern "C" void geoid_height(double *out, double lat, double lon)
{
    GeographicLib::Geoid egm96("egm96-15");
    *out = egm96(lat, lon);
}
