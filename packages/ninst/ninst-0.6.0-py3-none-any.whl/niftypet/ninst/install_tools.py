"""
Install tools for NiftyPET including:
* NiftyReg
* dcm2niix
"""
import glob
import logging
import multiprocessing
import os
import platform
import re
import shutil
import sys
from subprocess import PIPE, CalledProcessError, check_output, run
from textwrap import dedent

if os.getenv("DISPLAY", False):
    from functools import wraps
    from tkinter import Tk
    from tkinter.filedialog import askdirectory as ask

    @wraps(ask)
    def askdirectory(*args, **kwargs):
        Tk().withdraw()
        res = ask(*args, **kwargs)
        Tk().destroy()
        return res


else:

    def askdirectory(title="Folder: ", initialdir=None, name=""):
        """
        decreasing precedence: os.environ[name], raw_input, initialdir

        Args:
          initialdir (str):  default: ~
        """
        if initialdir is None:
            initialdir = os.path.expanduser("~")
        path = os.environ.get(name, None)
        if path is None:
            path = input(title)
        if path == "":
            return initialdir
        return path


from . import cudasetup as cs

log = logging.getLogger(__name__)

# NiftyReg
repo_reg = "https://github.com/KCL-BMEIS/niftyreg"
# repo_reg = 'https://cmiclab.cs.ucl.ac.uk/mmodat/niftyreg.git'
# 'git://git.code.sf.net/p/niftyreg/git'
sha1_reg = "731a565bd42ca97ff5968adb1c06133ea72f0856"
# 'f673b7837c0824f55dedb1534b32b55bf68a2823'
# '6bf84b492050a4b9a93431209babeab9bc8f14da'
# '62af1ca6777379316669b6934889c19863eaa708'
reg_ver = "1.5.61"

# dcm2niix
repo_dcm = "https://github.com/rordenlab/dcm2niix"
http_dcm_lin = repo_dcm + "/releases/download/v1.0.20200331/dcm2niix_lnx.zip"
# http_dcm_lin = repo_dcm + '/releases/download/v1.0.20190902/dcm2niix_lnx.zip'
http_dcm_win = repo_dcm + "/releases/download/v1.0.20200331/dcm2niix_win.zip"
# repo_dcm + '/releases/download/v1.0.20190902/dcm2niix_win.zip'
http_dcm_mac = repo_dcm + "/releases/download/v1.0.20200331/dcm2niix_mac.zip"
# repo_dcm + '/releases/download/v1.0.20190902/dcm2niix_mac.zip'
sha1_dcm = "485c387c93bbca3b29b93403dfde211c4bc39af6"
# 'f54be46667fce7994d2062e2623d12253c1bd968'
dcm_ver = "v1.0.20200331"  # 'v1.0.20190902'
# PREVIOUS WORKING:
# http_dcm_lin =  repo_dcm + '/releases/download/v1.0.20180622/'
# 'dcm2niix_27-Jun-2018_lnx.zip'
# http_dcm_win = repo_dcm + '/releases/download/v1.0.20180622/'
# 'dcm2niix_27-Jun-2018_win.zip'
# sha1_dcm =  '4b641113273d86ad73123816993092fc643ac62f'
# dcm_ver = '1.0.20180622'

# source and build folder names
dirsrc = "_src"
dirbld = "_bld"

# number of threads
ncpu = multiprocessing.cpu_count()

LOG_FORMAT = "%(levelname)s:%(asctime)s:%(name)s:%(funcName)s\n> %(message)s"


class LogHandler(logging.StreamHandler):
    """Custom formatting"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fmt = logging.Formatter(LOG_FORMAT)
        self.setFormatter(fmt)


def query_yesno(question):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    prompt = " [Y/n]: "
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()

        if choice == "":
            return True
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def check_platform():
    if not platform.system() in ["Windows", "Darwin", "Linux"]:
        log.error(
            dedent(
                f"""\
                the operating system is not supported: {platform.system()}
                only Linux, Windows and macOS are supported."""
            )
        )
        raise SystemError("unknown operating system (OS).")


def int_or_str(x):
    try:
        return int(x)
    except ValueError:
        return x


def get_version(bin, required=1, errmsg=""):
    try:
        ver = check_output([bin, "--version"]).decode("U8")
    except (CalledProcessError, FileNotFoundError):
        if required > 1:
            log.error(errmsg or f"{bin} not found")
        if required > 2:
            raise
        return False
    else:
        try:
            ver = re.findall(r"\d+\.\d[-\d.\w]*", ver, flags=re.M)[-1]
        except Exception:
            log.warn(f"could not parse {bin} --version:\n{ver}")
            return True
        return tuple(map(int_or_str, re.split("[.-]", ver)))


def check_depends(git=1, cuda=1, cmake=1, ninja=1, **kwargs):
    """
    Args:
      **kwargs: values(int):
        0: skip check
        1: check, no warn if not found
        2: required, warn if not found
        3: required, error if not found

    Returns:
      kwargs: values(truthy):
        False: not found
        True: found
        tuple: version numbers
    """
    outdct = {
        k: v
        for k, v in {
            "git": git,
            "cuda": cuda,
            "cmake": cmake,
            "ninja": ninja,
            **kwargs,
        }.items()
        if v
    }
    log.info(f"checking if [{'], ['.join(outdct)}] are installed...")

    if "cuda" in outdct:
        outdct["cuda"] = get_version(
            "nvcc", outdct["cuda"], "CUDA (nvcc) does not seem to be installed!"
        )
    if "nvcc" in outdct:
        outdct["nvcc"] = get_version(
            "nvcc", outdct["nvcc"], "CUDA (nvcc) does not seem to be installed!"
        )
    if "git" in outdct:
        outdct["git"] = get_version(
            "git",
            outdct["git"],
            (
                "git does not seem to be installed;"
                " get it from: https://git-scm.com/download"
            ),
        )
    if "cmake" in outdct:
        outdct["cmake"] = get_version(
            "cmake",
            outdct["cmake"],
            ("cmake does not seem to be installed; try conda/pip install cmake"),
        )
    if "ninja" in outdct:
        outdct["ninja"] = get_version(
            "ninja",
            outdct["ninja"],
            ("ninja does not seem to be installed; try conda/pip install ninja"),
        )

    for bin in set(outdct) - {"cuda", "nvcc", "git", "cmake", "ninja"}:
        # for p in os.getenv("PATH").split(os.path.pathsep):
        #     if os.path.isfile(os.path.join(p, bin)):
        #         outdct[bin] = True
        #         break
        # else:
        #     outdct[bin] = False
        outdct[bin] = get_version(bin, outdct[bin])

    return outdct


def check_version(Cnt, chcklst=None):
    """
    Check version and existence of all third-party software and input data.
    Output a dictionary with bool type of the requested bits in 'chcklst'.

    Args:
      chcklst (list): default: ["RESPATH", "REGPATH", "DCM2NIIX", "HMUDIR"]
    """
    if chcklst is None:
        chcklst = ["RESPATH", "REGPATH", "DCM2NIIX", "HMUDIR"]

    # at start, assume that nothing is present yet
    output = {}
    for itm in chcklst:
        output[itm] = False

    # niftyreg reg_resample first
    if "RESPATH" in chcklst and "RESPATH" in Cnt:
        try:
            p = run([Cnt["RESPATH"], "--version"], stdout=PIPE)
            out = p.stdout.decode("utf-8")
            if reg_ver in out:
                output["RESPATH"] = True
        except OSError:
            log.error("NiftyReg (reg_resample) either is NOT installed or is corrupt.")

    # niftyreg reg_aladin
    if "REGPATH" in chcklst and "REGPATH" in Cnt:
        try:
            p = run([Cnt["REGPATH"], "--version"], stdout=PIPE)
            out = p.stdout.decode("utf-8")
            if reg_ver in out:
                output["REGPATH"] = True
        except OSError:
            log.error("NiftyReg (reg_aladin) either is NOT installed or is corrupt.")

    # dcm2niix
    if "DCM2NIIX" in chcklst and "DCM2NIIX" in Cnt:
        try:
            p = run([Cnt["DCM2NIIX"], "-h"], stdout=PIPE)
            out = p.stdout.decode("utf-8")
            ver_str = re.search(r"(?<=dcm2niiX version v)\d{1,2}.\d{1,2}.\d*", out)
            if ver_str and dcm_ver in ver_str.group(0):
                output["DCM2NIIX"] = True
        except OSError:
            log.error("dcm2niix either is NOT installed or is corrupt.")

    # hdw mu-map list
    if "HMUDIR" in chcklst and "HMUDIR" in Cnt:
        for hi in Cnt["HMULIST"]:
            if os.path.isfile(os.path.join(Cnt["HMUDIR"], hi)):
                output["HMUDIR"] = True
            else:
                output["HMUDIR"] = False
                break

    return output


def download_dcm2niix(Cnt, path):
    log.info(
        dedent(
            """\
        ==============================================================
        dcm2niix will be installed directly from:
        https://github.com/rordenlab/dcm2niix/releases
        =============================================================="""
        )
    )

    # -create the installation folder
    if not os.path.isdir(path):
        os.mkdir(path)
    binpath = os.path.join(path, "bin")
    if not os.path.isdir(binpath):
        os.mkdir(binpath)

    import urllib.error
    import urllib.parse
    import urllib.request
    import zipfile

    http_dcm = {"Windows": http_dcm_win, "Linux": http_dcm_lin, "Darwin": http_dcm_mac}
    urllib.request.urlretrieve(
        http_dcm[platform.system()], os.path.join(path, "dcm2niix.zip")
    )

    zipf = zipfile.ZipFile(os.path.join(path, "dcm2niix.zip"), "r")
    zipf.extractall(os.path.join(path, "bin"))
    zipf.close()
    Cnt["DCM2NIIX"] = glob.glob(os.path.join(os.path.join(path, "bin"), "dcm2niix*"))[0]
    # ensure the permissions are given to the executable
    os.chmod(Cnt["DCM2NIIX"], 755)
    # update the resources.py file in ~/.niftypet
    Cnt = update_resources(Cnt)
    return Cnt


def install_tool(app, Cnt):
    """
    Install the requested software from the git 'repo'
    and check out the version given by 'sha1'.
    """
    # get the current working directory
    cwd = os.getcwd()

    # pick the target installation folder for tools
    if "PATHTOOLS" in Cnt and Cnt["PATHTOOLS"] != "":
        path_tools = Cnt["PATHTOOLS"]
    elif "PATHTOOLS" not in Cnt or Cnt["PATHTOOLS"] != "":
        if os.getenv("DISPLAY", False) and platform.system() in ["Linux", "Windows"]:
            log.info("DISPLAY: {}".format(os.environ["DISPLAY"]))
            dircore = askdirectory(
                title="choose a place for NiftyPET tools",
                initialdir=os.path.expanduser("~"),
            )
            # get the full (combined path)
            path_tools = os.path.join(dircore, Cnt["DIRTOOLS"])
        else:
            try:
                path_tools = askdirectory(
                    title="Enter path for NiftyPET tools (registration, etc): ",
                    name="PATHTOOLS",
                )
            except Exception:
                log.warning(
                    "manually enter the intended PATHTOOLS in resources.py"
                    " located in ~/.niftypet/"
                )
                raise ValueError("\n e> could not get the path for NiftyPET_tools \n")
        Cnt["PATHTOOLS"] = path_tools

    else:
        if platform.system() == "Linux":
            path_tools = os.path.join(os.path.expanduser("~"), Cnt["DIRTOOLS"])
        elif platform.system() == "Windows":
            path_tools = os.path.join(os.getenv("LOCALAPPDATA"), Cnt["DIRTOOLS"])
        else:
            log.error(
                """\
                \r=============================================================
                \ronly Linux and Windows operating systems are supported
                \rfor the additional tools installation!
                \r=============================================================
                """
            )
            raise SystemError("OS not supported!")
        Cnt["PATHTOOLS"] = path_tools

    # create the main tools folder
    if not os.path.isdir(path_tools):
        os.mkdir(path_tools)
    # identify the specific path for the requested app
    if app == "niftyreg":
        repo = repo_reg
        sha1 = sha1_reg
        path = os.path.join(path_tools, "niftyreg")
    elif app == "dcm2niix":
        repo = repo_dcm
        sha1 = sha1_dcm
        path = os.path.join(path_tools, "dcm2niix")

        if not Cnt["CMPL_DCM2NIIX"]:
            # avoid installing from source, instead download the full version:
            Cnt = download_dcm2niix(Cnt, path)
            return Cnt

    # Check if the source folder exists and delete it, if it does
    if os.path.isdir(path):
        shutil.rmtree(path)
    # Create an empty folder and enter it
    os.mkdir(path)
    os.chdir(path)

    # clone the git repository
    run(["git", "clone", repo, dirsrc])
    os.chdir(dirsrc)
    log.info("checking out the specific git version of the software...")
    run(["git", "checkout", sha1])
    os.chdir("../")

    # create the building folder
    if not os.path.isdir(dirbld):
        os.mkdir(dirbld)
    # go inside the build folder
    os.chdir(dirbld)

    # run cmake with arguments
    if platform.system() == "Windows":
        cmd = [
            "cmake",
            "../" + dirsrc,
            "-DBUILD_ALL_DEP=ON",
            "-DCMAKE_INSTALL_PREFIX=" + path,
            "-G",
            Cnt["MSVC_VRSN"],
        ]
        run(cmd)
        run(["cmake", "--build", "./", "--config", "Release", "--target", "install"])
    elif platform.system() in ["Linux", "Darwin"]:
        cmd = [
            "cmake",
            "../" + dirsrc,
            "-DBUILD_ALL_DEP=ON",
            "-DCMAKE_INSTALL_PREFIX=" + path,
        ]
        if Cnt["CMAKE_TLS_PAR"] != "":
            cmd.append(Cnt["CMAKE_TLS_PAR"])
        run(cmd)
        run(
            [
                "cmake",
                "--build",
                "./",
                "--config",
                "Release",
                "--target",
                "install",
                "--",
                "-j",
                str(ncpu),
            ]
        )

    # restore the current working directory
    os.chdir(cwd)

    if app == "niftyreg":
        try:
            Cnt["RESPATH"] = glob.glob(
                os.path.join(os.path.join(path, "bin"), "reg_resample*")
            )[0]
            Cnt["REGPATH"] = glob.glob(
                os.path.join(os.path.join(path, "bin"), "reg_aladin*")
            )[0]
        except IndexError:
            log.error("NiftyReg has NOT been successfully installed.")
            raise SystemError("Failed Installation (NiftyReg)")
        # updated the file resources.py
        Cnt = update_resources(Cnt)
        # check the installation:
        chck_niftyreg = check_version(Cnt, chcklst=["RESPATH", "REGPATH"])
        if not all(chck_niftyreg.values()):
            log.error("NiftyReg has NOT been successfully installed.")
            raise SystemError("Failed Installation (NiftyReg)")

    elif app == "dcm2niix":
        try:
            Cnt["DCM2NIIX"] = glob.glob(
                os.path.join(os.path.join(path, "bin"), "dcm2niix*")
            )[0]
        except IndexError:
            log.error("dcm2niix has NOT been successfully installed.")
            Cnt = download_dcm2niix(Cnt, path)
        # check the installation:
        if not check_version(Cnt, chcklst=["DCM2NIIX"]):
            log.error("dcm2niix has NOT been successfully compiled from github.")
            Cnt = download_dcm2niix(Cnt, path)
    return Cnt


def update_resources(Cnt):
    """Update resources.py with the paths to the new installed apps."""
    # list of path names which will be saved
    key_list = ["PATHTOOLS", "RESPATH", "REGPATH", "DCM2NIIX", "HMUDIR"]

    # get the local path to NiftyPET resources.py
    path_resources = cs.path_niftypet_local()
    resources_file = os.path.join(path_resources, "resources.py")

    # update resources.py
    if os.path.isfile(resources_file):
        f = open(resources_file, "r")
        rsrc = f.read()
        f.close()
        # get the region of keeping in synch with Python
        i0 = rsrc.find("# # # start NiftyPET tools # # #")
        i1 = rsrc.find("# # # end NiftyPET tools # # #")
        pth_list = []
        for k in key_list:
            if k in Cnt:
                pth_list.append("'" + Cnt[k].replace("\\", "/") + "'")
            else:
                pth_list.append("''")

        # modify resources.py with the new paths
        strNew = "# # # start NiftyPET tools # # #\n"
        for i in range(len(key_list)):
            if pth_list[i] != "''":
                strNew += key_list[i] + " = " + pth_list[i] + "\n"
        rsrcNew = rsrc[:i0] + strNew + rsrc[i1:]
        f = open(resources_file, "w")
        f.write(rsrcNew)
        f.close()

    return Cnt
