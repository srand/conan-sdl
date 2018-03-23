from conans import ConanFile, CMake, tools


class SdlConan(ConanFile):
    name = "sdl"
    version = "2.0.8"
    license = "http://www.gzip.org/zlib/zlib_license.html"
    url = "http://github.com/srand/conan-sdl"
    description = """
Simple DirectMedia Layer is a cross-platform development library designed to provide low level access to audio, keyboard, mouse, joystick, and graphics hardware via OpenGL and Direct3D. It is used by video playback software, emulators, and popular games including Valve's award winning catalog and many Humble Bundle games. 

SDL officially supports Windows, Mac OS X, Linux, iOS, and Android. Support for other platforms may be found in the source code. 

SDL is written in C, works natively with C++, and there are bindings available for several other languages, including C# and Python. 
"""
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    build_requires = "cmake_installer/[>=2.8.11]@conan/stable"

    def source(self):
        tools.get("https://www.libsdl.org/release/SDL2-%s.zip" % self.version)

    def build(self):
        defs = {}        
        defs["SDL_SHARED"] = "ON" if self.options.shared else "OFF"
        defs["SDL_STATIC"] = "OFF" if self.options.shared else "ON"

        cmake = CMake(self)
        cmake.configure(source_folder="SDL2-%s" % self.version, defs=defs)
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="SDL2-%s/include" % self.version)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["SDL2", "SDL2main"] if self.options.shared else ["SDL2-2.0", "SDL2main"]
