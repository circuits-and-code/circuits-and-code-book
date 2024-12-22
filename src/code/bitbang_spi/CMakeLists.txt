cmake_minimum_required(VERSION 3.10)
project(Generic_Library LANGUAGES C)

# Automatically find all C source files in the current directory and subdirectories
file(GLOB_RECURSE SOURCES "*.c")

if(SOURCES)
    message(STATUS "Found source files: ${SOURCES}")
else()
    message(WARNING "No source files found!")
endif()


# Create the static library
add_library(project_lib STATIC ${SOURCES})

# Automatically set include directories based on directory structure
target_include_directories(project_lib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# Enable all warnings and treat them as errors
target_compile_options(project_lib PRIVATE
    -Wall        # Enable all standard warnings
    -Wextra      # Enable extra warnings
    -Wpedantic   # Enforce strict compliance
    -Werror      # Treat warnings as errors
)

# Optional: Add a test executable to validate the build
# It will look for main.c as a placeholder test
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/main.c")
    add_executable(test_app main.c)
    target_link_libraries(test_app PRIVATE project_lib)
endif()
