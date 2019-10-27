"""Attempts to configure git to use kettlediff"""

import os
import argparse
import configparser

# import configobj


HOME = os.path.expanduser("~")


def parse_config(args):  # pylint: disable=R0912
    """parses the gitconfig file."""
    configpath = os.path.join(HOME, ".gitconfig")
    # config = configobj.ConfigObj(configpath, interpolation=None, indent_type="\t")
    config = configparser.ConfigParser(interpolation=None)
    config.read(configpath)
    if "core" not in config:
        config["core"] = {}
    if "attributesfile" not in config["core"]:
        config["core"]["attributesfile"] = "~/.gitattributes"
    attributespath = config["core"]["attributesfile"]

    if 'diff "kettle"' not in config:
        config['diff "kettle"'] = {}
    if "textconv" not in config['diff "kettle"'] and \
            "xfuncname" not in config['diff "kettle"']:
        if args.exe:
            config['diff "kettle"']["textconv"] = "\"'{}'\"".format(
                os.path.join(os.getcwd(), "kettlediff.exe").replace("\\", "/"))
        else:
            config['diff "kettle"']["textconv"] = "python \"'{}'\"".format(
                os.path.join(os.getcwd(), "kettlediff.py").replace("\\", "/"))
        config['diff "kettle"']["xfuncname"] = (
            "< name > (.*) < /name > | < order > | < hops > )")
    else:
        print("already diff for kettle in .gitconfig!")

    if 'diff "prpt"' not in config:
        config['diff "prpt"'] = {}
    if "textconv" not in config['diff "prpt"'] and \
            "xfuncname" not in config['diff "prpt"']:
        if args.exe:
            config['diff "prpt"']["textconv"] = "\"'{}'\"".format(
                os.path.join(os.getcwd(), "kettlediff.exe").replace("\\", "/"))
        else:
            config['diff "prpt"']["textconv"] = "python \"'{}'\"".format(
                os.path.join(os.getcwd(), "kettlediff.py").replace("\\", "/"))
        config['diff "prpt"']["xfuncname"] = ".*name=.*"
    else:
        print("already diff for prpt in .gitconfig!")

    if 'diff "xlsx"' not in config:
        config['diff "xlsx"'] = {}
    if "textconv" not in config['diff "xlsx"'] and \
            "xfuncname" not in config['diff "xlsx"']:
        if args.exe:
            config['diff "xlsx"']["textconv"] = "\"'{}'\"".format(
                os.path.join(os.getcwd(), "kettlediff.exe").replace("\\", "/"))
        else:
            config['diff "xlsx"']["textconv"] = "python \"'{}'\"".format(
                os.path.join(os.getcwd(), "kettlediff.py").replace("\\", "/"))
        config['diff "xlsx"']["xfuncname"] = ".*------ Sheet: .*"
    else:
        print("already diff for xlsx in .gitconfig!")

    sections = [section for section in config if section != "DEFAULT"]
    if not args.write:
        print("Template for .gitconfig:\n---------------------------")
        for section in sections:
            print("[{}]".format(section))
            for key, item in config[section].items():
                print("\t{} = {}".format(key, item))
        print("---------------------------")
    else:
        with open(configpath, "w") as file:
            for section in sections:
                print("[{}]".format(section), file=file)
                for key, item in config[section].items():
                    print("\t{} = {}".format(key, item), file=file)

    return attributespath


def parse_attribs(attributespath, args):  # pylint: disable=R0912
    """put attributes into file. needs path"""
    if os.path.isfile(os.path.expanduser(attributespath)):
        with open(os.path.expanduser(attributespath), "r") as file:
            text = file.read()
            out = text.splitlines()
            new = []
            if "*.prpt" not in text:
                new.append("*.prpt diff=prpt")
            else:
                print("prpt already in attributesfile!")
            if "*.ktr" not in text:
                new.append("*.ktr diff=kettle")
            else:
                print("ktr already in attributesfile!")
            if "*.kjb" not in text:
                new.append("*.kjb diff=kettle")
            else:
                print("kjb already in attributesfile!")
            if "*.xlsx" not in text:
                new.append("*.xlsx diff=xlsx")
            else:
                print("xlsx already in attributesfile!")
    else:
        out = []
        new = ["*.prpt diff=prpt", "*.ktr diff=kettle",
               "*.kjb diff=kettle", ".xslx diff=xlsx"]
    out.extend(new)
    if not args.write:
        print("\nTemplate for .gitattributes:\n---------------------------")
        print("\n".join(out), "\n---------------------------")
    else:
        with open(os.path.expanduser(attributespath), "w") as file:
            file.write("\n".join(out))


def main():
    """do the thing"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--write", action="store_true", dest="write",
                        help="write files instead of printing to console")
    parser.add_argument("--exe", action="store_true", dest="exe",
                        help="specify if using the executable instad the python file")
    args = parser.parse_args()
    if os.name == "nt":
        attributespath = parse_config(args)
        parse_attribs(attributespath, args)


if __name__ == '__main__':
    main()
