#!/usr/bin/python
# -*- coding: utf-8 -*-

class films:

  BW = [
    ("aa1",    ("-gimp_emulate_film_bw  1,1,0,1,0,0,0,0,0,0",  "Agfa APX 100")),
    ("aa25",   ("-gimp_emulate_film_bw  2,1,0,1,0,0,0,0,0,0",  "Agfa APX 25")),
    ("fn16",   ("-gimp_emulate_film_bw  3,1,0,1,0,0,0,0,0,0",  "Fuji Neopan 1600")),
    ("fna1",   ("-gimp_emulate_film_bw  4,1,0,1,0,0,0,0,0,0",  "Fuji Neopan Acros 100")),
    ("id1",    ("-gimp_emulate_film_bw  5,1,0,1,0,0,0,0,0,0",  "Ilford Delta 100")),
    ("id32",   ("-gimp_emulate_film_bw  6,1,0,1,0,0,0,0,0,0",  "Ilford Delta 3200")),
    ("id4",    ("-gimp_emulate_film_bw  7,1,0,1,0,0,0,0,0,0",  "Ilford Delta 400")),
    ("if.125", ("-gimp_emulate_film_bw  8,1,0,1,0,0,0,0,0,0",  "Ilford FP4 Plus 125")),
    ("ihp4",   ("-gimp_emulate_film_bw  9,1,0,1,0,0,0,0,0,0",  "Ilford HP5 Plus 400")),
    ("ih8",    ("-gimp_emulate_film_bw 10,1,0,1,0,0,0,0,0,0",  "Ilford HPS 800")),
    ("ipp.50", ("-gimp_emulate_film_bw 11,1,0,1,0,0,0,0,0,0", "Ilford Pan F Plus 50")),
    ("ixp2",   ("-gimp_emulate_film_bw 12,1,0,1,0,0,0,0,0,0", "Ilford XP2")),
    ("kbw4cn", ("-gimp_emulate_film_bw 13,1,0,1,0,0,0,0,0,0", "Kodak BW 400 CN")),
    ("khie",   ("-gimp_emulate_film_bw 14,1,0,1,0,0,0,0,0,0", "Kodak HIE (HS Infra)")),
    ("ktm1",   ("-gimp_emulate_film_bw 15,1,0,1,0,0,0,0,0,0", "Kodak T-Max 100")),
    ("ktm32",  ("-gimp_emulate_film_bw 16,1,0,1,0,0,0,0,0,0", "Kodak T-Max 3200")),
    ("ktm4",   ("-gimp_emulate_film_bw 17,1,0,1,0,0,0,0,0,0", "Kodak T-Max 400")),
    ("ktx4",   ("-gimp_emulate_film_bw 18,1,0,1,0,0,0,0,0,0", "Kodak Tri-X 400")),
    ("p664",   ("-gimp_emulate_film_bw 19,1,0,1,0,0,0,0,0,0", "Polaroid 664")),
    ("p667",   ("-gimp_emulate_film_bw 20,1,0,1,0,0,0,0,0,0", "Polaroid 667")),
    ("p672",   ("-gimp_emulate_film_bw 21,1,0,1,0,0,0,0,0,0", "Polaroid 672")),
    ("ri4",    ("-gimp_emulate_film_bw 22,1,0,1,0,0,0,0,0,0", "Rollei IR 400")),
    ("ro.25",  ("-gimp_emulate_film_bw 23,1,0,1,0,0,0,0,0,0", "Rollei Ortho 25")),
    ("rr1t",   ("-gimp_emulate_film_bw 24,1,0,1,0,0,0,0,0,0", "Rollei Retro 100 Tonal")),
    ("rr80s",  ("-gimp_emulate_film_bw 25,1,0,1,0,0,0,0,0,0", "Rollei Retro 80s")),
  ]
  COLOR = [
    # NEW
    ("auc1",     ("-gimp_emulate_film_negative_color 1,1,0,1,0,0,0,0,0",  "Agfa Ultra Color 100")),
    ("av2",      ("-gimp_emulate_film_negative_color 2,1,0,1,0,0,0,0,0",  "Agfa Vista 200")),
    ("fshg16",   ("-gimp_emulate_film_negative_color 4,1,0,1,0,0,0,0,0",  "Fuji Superia HG 1600")),
    ("fsr1",     ("-gimp_emulate_film_negative_color 5,1,0,1,0,0,0,0,0",  "Fuji Superia Reala 100")),
    ("fsx8",     ("-gimp_emulate_film_negative_color 6,1,0,1,0,0,0,0,0",  "Fuji Superia X-Tra 800")),
    ("ke1x",     ("-gimp_emulate_film_negative_color 7,1,0,1,0,0,0,0,0",  "Kodak Elite 100 XPRO")),
    ("kec2",     ("-gimp_emulate_film_negative_color 8,1,0,1,0,0,0,0,0",  "Kodak Elite Color 200")),
    ("kec4",     ("-gimp_emulate_film_negative_color 9,1,0,1,0,0,0,0,0",  "Kodak Elite Color 400")),
    ("lr1",      ("-gimp_emulate_film_negative_color 12,1,0,1,0,0,0,0,0", "Lomography Redscale 100")),
    # OLD
    ("fs1",      ("-gimp_emulate_film_negative_old 3,1,100,0,1,0,0,0,0,0",  "Fuji Superia 100")),
    ("fs2",      ("-gimp_emulate_film_negative_color 3,1,0,1,0,0,0,0,0",  "Fuji Superia 200")),
    ("fs4",      ("-gimp_emulate_film_negative_old 4,1,100,0,1,0,0,0,0,0",  "Fuji Superia 400")),
    ("fs8",      ("-gimp_emulate_film_negative_old 5,1,100,0,1,0,0,0,0,0",  "Fuji Superia 800")),
    ("fs8a",     ("-gimp_emulate_film_negative_old 3,0,50,0,1,0,0,0,0,0",  "Fuji Superia 800 (a)")),
    ("fs16",     ("-gimp_emulate_film_negative_old 6,1,100,0,1,0,0,0,0,0",  "Fuji Superia 1600")),
    ("fs16-70",  ("-gimp_emulate_film_negative_old 6,1,70,0,1,0,0,0,0,0",  "Fuji Superia 1600 (70%)")),
    ("fs16-40",  ("-gimp_emulate_film_negative_old 6,1,40,0,1,0,0,0,0,0",  "Fuji Superia 1600 (40%)")),
    ("fs16-20",  ("-gimp_emulate_film_negative_old 6,1,40,0,1,0,0,0,0,0",  "Fuji Superia 1600 (20%)")),
    ("kp.160nc", ("-gimp_emulate_film_negative_old 7,1,100,0,1,0,0,0,0,0",  "Kodak Portra 160 NC")),
    ("kp.160vc", ("-gimp_emulate_film_negative_old 8,1,100,0,1,0,0,0,0,0",  "Kodak Portra 160 VC")),
    ("kp4nc",    ("-gimp_emulate_film_negative_old 9,1,100,0,1,0,0,0,0,0",  "Kodak Portra 400 NC")),
    ("kp4uc",    ("-gimp_emulate_film_negative_old 10,1,100,0,1,0,0,0,0,0", "Kodak Portra 400 UC")),
    ("kp4vc",    ("-gimp_emulate_film_negative_old 11,1,100,0,1,0,0,0,0,0", "Kodak Portra 400 VC")),
  ]
  DICT = dict(BW + COLOR)
