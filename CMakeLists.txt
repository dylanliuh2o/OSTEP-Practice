cmake_minimum_required(VERSION 3.10)

project(OSTEP-Practice)

find_package(Python3 REQUIRED COMPONENTS Interpreter)

message(STATUS "Python 3 executable: ${Python3_EXECUTABLE}")

# compile options
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(CMAKE_INSTALL_PREFIX "${CMAKE_SOURCE_DIR}/install" CACHE PATH "Install path prefix" FORCE)

# decide which chapters to be build
set(ENABLED_CHAPTERS
    chapter_01
    chapter_02
    chapter_03
    chapter_04
    chapter_05
)

# setting source directory
set(SRC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src)

# search chapter directories
file(GLOB CHAPTER_DIRS CONFIGURE_DEPENDS "${SRC_DIR}/*")
foreach(dir ${CHAPTER_DIRS})
    if(IS_DIRECTORY ${dir})
        get_filename_component(dirname ${dir} NAME)
        list(FIND ENABLED_CHAPTERS ${dirname} index)
        if(NOT index EQUAL -1)
            message(STATUS "Adding chapter: ${dirname}")
            add_subdirectory(${dir})
        else()
            message(STATUS "Skipping: ${dir}")
        endif()
    endif()
endforeach()

# ===============================
# auto generate VSCode launch.json
# ===============================
add_custom_target(update_launch_json ALL
    COMMAND ${CMAKE_COMMAND} -E echo "Updating launch.json..."
    COMMAND ${CMAKE_COMMAND} -E env PYTHONPATH=${CMAKE_SOURCE_DIR}
            ${Python3_EXECUTABLE} ${CMAKE_SOURCE_DIR}/scripts/gen_launch.py
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Generating VSCode launch.json for all executables"
)


