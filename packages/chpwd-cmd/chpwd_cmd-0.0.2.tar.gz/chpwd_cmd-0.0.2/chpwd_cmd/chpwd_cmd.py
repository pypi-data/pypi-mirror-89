import sys
from chpwd_cmd.workdir import WorkDir
from chpwd_cmd.config_file import ConfigFile, ConfigFileError
from chpwd_cmd.arguments import Arguments, ArgumentsError


def main():
    try:
        args = Arguments().get()
        workdirs = ConfigFile().config['workdir']
    except ConfigFileError:
        sys.exit()
    except ArgumentsError:
        Arguments().help()
        sys.exit()

    for workdir_name in workdirs:
        wd = WorkDir(workdir_name, workdirs[workdir_name], args.cwd)
        wd.execute(args.mode)


if __name__ == "__main__":
    main()
