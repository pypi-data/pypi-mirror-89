include_directories(${openfst_SOURCE_DIR}/src/include)
pybind11_add_module(_kaldilm kaldilm.cc)
target_link_libraries(_kaldilm PRIVATE kaldilm_core)
set_target_properties(_kaldilm PROPERTIES BUILD_RPATH_USE_ORIGIN TRUE)
