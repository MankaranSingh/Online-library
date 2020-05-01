import argparse
from safaribooks import SafariBooks

arguments = argparse.ArgumentParser(prog="safaribooks.py",
                                    description="Download and generate an EPUB of your favorite books"
                                    " from Safari Books Online.",
                                    add_help=False,
                                    allow_abbrev=False)

login_arg_group = arguments.add_mutually_exclusive_group()
login_arg_group.add_argument(
    "--cred", metavar="<EMAIL:PASS>", default=False,
    help="Credentials used to perform the auth login on Safari Books Online."
    " Es. ` --cred \"account_mail@mail.com:password01\" `."
)
login_arg_group.add_argument(
    "--login", action='store_true',
    help="Prompt for credentials used to perform the auth login on Safari Books Online."
)

arguments.add_argument(
    "--no-cookies", dest="no_cookies", action='store_true',
    help="Prevent your session data to be saved into `cookies.json` file."
)
arguments.add_argument(
    "--no-kindle", dest="no_kindle", action='store_true',
    help="Remove some CSS rules that block overflow on `table` and `pre` elements."
    " Use this option if you're not going to export the EPUB to E-Readers like Amazon Kindle."
)
arguments.add_argument(
    "--preserve-log", dest="log", action='store_true', help="Leave the `info_XXXXXXXXXXXXX.log`"
    " file even if there isn't any error."
)
arguments.add_argument(
    "--help", action="help", default=argparse.SUPPRESS, help='Show this help message.')
arguments.add_argument("--folder_name", metavar='<FOLDER>',
                       help="Folder's name in book directory", default='')
arguments.add_argument(
    "bookid", metavar='<BOOK ID>',
    help="Book digits ID that you want to download. You can find it in the URL (X-es):"
    " `" + "SAFARI_BASE_URL" + "/library/view/book-name/XXXXXXXXXXXXX/`"
)
args_parsed = arguments.parse_args(
    ['--cred', 'jaskeerat781999@gmail.com:2+#YeZ.zEKUG6ge', '9781491903063', '--folder_name', 'test'])

if args_parsed.cred or args_parsed.login:
    user_email = ""
    pre_cred = ""

    if args_parsed.cred:
        pre_cred = args_parsed.cred

    else:
        user_email = input("Email: ")
        passwd = getpass.getpass("Password: ")
        pre_cred = user_email + ":" + passwd

    parsed_cred = SafariBooks.parse_cred(pre_cred)

    if not parsed_cred:
        arguments.error("invalid credential: %s" % (
            args_parsed.cred if args_parsed.cred else (
                user_email + ":*******")
        ))

    args_parsed.cred = parsed_cred

else:
    if args_parsed.no_cookies:
        arguments.error(
            "invalid option: `--no-cookies` is valid only if you use the `--cred` option")

print(args_parsed)
SafariBooks(args_parsed)
