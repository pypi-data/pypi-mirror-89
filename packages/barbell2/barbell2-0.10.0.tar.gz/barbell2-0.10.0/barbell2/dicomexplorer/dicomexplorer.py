import os
import pydicom
from pydicom._dicom_dict import DicomDictionary
from barbell2.lib import BasicShell


INTRO = """
Welcome to the DICOM Explorer!
------------------------------
This tool allows you to explore lots of DICOM files at the same time. Type 'help' to view a short list of
commands. Type 'help <command>' to view details about a given command.
"""

PROMPT = '(shell) '


def is_dicom(file_path):
    if not os.path.isfile(file_path):
        return False
    try:
        with open(file_path, "rb") as f:
            return f.read(132).decode("ASCII")[-4:] == "DICM"
    except:
        return False


class DicomExplorerShell(BasicShell):

    def __init__(self):
        super(DicomExplorerShell, self).__init__()
        self.intro = INTRO
        self.prompt = PROMPT
        self.debug = True

    # LOADING FILES AND DIRECTORIES

    def do_load_file(self, file_path):
        """
        Usage: load_file <file name or path>
        Load a single DICOM file. If only the name is provided, it assumed that the file is located in the
        current directory.
        """
        if not os.path.isfile(file_path):
            file_path = os.path.join(self.current_dir, file_path)
        if not is_dicom(file_path):
            self.poutput('File is not DICOM')
            return
        self.poutput('Loading...')
        self.result_manager.add_result_data([file_path])
        self.poutput('Loading done')

    def do_load_dir(self, dir_path):
        """
        Usage: load_dir <dir name or path>
        Load (recursively) all DICOM files in the given directory. If only the directory name is given, it is
        assumed that the directory is located in the current directory.
        """
        if not os.path.isdir(dir_path):
            dir_path = os.path.join(self.current_dir, dir_path)
        self.poutput('Loading {}...'.format(dir_path))
        data = []
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if not f.startswith('._'):
                    f = os.path.join(root, f)
                    if is_dicom(f):
                        data.append(f)
        self.result_manager.add_result_data(data)
        self.poutput('Loading done')

    def do_show_files(self, n):
        """
        Usage: show_files [n]
        Show all (or first n) files loaded in the current result set. If you want to show files from another result set
        select it first using the set_current_result command.
        """
        files = self.result_manager.get_current_result_data()
        n = -1 if n == '' else int(n)
        count = 0
        for f in files:
            self.poutput(f)
            if count == n:
                break
            count += 1
        self.poutput('Total nr. of files: {}'.format(len(files)))

    def do_lookup(self, tag_name):
        """
        Usage: lookup <tag name>
        Lookup tag <tag name> in the DICOM dictionary. You can specify only parts of a tag name, e.g.,
        "Transmit" will return multiple dictionary entries containing the word "Transmit" (like Transmit
        Coil Name). Being able to lookup tags comes in handy when you search for them in DICOM files.
        Note that (parts of) the tag name does not have to be case-sensitive.
        """
        for key, value in DicomDictionary.items():
            output = '{}: {}'.format(key, value)
            if tag_name == '':
                self.poutput(output)
            else:
                for item in value:
                    if tag_name in item:
                        self.poutput(output)

    def do_find_tag(self, tag_name):
        """
        Usage: find_tag <tag name>
        Find tag <tag name> in the currently loaded DICOM files.
        """
        files = self.result_manager.get_current_result_data()
        for f in files:
            p = pydicom.read_file(f)
            for tag in p.keys():
                if tag in list(DicomDictionary.keys()):
                    if tag_name == DicomDictionary[tag][4]:
                        self.poutput('{}: {}'.format(f, p[tag].value))
                        break
                else:
                    self.poutput('Warning: tag {} cannot be found in the DICOM dictionary'.format(tag))

    def do_show_header(self, file_name):
        """
        Usage: show_header <file name>
        Show DICOM header of <file name>. If <file name> is left empty, this function will search for
        all file paths that contain the given file name. If only one is encountered, the DICOM header will
        be displayed. If multiple files are encountered, a list of those files is displayed so that you can
        select a specific one (with its full path).
        """
        files = self.result_manager.get_current_result_data()
        count = 0
        counted_files = []
        for f in files:
            if file_name in f:
                count += 1
                counted_files.append(f)
        if count == 0:
            if os.path.isfile(file_name):
                p = pydicom.read_file(file_name)
                self.poutput(p)
            else:
                self.poutput('Could not find file {}'.format(file_name))
        elif count == 1:
            p = pydicom.read_file(counted_files[0])
            self.poutput(p)
        elif count > 1:
            self.poutput('Found multiple files with same name:')
            for f in counted_files:
                self.poutput(f)
            self.poutput('Please select full file path of file you want and repeat this command')

    def do_check_pixels(self, _):
        """
        Usage: check_pixels
        Check that each DICOM file contains pixel values that can be loaded using pydicom and NumPy. Sometimes,
        images may be compressed in some way (e.g., using JPEG2000). In that case, they cannot be loaded with
        pydicom and their pixel values need to be extracted to raw format.
        """
        files = self.result_manager.get_current_result_data()
        count = 0
        for f in files:
            p = pydicom.read_file(f)
            try:
                p.convert_pixel_data()
                self.poutput('OK: {}'.format(f))
            except NotImplementedError:
                count += 1
                self.poutput('ERROR: could not load pixel data {}'.format(f))
        self.poutput('Pixel data for {} out of {} files could not be loaded'.format(count, len(files)))


def main():
    import sys
    shell = DicomExplorerShell()
    sys.exit(shell.cmdloop())


if __name__ == '__main__':
    main()
