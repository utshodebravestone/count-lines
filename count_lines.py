import os
import shutil
import click


class Output:
    def __init__(self, filepath: str, lines: int, empty_lines: int):
        self.filepath = filepath
        self.lines = lines
        self.empty_lines = empty_lines

    def __str__(self):
        return f'file: {self.filepath}, lines:{self.lines}, empty lines: {self.empty_lines}'


def count_lines_in_a_file(filepath) -> Output:
    try:
        with open(filepath, mode='r') as file:
            lines = file.read().split('\n')
            newlines = filter(lambda line: line.isspace() or line == '', lines)
            return Output(filepath, len(lines), len(list(newlines)))
    except FileNotFoundError:
        click.echo(f'File \'{filepath}\' not found.')


@click.command()
@click.argument('directory', nargs=1)
@click.option('--skip-empty', is_flag=True,
              help='Skip empty lines.')
@click.option('--skip-dirs', type=str,
              help='Skip given directories. Take directories as strings separated by comma(s) (\',\').')
def count_lines(directory: str, skip_empty, skip_dirs: str):
    """A CLI tool that counts lines on files that exists in a given DIRECTORY."""

    outputs: list[Output] = []
    total_line_count = 0
    skip_dirs = set(map(
        lambda directory: directory.strip(), skip_dirs.split(','))) if skip_dirs is not None else set()

    for parent, _, files in os.walk(directory):
        parents = parent.split('/')
        if len(skip_dirs.intersection(parents)) > 0:
            continue
        try:
            for file in files:
                filepath = f'{parent}/{file}'
                outputs.append(count_lines_in_a_file(filepath))
        except Exception as e:
            click.echo(f'Exception: {e}', err=True)

    for output in outputs:
        if skip_empty:
            line_count = output.lines - output.empty_lines
        else:
            line_count = output.lines

        click.echo(f'File {output.filepath} ::  {line_count}')
        total_line_count += line_count

    click.echo('-' * shutil.get_terminal_size().columns)
    click.echo(
        f'Total counted lines (on directory \'{directory}\') :: {total_line_count}.')


if __name__ == '__main__':
    count_lines()
