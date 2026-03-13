[app]

# (str) Title of your application
title = Zo3rob Supermarket

# (str) Package name
package.name = zo3rob

# (str) Package domain (needed for android packaging)
package.domain = org.zarab

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (list) List of directory to exclude (let empty to exclude none)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using Python regular expressions
#source.exclude_regexes = (.*__pycache__.*|.*\.pyc|.*\.pyo)

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,arabic_reshaper,python-bidi,six,pyjnius

# (str) Custom source folders for requirements
# сад allow to include custom implementations of python package
# requirements.source.kivy = ../../kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (int) Android API to use
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
#android.ndk = 19b

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (list) Android white list
#android.whitelist =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (str) Android additional libraries
#android.add_libs_armeabi = lib/armeabi/libf77blas.so:lib/armeabi/liblapack.so

# (bool) Copy library instead of making a lib library link
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (list) Android entry point, default is to use start.py
#android.entrypoint = main.py

# (list) List of Java files to add to the android project (can be GSS)
#android.add_src =

# (list) Android AAR archives to add (currently ONLY worked with android.gradle_dependencies)
#android.add_aars =

# (list) Gradle dependencies to add
#android.gradle_dependencies =

# (list) Add java compile options
# android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# (list) Java classes to add as activities to the manifest.
#android.add_activities = com.example.ExampleActivity

# (str) OUYA Console category. Should be one of GAME or APP
#android.ouya.category = APP

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters =

# (str) launchMode to set for the main activity
#android.manifest.launch_mode = standard

# (list) Android additional modules to build (for example, sqlite3)
#android.add_modules = sqlite3

# (bool) Indicate whether the screen should stay on
#android.meta_data =

# (list) Android runtime permissions
#android.runtime_permissions =

# (str) Android library object
#android.library_path =

# (str) Android log direction (stdout, stderr or both)
#android.log_device = stdout

# (str) Android log file
#android.log_file =

# (str) Android log tag
#android.log_tag =

# (bool) use the log filter on logcat
#android.log_filter = 1

# (bool) indicate whether to build in a docker container
#android.use_docker = 0

# (list) inclusions for the debug/release build
#android.inclusions =

# (list) exclusions for the debug/release build
#android.exclusions =

# (list) list of additional files to include in the APK
#android.add_external_libs =

# (list) list of additional files to include in the AAB
#android.add_external_libs_aab =

# (list) list of assets to include in the APK
#android.add_assets =

# (list) list of assets to include in the AAB
#android.add_assets_aab =

# (str) path to the keystore for signing the APK
#android.keystore =

# (str) password for the keystore
#android.keystore_password =

# (str) key alias in the keystore
#android.keyalias =

# (str) password for the key alias
#android.keyalias_password =

# (bool) whether to build the APK as a release version
#android.release = 0

# (bool) whether to build the APK as a signed version
#android.signed = 0

# (str) the build tool to use
#android.build_tool = buildozer

# (str) the build command to use
#android.build_command = android debug

# (str) the log level to use
#android.log_level = 2

# (bool) use the lock file for the build
#android.use_lock = 1

# (str) the build directory
#android.build_dir = .buildozer

# (str) the output directory
#android.bin_dir = bin

[buildozer]

# (int) log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) display warning lines
warn_on_root = 1
