#!/usr/bin/env python

"""w01fm00n
Copyright (C) 2020 w01f - https://github.com/w01fdev/

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

########################################################################

w01f hacks from Linux for Linux!

fck capitalism, fck patriarchy, fck racism, fck animal oppression ...

########################################################################
"""


import argparse
import csv
import os
import tarfile
import time

from .program import DATE, VERSION


class DirectoryScanner:
    """Forensic search for directories and files on the hard drive."""

    def __init__(self, root, file, raw=False):
        """Initalisation of the class.

        :param root: <str>
            the root directory from which the scan should start.
        :param file: <str>
            here the file is specified where the data is to be saved in
            <.csv> format. a complete path can be specified or only a
            file name with extension. it is important that the
            extension is <.csv>.
        :param raw: <bool> -> default: <False>
            if the argument is set to <True>, the data is stored in
            raw mode. this is sometimes difficult to read for humans.

            If <False> is passed as an argument, the data is converted
            as far as possible to a human-friendly format so that it
            can be read without the need for further tools. at the same
            time, however, care is taken to ensure that it can still be
            easily imported and used in tools such as pandas in order
            to waste as little code and time as possible in data
            preparation.

            See module <os.stat> for more information.
        """

        self._root = root
        self._exceptions_root()
        self._file = file
        self._exceptions_file()
        self._raw = raw
        self._keys = ['user_id', 'group_id', 'file_mode', 'device_identifier',
                      'created_win', 'last_access', 'last_modified',
                      'file_size', 'path']
        self._stopwatch = Stopwatch('scan')
        # counter
        self._dir_ix = 0
        self._files_ix = 0

    def get_directory_counter(self):
        """Returns the directory counter.

        :return: <int>
        """

        return self._dir_ix

    def get_files_counter(self):
        """Returns the files counter.

        :return: <int>
        """

        return self._files_ix

    def get_total_counter(self):
        """Returns the complete counter (directories + files)

        :return: <int>
        """

        return self._dir_ix + self._files_ix

    def get_all_counters(self):
        """Returns all counters in a list (total, directories, files).

        :return: <list>
        """

        return self.get_total_counter(), self.get_directory_counter(), self.get_files_counter()

    def run(self):
        """Starts a forensic scan and returns the data as <dict> in a <list>.

        :return: <list>
        """

        self._stopwatch.run()

        file = open(self._file, 'w', newline='')
        writer = csv.DictWriter(file, fieldnames=self._keys)
        writer.writeheader()

        for self._dir_ix, (root, _, files) in enumerate(os.walk(self._root), start=1):
            print(root)

            for filename in files:
                self._files_ix += 1
                path = os.path.join(root, filename)
                try:
                    data = self._run_path_processing(path)
                except FileNotFoundError:
                    continue
                writer.writerow(data)
                print(path)

        self._output_results()
        self._stopwatch.run()

    def _exceptions_file(self):
        """Exception errors for argument <file> | <self._file>."""

        path = os.path.dirname(self._file)
        _, ext = os.path.splitext(self._file)

        if isinstance(self._file, str):
            if not ext == '.csv':
                raise ValueError('file extension must be <.csv>.')
            if path and not os.access(path, os.W_OK):
                raise PermissionError('no access')
        else:
            raise TypeError('argument must be type <str>')

    def _exceptions_root(self):
        """Exception errors for argument <root> | <self._root>."""

        if isinstance(self._root, str):
            if os.path.exists(self._root):
                if not os.path.isdir(self._root):
                    raise NotADirectoryError('<root> must be a directory')
                if not os.access(self._root, os.R_OK):
                    raise PermissionError('no access')
            else:
                raise NotADirectoryError('directory does not exist')
        else:
            raise TypeError('argument must be type <str>')

    def _output_results(self):
        """Outputs a small text-based statistic of the result."""

        text = '\nscan executed: total: {:,} | directories: {:,} | files: {:,}'
        print(text.format(*self.get_all_counters()))

    def _run_path_processing(self, path):
        """Processes the path according to the user input.

        is called from method <run>

        :param path: absolute path to a directory or file
        """

        data = {}
        stat = os.stat(path)
        values = [stat.st_uid, stat.st_gid, stat.st_mode, stat.st_dev]

        if self._raw:
            values.extend([stat.st_ctime, stat.st_atime, stat.st_mtime, stat.st_size])
        else:
            values.extend(
                [
                    # importable with module <datetime.datetime.fromisoformat()>
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_ctime)),
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_atime)),
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime)),
                    # size in megabyte
                    '{:09.2f}'.format(stat.st_size / (1024 ** 2)),
                ]
            )

        values.append(path)

        for key, value in zip(self._keys, values):
            data[key] = value

        return data


class Stopwatch:
    """Measures the time between 2 points."""

    def __init__(self, operation_name=None):
        """Initalisation of the class.

        :param operation_name: <str>
            the time [hh:mm:ss] is automatically output in the terminal
            after the stop if an argument is passed here.
            Examples -> <scan>, <archiving>, <search>
        """

        self._counter = 0
        self._name = operation_name

    def get_counter(self):
        """Returns the value of the counter

        :return: <float>
        """

        return self._counter

    def get_operation_name(self):
        """Get the operation name.

        :return: <str>
        """

        return self._name

    def reset(self):
        """Reset the counter."""

        self._counter = 0
        print('counter reset')

    def run(self):
        """Starts | ends the stopwatch.

        the method can also be used as start or end. it automatically
        detects which one applies and determines the time in seconds.

        to avoid confusion, start and end are also available separately
        as methods.
        """

        if not self._counter:
            self.start()
        else:
            self.stop()

    def start(self):
        """Start the stopwatch. more detailed information in method <run>."""

        self._counter = time.perf_counter()

    def set_operation_name(self, name):
        """Set the operation name.

        :param name: <str>
        """

        self._name = name

    def stop(self):
        """Stop the stopwatch. more detailed information in method <run>."""

        self._counter = time.perf_counter() - self._counter
        if self._name:
            self._output_duration()

    def _output_duration(self):
        """Output of the duration with simple change of the operation text."""

        print('duration of the {}: {} [hh:mm:ss]'.format(self._name, self._seconds_to_hhmmss()))

    def _seconds_to_hhmmss(self):
        """Converts seconds to hh:mm:ss.

        :return: <str>
        """

        return time.strftime('%H:%M:%S', time.gmtime(self._counter))


class FileArchiving:
    """Packing and unpacking files | directories."""

    def __init__(self, input_path, output_path='data.tar.gz'):
        """Initalisation of the class.

        :param input_path: <str>
        :param output_path: <str>
        """

        self._input = input_path
        self._output = output_path
        self._stopwatch = Stopwatch('archive created')

    def create_archive(self):
        """A <tar.gz> archive is created."""

        self._stopwatch.run()

        # <file_or_dir> can be a file as well as a directory
        path, file_or_dir = os.path.split(self._input)
        # the directory is changed, otherwise the whole path is visible in the archive.
        if path:
            os.chdir(path)

        with tarfile.open(self._output, 'w:gz') as tar:
            tar.add(file_or_dir)
            self._stopwatch.run()

    def delete(self):
        """Delete the file or directory after creating the archive."""

        if tarfile.is_tarfile(self._output):
            _, file_or_dir = os.path.split(self._input)
            os.remove(file_or_dir)
            self._output_executed('deleted')

    def get_input_path(self):
        """returns the input path.

        :return: <str>
        """

        return self._input

    def get_output_path(self):
        """returns the output path.

        :return: <str>
        """

        return self._output

    def set_input_path(self, path):
        """Sets a new input path to a file or directory.

        :param path: <str>
        """

        self._input = path

    def set_output_path(self, path):
        """Sets a new output path to a file.

        :param path: <str>
        """

        self._output = path

    def _output_executed(self, operation):
        print('executed: <{}> {}'.format(os.path.basename(self._input), operation))


def _console():
    """Arguments for control via the console.

    :return: <class 'argparse.Namespace'>
    """

    parser = argparse.ArgumentParser(prog='w01fm00n')
    parser.add_argument('root', action='store', help='root directory of the scan')
    parser.add_argument('file', action='store', help='file into which the scan is to be written')
    parser.add_argument('-a', '--archive', action='store_true',
                        help='archive the <.csv> file as <.tar.gz> and then delete it.')
    parser.add_argument('-r', '--raw', action='store_true',
                        help='output in raw format -> partly difficult to read for humans')
    parser.add_argument('-v', '--version', action='version', version='version: {} ({})'.format(
        VERSION, DATE
    ))

    return parser.parse_args()


def main():
    """Main function of the program."""

    args = _console()

    if args.root and args.file:
        scan = DirectoryScanner(args.root, args.file, raw=args.raw)
        scan.run()
        if args.archive:
            archive = FileArchiving(args.file)
            archive.create_archive()
            archive.delete()
