import png
import sys

if len(sys.argv) > 1:
  FILE = sys.argv[1]
else:
  FILE = 'extract_subset.pl'

f = open(FILE, 'rb')
header_vals = []
for c in range(5):
  bytes = f.read(4)
  hexstr = ''.join(["{0:x}".format(ord(b)) for b in bytes])
  intval = int(hexstr, 16)
  print '%s (%d)' % (hexstr, intval)

  header_vals.append(intval)

start_x = header_vals[0]
start_y = header_vals[1]
end_x = header_vals[2]
end_y = header_vals[3]
width = end_x# - start_x
height = end_y# - start_y
bits_per_pixel = header_vals[4]
bit_range = 2 ** bits_per_pixel
bytes_per_pixel = bits_per_pixel / 8

print 'Parsing %dx%d file at %d bytes per pixel' % (width, height, bytes_per_pixel)

rows = []
last_colored_int = 0
for y in range(height):
  row = []
  for x in range(width):
    pixel = f.read(bytes_per_pixel)
    if pixel == '':
      print 'EOF before expected'
      break
    hexstr = ''.join(["{0:x}".format(ord(b)) for b in pixel])
    intval = int(hexstr, 16)
    if intval <= 4000:
      intval = last_colored_int
    else:
      last_colored_int = intval
    if abs(intval - bit_range / 2) < 1000:
      intval = 0
    row.append(intval)
  rows.append(row)

f.close()  # close input

# Write output
f = open('output.png', 'wb')
w = png.Writer(width, height, greyscale=True, bytes_per_sample=bytes_per_pixel)
w.write(f, rows)
f.close()
