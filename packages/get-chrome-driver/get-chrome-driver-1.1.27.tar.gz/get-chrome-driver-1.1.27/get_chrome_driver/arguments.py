from .platforms import Platforms

platforms = Platforms()

descriptor = '  {:<30} {}'
message_help_required_release = descriptor.format('', 'required: add a release version')
message_help_optional_extract = descriptor.format('', 'optional: use --extract to extract the zip file')

args_options = [
    ['--beta-version', 'print the beta release version'],
    ['--stable-version', 'print the stable release version'],
    ['--latest-urls', 'print the beta and stable release urls for all platforms'],
    ['--release-url', 'print the url of a release for a platform' + '\n'
     + message_help_required_release],
    ['--beta-url', 'print the beta release url for a platform'],
    ['--stable-url', 'print the stable release url for a platform'],
    ['--auto-download', 'auto download a ChromeDriver release for the installed Chrome Version' + '\n'
     + message_help_optional_extract],
    ['--download-beta', 'download the beta release for a platform' + '\n'
     + message_help_optional_extract],
    ['--download-stable', 'download the stable release for a platform' + '\n'
     + message_help_optional_extract],
    ['--download-release', 'download a specific release' + '\n'
     + message_help_required_release + '\n'
     + message_help_optional_extract],
    ['--extract', 'extract the compressed driver file'],
    ['--version', 'program version'],
    ['--help', 'show help']
]


def print_help():
    print('usage: ' + 'get-chrome-driver' + ' [options]')
    print('')
    print('options: ')
    for i, argument in enumerate(args_options):
        print(descriptor.format(argument[0], argument[1]))
    print('')
    print('The downloaded driver can be found at: ')
    print('<current directory>/<chromedriver>/<version>/<bin>/<chromedriver>')
