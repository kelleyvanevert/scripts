#!/usr/bin/python
# -*- coding: utf-8 -*-

import textwrap
from abc import ABCMeta, abstractmethod
import pyparsing as pp
import sys
import operator

from kph.films import films


name = pp.Word(pp.alphas).setResultsName("name")
params = pp.Group(pp.ZeroOrMore(pp.Word(pp.alphanums + ".,_"))).setResultsName("params")

ops = pp.Forward()
op = (name + params + pp.Group(ops).setResultsName("ops") | pp.Empty()).setResultsName("op")
ops << pp.ZeroOrMore((pp.Literal("(").suppress() + pp.Group(op) + pp.Literal(")").suppress()).setParseAction(lambda t: t))
#print op.parseString("kelley julia (film fs16) (film fs8)", parseAll=True)['op']['ops']

START = op
#START = op | pp.Literal("(").suppress() + op + pp.Literal(")").suppress()



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



class TreeNode:

  # pre-order
  def methodreduce_pre(self, method, join_op, depth = 0, index = 0, width = 1):
    results = [getattr(self, method)(depth, index, width)] + \
      [ child.methodreduce_pre(method, join_op, depth + 1, index, len(self.children)) for index, child in enumerate(self.children) ]
    return reduce(join_op, results)

  # post-order
  def methodreduce_post(self, method, join_op, depth = 0, index = 0, width = 1):
    results = [ child.methodreduce_post(method, join_op, depth + 1, index, len(self.children)) for index, child in enumerate(self.children) ] \
      + [getattr(self, method)(depth, index, width)]
    return reduce(join_op, results)




class Transform(TreeNode):

  KNOWN_TRANSFORMS = {}

  # actually private => use [make]
  def __init__(self, name, params = [], children = []):
    self.name = name
    self.params = params
    self.children = children

    self.tmp_dir = "./"
    if self.name is not "id":
      self.tmp_dir += "transformed/" + str(self) + "/"

    self.validate()

  @staticmethod
  def make(name, params = [], children = []):
    if name in Transform.KNOWN_TRANSFORMS:
      return Transform.KNOWN_TRANSFORMS[name](name, params, children)
    else:
      raise NotImplementedError("Transform [%s] not known" % name)

  def __str__(self):
    if self.name is 'id':
      return '()'
    else:
      return "(" + " ".join([self.name] + self.params + [ str(t) for t in self.children ]) + ")"

  def __unicode__(self):
    return unicode(self)

  def str_command(self):
    return " ".join([self.name] + self.params)

  def to_str_lines(self, depth, index, width):
    indent = "   " * (depth - 1)
    if depth is 0:
      branch = ""
    else:
      branch = u"└─ " if index is width - 1 else u"├─ "
    return [indent + branch + self.str_command()]

  def tree(self):
    return "\n".join(self.methodreduce_pre("to_str_lines", operator.add))

  @abstractmethod
  def cmd_lines(self):
    raise NotImplementedError("Transform method [cmd_lines] must be implemented")

  def _cmd_lines_decorate(self, depth, index, width):
    if self.name is "id":
      return []
    return [
      '  if [ -f "%s$f" ]; then' % self.tmp_dir,
      '    echo "    %s (exists)"' % self.name,
      '  else',
      '    echo -n "    %s..."' % self.name
      ] + [ "    " + l for l in self.cmd_lines() ] + [
      '    echo " DONE"',
      '  fi'
      ]

  def _ensure_dir_exists(self, depth, index, width):
    return ['mkdir -p "%s"' % self.tmp_dir]

  def cmd(self):
    return "" + \
      'echo "Creating directories..."\n' + \
      "\n".join(self.methodreduce_pre("_ensure_dir_exists", operator.add)) + "\n" + \
      'echo "Processing photos..."\n' + \
      "for f in *.jpg; do\n" + \
      '  echo "  $f..."\n' + \
      "\n".join(self.methodreduce_post("_cmd_lines_decorate", operator.add)) + "\n" + \
      "done\n" + \
      'echo "DONE!"'

  # may be overridden
  def validate(self):
    return True

  @staticmethod
  def parse(str):
    try:
      r = START.parseString(str, parseAll = True)
    except:
      return False

    return Transform._fromParseResults(r)

  @staticmethod
  def _fromParseResults(r):
    if r.name is '':
      return Transform.make("id")
    else:
      return Transform.make(r.name, r.params.asList(), [ Transform._fromParseResults(r2) for r2 in r.ops ])


class IdentityTransform(Transform):
  """
    Identity transform
  """

  def cmd_lines(self):
    return []

Transform.KNOWN_TRANSFORMS["id"] = IdentityTransform


class BlendTransform(Transform):
  """
    Blend two images
      blend <PERCENTAGE> <MODE> () ()
  """

  KNOWN_BLEND_MODES = ["lighten", "blend"]

  def cmd_lines(self):
    return ['composite -blend %s%% -compose %s "%s$f" "%s$f" "%s$f"' % \
      tuple([self._percentage, self._mode] + [ t.tmp_dir for t in self.children ] + [ self.tmp_dir ])]

  def validate(self):
    # num children
    if len(self.children) is not 2:
      raise Exception("Blend transform takes 2 arguments")

    # percentage
    try:
      self._percentage = int(self.params[0])
      if self._percentage < 0 or self._percentage > 100:
        raise Exception
    except:
      raise Exception("Blend param #1 must be an integer in the range 0 .. 100")

    # mode
    self._mode = self.params[1]
    if self._mode not in BlendTransform.KNOWN_BLEND_MODES:
      raise Exception("Blend param #2 (%s) must be a valid blend mode, i.e. one of: " % self._mode + ", ".join(BlendTransform.KNOWN_BLEND_MODES))

Transform.KNOWN_TRANSFORMS["blend"] = BlendTransform


class FilmTransform(Transform):
  """
    Film emulation
      film <FILM> ()

    For a list of films:
      kph f -l
  """

  def cmd_lines(self):
    return ['gmic -v -1 "%s$f" %s -o "%s$f"' % (self.children[0].tmp_dir, self._film, self.tmp_dir)]

  def validate(self):
    # num children
    if len(self.children) is not 1:
      raise Exception("Film transform takes 1 argument")

    if self.params[0] not in films.DICT:
      raise Exception("Film param #1 (%s) is not a valid film" % self.params[0])
    self._film = films.DICT[self.params[0]][0]

Transform.KNOWN_TRANSFORMS["film"] = FilmTransform


class DarktableTransform(Transform):
  """
    Darktable transform
      dt <XMP_FILE> ()
  """

  def cmd_lines(self):
    return ['darktable-cli "%s$f" %s "%s$f"' % (self.children[0].tmp_dir, self._xmp, self.tmp_dir)]

  def validate(self):
    # num children
    if len(self.children) is not 1:
      raise Exception("Darktable transform takes 1 argument")

    # xmp file existence -- TODO
    self._xmp = self.params[0]

Transform.KNOWN_TRANSFORMS["dt"] = DarktableTransform


#print Transform.parse("blend .5 lighten (dt darken.xmp (film fs16 ()))")

#t = Transform("blend", [".5", "lighten"])
#print t.tmp_dir
