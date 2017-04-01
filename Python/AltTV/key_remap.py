'''
Written By: Eliyahu Baranskiy
E-Mail: elibj123@gmail.com

How to use this:
Take a look at the key_codes.txt file
It contains the code for all common keys along with their descriptions,
feel free to add a comment at the end of each lines with '#'

This tool goes over the file and creates a reg file to disable the keys in the file
If you want to keep some keys enabled, comment out their entire line (add a '#' at the beginning of the line)

This tool generates two files: remap.reg, undo_remap.reg

After loading the reg file, you should restart your computer for anything to take effect
Avoid disabling important keys such as ctrl, alt or del. But worry not, your mouse will be functioning

Notice that this tool doesnt log or intercept keystrokes, but merely disables them at low-level
'''

with open('files/data/key_codes.txt', 'r') as f:
    codes = f.readlines()

remap_str = 'Windows Registry Editor Version 5.00\n\n' \
          '[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layout]\n' \
          '"Scancode Map"=hex:' \
          '00,00,00,00,' \
          '00,00,00,00,' \
          '%s'

undo_remap_str = 'Windows Registry Editor Version 5.00\n\n' \
          '[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layout]\n' \
          '"Scancode Map"=hex:' \
          '00,00,00,00,' \
          '00,00,00,00,' \
          '%s'

code_count = 1
for code in codes:
    code = code.split('#')[0].strip()
    if code == '':
        continue
    code += ',00,' if len(code) == 2 else ','

    remap_str += code
    remap_str += '00,00,'
    undo_remap_str += code + code

    code_count += 1

count_hex = hex(code_count)[2:] + ',00,00,00,'

remap_str += '00,00,00,00'
remap_str %= count_hex

undo_remap_str += '00,00,00,00'
undo_remap_str %= count_hex

with open('files/data/keymaps/remap.reg', 'w+') as f:
    f.write(remap_str)

with open('files/data/keymaps/undo_remap.reg', 'w+') as f:
    f.write(undo_remap_str)
