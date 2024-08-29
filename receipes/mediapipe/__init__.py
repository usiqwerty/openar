from pythonforandroid.recipe import NDKRecipe


class Mediapipe(NDKRecipe):
    version = '0.10.13'
    url = 'https://github.com/google/mediapipe/archive/v{version}.zip'
    depends = ['python3', 'setuptools']
    call_hostpython_via_targetpython = False
    install_in_hostpython = False
    build_cmd: list
    generated_libraries = ['_framework_bindings.so']
    # build_cmd = [
    #     'bazel',
    #     'build',
    #     '--compilation_mode=opt',
    #     '--copt=-DNDEBUG',
    #     '--action_env=PYTHON_BIN_PATH=/mnt/d/AR_headset/.buildozer/android/platform/build-armeabi-v7a/build/other_builds/hostpython3/desktop/hostpython3/native-build/python3',
    #     '//mediapipe/python:_framework_bindings.so',
    #     '--define=MEDIAPIPE_DISABLE_GPU=1',
    #     '--define=OPENCV=source'
    # ]
    # def get_recipe_env(self, arch):
    #     env = super().get_recipe_env(arch)
    #     env['ANDROID_SDK_HOME'] = '/path/to/your/android/sdk'
    #     env['ANDROID_NDK_HOME'] = '/path/to/your/android/ndk'
    #     env['BAZEL_DIR'] = '/path/to/your/bazel'
    #     return env


recipe = Mediapipe()
