import os
import secrets
import subprocess


class DefaultSandbox:
    """
    DOCKER SUPPORT REMOVED
    container time limit is now a prepare and post script + usercode timelimit

    Here wow it works. files are a dict *cough* json *cough* where key is file
    path and value is content, if it is in folder than folder will be
    created. All files are placed relative to temp dir and should not begin
    with "/". if you want some file be accessed during execution of
    run_command then put them inside usercode/ folder like
    "usercode/file.py" os it can be accessed by isolate and run_command.

    run_command is what supplied to isolate to run in
    safe boundaries like "/bin/python3 files.py", isolate run this command
    inside usercode folder in sandbox, "/bin/python3 usercode/files.py" IS
    NOT CORRECT PATH.
    stdin -> usercode/input_file
    stdout -> usercode/output_file
    stderr -> usercode/

    For compilation, test generation or other stuff that should
    be done before usercode execution you can do in prepare.sh. This script
    is executed before usercode in temp folder so you can access all files
    you added there. Also if you prepare script fails you should write something
    to prepare_errors because if there is anything then usercode won't executed
    but post.sh script still will be executed so you can do some debug stuff.

    And for last you have post.sh script. It is used to
    prepare output. By default only meta, prepare_logs, prepare_errors supplied
    in response but you can add additional files by writing their names
    in payload_files files in format '{name}@{path}' like this
    `
    output@usercode/output_file
    error_file@usercode/error_file
    `.
    Be careful because currently scripts are executed as root.


    ALL PATH ARE RELATIVE TO THE ROOT OF SANDBOX. ACCESS FILES ONLY WITH "./"
    or with out any slash.
    ELSE YOU CAN CRASH WORKER.


    @:param app for logging.
    @:param container_wall_time_limit prepare and post script + usercode timelimit in seconds
    @:param wall_time_limit usercode wall time limit in secods
    @:param time_limit usercode time limit in seconds
    @:param memory_limit for run_command in kilobytes
    @:param app_path path to app where payload folder contains. for difference payload versions
    @:param files. files to write.
    @:param run_command is what isolate run within sandbox
    @:param temp_folder is where temp files will be stored

    run_command stdin file is "usercode/input_file",
    stdout "usercode/output_file" and
    stderr "usercode/error_file".

    TODO: docs
    """

    def __init__(self,
                 container_wall_time_limit: int,
                 wall_time_limit: int,
                 time_limit: int,
                 memory_limit: int,
                 app_path: str,
                 files: dict,
                 run_command: str,
                 temp_folder='temp/'):
        self.container_wall_time_limit = container_wall_time_limit
        self.wall_time_limit = wall_time_limit
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.app_path = app_path
        # folder were code is contained. look like: self.app_path + self.folder
        self.id = secrets.token_hex(16)
        self.folder = temp_folder + self.id
        self.files = files
        self.run_command = run_command
        print('Sandbox created')

    @property
    def run(self) -> dict:
        res = self.prepare()
        # rm folder to be sure.
        subprocess.run(f'rm -rf {self.app_path}{self.folder}', shell=True)
        return res

    def create_and_write_to_file(self, path, data):
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            path = open(path, 'w')
            path.write(data)
            path.close()
        except IOError:
            print(
                f'FAILED TO WRITE/OPEN FILE: {path}')
            return self.internal_error(f'FAILED TO WRITE/OPEN FILE: {path}')

    def prepare(self):
        """
        copying payload, usercode and input to temp directory and
        setting permissions
        """

        # Copy payload folder at /app/payload
        cp = subprocess.run(
            f'mkdir {self.app_path}{self.folder} && cp -rp {self.app_path}payload/* {self.app_path}{self.folder}',
            shell=True)
        if cp.returncode != 0:
            print(
                f'COMMAND FAILED:Copy payload failed ')
            return self.internal_error('Copy payload failed')

        # create all request files
        for path, data in self.files.items():
            self.create_and_write_to_file(
                f'{self.app_path}{self.folder}/{path}', data)

        cp = subprocess.run(f'chmod -R 777 {self.app_path}{self.folder}',
                            shell=True)
        cp = subprocess.run(
            f'chmod -R 666 {self.app_path}{self.folder}/usercode', shell=True)
        cp = subprocess.run(
            f'chmod 667 {self.app_path}{self.folder}/usercode', shell=True)
        print('Files copied')
        return self.execute()

    def internal_error(self, message):
        subprocess.run(f'rm -r {self.app_path}{self.folder}', shell=True)
        return {
            'IE': True,
            'errors': message,
        }

    def execute(self):
        """
        executing usercode with given input.
        steps:
        1. run script defaultSandboxRunScript and configuration to run using "isolate".
        2. parse isolate meta
        3. return data

        check meta for MLE, TLE, RE, etc...
        :return result of run as dict:
                {
                'payload': {} is a dict of files that were declared in file payload_files
                'prepare_logs': log of prepare_script from stdout
                'prepare_errors': log of prepare_script from stderr
                'meta': log of isolate if prepare_error is empty
                'IE': if true none of above are valid. caught internal error
                }
        """

        run_command = f'defaultSandboxRunScript.sh {self.app_path}{self.folder} {str(self.memory_limit)} {str(self.time_limit)} {self.wall_time_limit} {self.run_command.format(self.app_path + self.folder + "/usercode")} '
        try:
            subprocess.run(f'{self.app_path}{self.folder}/{run_command}',
                           timeout=self.container_wall_time_limit,
                           stderr=subprocess.PIPE,
                           shell=True,
                           stdout=subprocess.PIPE)
        except subprocess.TimeoutExpired:
            return self.internal_error(
                'Wall time exceeded\nInternal error, see logs')
        except subprocess.CalledProcessError:
            pass
        except:
            subprocess.run(f'rm -r {self.app_path}{self.folder}', shell=True)
            return self.internal_error('Internal error, see logs')
        meta = str()
        try:
            fs = open(f'{self.app_path}{self.folder}/meta')
            meta = fs.read()
        except IOError:
            print(
                'FAILED TO WRITE/OPEN FILE: meta. some how sandbox failed')
            return self.internal_error(
                'FAILED TO WRITE/OPEN FILE: meta. some how sandbox failed')
        parsed_meta = dict()
        print(meta)
        for i in meta.split('\n'):
            if i != '':
                parsed_meta[i[0:i.find(':')]] = i[i.find(':') + 1:]

        prepare_logs = ''
        try:
            fs = open(f'{self.app_path}{self.folder}/prepare_logs')
            prepare_logs = fs.read()
        except IOError:
            print('FAILED TO WRITE/OPEN FILE: /prepare_logs')

        prepare_errors = ''
        try:
            fs = open(f'{self.app_path}{self.folder}/prepare_errors')
            prepare_errors = fs.read()
        except IOError:
            print('FAILED TO WRITE/OPEN FILE: /prepare_errors')

        logs = ''
        try:
            fs = open(f'{self.app_path}{self.folder}/logs')
            logs = fs.read()
        except IOError:
            print('FAILED TO WRITE/OPEN FILE: /logs')

        # if 'max-rss' in parsed_meta and 'time' in parsed_meta:
        #     output_file += f'''\n=====\nИспользовано: {parsed_meta["time"]} с, {parsed_meta["max-rss"]} КБ'''

        data = {
            'payload': {},
            'prepare_logs': prepare_logs,
            'prepare_errors': prepare_errors,
            'logs': logs,
            'meta': parsed_meta,
            'IE': False
        }
        try:
            fs = open(f'{self.app_path}{self.folder}/payload_files')
            payload_files = fs.read().split('\n')
            for np in payload_files:
                try:
                    (name, path) = np.split('@')
                    try:
                        fs = open(f'{self.app_path}{self.folder}/{path}')
                        data['payload'][name] = fs.read()
                    except IOError:
                        print(
                            f'FAILED TO WRITE/OPEN FILE: /{path}')
                except ValueError:
                    continue
        except IOError:
            print('failed to open file /response_file')
        subprocess.run(f'rm -rf {self.app_path}{self.folder}', shell=True)
        return data
