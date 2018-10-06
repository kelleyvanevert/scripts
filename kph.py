#!/usr/bin/python

import click
import os
import sys
import textwrap

sys.path.append('/home/kelley/documents/code')
from kph.transforms import Transform
from kph.films import films


fish_function_dir  = "/home/kelley/.config/fish/functions"
sys.path.append(fish_function_dir)



p = click.echo # "print"

e = os.system  # "execute"
d = textwrap.dedent

# "execute multiline command"
def em(string):
  e(d(string))


class AliasedGroup(click.Group):

  # make sure commands are listed in the order in which they were added

  def __init__(self, name=None, commands=None, **attrs):
    click.Group.__init__(self, name, commands, **attrs)
    self.commands_add_order = []

  def add_command(self, cmd, name=None):
    click.Group.add_command(self, cmd, name)
    name = name or cmd.name
    self.commands_add_order.append(name)

  def list_commands(self, ctx):
    return sorted(self.commands, key=lambda t: self.commands_add_order.index(t))

  # make commands accessible by prefixes

  def get_command(self, ctx, cmd_name):
    rv = click.Group.get_command(self, ctx, cmd_name)
    if rv is not None:
      return rv
    matches = [x for x in self.list_commands(ctx)
                       if x.startswith(cmd_name)]
    if not matches:
      return None
    elif len(matches) == 1:
      return click.Group.get_command(self, ctx, matches[0])
    ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS, cls=AliasedGroup, help="""

  The commands prepended with an @ are proxies to fish functions residing in `%s`

""" % fish_function_dir)
@click.pass_context
def cli(ctx):

  if ctx.invoked_subcommand is None:
    e("kph.py -h") # ugly, but I can't find out another way
  else:
    pass


class color:
  PURPLE    = '\033[95m'
  CYAN      = '\033[96m'
  DARKCYAN  = '\033[36m'
  BLUE      = '\033[94m'
  GREEN     = '\033[92m'
  YELLOW    = '\033[93m'
  RED       = '\033[91m'
  BOLD      = '\033[1m'
  UNDERLINE = '\033[4m'
  END       = '\033[0m'

command = cli.command
option = click.option
argument = click.argument


@command('video', short_help = 'Transform videos')
@option('-s', '--stabilize', is_flag = True, help = 'Stabilization')
@option('-w', '--widescreen', is_flag = True, help = 'If set, crops to cinematic 1:2.4 widescreen format')
@option('-D', '--delete', is_flag = True, help = 'Delete .MOV files directly after transform')
@option('-q', '--quality', default = 18, help = 'H.264 crf (0=lossless .. 51=worst), defaults to 18')
def video(stabilize, widescreen, delete, quality):
  p('Transforming video...')

  crop = 'in_w:in_h-280' if widescreen else 'in_w:in_h'

  ffmpeg = 'ffmpeg' # '/home/kelley/bin/ffmpeg'
                    # => self-built ffmpeg needed for libvidstab

  first_pass_detect_shake = d("""\
    if [ ! -e $f.trf ]; then
      echo "> Detecting shake...";
      %s -i $f -vf vidstabdetect=shakiness=8:result="$f.trf" -f null -;
    fi;
  """ % ffmpeg) if stabilize else ""

  remove_shake_vf = '-vf "%s unsharp=5:5:0.8:3:3:0.4, crop=%s"' % ('vidstabtransform=input="$f.trf", ' if stabilize else '', crop)

  em("""\
    mkdir -p t %s;
    for f in *.MOV; do
      echo "Converting $f...";
      %s
      echo "> Transcoding...";
      %s -i $f -c:v libx264 -profile:v high -crf %s %s -c:a aac -strict experimental "t/${f%%.*}.mp4";
      %s
    done
  """ % ("" if delete else "done", first_pass_detect_shake, ffmpeg, quality, remove_shake_vf, "rm $f;" if delete else "mv $f done;"))


@command('resize', short_help = 'Resize photos')
@option('-v', '--verbosity', default=2)
@option('-s', '--size', default=1280)
@option('-p', '--preserve-noise', is_flag = True, help = 'Use -sample instead of -resize to preserve noise')
@option('-d', '--output-directory', default='AUTO')
@option('-D', '--density', default = -1)
@option('-f', '--output-filetype', default = 'jpg')
def resize(verbosity, size, preserve_noise, output_directory, density, output_filetype):
  if output_directory == 'AUTO':
    output_directory = 's%s%s' % (size, "p" if preserve_noise else "")
  p('Resizing images [size = %s, out dir = %s]...' % (size, output_directory))

  density = "" if density is -1 else ("-density %s" % density)

  em("""\
    export v=%s;
    if ls *.jpg 1> /dev/null 2>&1; then
      mkdir -p "%s";
      for f in *.jpg; do
        if [ -f "%s/${f%%.*}.%s" ]; then
          if [ "$v" -gt 1 ]; then
            echo "$f (exists)";
          fi;
        else
          echo -n "$f...";
          convert "$f" -%s %sx%s %s "%s/${f%%.*}.%s";
          echo " DONE";
        fi;
      done;
      echo "  DONE";
    else
      echo "(No files)";
    fi;
  """ % (verbosity, output_directory, output_directory, output_filetype, "sample" if preserve_noise else "resize", size, size, density, output_directory, output_filetype))


@command('film', short_help = 'Film emulation')
@option('-v', '--verbosity', default=2)
@option('-l', '--list-films', is_flag = True, help = 'List all available films')
@option('-f', '--film', default='fs1', help = "Default Fuji Superia 100. Use -l to list all films")
@option('-g', '--grain', is_flag = True, help = "Add grain")
def film(verbosity, list_films, film, grain):
  if not list_films and film not in films.DICT:
    p("Invalid film, choose from:")
    list_films = True

  if list_films:
    p("\n======================================= BLACK AND WHITE FILMS ======================================")
    l = ["%6s (%s)" % (a, c) for (a, (b, c)) in films.BW]
    for a, b, c in zip(l[::3], l[1::3], l[2::3]):
      p('  {:<33}{:<33}{:<}'.format(a,b,c))

    p("\n============================================ COLOR FILMS ===========================================")
    l = ["%6s (%s)" % (a, c) for (a, (b, c)) in films.COLOR]
    for a, b, c in zip(l[::3], l[1::3], l[2::3]):
      p('  {:<33}{:<33}{:<}'.format(a,b,c))
    return

  outdir = "film-" + film + ("-grain" if grain else "")
  cmd = films.DICT[film][0]
  grain_cmd = "-gimp_emulate_grain 1,1,0.2,100,0,0,1,0,0,0,0,0" if grain else ""
  p("Applying film emulation [%s]...\n (gmic <IN> %s -o <OUT>)" % (films.DICT[film][1], cmd))
  em("""\
    export v=%s;
    mkdir -p %s;
    if ls *.jpg 1> /dev/null 2>&1; then export ext=jpg; else export ext=png; fi;
    for f in *.$ext; do
      if [ -f %s/$f ]; then
        if [ "$v" -gt 1 ]; then
          echo "$f (exists)";
        fi;
      else
        echo -n "$f...";
        gmic -v -1 $f %s %s -o %s/$f;
        echo " DONE";
      fi;
    done;
    echo "  DONE";
  """ % (verbosity, outdir, outdir, cmd, grain_cmd, outdir))



@command('transform', short_help = 'Apply transformations')
@option('-l', '--list-transforms', is_flag = True, help = 'List known transformations')
@argument('transformation', default = 'nope')
@argument('files', default = '*') # , type = click.Path(exists = True)
def transform(list_transforms, transformation, files):
  if list_transforms:
    for t in Transform.KNOWN_TRANSFORMS:
      p(color.BOLD + t + color.END)
      p(Transform.KNOWN_TRANSFORMS[t].__doc__)
    return

  try:
    t = Transform.parse(transformation)
  except Exception, e2:
    p("ERROR:\n  Couldn't parse transformation:")
    p("  - " + transformation)
    print e2
    return

  p(color.BOLD + "\nTRANSFORMATION TREE:" + color.END)
  p(t.tree())

  p(color.BOLD + "\nCOMMAND:" + color.END)
  p(t.cmd())

  if click.confirm("\nShall we continue?"):
    p(color.BOLD + "\nOK GO!" + color.END)
    e(t.cmd())



'''
@command('watermark', short_help='Add watermarks to photos')
@option('-d', '--output-directory', default='w')
@option('-f', '--force', is_flag=True)
def watermark(output_directory, force):
  click.echo('Adding watermarks [out dir = %s]...' % output_directory)
  em("""\
    bg_size=3872x2574;
    mkdir -p %s;

    for f in *.jpg; do
      if [ -f %s/$f ] && %s; then
        echo "$f (exists)";
      else
        echo -n "$f...";
        composite -size $bg_size -gravity center -compose atop /home/kelley/photos/res/watermark.png $f %s/$f;
        echo "DONE";
      fi;
    done
  """ % (output_directory, output_directory, str(not force).lower(), output_directory))
'''


@command('test', short_help = 'Test args etc')
@option('-d', '--output-directory', default='.')
@option('-f', '--force', is_flag=True)
def test(output_directory, force):
  p('Args:')
  p('- output directory: %s' % output_directory)
  p('- force: %s' % force)

  em("""\
    for f in *.MOV; do
      echo "Converting $f...";
    done
  """)





def make_fish_proxy(fish_fn_name):
  module = __import__(fish_fn_name)

  short_help = module.short_help if hasattr(module, "short_help") else "(fish proxy)"
  help = module.help if hasattr(module, "help") else "(no help available)"
  
  @command("@" + fish_fn_name, short_help=short_help, help=help)
  @argument("args", nargs=-1)

  def _function(args):
    args = " ".join([ str(s) for s in args ])
    cmd = 'fish -c "%s %s"' % (fish_fn_name, args)
    #p(cmd)
    e(cmd)



if __name__ == '__main__':

  for root, dirs, files in os.walk(fish_function_dir):
    for file in files:
      s = os.path.splitext(file)
      if s[1] == ".py":
        fish_fn_name = s[0]
        make_fish_proxy(fish_fn_name)

  cli()
