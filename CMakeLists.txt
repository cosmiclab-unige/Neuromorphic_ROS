cmake_minimum_required(VERSION 3.0.2)
project(main_pkg)


find_package(catkin REQUIRED COMPONENTS
  message_generation
  rospy
  std_msgs
  message_runtime
)

add_message_files(
  FILES
  SensorsData.msg
)


generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS message_runtime
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  scripts/ReadData.py
  scripts/PlotSpikes.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
