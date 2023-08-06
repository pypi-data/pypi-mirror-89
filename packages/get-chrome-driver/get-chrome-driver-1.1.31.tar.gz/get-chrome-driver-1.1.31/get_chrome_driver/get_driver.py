import os
import requests
import zipfile
import platform as pl
import xml.etree.ElementTree as ElTree
import subprocess
import struct
from urllib.request import urlopen
from bs4 import BeautifulSoup

from requests.exceptions import RequestException
from requests.exceptions import HTTPError

from . import constants
from . import retriever
from .platforms import Platforms
from .phase import Phase
from .exceptions import GetChromeDriverError
from .exceptions import UnknownPlatformError
from .exceptions import ReleaseUrlError
from .exceptions import UnknownReleaseError
from .exceptions import DownloadError
from .exceptions import VersionError


class GetChromeDriver:

    def __init__(self, platform=None) -> None:
        self.__platforms = Platforms()

        if not platform:
            if pl.system() == 'Windows':
                self.__platform = self.__check_platform(self.__platforms.win)
            elif pl.system() == 'Linux':
                self.__platform = self.__check_platform(self.__platforms.linux)
            elif pl.system() == 'Darwin':
                self.__platform = self.__check_platform(self.__platforms.mac)
        else:
            self.__platform = self.__check_platform(platform)

        self.__phases = Phase()

    def stable_release_version(self) -> str:
        """ Return the latest stable release version """

        return self.__latest_release_version('stable')

    def beta_release_version(self) -> str:
        """ Return the latest beta release version """

        return self.__latest_release_version('beta')

    def __latest_release_version(self, phase) -> str:
        """ Return the stable or beta release version """

        res = requests.get(constants.CHROMEDRIVER_CHROMIUM_URL)

        if res.status_code != 200:
            raise GetChromeDriverError('error: could not connect to ' + constants.CHROMEDRIVER_CHROMIUM_URL)

        soup = BeautifulSoup(res.content, 'html.parser')
        ul = soup.select_one(constants.UL_RELEASES_SELECTOR)
        for li in ul:
            li_text = li.text.replace(u'\u00A0', ' ')
            if self.__phases.stable == phase:
                release_str = constants.LATEST_STABLE_RELEASE_STR
            else:
                release_str = constants.LATEST_BETA_RELEASE_STR

            if li_text[:len(release_str)].lower() == release_str.lower():
                try:
                    release = li.a['href'].split('path=')[-1:][0][:-1]
                except TypeError:
                    raise UnknownReleaseError('error: could not find release version')
                else:
                    self.__check_release(release)
                    return release

    def stable_release_url(self) -> str:
        """ Return the latest stable release url """

        return self.release_url(self.__latest_release_version(self.__phases.stable))

    def beta_release_url(self) -> str:
        """ Return the latest beta release url """

        return self.release_url(self.__latest_release_version(self.__phases.beta))

    def release_url(self, release) -> str:
        """ Return the release download url """

        self.__check_release(release)

        arch = struct.calcsize('P') * 8
        arch_64 = 64

        if self.__platform == self.__platforms.win:

            # 64bit
            if arch == arch_64:
                try:
                    url = (constants.CHROMEDRIVER_STORAGE_URL + '/' + release + '/' + constants.CHROMEDRIVER + '_'
                           + self.__platforms.win_64 + constants.ZIP_TYPE)
                    self.__check_url(url)
                    return url
                except ReleaseUrlError:
                    pass
            # 32bit
            url = (constants.CHROMEDRIVER_STORAGE_URL + '/' + release + '/' + constants.CHROMEDRIVER + '_'
                   + self.__platforms.win_32 + constants.ZIP_TYPE)
            self.__check_url(url)
            return url

        elif self.__platform == self.__platforms.linux:

            # 64bit
            if arch == arch_64:
                try:
                    url = (constants.CHROMEDRIVER_STORAGE_URL + '/' + release + '/' + constants.CHROMEDRIVER + '_'
                           + self.__platforms.linux_64 + constants.ZIP_TYPE)
                    self.__check_url(url)
                    return url
                except ReleaseUrlError:
                    pass
            # 32bit
            url = (constants.CHROMEDRIVER_STORAGE_URL + '/' + release + '/' + constants.CHROMEDRIVER + '_'
                   + self.__platforms.linux_32 + constants.ZIP_TYPE)
            self.__check_url(url)
            return url

        elif self.__platform == self.__platforms.mac:

            # 64bit
            if arch == arch_64:
                try:
                    url = (constants.CHROMEDRIVER_STORAGE_URL + '/' + release + '/' + constants.CHROMEDRIVER + '_'
                           + self.__platforms.mac_64 + constants.ZIP_TYPE)
                    self.__check_url(url)
                    return url
                except ReleaseUrlError:
                    pass
            # 32bit
            url = (constants.CHROMEDRIVER_STORAGE_URL + '/' + release + '/' + constants.CHROMEDRIVER + '_'
                   + self.__platforms.mac_32 + constants.ZIP_TYPE)
            self.__check_url(url)
            return url

    def download_stable_release(self, output_path=None, extract=False) -> None:
        """ Download the latest stable chromedriver release """

        release = self.__latest_release_version(self.__phases.stable)
        self.download_release(release, output_path, extract)

    def download_beta_release(self, output_path=None, extract=False) -> None:
        """ Download the latest stable chromedriver release """

        release = self.__latest_release_version(self.__phases.beta)
        self.download_release(release, output_path, extract)

    def download_release(self, release, output_path=None, extract=False) -> str:
        """ Download a chromedriver release """

        self.__check_release(release)

        def download(url_download) -> str:
            if output_path is None:
                output_path_no_file_name = constants.CHROMEDRIVER + '/' + release + '/bin'
            else:
                output_path_no_file_name = output_path

            try:
                output_path_with_file_name, file_name = retriever.download(url=url_download,
                                                                           output_path=output_path_no_file_name)
            except (OSError, HTTPError, RequestException) as err:
                raise DownloadError(err)

            if extract:
                with zipfile.ZipFile(output_path_with_file_name, 'r') as zip_ref:
                    zip_ref.extractall(path=output_path_no_file_name)
                os.remove(output_path_with_file_name)

                if pl.system() == 'Linux' or pl.system() == 'Darwin':
                    os.chmod(output_path_no_file_name + '/' + constants.CHROMEDRIVER, 0o755)

            return output_path_no_file_name

        url = self.release_url(release)
        if self.__platform == self.__platforms.win:
            return download(url)
        elif self.__platform == self.__platforms.linux:
            return download(url)
        elif self.__platform == self.__platforms.mac:
            return download(url)

    def __check_url(self, url) -> None:
        """ Check if url is valid """

        if requests.head(url).status_code != 200:
            raise ReleaseUrlError('error: Invalid url')

    def __check_release(self, release) -> None:
        """ Check if release format is valid """

        split_release = release.split('.')

        for number in split_release:
            if not number.isnumeric():
                raise UnknownReleaseError('error: Invalid release format')

    def __check_platform(self, platform) -> str:
        """ Check if platform is valid """

        if platform not in self.__platforms.list:
            raise UnknownPlatformError('error: platform not recognized, choose a platform from: '
                                       + str(self.__platforms.list))

        return platform

    def matching_version(self):
        """ Return a matching ChromeDriver version """

        all_chromedriver_versions = self.__get_all_chromedriver_versions()
        installed_chrome_version = self.__get_installed_chrome_version()

        chromedriver_version_to_download = ''
        for chromedriver_version in reversed(all_chromedriver_versions):
            if '.'.join(installed_chrome_version.split('.')[:-1]) == '.'.join(chromedriver_version.split('.')[:-1]):
                chromedriver_version_to_download = chromedriver_version
                break
        return chromedriver_version_to_download

    def auto_download(self, extract=False) -> str:
        """ Download ChromeDriver for the installed Chrome version on machine """

        chromedriver_version_to_download = self.matching_version()
        if chromedriver_version_to_download == '':
            raise VersionError('error: unable to find a ChromeDriver version for the installed Chrome version')

        path = constants.CHROMEDRIVER + '/' + chromedriver_version_to_download + '/' + 'bin'
        for root, dirs, files in os.walk(path):
            for file in files:
                if file[:len(constants.CHROMEDRIVER)] == constants.CHROMEDRIVER:
                    return path

        return self.download_release(chromedriver_version_to_download, extract=extract)

    def install(self) -> None:
        """ Install ChromeDriver for the installed Chrome version on machine """

        output_path = self.auto_download(extract=True)
        path = os.path.join(os.path.abspath(os.getcwd()), output_path)
        os.environ['PATH'] += os.pathsep + os.pathsep.join([path])

    def __get_all_chromedriver_versions(self) -> list:
        """ Return a list with all ChromeDriver versions """

        key_texts = []
        versions = []

        url = constants.CHROMEDRIVER_STORAGE_URL

        with urlopen(url) as xml_file:
            tree = ElTree.parse(xml_file)
            root = tree.getroot()

            for root_item in root:
                # Remove namespace
                root_item.tag = root_item.tag.split('}', 1)[1]

            for content in root.findall('Contents'):

                for content_item in content:
                    # Remove namespace
                    content_item.tag = content_item.tag.split('}', 1)[1]

                    key_texts.append(content.find('Key').text)

        for text in key_texts:

            version = ''
            for char in text:
                if char.isnumeric() or char == '.':
                    version += char
                else:
                    break

            if len(version) < 1:
                continue

            versions.append(version)

        return list(dict.fromkeys(versions))

    def __get_installed_chrome_version(self) -> str:
        """ Return the installed Chrome version on the machine """

        if pl.system() == 'Windows':
            process = subprocess.Popen(
                ['reg', 'query', 'HKEY_CURRENT_USER\\SOFTWARE\\Google\\Chrome\\BLBeacon', '/v', 'version'],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            return process.communicate()[0].decode('UTF-8').split()[-1]

        elif pl.system() == 'Linux':
            process = subprocess.Popen(
                ['google-chrome', '--version'],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            return process.communicate()[0].decode('UTF-8').split()[-1]

        elif pl.system() == 'Darwin':
            process = subprocess.Popen(
                ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            return process.communicate()[0].decode('UTF-8').split()[-1]
