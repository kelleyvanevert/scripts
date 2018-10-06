#!/usr/bin/fish

# This script assumes the directory is filled with pdf files, each page of which
#  is a portrait oriented A4 page, and has a landscape oriented 10x15cm image in
#  the top right corner.
# It then cuts each of these images out, and puts them in the `im` directory,
#  and then applies a little extra coloring to them and put the result in the
#  `im/exp` directory.

mkdir -p im;
mkdir -p im/exp;

echo '<?xml version="1.0" encoding="UTF-8"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 4.4.0-Exiv2">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:xmp="http://ns.adobe.com/xap/1.0/"
    xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/"
    xmlns:darktable="http://darktable.sf.net/"
   xmp:Rating="1"
   xmpMM:DerivedFrom="1-1-03.jpg"
   darktable:xmp_version="2"
   darktable:raw_params="0"
   darktable:auto_presets_applied="1"
   darktable:history_end="7">
   <darktable:mask_id>
    <rdf:Seq/>
   </darktable:mask_id>
   <darktable:mask_type>
    <rdf:Seq/>
   </darktable:mask_type>
   <darktable:mask_name>
    <rdf:Seq/>
   </darktable:mask_name>
   <darktable:mask_version>
    <rdf:Seq/>
   </darktable:mask_version>
   <darktable:mask>
    <rdf:Seq/>
   </darktable:mask>
   <darktable:mask_nb>
    <rdf:Seq/>
   </darktable:mask_nb>
   <darktable:mask_src>
    <rdf:Seq/>
   </darktable:mask_src>
   <darktable:history>
    <rdf:Seq>
     <rdf:li
      darktable:operation="flip"
      darktable:enabled="1"
      darktable:modversion="2"
      darktable:params="ffffffff"
      darktable:multi_name=""
      darktable:multi_priority="0"
      darktable:blendop_version="7"
      darktable:blendop_params="gz12eJxjYGBgkGAAgRNODESDBnsIHll8ANNSGQM="/>
     <rdf:li
      darktable:operation="flip"
      darktable:enabled="1"
      darktable:modversion="2"
      darktable:params="05000000"
      darktable:multi_name=""
      darktable:multi_priority="0"
      darktable:blendop_version="7"
      darktable:blendop_params="gz12eJxjYGBgkGAAgRNODESDBnsIHll8ANNSGQM="/>
     <rdf:li
      darktable:operation="tonecurve"
      darktable:enabled="1"
      darktable:modversion="4"
      darktable:params="gz08eJxjYICA9G3fbP37I2wXt12x47Z6YKcha29/SMPXnoGhAYoHHNhD8KBxDzoYlO5jBWJmKGZCwoxQeRANAH07DyQ="
      darktable:multi_name=""
      darktable:multi_priority="0"
      darktable:blendop_version="7"
      darktable:blendop_params="gz12eJxjYGBgkGAAgRNODESDBnsIHll8ANNSGQM="/>
     <rdf:li
      darktable:operation="velvia"
      darktable:enabled="1"
      darktable:modversion="2"
      darktable:params="0000c8410000803f"
      darktable:multi_name=""
      darktable:multi_priority="0"
      darktable:blendop_version="7"
      darktable:blendop_params="gz12eJxjYGBgkGAAgRNODESDBnsIHll8ANNSGQM="/>
     <rdf:li
      darktable:operation="vibrance"
      darktable:enabled="1"
      darktable:modversion="2"
      darktable:params="0000c841"
      darktable:multi_name=""
      darktable:multi_priority="0"
      darktable:blendop_version="7"
      darktable:blendop_params="gz12eJxjYGBgkGAAgRNODESDBnsIHll8ANNSGQM="/>
     <rdf:li
      darktable:operation="splittoning"
      darktable:enabled="1"
      darktable:modversion="1"
      darktable:params="ae47213f0000003fcdcc4c3e0000003f0000003f00000442"
      darktable:multi_name=""
      darktable:multi_priority="0"
      darktable:blendop_version="7"
      darktable:blendop_params="gz12eJxjYGBgkGAAgRNODESDBnsIHll8ANNSGQM="/>
     <rdf:li
      darktable:operation="flip"
      darktable:enabled="0"
      darktable:modversion="2"
      darktable:params="05000000"
      darktable:multi_name=""
      darktable:multi_priority="0"
      darktable:blendop_version="7"
      darktable:blendop_params="gz12eJxjYGBgkGAAgRNODESDBnsIHll8ANNSGQM="/>
    </rdf:Seq>
   </darktable:history>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>' > p.xmp;

for f in *.pdf;
  set g (basename $f .pdf);
  set n (pdfinfo $g.pdf 2>/dev/null | grep "Pages" | sed 's/^Pages:\s*\(.*\)$/\1/i');
  for i in (seq 0 (math "$n - 1"));
    set h "im/$g-$i.jpg";
    set h2 "im/exp/$g-$i.jpg";

    echo -n "Extracting $g.pdf[$i] -> $h ... ";
    if test -e "$h";
      echo "(exists)";
    else;
      convert -density 600 $g.pdf[$i] -crop 3555x2370+1382+3 -quality 93 -sharpen 1x1.0 $h;
      echo "DONE";
    end;

    echo -n "  Post -> $h2 ... ";
    if test -e "$h2";
      echo "(exists)";
    else;
      darktable-cli $h p.xmp $h2;
      # echo "DONE"; # darktable-cli already prints something
    end;
  end;
end;
