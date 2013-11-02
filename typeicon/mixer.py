#coding: UTF8

from PIL import Image
import os

fold_prefix = 'win-%d'
resl = [16,32]

d = {}
for i in open('map.txt', 'r'):
    i = i.replace('\n', '')
    if not i or i.startswith('#'):continue
    print [i]
    if i.find(' ') == -1:
        ico_type = i
        etc = [i]
    else:
        ico_type, etc_str = i.split(' ', 1)
        etc = etc_str.split(' ')
        etc.append(ico_type)
    
    d[ico_type] = {'res': {}, 'etc': etc}
    failed = False
    for j in resl:
        fn = os.path.join(fold_prefix%(j), '%s.png'%(ico_type))
        try:
            test_img = Image.open(fn)
            if (test_img.size != (j, j)):
                raise IOError('Size Mismatch')
            d[ico_type]['res'][j] = test_img
        except IOError:
            print 'Icon not found: %s @ %d'%(ico_type, j)
            failed = True
            break
    if failed: 
        del(d[ico_type])
        continue
    
icon_count = len(d.keys())
icon_max = max(resl)
try:
    os.mkdir('typeicon')
except:
    pass
for r in resl:
    i = Image.new('RGBA', (icon_count * icon_max, icon_max))
    for index, k in enumerate(d):
        i.paste(d[k]['res'][r], (icon_max * index, 0))
    i.save('typeicon/typeicon-%d.png'%(r))

buf = ''
for index, i in enumerate(d):
    buf += '.ti-%s {background-position: -%dpx 0px;}\n'%(i, index * icon_max)
for i in resl:
    f = open('typeicon/typeicon-%d.css'%(i), 'wb')
    f.write(""".typeicon {
	display: inline-block;
	width: %dpx;
	height: %dpx;
	background: url(typeicon-%d.png) no-repeat 0 0;
	overflow: hidden;
	vertical-align: text-bottom;
}

.typeiconTableCol {
	width: %dpx;
	padding: 3px;
}
"""%(i, i, i, i))
    f.write(buf)
    f.close()

f = open('typeicon/typeicon.js', 'wb')
f.write('typeicon_map = {\n')
for ti in d:
    for etc in d[ti]['etc']:
        f.write('\t"%s": "ti-%s",\n'%(etc, ti))
f.write("""\t"":""
};

$(document).ready(function () {
	$(".typeiconTableCol").each(function () {
		var node = $(this).next().find("a");
		var a = node.attr("href");
		var ext = "file";
		if (!a) return;
		
		if (a.substr(a.length - 1, 1) === "/") {
			ext = "folder";
		} else {
			if (a.lastIndexOf(".") >= 0) {
				ext = a.slice(a.lastIndexOf(".") + 1, a.length).toLowerCase();
				if (!typeicon_map[ext]) ext = "file";
			}
		}
		$(this).find(".typeicon").removeClass("ti-folder").addClass(typeicon_map[ext]);
	});
})
""");
f.close()
