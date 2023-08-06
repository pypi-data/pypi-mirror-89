from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel
from rich.prompt import Prompt
from collections import defaultdict
from timeit import default_timer as timer
import os
import pathlib
import subprocess
import time
import sys

console = Console()

class MyProgress(Progress):
    success = 1
    failed = 2
    def get_renderables(self):
        yield Panel(self.make_tasks_table(self.tasks), expand=False)

class cms_item:
    def __init__(self, data_files=[], co_meta_file=None):
        self.data_files = data_files
        self.co_meta_file = co_meta_file

    """ a CMS usually contains 3 *.data files and 1 co.meta file
    Sample path for data file: ./project/cms/com/sample/authentication/Message/accessDenied/15C3E8CF5E976B46.data
    Sample path for co.meta file: ./project/cms/com/sample/authentication/Message/accessDenied/co.meta

    The unique path that is used in the program starts after 'project/cms/'
    In this case, I use path of co_meta_file, since a CMS only one co_meta_file
    """
    def get_cms_identification_path(self):
        return pathlib.Path(*self.data_files[0].parents[0].parts[1:])
    
    def get_dir(self):
        return self.co_meta_file.parents[0]
    
    def __str__(self):
        return str(self.get_dir())

class cms_cleaner:

    def __init__(self):
        self.used = 0
        self.unused = 0
        self.success = 0
        self.failed = 0
    
    def get_unused_cms(self):
        self.unused_cms = []

        with MyProgress("[progress.description]{task.description}", BarColumn(), TextColumn(text_format="[progress.percentage]{task.percentage:>3.0f}% [green]{task.completed} of {task.total} [bold green] | Used: [bold white]{task.fields[found]} | [bold red]Unused: [bold white]{task.fields[not_found]} "), "Took [bold blue]{task.fields[time_elapsed]}s") as progress:
            task = progress.add_task(total=len(self.cms_items), description='Finding unused CMS', found=0, not_found=0, time_elapsed=0)
            t = timer()
            for cms_item in self.cms_items:
                grep_cmd = 'grep -r "{}" . --include \*.java --include \*.mod --include \*.xhtml --include \*.drl'.format(cms_item.get_cms_identification_path())
                out = subprocess.Popen(grep_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                (stdout, stderr) = out.communicate()
                result = stdout.decode().split()
                self.used += 1 if len(result) > 0 else 0
                if len(result) == 0:
                    self.unused += 1
                    self.unused_cms.append(cms_item)
                progress.advance(task)
                progress.update(task, found=self.used, not_found=self.unused, time_elapsed=int(timer() - t))
        self.remove_unused_cms()

    
    def remove_unused_cms(self):
        if len(self.unused_cms) == 0:
            print("There is no unused CMS")
        else:
            choice = Prompt.ask("Do you want to clean up {} unused CMS".format(len(self.unused_cms)), choices=["Y", "N"])
            if choice == 'Y':
                failed_cms = []
                t = timer()
                with MyProgress("[progress.description]{task.description}", BarColumn(), TextColumn(text_format="[progress.percentage]{task.percentage:>3.0f}% [green]{task.completed} of {task.total} [bold green] | Success: [bold white]{task.fields[success]} | [bold red]Faied: [bold white]{task.fields[failed]} "), "Took [bold blue]{task.fields[time_elapsed]}s") as progress:
                    task = progress.add_task(total=len(self.unused_cms), description='Deleting unused CMS', success=0, failed=0, time_elapsed=0)
                    for cms_item in self.unused_cms:
                        delete_cmd = 'rm -rf {}'.format(cms_item.get_dir())
                        out = subprocess.Popen(delete_cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                        out.communicate()
                        status_code = out.poll()
                        self.success += 1 if status_code == 0 else 0
                        if status_code != 0:
                            failed_cms.append(cms_item)
                            self.failed += 1
                        progress.advance(task)
                        progress.update(task, success=self.success, failed=self.failed, time_elapsed=int(timer() - t))
                
                if len(failed_cms) > 0:
                    console.print("[bold red]These CMS are failed to delete:")
                    for cms_item in failed_cms:
                        console.print('[bold purple]' + str(cms_item))


    def get_all_cms(self):
        find_cmd = 'find . -regex ".*/cms/.*.data"'
        out = subprocess.Popen(find_cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (stdout, stderr) = out.communicate()
        file_list = stdout.decode().split()
        self.cms_items = self.__convert_cms_files_to_cms_items(file_list)
    
    def __convert_cms_files_to_cms_items(self, file_list):
        cms_item_map = defaultdict(lambda: defaultdict(lambda: []))
        for p in file_list:
            path = pathlib.Path(p)
            cms_item_map[str(pathlib.Path(*path.parents[0].parts[2:]))]['data_files'].append(p)
        
        cms_items = []
        for key in cms_item_map:
            m = cms_item_map[key]
            path = pathlib.Path(m['data_files'][0])
            co_meta_path = pathlib.Path(*path.parents[0].parts) / 'co.meta'
            data_path = [pathlib.Path(_) for _ in m['data_files']]
            cms_items.append(cms_item(data_path, co_meta_path))
        return cms_items
 
    
if __name__ == '__main__':
    path = Prompt.ask("Please enter the absolute path to your project")
    console.print("Process [bold purple]" + path)
    os.chdir(path)
    cleaner = cms_cleaner()
    cleaner.get_all_cms()
    cleaner.get_unused_cms()

