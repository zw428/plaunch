# plaunch
Pretty Launcher

![preview](https://github.com/zw428/plaunch/blob/master/ex.png?raw=true)

`plaunch` is a minimal program launcher written in python using `pyqt5` that
displays a list of programs with images next to them.

I made this with games in mind, mostly because I have a mix of steam and
non-steam games, and I'd rather not depend on steam to launch everything.
Nothing is stopping anyone from using this for any type of media like movies or
albums/playlists, or as a program launcher.

## Usage

`python pylaunch.py filename`

File should have lines formatted as: `"image_filename","title","shell_command"`

for example, one of my lines looks like this: `"dcss.png","DCSS","crawl-tiles"`

## Using

Single click to select, arrow key navigation, double click or enter to launch

## Plans:
- add screenshot
- nicer styling
- forced image dimensions
- keyboard searching
- categories
