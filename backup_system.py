'''
This module is used to backup the system.
To do so, it looks the current folder and subfolders and searches for 
the new files in the system according to the current folders.
'''

# Create the project tree
from dataclasses import dataclass
import os
import shutil
from time import sleep
from typing import Union

from utils.logger import LOGGER

FAILED_FILES_PATH = 'failed_files.txt'
with open(FAILED_FILES_PATH, 'w') as failed_files:
    pass

@dataclass
class ProjectTree:
    parent: Union['ProjectTree', None]
    folders: 'list[ProjectTree]'
    files: 'list[str]'
    name: 'str'

    @property
    def fullname(self) -> str:
        return self.name
        # if self.parent is None:
        #     return self.name

        # return os.path.join(self.parent.fullname, self.name)

    def __post_init__(self):
        self._depth = 0 if self.parent is None else self.parent._depth + 1

    def to_string(self, max_depth: int = -1) -> str:
        if max_depth > 0 and self._depth > max_depth:
            return ''
        ret = f'{self.name}'
        if self.files:
            for file in self.files:
                ret += f'\n\t{file}'
        
        if self.folders:
            for folder in self.folders:
                folder_repr = folder.to_string(max_depth)
                if folder_repr == '':
                    continue

                folder_repr = folder_repr.replace('\n', '\n\t')
                ret += f'\n\t{folder_repr}'

        return ret


    def __repr__(self) -> str:
        return self.to_string()

def create_project_tree(tree_path: str, base_path_remove: str, parent: Union[ProjectTree, None]) -> ProjectTree:
    '''
    This function creates the project tree.
    '''

    # Remove base path from the tree path
    tree_path = tree_path.replace(base_path_remove, '') or '.'
    tree_path = os.path.normpath(tree_path)

    # Create the project tree
    LOGGER.log_trace(f'Creating project tree for {tree_path=}')
    folder_tree = ProjectTree(parent=parent, folders=[], files=[], name=tree_path)

    # Get the files and folders in the current folder
    prefixed = lambda basename: os.path.join(tree_path, basename)

    files = [file for file in os.listdir(tree_path) if os.path.exists(prefixed(file)) and os.path.isfile(prefixed(file))]
    folders = [folder for folder in os.listdir(tree_path) if os.path.exists(prefixed(folder)) and os.path.isdir(prefixed(folder))]

    # Add the files and folders to the folder tree
    folder_tree.files = files

    # Add the folders to the folder tree
    for folder in folders:
        folder_tree.folders.append(create_project_tree(
            tree_path=os.path.join(tree_path, folder),
            base_path_remove=base_path_remove,
            parent=folder_tree
        ))

    # Return the folder tree
    return folder_tree

def remove_project_ignored_files(project_tree: ProjectTree, ignored_files: 'list[str]') -> None:
    '''
    This function removes the ignored files from the project tree.
    '''
    # Remove the ignored files and folders from the project tree
    project_tree.files = [file for file in project_tree.files if file not in ignored_files]

    # print([os.path.join(project_tree.name, os.path.basename(folder.name)) for folder in project_tree.folders])
    invalid_folders = [ os.path.normpath(os.path.join(project_tree.name, invalid_folder)) for invalid_folder in ignored_files ]
    project_tree.folders = [ folder for folder in project_tree.folders if folder.name not in invalid_folders ]


def copy_folder_tree_from_system(folder_tree: ProjectTree, system_root: str, dest_path: str) -> None:
    '''
    This function copies the folder tree from the system.
    '''

    LOGGER.log_trace(f'@copy_folder_tree_from_system: {folder_tree.fullname=}')

    # Create the folder in the destination path
    LOGGER.log_trace(f'Creating destination folder {dest_path}')
    dest_folder_fullname = os.path.join(dest_path, folder_tree.fullname)
    if not os.path.exists(dest_folder_fullname):
        # Create the folder recursively
        os.makedirs(dest_folder_fullname)
    
    # Copy the files in the folder tree
    LOGGER.log_trace(f'Inner files: {folder_tree.files=}')
    for file in folder_tree.files:
        file_fullname = os.path.normpath(os.path.join(folder_tree.fullname, file))
        dest_file_fullname = os.path.normpath(os.path.join(dest_path, folder_tree.fullname, file))
        system_file_fullname = os.path.normpath(os.path.join(system_root, folder_tree.fullname, file))
        


        LOGGER.log_trace(f'Copying file {file_fullname} from {system_file_fullname} to {dest_file_fullname}')
        if not os.path.exists(system_file_fullname):
            LOGGER.log_error(f'File {file_fullname} does not exist in {system_file_fullname}')
            with open(FAILED_FILES_PATH, 'a') as failed_files:
                failed_files.write(f'{file_fullname}\n')
            continue

        # Check for permissions
        # if not os.access(system_file_fullname, os.R_OK):
        #     LOGGER.log_error(f'File {file_fullname} is not readable in {system_file_fullname}')
        #     continue

        # if not os.access(dest_file_fullname, os.W_OK):
        #     LOGGER.log_error(f'File {file_fullname} is not writable in {dest_file_fullname}')
        #     continue
            
        shutil.copy(system_file_fullname, dest_file_fullname)
        # os.copy(os.path.join(system_root, folder_tree.name, file), os.path.join(dest_path, folder_tree.name, file))

    # Copy the folders in the folder tree
    for folder in folder_tree.folders:
        copy_folder_tree_from_system(folder, system_root, os.path.join(dest_path, folder_tree.name))


# Create the backup
def backup(tree_path: str, sys_path: str, dest_path: 'str') -> 'None':
    '''
    This function creates the backup.
    '''
    LOGGER.log_info(f'Backuping the system from {sys_path} to {dest_path}')

    # Create the project tree
    LOGGER.log_trace(f'Creating the project tree from {tree_path}')
    project_tree = create_project_tree(
        tree_path=tree_path, # /home/user/project
        base_path_remove=tree_path, # e.g. /home/user/project/folder -> folder
        parent=None # Root folder doesn't have a parent
    )

    if os.path.commonpath([tree_path, dest_path]) == tree_path:
        LOGGER.log_error(f'The destination path {dest_path} is inside the tree path {tree_path}')
        raise Exception(f'The destination path {dest_path} is inside the tree path {tree_path}')

    IGNORED_FILES_AND_FOLDERS = ['.gitignore', '.git', '.vscode', 'backup_system.py', 'requirements.txt', '__pycache__', FAILED_FILES_PATH]

    remove_project_ignored_files(project_tree, IGNORED_FILES_AND_FOLDERS)

    LOGGER.log_trace(f'Project tree created')
    LOGGER.log_trace(f'Project tree: \n{project_tree.to_string(1)}')

    if os.path.exists(dest_path) and os.path.isdir(dest_path):
        print('Destination path already exists')
        input(f'Press enter to delete {dest_path} ...')
        shutil.rmtree(dest_path)
        os.mkdir(dest_path)

    LOGGER.log_trace(f'Copying the project tree from {sys_path} to {dest_path}')
    sleep(1)
    copy_folder_tree_from_system(project_tree, sys_path, dest_path)

if __name__ == '__main__':
    cwd = os.getcwd()
    backup(
        tree_path=cwd,
        sys_path='/',
        dest_path='/home/marucs/testbkpdelme'
    )