# decide which subdir to be build
set(ENABLED_SUBDIRS
    p3
)

# search sub-directories
file(GLOB CHILD_DIRS RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} *)
foreach(dir ${CHILD_DIRS})
    if(IS_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/${dir}")
        get_filename_component(dirname ${dir} NAME)
        list(FIND ENABLED_SUBDIRS ${dirname} index)
        if(NOT index EQUAL -1)
            message(STATUS "Adding subdir: ${dirname}")
            add_subdirectory(${dir})
        else()
            message(STATUS "Skipping: ${dir}")
        endif()
    endif()
endforeach()