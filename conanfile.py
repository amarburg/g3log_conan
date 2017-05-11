from conans import ConanFile, CMake
import os

class G3logConan(ConanFile):
  name = "g3log"
  version = "master"
  url = "https://github.com/amarburg/g3log_conan.git"
  source_url = "https://github.com/KjellKod/g3log"
  commit = "master"
  settings = "os", "compiler", "build_type", "arch"
  options = {"shared": [True, False], "build_parallel": [True, False]}
  default_options = "shared=True", "build_parallel=True"

  def source(self):
    if not os.path.isdir('g3log'):
      self.run('git clone %s g3log' % self.source_url)
    else:
      self.run('cd g3log && git fetch origin')

    self.run('cd g3log && git checkout %s' % self.commit)

  def build(self):
    cmake = CMake(self.settings)

    cmake_opts = " -DBUILD_EXAMPLES:BOOL=False"
    # cmake_opts += " -DBUILD_TESTS:BOOL=False"
    # cmake_opts += " -DBUILD_SHARED_LIBS=True" if self.options.shared else ""

    if self.options.build_parallel:
      build_opts = "-- -j"

    # Explicitly disable RPATH on OSX
    if self.settings.os == "Macos":
      cmake_opts += " -DCMAKE_SKIP_RPATH:BOOL=ON"

    self.run('cmake "%s/g3log" %s %s' % (self.conanfile_directory, cmake.command_line, cmake_opts ))
    self.run('cmake --build . %s' % cmake.build_config)

  def package(self):
    self.copy("*.h",   src="g3log/src/", dst="include/")
    self.copy("*.hpp", src="include/", dst="include/")  ## The auto-generated generated_definitions.hpp appears in include/g3log, not with the "source" header files
    self.copy("*.hpp", src="g3log/src/", dst="include/")

    if self.options.shared:
      if self.settings.os == "Macos":
          self.copy(pattern="*.dylib", dst="lib", keep_path=False)
      else:
          self.copy(pattern="*.so*", dst="lib", keep_path=False)
    else:
        self.copy(pattern="*.a", dst="lib", keep_path=False)

  def package_info(self):
      self.cpp_info.libs = ["g3logger"]
