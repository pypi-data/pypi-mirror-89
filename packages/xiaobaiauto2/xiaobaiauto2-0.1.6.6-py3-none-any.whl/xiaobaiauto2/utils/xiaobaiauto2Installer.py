#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'chinese_chromedriver_installer.py'
__create_time__ = '2020/7/17 1:04'

from typing import Optional
from urllib.request import urlretrieve, urlopen
from urllib.error import URLError
from winreg import *
from re import findall, IGNORECASE
from zipfile import ZipFile
from os import remove, path, popen
import platform, sys, subprocess, ssl, tarfile, ctypes

ssl._create_default_https_context = ssl._create_unverified_context

download_filename = ''

def back(a,b,c):
    '''''回调函数
    @a:已经下载的数据块
    @b:数据块的大小
    @c:远程文件的大小
    '''
    per = 100.0*a*b/c
    if per > 100:
        per = 100
    print(end='\r')
    print(f'{download_filename}已下载%.2f%%' % per, end='')

def get_osname():
    ''' 判断当前系统 : windows/mac/ubuntu/centos '''
    if sys.platform == 'win32':
        ''' windows '''
        return 'windows'
    elif sys.platform == 'darwin':
        ''' Mac OS '''
        return 'mac'
    elif sys.platform == 'linux2':
        if 'ubuntu' in platform.platform().lower():
            ''' ubuntu '''
            return 'ubuntu'
        elif 'redhat' in platform.platform().lower():
            ''' redhat/centos '''
            return 'centos'
        else:
            return 'other'
    else:
        return 'other'

def is_admin():
    ''' 适用于windwos 判断当前是否为管理员 return True/False '''
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def unZip(file: Optional[str] = None, filename: Optional[str] = None, path: Optional[str] = None, **kwargs):
    '''
    解压文件 支持：*.zip *.tar.gz
    :param file:        待解压文件
    :param filename:    解压后的文件名（适应与单文件）
    :param path:        解压的目录
    :param kwargs       扩展参数
    :return:
    样例：
        unZip(file='chromedriver.zip', path='C:/Windows')
        unZip(file='chromedriver.tar.gz', filename='chromedriver.exe')
    '''
    if path not in [None, ''] and filename in [None, '']:
        if '.zip' == file[-4:]:
            ZipFile(file).extractall(path=path)
        elif '.tar.gz' == file[-7:]:
            tarfile.open(file).extractall(path=path)
    elif path in [None, ''] and filename not in [None, '']:
        if '.zip' == file[-4:]:
            ZipFile(file).extract(filename)
        elif '.tar.gz' == file[-7:]:
            tarfile.open(file).extract(filename)

def download(url: Optional[str] = None, **kwargs):
    '''
    下载文件
    :param url:         下载链接
    :param file:        下载文件名
    :param filename:    (解压后)文件名（适应压缩为单文件）
    :param path:        (解压)/(移动)的目录
    :param unzip:       是否解压
    :param del_src:     是否删除下载文件
    :param kwargs:
    :return:
    样例：
        download(url='https://api.xiaobai.com/adb.zip', file='adb.zip', path='D:/adb', unzip=True, del_src=True)
    '''
    global download_filename
    download_filename = kwargs.get('file')
    if url not in [None, '']:
        try:
            if 'unzip' not in kwargs.keys() and 'path' in kwargs.keys():
                urlretrieve(url, kwargs.get('path') + '/' + download_filename, back)
            else:
                urlretrieve(url, download_filename, back)
        except URLError as e:
            print('您的文件下载失败，请确认后重试！')
            exit(0)
        if 'unzip' in kwargs.keys() and kwargs.get('unzip'):
            if 'filename' in kwargs.keys() and 'path' not in kwargs.keys():
                unZip(file=download_filename, filename=kwargs.get('filename'))
            elif 'path' in kwargs.keys() and 'filename' not in kwargs.keys():
                unZip(file=download_filename, path=kwargs.get('path'))
        if 'del_src' in kwargs.keys() and kwargs.get('del_src'):
            remove(download_filename)

def _shell(cmd: Optional[str] = '', isSubprocess: Optional[bool] = True, powershell: Optional[bool] = False):
    ''' subprocess '''
    name = get_osname()
    if isSubprocess:
        if powershell:
            if cmd == '' and name == 'windows' and powershell:
                args = ["powershell",
                        "Set-ExecutionPolicy RemoteSigned -scope CurrentUser",
                        "iex (new-object net.webclient).downloadstring('https://get.scoop.sh')",
                        "iwr -useb get.scoop.sh | iex"]
            else:
                args = ['powershell', cmd]
        else:
            cmd_list = cmd.split(' ')
            args = [cmd_list[0], ' '.join(cmd_list[1:])]
        try:
            sp = subprocess.Popen(args, stdout=subprocess.PIPE)
            return sp.stdout.read()
        except Exception as e:
            return False
    else:
        try:
            popen(cmd)
        except Exception as e:
            exit(0)

def setEnv(name: Optional[str] = None, value: Optional[str] = None,
           addPath: Optional[bool] = True, endPath: Optional[str] = '/bin'):
    '''
    添加(系统)环境变量
    :param name:        环境变量名
    :param value:       环境变量值
    :param addPath:     是否添加到PATH
    :param endPath:     追加的路径
    :return:
    样例：
        setEnv(JAVA_HOME, 'D:/JDK', True, '/bin')
        setEnv(JAVA_HOME, 'D:/JDK')
    '''
    if name is None or value is None: return None
    os = get_osname()
    if os == 'windows':
        value = value.replace('/', '\\')
        endPath = endPath.replace('/', '\\')
        if is_admin():
            env = '系统'
            read_env_key = OpenKey(HKEY_LOCAL_MACHINE, 'SYSTEM\ControlSet001\Control\Session Manager\Environment')
            write_env_key = OpenKey(HKEY_LOCAL_MACHINE, 'SYSTEM\ControlSet001\Control\Session Manager\Environment',
                              access=KEY_WRITE)
        else:
            env = '用户'
            read_env_key = OpenKey(HKEY_CURRENT_USER, 'Environment')
            write_env_key = OpenKey(HKEY_CURRENT_USER, 'Environment', access=KEY_WRITE)
        path_env = QueryValueEx(read_env_key, 'path')[0]
        # add key
        SetValueEx(write_env_key, name, 0, REG_SZ, value)
        if addPath:
            SetValueEx(write_env_key, 'path', 0, REG_EXPAND_SZ, f'%{name}%{endPath};{path_env}')
        FlushKey(write_env_key)
        print(f'\n{env}环境变量{name}已经设置完毕！')
    else:
        cmd = f'\nexport {name}={value}'
        if addPath:
            cmd += f'\nexport PATH=$PATH:${name}{endPath}'
        try:
            with open('/etc/profile', 'a') as f:
                f.write(cmd)
                f.flush()
                f.close()
            _shell('source /etc/profile')
            print(f'\n环境变量 {name} 已经设置完毕！')
        except PermissionError as e:
            print('\n未使用管理员权限')
            try:
                with open('~/.bash_profile', 'a') as f:
                    f.write(cmd)
                    f.flush()
                    f.close()
                print(f'\n环境变量 {name} 已经设置完毕！')
            except Exception as e:
                print('\n环境变量设置失败！')

def getWebList(url: Optional[str] = None, match: Optional[str] = None, flags: Optional[int] = IGNORECASE):
    '''
    获取网页中指定规则的所有值，存储到列表中，默认
    :param url:     链接地址
    :param match:   匹配规则
    :param flags:   匹配模式 默认(IGNORECASE)忽略大小写
    :return:
    样例：
        getWebList('https://www.baidu.com', 'href="(.+?)"')
    '''
    if url is not None and match is not None:
        try:
            res = urlopen(url=url).read().decode('utf-8')
            return findall(match, res, flags)
        except URLError as e:
            print(e)
            exit(0)
    else:
        return []

def chromedriver_download(version: Optional[str] = '87', dest_dir: Optional[str] = '.'):
    '''
    自动下载chromedriver驱动文件
    :param version: 87,88等chrome浏览器版本号（整数）
    :return:
    '''
    TAOBAO_MIRROR_DOWNLOAD_URL = 'https://npm.taobao.org/mirrors/chromedriver/'
    name = get_osname()
    if name == 'windows':
        try:
            if version == '':
                chrome_current_version = EnumValue(OpenKey(HKEY_CURRENT_USER, 'Software\Google\Chrome\BLBeacon'), 0)[1]
                cur_version = chrome_current_version.split('.')[0]
            else:
                cur_version = version
            LAST_VERSION = getWebList(TAOBAO_MIRROR_DOWNLOAD_URL, f'/mirrors/chromedriver/{cur_version}([0-9\.]+)/">')[0]
            DOWNLOAD_URL = f'{TAOBAO_MIRROR_DOWNLOAD_URL}{cur_version}{LAST_VERSION}/chromedriver_win32.zip'
            download(DOWNLOAD_URL, file='chromedriver_win32.zip', path=dest_dir, unzip=True, del_src=True)
        except Exception as e:
            raise ('是不是没安装Chrome浏览器呢？' + str(e))
    elif name == 'mac':
        if version == '':
            cur_version = ''
        else:
            cur_version = version
        try:
            LAST_VERSION = getWebList(TAOBAO_MIRROR_DOWNLOAD_URL, f'/mirrors/chromedriver/{cur_version}([0-9\.]+)/">')[0]
            DOWNLOAD_URL = f'{TAOBAO_MIRROR_DOWNLOAD_URL}{LAST_VERSION}/chromedriver_linux64.zip'
            download(DOWNLOAD_URL, file='chromedriver_linux64.zip', path='/usr/local/bin', unzip=True, del_src=True)
        except Exception as e:
            pass
    else:
        if version == '':
            cur_version = ''
        else:
            cur_version = version
        try:
            LAST_VERSION = getWebList(TAOBAO_MIRROR_DOWNLOAD_URL, f'/mirrors/chromedriver/{cur_version}([0-9\.]+)/">')[0]
            DOWNLOAD_URL = f'{TAOBAO_MIRROR_DOWNLOAD_URL}{LAST_VERSION}/chromedriver_mac64.zip'
            download(DOWNLOAD_URL, file='chromedriver_mac64.zip', path='/usr/local/bin', unzip=True, del_src=True)
        except Exception as e:
            pass

def tesseract_download():
    TESSERACT_DOWNLOAD_URL = 'https://api.256file.com/download/56476_tesseract.exe'
    download(url=TESSERACT_DOWNLOAD_URL, file='tesseract.exe', unzip=False)

def update_keyword_db():
    KEYWORD_DB_DOWNLOAD_URL = ''
    urlretrieve(KEYWORD_DB_DOWNLOAD_URL, 'xiaobaiauto2.db', back)
    # popen('xiaobaiauto2.db', )

def jdk_install(version: Optional[str] = '8', dest_dir: Optional[str] = '.'):
    '''
    下载并安装openjdk
    windows: scoop install oraclejdk{version}
    mac os: brew cask install adoptopenjdk{version}
    ubuntu: apt install openjdk-{version}-jre
    centos: yum install java-1.{version}.0-openjdk
    mirror: https://mirrors.tuna.tsinghua.edu.cn/AdoptOpenJDK/{version}/jdk/x64/{os}/
    '''
    os = get_osname()
    if os == 'windows':
        url = f'https://mirrors.tuna.tsinghua.edu.cn/AdoptOpenJDK/{version}/jdk/x64/{os}/'
        filename = getWebList(url, match='href="OpenJDK(.+?).zip"', flags=0)
        if len(filename) > 0:
            url = f'{url}OpenJDK{filename[0]}.zip'
            download(url=url, file=f'jdk{version}_{os}_64.zip', path=dest_dir, unzip=True, del_src=True)
    elif os == 'mac':
        ''' Mac OS '''
        try:
            _shell(cmd='/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"')
        except Exception as e:
            pass
        url = f'https://mirrors.tuna.tsinghua.edu.cn/AdoptOpenJDK/{version}/jdk/x64/{os}/'
        filename = getWebList(url, match='href="OpenJDK(.+?).tar.gz"', flags=0)
        if len(filename) > 0:
            url = f'{url}OpenJDK{filename[0]}.tar.gz'
            download(url=url, file=f'jdk{version}_{os}_64.tar.gz', path=dest_dir, unzip=True, del_src=True)
    else:
        url = f'https://mirrors.tuna.tsinghua.edu.cn/AdoptOpenJDK/{version}/jdk/x64/linux/'
        filename = getWebList(url, match='href="OpenJDK(.+?).tar.gz"', flags=0)
        if len(filename) > 0:
            url = f'{url}OpenJDK{filename[0]}.tar.gz'
            download(url=url, file=f'jdk{version}_{os}_64.tar.gz', path=dest_dir, unzip=True, del_src=True)
    if dest_dir != '.' and path.isdir(dest_dir):
        value = f'{dest_dir}/jdk{version}_{os}_64'
    else:
        value = f'{path.abspath(path.curdir)}/jdk{version}_{os}_64'
    setEnv('JAVA_HOME', value)

def jmeter_install(version: Optional[str] = '5.3', dest_dir: Optional[str] = '.'):
    ''' 下载并配置环境变量 '''
    src_list = [
        'https://mirror.bit.edu.cn/apache/jmeter/binaries/',
        'https://mirrors.bfsu.edu.cn/apache/jmeter/binaries/',
        'https://mirrors.tuna.tsinghua.edu.cn/apache/jmeter/binaries/'
    ]
    file = f'apache-jmeter-{version}.zip'
    download(src_list[2] + file, file=file, path=dest_dir, unzip=True, del_src=True)
    setEnv('JMETER_HOME', f'{path.abspath(dest_dir)}/apache-jmeter-{version}')
    # set Chinese
    with open(path.abspath(dest_dir) + f'/apache-jmeter-{version}/bin/jmeter.properties', 'a', encoding='utf-8') as fw:
        fw.write('\n\nlanguage=zh_CN')
        fw.flush()
        fw.close()
    print('JMeter已设置中文')

def jenkins_war_install(version: Optional[str] = 'latest', dest_dir: Optional[str] = '.'):
    url = f'https://mirrors.tuna.tsinghua.edu.cn/jenkins/war-stable/{version}/jenkins.war'
    download(url=url, file='jenkins.war', path=dest_dir)

def git_windows_install(version: Optional[str] = 'latest', dest_dir: Optional[str] = '.'):
    if version == 'latest':
        if get_osname() == 'windows':
            url = 'https://mirrors.tuna.tsinghua.edu.cn/github-release/git-for-windows/git/LatestRelease/'
            files = getWebList(url=url, match='href="Git-(.+?)-64-bit.exe"')
            download(url=f'{url}Git-{files[0]}-64-bit.exe', file=f'Git-{files[0]}-64-bit.exe', path=dest_dir)
        else:
            print('非windows系统可以使用命令自行安装哦！')
    else:
        print('该程序暂不持支选择版本哦！')

def node_install(version: Optional[str] = 'latest', dest_dir: Optional[str] = '.'):
    name = get_osname()
    res = urlopen(url='https://npm.taobao.org/mirrors/node/index.tab').read().decode('utf-8')
    all_lines = res.split('\n')
    if len(all_lines) > 1:
        if version == 'latest':
            version = all_lines[1].split('\t')[0][1:]
        else:
            version = [v.split('\t')[0][1:] for v in all_lines if f'v{version}' in v.split('\t')[0]]
            if len(version) == 0:
                version = all_lines[1].split('\t')[0][1:]
        if name == 'windows':
            url = f'https://npm.taobao.org/mirrors/node/v{version}/node-v{version}-win-x64.zip'
            download(url=url, file=f'node-v{version}-win-x64.zip', path=dest_dir, unzip=True, del_src=True)
            setEnv(name='NODE_HOME', value=f'{path.abspath(dest_dir)}/node-v{version}-win-x64', endPath='')
        elif name == 'mac':
            url = f'https://npm.taobao.org/mirrors/node/v{version}/node-v{version}-darwin-x64.tar.gz'
            download(url=url, file=f'node-v{version}-darwin-x64.tar.gz', path=dest_dir, unzip=True, del_src=True)
            setEnv(name='NODE_HOME', value=f'{path.abspath(dest_dir)}/node-v{version}-darwin-x64', endPath='')
        else:
            url = f'https://npm.taobao.org/mirrors/node/v{version}/node-v{version}-linux-x64.tar.gz'
            download(url=url, file=f'node-v{version}-linux-x64.tar.gz', path=dest_dir, unzip=True, del_src=True)
            setEnv(name='NODE_HOME', value=f'{path.abspath(dest_dir)}/node-v{version}-linux-x64', endPath='')