cmake_minimum_required(VERSION 3.20)
project(TaskMgr_dbApi_ LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Drogon CONFIG REQUIRED)
find_package(libpqxx CONFIG REQUIRED)

add_executable(${PROJECT_NAME}
   TaskMgr_dbApi_/TaskMgr_dbApi_.cpp    
)

target_link_libraries(${PROJECT_NAME} PRIVATE
    Drogon::Drogon
    libpqxx::pqxx
)

if (MSVC)
    target_compile_options(${PROJECT_NAME} PRIVATE /W4 /permissive-)
endif()