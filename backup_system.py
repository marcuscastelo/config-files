'''
This module is used to backup the system.
To do so, it looks the current folder and subfolders and searches for 
the new files in the system according to the current folders.
'''

# Create the project tree
from dataclasses import dataclass
from datetime import datetime
import os
import shutil
from time import sleep
from typing import Union

from utils.logger import LOGGER

FAILED_FILES_PATH = 'failed_files.txt'
with open(FAILED_FILES_PATH, 'w') as failed_files:
    pass

BACKUP_FOLDER = 'backup'

@dataclass
class ProjectTree:
    base_path: str
    parent: Union['ProjectTree', None]
    folders: 'list[ProjectTree]'
    files: 'list[str]'
    name: 'str'

   

    @property
    def relative_path(self) -> str:
        if self.parent is None:
            return self.name

        return os.path.join(self.parent.relative_path, self.name)

    @property
    def abs_path(self) -> str:
        return os.path.join(self.base_path, self.relative_path)

    def __post_init__(self):
        self._depth = 0 if self.parent is None else self.parent._depth + 1

    def to_string(self, max_depth: int = -1) -> str:
        if max_depth > 0 and self._depth > max_depth:
            return ''
        ret = f'{self.relative_path}'
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

def create_project_tree(tree_real_path: str, base_path: str, parent: Union[ProjectTree, None]) -> ProjectTree:
    '''
    This function creates the project tree.
    '''

    # Remove base path from the tree path
    tree_proj_path = tree_real_path.replace(base_path, '') or '.'
    tree_proj_path = tree_proj_path.lstrip('/')
    tree_proj_path = tree_proj_path.lstrip('\\')
    tree_proj_path = tree_proj_path.rstrip('/')
    tree_proj_path = tree_proj_path.rstrip('\\')

    tree_proj_path = os.path.normpath(tree_proj_path)

    # Create the project tree
    LOGGER.log_trace(f'Creating project tree for {tree_proj_path=}')
    folder_tree = ProjectTree(base_path=base_path, parent=parent, folders=[], files=[], name=os.path.basename(tree_proj_path))

    # Get the files and folders in the current folder
    prefixed_real = lambda basename: os.path.join(tree_real_path, basename)

    files = [file for file in os.listdir(tree_real_path) if os.path.exists(prefixed_real(file)) and os.path.isfile(prefixed_real(file))]
    folders = [folder for folder in os.listdir(tree_real_path) if os.path.exists(prefixed_real(folder)) and os.path.isdir(prefixed_real(folder))]

    # Add the files and folders to the folder tree
    folder_tree.files = files

    # Add the folders to the folder tree
    for folder in folders:
        folder_tree.folders.append(create_project_tree(
            tree_real_path=os.path.join(tree_real_path, folder),
            base_path=base_path,
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
    invalid_folders = [ os.path.normpath(os.path.join(project_tree.relative_path, invalid_folder)) for invalid_folder in ignored_files ]
    project_tree.folders = [ folder for folder in project_tree.folders if folder.relative_path not in invalid_folders ]


def copy_folder_tree_from_system(folder_tree: ProjectTree, system_root: str, dest_root: str) -> None:
    '''
    This function copies the folder tree from the system.
    '''

    LOGGER.log_trace(f'@copy_folder_tree_from_system: {folder_tree.relative_path=}, {system_root=}, {dest_root=}')
    rel_path = folder_tree.relative_path
    dest_folder = os.path.normpath(os.path.join(dest_root, rel_path))

    # Create the folder in the destination path
    LOGGER.log_trace(f'Creating destination folder {dest_folder}')
    if not os.path.exists(dest_folder):
        # Create the folder recursively
        os.makedirs(dest_folder)
    
    # Copy the files in the folder tree
    LOGGER.log_trace(f'Inner files: {folder_tree.files=}')
    for file in folder_tree.files:
        relative_path = os.path.join(rel_path, file)

        file_fullname = os.path.normpath(os.path.join(relative_path))
        dest_file_fullname = os.path.normpath(os.path.join(dest_root, relative_path))
        system_file_fullname = os.path.normpath(os.path.join(system_root, relative_path))

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
        LOGGER.log_trace(f'Recurse in inner folder: {folder.relative_path=}')
        copy_folder_tree_from_system(
            folder_tree=folder, 
            system_root=system_root,
            dest_root=dest_root,
        )
        # break


# Create the backup
def backup(tree_path: str, sys_path: str, dest_path: 'str') -> 'None':
    '''
    This function creates the backup.
    '''
    LOGGER.log_info(f'Backuping the system from {sys_path} to {dest_path}')

    # Create the project tree
    LOGGER.log_trace(f'Creating the project tree from {tree_path}')
    project_tree = create_project_tree(
        tree_real_path=tree_path, # /home/user/project
        base_path=tree_path, # e.g. /home/user/project/folder -> folder
        parent=None # Root folder doesn't have a parent
    )

    IGNORED_FILES_AND_FOLDERS = ['.gitignore', '.git', '.vscode', 'backup_system.py', 'requirements.txt', '__pycache__', FAILED_FILES_PATH, BACKUP_FOLDER]
    remove_project_ignored_files(project_tree, IGNORED_FILES_AND_FOLDERS)

    LOGGER.log_trace(f'Project tree created')
    LOGGER.log_trace(f'Project tree: \n{project_tree.to_string(1)}')


    if dest_path == tree_path:
        os.rename(tree_path, f'{tree_path}_backup_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')
    elif os.path.commonpath([tree_path, dest_path]) == tree_path:
        LOGGER.log_error(f'The destination path {dest_path} is inside the tree path {tree_path}')
        raise Exception(f'The destination path {dest_path} is inside the tree path {tree_path}')

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
        tree_path=os.path.join(cwd, 'backup_old'),
        sys_path=os.path.join(cwd, '/'),
        dest_path=os.path.join(cwd, 'backup2')
    )


# TODO: if not foudn on sys_path, copy from tree_path (to avoid removing valid files)
# TODO: "install" tree_path to sys_path (reverse of backup)