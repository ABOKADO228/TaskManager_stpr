# CMakeList.txt: проект CMake для TaskMgr_dbApi_; включите исходный код и определения,
# укажите здесь логику для конкретного проекта.
#

# Добавьте источник в исполняемый файл этого проекта.
add_executable (TaskMgr_dbApi_ "TaskMgr_dbApi_.cpp" "TaskMgr_dbApi_.h")

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET TaskMgr_dbApi_ PROPERTY CXX_STANDARD 20)
endif()

# TODO: Добавьте тесты и целевые объекты, если это необходимо.
