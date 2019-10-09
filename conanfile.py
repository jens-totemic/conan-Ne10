# -*- coding: utf-8 -*-
import os
from conans import ConanFile, CMake, tools


class PahocConan(ConanFile):
    name = "Ne10"
    version = "1.2.2-2018.11.15" # version number rarely changes, so add date
    #source_subfolder = "sources"
    scm = {
        "type": "git",
        #"subfolder": source_subfolder,
        "url": "https://github.com/projectNe10/Ne10.git",
        # latest commit, 2018.11.15 
        "revision": "1f059a764d0e1bc2481c0055c0e71538470baa83"
    }

    homepage = "https://github.com/projectNe10/Ne10"
    description = "An open optimized software library project for the ARM® Architecture."
    url = "https://github.com/jens-totemic/conan-Ne10"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "fPIC": [True, False]}
    default_options = {"shared": False,
                       "fPIC": True}
    generators = "cmake"
    exports = "LICENSE"
    exports_sources = ["01-build-c-only.patch"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    # def source(self):
    #     sha256 = "96efc8b5691dc0b6b0820617113ccfffa76153b274f80d5fa4768067bf08a1b1"
    #     tools.get("%s/archive/v%s.zip" % (self.homepage, self.version), sha256=sha256)
    #     os.rename("paho.mqtt.c-%s" % self.version, self._source_subfolder)

    # def requirements(self):
    #     if self.options.SSL:
    #         self.requires("OpenSSL/1.0.2s@conan/stable")

    def _configure_cmake(self):
        cmake = CMake(self)
        armOnly = self.settings.os == "Linux" and self.settings.arch.startswith("arm")
        cmake.definitions["GNULINUX_PLATFORM"] = True
        cmake.definitions["NE10_BUILD_ARM_ONLY"] = armOnly
        cmake.definitions["NE10_BUILD_SHARED"] = self.options.shared
        cmake.definitions["NE10_BUILD_STATIC"] = not self.options.shared
        cmake.configure()
        return cmake

    def build(self):
        tools.patch(patch_file="01-build-c-only.patch")
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs.append(os.path.join("include", "ne10"))

    # def package_info(self):
    
    #     if self.options.shared and self:
    #         # Python 3.7 reserves async as a keyword so we can't access variable with dot 
    #         if self.options.asynchronous:
    #             if self.options.SSL:
    #                 self.cpp_info.libs = ["paho-mqtt3as"]
    #             else:
    #                 self.cpp_info.libs = ["paho-mqtt3a"]
    #         else:
    #             if self.options.SSL:
    #                 self.cpp_info.libs = ["paho-mqtt3cs"]
    #             else:
    #                 self.cpp_info.libs = ["paho-mqtt3c"]
    #     else:
    #         if self.options.asynchronous:
    #             if self.options.SSL:
    #                 self.cpp_info.libs = ["paho-mqtt3as-static"]
    #             else:
    #                 self.cpp_info.libs = ["paho-mqtt3a-static"]
    #         else:
    #             if self.options.SSL:
    #                 self.cpp_info.libs = ["paho-mqtt3cs-static"]
    #             else:
    #                 self.cpp_info.libs = ["paho-mqtt3c-static"]

    #     if self.settings.os == "Windows":
    #         if not self.options.shared:
    #             self.cpp_info.libs.append("ws2_32")
    #             if self.settings.compiler == "gcc":
    #                 self.cpp_info.libs.extend(["wsock32", "uuid", "crypt32", "rpcrt4"])
    #     else:
    #         if self.settings.os == "Linux":
    #             self.cpp_info.libs.extend(["c", "dl", "pthread"])
    #         elif self.settings.os == "FreeBSD":
    #             self.cpp_info.libs.extend(["compat", "pthread"])
    #         else:
    #             self.cpp_info.libs.extend(["c", "pthread"])
